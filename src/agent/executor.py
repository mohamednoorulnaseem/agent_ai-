"""
Task execution module for the AI agent.
Handles executing tasks and interacting with the codebase.
"""

from typing import Any, Dict, List
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.base import LLM
from agent.planner import Task
from repo.scanner import Scanner
from repo.patcher import Patcher


class Executor:
    """Executes tasks using the LLM and repository tools."""
    
    def __init__(self, llm: LLM, repo_path: str):
        self.llm = llm
        self.scanner = Scanner(repo_path)
        self.patcher = Patcher(repo_path)
        self.execution_history: List[Dict[str, Any]] = []
    
    def execute_task(self, task: Task, context: str = "") -> str:
        """
        Execute a single task using the LLM.
        
        Args:
            task: The task to execute
            context: Additional context about the codebase
            
        Returns:
            The result of task execution
        """
        # Get repository information
        repo_info = self.scanner.scan_repository()
        
        messages = [
            {
                "role": "system",
                "content": "You are a code-aware AI assistant. Help execute development tasks. "
                          "Be specific about file paths and code changes needed.",
            },
            {
                "role": "user",
                "content": f"Task: {task.description}\n\nRepository Context:\n{repo_info}\n\nAdditional Context:\n{context}",
            },
        ]
        
        response = self.llm.completion(messages)
        
        # Record execution
        self.execution_history.append({
            "task_id": task.id,
            "task_description": task.description,
            "response": response,
        })
        
        return response
    
    def apply_changes(self, file_path: str, changes: str) -> bool:
        """
        Apply code changes to a file.
        
        Args:
            file_path: Path to the file to modify
            changes: Description of changes or new content
            
        Returns:
            Success status
        """
        try:
            return self.patcher.apply_patch(file_path, changes)
        except Exception as e:
            print(f"Error applying changes: {e}")
            return False
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the history of executed tasks."""
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history."""
        self.execution_history = []
