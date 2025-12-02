#!/usr/bin/env python
"""
Test script demonstrating the AI Agent framework.
Shows planning, execution, and history tracking.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config_and_llm
from agent.planner import Planner
from agent.executor import Executor
from agent.history import ConversationHistory


def main():
    """Demonstrate the agent framework."""
    print("=" * 60)
    print("AI Agent Framework - Demonstration")
    print("=" * 60)
    
    # Load configuration and LLM
    print("\n1. Loading configuration...")
    config, llm = load_config_and_llm()
    print(f"   ✓ LLM Provider: {config['llm']['provider']}")
    
    # Initialize components
    print("\n2. Initializing components...")
    planner = Planner(llm)
    executor = Executor(llm, ".")
    history = ConversationHistory()
    print("   ✓ Planner, Executor, and History initialized")
    
    # Scan repository
    print("\n3. Scanning repository...")
    repo_info = executor.scanner.scan_repository()
    print("   " + repo_info.replace("\n", "\n   "))
    
    # Plan a goal
    print("\n4. Planning a goal...")
    goal = "Implement a data processing pipeline"
    print(f"   Goal: {goal}")
    history.add_message("user", goal)
    
    tasks = planner.plan(goal)
    print(f"   ✓ Created {len(tasks)} tasks:")
    for task in tasks:
        print(f"     [{task.id}] {task.description}")
    history.add_message("assistant", planner.get_plan_summary())
    
    # Execute first task
    if tasks:
        print("\n5. Executing first task...")
        task = tasks[0]
        print(f"   Task: {task.description}")
        
        result = executor.execute_task(task)
        planner.mark_task_complete(task.id, result)
        
        print(f"   ✓ Result: {result[:100]}...")
        history.add_message("user", f"Execute task {task.id}")
        history.add_message("assistant", result)
    
    # Show conversation history
    print("\n6. Conversation History:")
    summary = history.get_summary()
    print(f"   Total messages: {summary['total_messages']}")
    print(f"   User messages: {summary['user_messages']}")
    print(f"   Assistant messages: {summary['assistant_messages']}")
    
    # Show plan summary
    print("\n7. Plan Summary:")
    print("   " + planner.get_plan_summary().replace("\n", "\n   "))
    
    print("\n" + "=" * 60)
    print("Demonstration Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Run interactive mode: python cli.py --interactive")
    print("  - Scan repository: python cli.py --scan")
    print("  - Plan a goal: python cli.py --goal 'Your goal here'")
    print("=" * 60)


if __name__ == "__main__":
    main()
