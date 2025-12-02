"""
Unit tests for the AI Agent framework.
Tests core components: planner, executor, scanner, patcher, and history.
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.planner import Planner, Task
from agent.executor import Executor
from agent.history import ConversationHistory
from repo.scanner import Scanner
from repo.patcher import Patcher
from llm.mock import MockLLM


class TestTask(unittest.TestCase):
    """Tests for Task class."""
    
    def test_task_creation(self):
        """Test creating a task."""
        task = Task(1, "Test task", priority=5)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Test task")
        self.assertEqual(task.priority, 5)
        self.assertFalse(task.completed)
    
    def test_task_completion(self):
        """Test marking task as complete."""
        task = Task(1, "Test task")
        task.completed = True
        self.assertTrue(task.completed)
    
    def test_task_to_dict(self):
        """Test task serialization."""
        task = Task(1, "Test task", priority=3)
        task_dict = task.to_dict()
        self.assertEqual(task_dict["id"], 1)
        self.assertEqual(task_dict["description"], "Test task")
        self.assertEqual(task_dict["priority"], 3)


class TestPlanner(unittest.TestCase):
    """Tests for Planner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.llm = MockLLM()
        self.planner = Planner(self.llm)
    
    def test_planner_initialization(self):
        """Test planner initialization."""
        self.assertIsNotNone(self.planner.llm)
        self.assertEqual(len(self.planner.tasks), 0)
    
    def test_plan_creation(self):
        """Test creating a plan from a goal."""
        goal = "Create a new feature"
        tasks = self.planner.plan(goal)
        
        self.assertGreater(len(tasks), 0)
        self.assertIsInstance(tasks[0], Task)
    
    def test_get_next_task(self):
        """Test getting the next unfinished task."""
        self.planner.plan("Test goal")
        next_task = self.planner.get_next_task()
        
        self.assertIsNotNone(next_task)
        self.assertFalse(next_task.completed)
    
    def test_mark_task_complete(self):
        """Test marking tasks as complete."""
        tasks = self.planner.plan("Test goal")
        task_id = tasks[0].id
        
        self.planner.mark_task_complete(task_id, "Completed")
        self.assertTrue(self.planner.tasks[task_id].completed)
        self.assertEqual(self.planner.tasks[task_id].result, "Completed")
    
    def test_plan_summary(self):
        """Test getting plan summary."""
        self.planner.plan("Test goal")
        summary = self.planner.get_plan_summary()
        
        self.assertIn("Current Plan:", summary)
        self.assertGreater(len(summary), 0)


