"""
Examples demonstrating the AI Agent framework.
Shows how to use different components programmatically.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config_and_llm
from agent.planner import Planner
from agent.executor import Executor
from agent.history import ConversationHistory
from persistence import DatabaseManager, PersistentPlanner
from repo.scanner import Scanner


def example_1_basic_planning():
    """Example 1: Basic planning without persistence."""
    print("\n" + "=" * 60)
    print("Example 1: Basic Planning")
    print("=" * 60)
    
    # Load configuration
    config, llm = load_config_and_llm()
    
    # Create planner
    planner = Planner(llm)
    
    # Plan a goal
    goal = "Build a Python CLI tool for file management"
    print(f"\nGoal: {goal}")
    
    tasks = planner.plan(goal)
    print(f"\nGenerated {len(tasks)} tasks:")
    for task in tasks:
        print(f"  [{task.id}] {task.description}")
    
    # Display plan summary
    print("\n" + planner.get_plan_summary())


def example_2_planning_with_execution():
    """Example 2: Planning and executing tasks."""
    print("\n" + "=" * 60)
    print("Example 2: Planning and Execution")
    print("=" * 60)
    
    config, llm = load_config_and_llm()
    
    planner = Planner(llm)
    executor = Executor(llm, ".")
    
    goal = "Create a web scraper"
    print(f"\nGoal: {goal}")
    
    # Plan
    tasks = planner.plan(goal)
    print(f"Created {len(tasks)} tasks")
    
    # Execute first 3 tasks
    for i, task in enumerate(tasks[:3]):
        print(f"\nExecuting task {i+1}: {task.description}")
        result = executor.execute_task(task)
        planner.mark_task_complete(task.id, result)
        print(f"Result: {result[:80]}...")


def example_3_conversation_tracking():
    """Example 3: Tracking conversation history."""
    print("\n" + "=" * 60)
    print("Example 3: Conversation History")
    print("=" * 60)
    
    config, llm = load_config_and_llm()
    
    planner = Planner(llm)
    history = ConversationHistory()
    
    # Simulate conversation
    user_messages = [
        "Plan a machine learning project",
        "What are the initial setup steps?",
        "How do we validate the models?",
    ]
    
    for msg in user_messages:
        print(f"\nUser: {msg}")
        history.add_message("user", msg)
        
        # Get response from LLM
        response = llm.completion([{"role": "user", "content": msg}])
        print(f"Assistant: {response[:100]}...")
        history.add_message("assistant", response)
    
    # Show summary
    summary = history.get_summary()
    print("\n" + "=" * 40)
    print("Conversation Summary:")
    print(f"  Total messages: {summary['total_messages']}")
    print(f"  User messages: {summary['user_messages']}")
    print(f"  Assistant messages: {summary['assistant_messages']}")


def example_4_repository_scanning():
    """Example 4: Scanning and analyzing repositories."""
    print("\n" + "=" * 60)
    print("Example 4: Repository Scanning")
    print("=" * 60)
    
    scanner = Scanner(".", ignore_dirs=[".git", "__pycache__", ".egg-info"])
    
    print("\nScanning current repository...")
    info = scanner.scan_repository(max_depth=3)
    print(info)
    
    # Get Python files
    py_files = scanner.get_files_by_extension(".py")
    print(f"\nPython files found: {len(py_files)}")
    for f in py_files[:5]:
        print(f"  - {f}")


def example_5_persistence():
    """Example 5: Using persistence layer."""
    print("\n" + "=" * 60)
    print("Example 5: Database Persistence")
    print("=" * 60)
    
    # Create in-memory database for demo
    db = DatabaseManager(":memory:")
    
    # Save a plan
    print("\nSaving plan...")
    plan_id = db.save_plan("Create an API server")
    print(f"Plan ID: {plan_id}")
    
    # Save tasks
    print("Saving tasks...")
    task1_id = db.save_task(plan_id, 1, "Set up FastAPI project", 0)
    task2_id = db.save_task(plan_id, 2, "Implement endpoints", 1)
    
    # Mark task as complete
    print("Marking task as complete...")
    db.update_task(task1_id, True, "Project set up successfully")
    
    # Save conversation
    print("Saving conversation...")
    db.save_conversation("user", "Plan an API server")
    db.save_conversation("assistant", "I'll help you plan an API server...")
    
    # Get statistics
    print("\nPlan Statistics:")
    stats = db.get_plan_statistics(plan_id)
    print(f"  Total tasks: {stats['total_tasks']}")
    print(f"  Completed tasks: {stats['completed_tasks']}")
    print(f"  Total executions: {stats['total_executions']}")
    
    # Get conversation history
    print("\nConversation History:")
    messages = db.get_conversation_history(10)
    for msg in messages:
        print(f"  {msg['role']}: {msg['content'][:50]}...")
    
    db.close()


def example_6_end_to_end():
    """Example 6: Complete end-to-end workflow."""
    print("\n" + "=" * 60)
    print("Example 6: End-to-End Workflow")
    print("=" * 60)
    
    config, llm = load_config_and_llm()
    
    # Initialize components
    db = DatabaseManager(":memory:")
    planner = Planner(llm)
    executor = Executor(llm, ".")
    history = ConversationHistory()
    
    # User starts with a goal
    goal = "Implement a data validation system"
    print(f"\nGoal: {goal}")
    
    # Add to history
    history.add_message("user", goal)
    
    # Scan repository
    print("\n1. Scanning repository...")
    scanner = Scanner(".")
    repo_info = scanner.scan_repository()
    print("   Repository scanned")
    
    # Create plan
    print("\n2. Creating plan...")
    db_plan_id = db.save_plan(goal)
    tasks = planner.plan(goal)
    
    for task in tasks:
        db.save_task(db_plan_id, task.id, task.description, task.priority)
    
    print(f"   Created {len(tasks)} tasks")
    history.add_message("assistant", planner.get_plan_summary())
    
    # Execute tasks
    print("\n3. Executing tasks...")
    for i, task in enumerate(tasks[:2]):
        result = executor.execute_task(task)
        planner.mark_task_complete(task.id, result)
        db.save_execution(task.id, result)
        print(f"   Task {i+1} completed")
        history.add_message("user", f"Execute task {task.id}")
        history.add_message("assistant", result)
    
    # Show final state
    print("\n4. Final State:")
    stats = db.get_plan_statistics(db_plan_id)
    history_summary = history.get_summary()
    
    print(f"   Tasks completed: {stats['completed_tasks']}/{stats['total_tasks']}")
    print(f"   Conversation messages: {history_summary['total_messages']}")
    print(f"   Total executions: {stats['total_executions']}")
    
    db.close()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("AI Agent Framework - Examples")
    print("=" * 60)
    
    examples = [
        ("Basic Planning", example_1_basic_planning),
        ("Planning with Execution", example_2_planning_with_execution),
        ("Conversation Tracking", example_3_conversation_tracking),
        ("Repository Scanning", example_4_repository_scanning),
        ("Database Persistence", example_5_persistence),
        ("End-to-End Workflow", example_6_end_to_end),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nRunning all examples...\n")
    
    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\nError in {name}: {e}")
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
