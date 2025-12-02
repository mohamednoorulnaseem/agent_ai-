"""
Task planning module for the AI agent.
Handles breaking down goals into actionable tasks.
"""

from typing import List, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm.base import LLM


class Task:
    """Represents a single task in the plan."""
    
    def __init__(self, id: int, description: str, priority: int = 0, dependencies: List[int] = None):
        self.id = id
        self.description = description
        self.priority = priority
        self.dependencies = dependencies or []
        self.completed = False
        self.result = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "dependencies": self.dependencies,
            "completed": self.completed,
            "result": self.result,
        }


class Planner:
    """Plans and manages tasks for the agent."""
    
    def __init__(self, llm: LLM):
        self.llm = llm
        self.tasks: Dict[int, Task] = {}
        self.task_counter = 0
    
    def plan(self, goal: str) -> List[Task]:
        """
        Break down a goal into actionable tasks using the LLM.
        
        Args:
            goal: The high-level goal to plan
            
        Returns:
            List of tasks to accomplish the goal
        """
        messages = [
            {
                "role": "system",
                "content": "You are a task planning assistant. Break down the given goal into specific, actionable tasks. "
                          "Format your response as a numbered list with each task on a new line.",
            },
            {
                "role": "user",
                "content": f"Plan the following goal into actionable tasks:\n{goal}",
            },
        ]
        
        response = self.llm.completion(messages)
        tasks = self._parse_tasks(response)
        
        for task in tasks:
            self.tasks[task.id] = task
        
        return tasks
    
    def _parse_tasks(self, response: str) -> List[Task]:
        """Parse task descriptions from LLM response."""
        tasks = []
        lines = response.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove numbering (e.g., "1.", "1)", etc.)
            for i in range(10):
                prefixes = [f"{i}.", f"{i})", f"{i}:"]
                for prefix in prefixes:
                    if line.startswith(prefix):
                        line = line[len(prefix):].strip()
                        break
            
            if line:
                self.task_counter += 1
                task = Task(
                    id=self.task_counter,
                    description=line,
                    priority=len(tasks),
                )
                tasks.append(task)
        
        return tasks
    
    def get_next_task(self) -> Task:
        """Get the next unfinished task."""
        for task_id in sorted(self.tasks.keys()):
            task = self.tasks[task_id]
            if not task.completed:
                # Check dependencies
                if all(self.tasks[dep_id].completed for dep_id in task.dependencies):
                    return task
        return None
    
    def mark_task_complete(self, task_id: int, result: Any = None):
        """Mark a task as completed."""
        if task_id in self.tasks:
            self.tasks[task_id].completed = True
            self.tasks[task_id].result = result
    
    def get_plan_summary(self) -> str:
        """Get a summary of the current plan."""
        summary = "Current Plan:\n"
        for task_id in sorted(self.tasks.keys()):
            task = self.tasks[task_id]
            status = "✓" if task.completed else "○"
            summary += f"{status} [{task.id}] {task.description}\n"
        return summary
