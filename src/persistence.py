"""
Persistence layer for storing plans, executions, and conversations.
Uses SQLite for lightweight, portable storage.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class DatabaseManager:
    """Manages persistence of agent data."""
    
    def __init__(self, db_path: str = "agent.db"):
        self.db_path = db_path
        self.conn = None
        self.init_database()
    
    def init_database(self):
        """Initialize database tables."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Plans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        """)
        
        # Tasks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER NOT NULL,
                task_id INTEGER NOT NULL,
                description TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                completed BOOLEAN DEFAULT 0,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plan_id) REFERENCES plans(id)
            )
        """)
        
        # Executions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                response TEXT NOT NULL,
                duration_seconds FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        """)
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.conn.commit()
    
    def save_plan(self, goal: str) -> int:
        """Save a plan to the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO plans (goal) VALUES (?)",
            (goal,)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def save_task(self, plan_id: int, task_id: int, description: str, priority: int = 0) -> int:
        """Save a task to the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (plan_id, task_id, description, priority) VALUES (?, ?, ?, ?)",
            (plan_id, task_id, description, priority)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def update_task(self, task_db_id: int, completed: bool, result: str = None):
        """Update a task's completion status."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tasks SET completed = ?, result = ? WHERE id = ?",
            (completed, result, task_db_id)
        )
        self.conn.commit()
    
    def save_execution(self, task_db_id: int, response: str, duration: float = None):
        """Save task execution record."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO executions (task_id, response, duration_seconds) VALUES (?, ?, ?)",
            (task_db_id, response, duration)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def save_conversation(self, role: str, content: str):
        """Save a conversation message."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (role, content) VALUES (?, ?)",
            (role, content)
        )
        self.conn.commit()
    
    def get_plan(self, plan_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a plan by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM plans WHERE id = ?", (plan_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_plan_tasks(self, plan_id: int) -> List[Dict[str, Any]]:
        """Get all tasks for a plan."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM tasks WHERE plan_id = ? ORDER BY priority",
            (plan_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_plans(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent plans."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM plans ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def get_conversation_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get conversation history."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT role, content, created_at FROM conversations ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        return [dict(row) for row in cursor.fetchall()]
    
    def get_plan_statistics(self, plan_id: int) -> Dict[str, Any]:
        """Get statistics for a plan."""
        cursor = self.conn.cursor()
        
        # Get plan info
        cursor.execute("SELECT * FROM plans WHERE id = ?", (plan_id,))
        plan = dict(cursor.fetchone())
        
        # Get task counts
        cursor.execute(
            "SELECT COUNT(*) as total, SUM(completed) as completed FROM tasks WHERE plan_id = ?",
            (plan_id,)
        )
        task_stats = dict(cursor.fetchone())
        
        # Get execution count
        cursor.execute(
            "SELECT COUNT(*) as total_executions FROM executions WHERE task_id IN (SELECT id FROM tasks WHERE plan_id = ?)",
            (plan_id,)
        )
        exec_stats = dict(cursor.fetchone())
        
        return {
            "plan": plan,
            "total_tasks": task_stats["total"],
            "completed_tasks": task_stats["completed"],
            "total_executions": exec_stats["total_executions"],
        }
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def clear_all(self):
        """Clear all tables (for testing)."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM conversations")
        cursor.execute("DELETE FROM executions")
        cursor.execute("DELETE FROM tasks")
        cursor.execute("DELETE FROM plans")
        self.conn.commit()


class PersistentPlanner:
    """Planner with persistence."""
    
    def __init__(self, llm, db_manager: DatabaseManager):
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from agent.planner import Planner
        self.planner = Planner(llm)
        self.db = db_manager
        self.current_plan_id = None
        self.task_db_map = {}  # Maps task_id to db_id
    
    def plan(self, goal: str) -> List[Any]:
        """Create and persist a plan."""
        # Create plan in memory
        tasks = self.planner.plan(goal)
        
        # Save to database
        self.current_plan_id = self.db.save_plan(goal)
        
        for task in tasks:
            db_id = self.db.save_task(
                self.current_plan_id,
                task.id,
                task.description,
                task.priority
            )
            self.task_db_map[task.id] = db_id
        
        return tasks
    
    def mark_task_complete(self, task_id: int, result: str = None):
        """Mark task complete and persist."""
        self.planner.mark_task_complete(task_id, result)
        
        if task_id in self.task_db_map:
            db_id = self.task_db_map[task_id]
            self.db.update_task(db_id, True, result)
    
    def get_plan_summary(self) -> str:
        """Get plan summary."""
        return self.planner.get_plan_summary()
    
    def get_tasks(self) -> Dict[int, Any]:
        """Get all tasks."""
        return self.planner.tasks


if __name__ == "__main__":
    # Demo
    db = DatabaseManager(":memory:")
    
    plan_id = db.save_plan("Test goal")
    task_id = db.save_task(plan_id, 1, "Test task", 0)
    db.update_task(task_id, True, "Completed")
    db.save_conversation("user", "Hello")
    db.save_conversation("assistant", "Hi there")
    
    stats = db.get_plan_statistics(plan_id)
    print(f"Plan statistics: {stats}")
    
    db.close()