class TestConversationHistory(unittest.TestCase):
    """Tests for ConversationHistory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.history = ConversationHistory(max_messages=10)
    
    def test_add_message(self):
        """Test adding messages."""
        self.history.add_message("user", "Hello")
        self.assertEqual(len(self.history.messages), 1)
    
    def test_get_messages(self):
        """Test retrieving messages."""
        self.history.add_message("user", "Hello")
        self.history.add_message("assistant", "Hi there")
        
        messages = self.history.get_messages()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
    
    def test_message_limit(self):
        """Test message history limit."""
        history = ConversationHistory(max_messages=5)
        
        for i in range(10):
            history.add_message("user", f"Message {i}")
        
        self.assertLessEqual(len(history.messages), 5)
    
    def test_clear_history(self):
        """Test clearing history."""
        self.history.add_message("user", "Test")
        self.history.clear()
        self.assertEqual(len(self.history.messages), 0)
    
    def test_history_summary(self):
        """Test getting history summary."""
        self.history.add_message("user", "Hello")
        self.history.add_message("assistant", "Hi")
        
        summary = self.history.get_summary()
        self.assertEqual(summary["total_messages"], 2)
        self.assertEqual(summary["user_messages"], 1)
        self.assertEqual(summary["assistant_messages"], 1)


class TestScanner(unittest.TestCase):
    """Tests for Scanner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = Scanner(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_scanner_initialization(self):
        """Test scanner initialization."""
        self.assertEqual(self.scanner.repo_path, self.temp_dir)
        self.assertGreater(len(self.scanner.ignore_dirs), 0)
    
    def test_scan_empty_directory(self):
        """Test scanning an empty directory."""
        summary = self.scanner.scan_repository()
        self.assertIn("Repository:", summary)
        self.assertIn("Total Files: 0", summary)
    
    def test_scan_with_files(self):
        """Test scanning directory with files."""
        # Create test files
        test_file = os.path.join(self.temp_dir, "test.py")
        with open(test_file, "w") as f:
            f.write("print('hello')\n")
        
        summary = self.scanner.scan_repository()
        self.assertIn("Total Files: 1", summary)
        self.assertIn(".py: 1 files", summary)
    
    def test_get_files_by_extension(self):
        """Test getting files by extension."""
        # Create test files
        py_file = os.path.join(self.temp_dir, "test.py")
        txt_file = os.path.join(self.temp_dir, "readme.txt")
        
        with open(py_file, "w") as f:
            f.write("code")
        with open(txt_file, "w") as f:
            f.write("text")
        
        self.scanner.scan_repository()
        py_files = self.scanner.get_files_by_extension(".py")
        
        self.assertEqual(len(py_files), 1)


class TestPatcher(unittest.TestCase):
    """Tests for Patcher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.patcher = Patcher(self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_create_file(self):
        """Test creating a file."""
        file_path = "test.txt"
        content = "Hello, World!"
        
        success = self.patcher.create_file(file_path, content)
        self.assertTrue(success)
        
        full_path = os.path.join(self.temp_dir, file_path)
        self.assertTrue(os.path.exists(full_path))
        
        with open(full_path, "r") as f:
            self.assertEqual(f.read(), content)
    
    def test_apply_patch(self):
        """Test applying a patch."""
        file_path = "test.txt"
        original = "Original content"
        new_content = "New content"
        
        # Create original file
        full_path = os.path.join(self.temp_dir, file_path)
        with open(full_path, "w") as f:
            f.write(original)
        
        # Apply patch
        success = self.patcher.apply_patch(file_path, new_content)
        self.assertTrue(success)
        
        with open(full_path, "r") as f:
            self.assertEqual(f.read(), new_content)
    
    def test_apply_diff(self):
        """Test applying a diff."""
        file_path = "test.py"
        original = "def hello():\n    print('world')"
        new_content = "def hello():\n    print('updated')"
        
        # Create file
        full_path = os.path.join(self.temp_dir, file_path)
        with open(full_path, "w") as f:
            f.write(original)
        
        # Apply diff
        success = self.patcher.apply_diff(file_path, "print('world')", "print('updated')")
        self.assertTrue(success)
        
        with open(full_path, "r") as f:
            content = f.read()
            self.assertIn("print('updated')", content)
    
    def test_delete_file(self):
        """Test deleting a file."""
        file_path = "test.txt"
        full_path = os.path.join(self.temp_dir, file_path)
        
        # Create file
        with open(full_path, "w") as f:
            f.write("content")
        
        # Delete file
        success = self.patcher.delete_file(file_path)
        self.assertTrue(success)
        self.assertFalse(os.path.exists(full_path))
    
    def test_change_history(self):
        """Test tracking change history."""
        self.patcher.create_file("test.txt", "content")
        
        history = self.patcher.get_change_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["action"], "create")


class TestExecutor(unittest.TestCase):
    """Tests for Executor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.llm = MockLLM()
        self.executor = Executor(self.llm, self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_executor_initialization(self):
        """Test executor initialization."""
        self.assertIsNotNone(self.executor.llm)
        self.assertIsNotNone(self.executor.scanner)
        self.assertIsNotNone(self.executor.patcher)
    
    def test_execute_task(self):
        """Test executing a task."""
        task = Task(1, "Test task")
        result = self.executor.execute_task(task)
        
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
    
    def test_execution_history(self):
        """Test execution history tracking."""
        task = Task(1, "Test task")
        self.executor.execute_task(task)
        
        history = self.executor.get_execution_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["task_id"], 1)


class TestIntegration(unittest.TestCase):
    """Integration tests for the full system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.llm = MockLLM()
        self.planner = Planner(self.llm)
        self.executor = Executor(self.llm, self.temp_dir)
        self.history = ConversationHistory()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_full_workflow(self):
        """Test complete planning and execution workflow."""
        # Plan a goal
        goal = "Create a new module"
        self.history.add_message("user", goal)
        tasks = self.planner.plan(goal)
        self.history.add_message("assistant", self.planner.get_plan_summary())
        
        # Execute first task
        if tasks:
            task = tasks[0]
            result = self.executor.execute_task(task)
            self.planner.mark_task_complete(task.id, result)
            self.history.add_message("user", f"Execute {task.id}")
            self.history.add_message("assistant", result)
        
        # Verify state
        self.assertGreater(len(tasks), 0)
        self.assertGreater(self.history.get_summary()["total_messages"], 0)
        self.assertGreater(len(self.executor.get_execution_history()), 0)


if __name__ == "__main__":
    unittest.main()
