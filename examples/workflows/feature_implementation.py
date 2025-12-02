"""
Example 1: Feature Implementation Workflow

This example demonstrates how to use the AI Agent to plan and implement
a new feature in your codebase.

Flow:
1. Define the feature goal
2. Agent plans implementation steps
3. Execute each step
4. Track progress with conversation history
"""

from src.config import load_config_and_llm
from src.agent.planner import Planner
from src.agent.executor import Executor
from src.agent.history import ConversationHistory
from typing import Dict, Any


def feature_implementation_workflow(
    feature_goal: str,
    repo_path: str = ".",
    config_file: str = "agent.config.yaml"
) -> Dict[str, Any]:
    """
    Execute a feature implementation workflow.

    Args:
        feature_goal: Description of the feature to implement
        repo_path: Path to the repository
        config_file: Path to configuration file

    Returns:
        Dictionary with workflow results including tasks and execution status
    """
    # Step 1: Load configuration and initialize LLM
    print("🔧 Loading configuration...")
    config: Dict[str, Any]
    llm: Any
    config, llm = load_config_and_llm(config_file)

    # Step 2: Initialize agent components
    print("🚀 Initializing agent components...")
    planner: Planner = Planner(llm)
    executor: Executor = Executor(llm, repo_path)
    history: ConversationHistory = ConversationHistory()

    # Step 3: Plan the feature
    print(f"\n📋 Planning feature: {feature_goal}\n")
    history.add_message("user", f"Implement feature: {feature_goal}")

    tasks: list = planner.plan(feature_goal)
    print(f"✅ Created {len(tasks)} implementation tasks:\n")

    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task.description}")

    plan_summary: str = planner.get_plan_summary()
    history.add_message("assistant", plan_summary)

    # Step 4: Execute tasks
    print("\n⚙️  Executing tasks...\n")
    results: Dict[int, str] = {}

    for i, task in enumerate(tasks, 1):
        print(f"[{i}/{len(tasks)}] Executing: {task.description}")
        try:
            result: str = executor.execute_task(task)
            results[task.id] = result
            planner.mark_task_complete(task.id, result)
            history.add_message("user", f"Execute task {task.id}")
            history.add_message("assistant", result)
            print(f"    ✓ Task completed\n")
        except Exception as e:
            print(f"    ✗ Task failed: {e}\n")
            results[task.id] = f"Failed: {str(e)}"

    # Step 5: Generate summary
    print("\n📊 Workflow Summary")
    print("-" * 50)
    summary: Dict[str, Any] = history.get_summary()
    print(f"Total Messages: {summary['total_messages']}")
    print(f"Tasks Completed: {len(results)}")
    print(f"Workflow Status: {'Completed' if len(results) == len(tasks) else 'Partial'}")

    return {
        "feature": feature_goal,
        "tasks": len(tasks),
        "completed": len(results),
        "results": results,
        "history_summary": summary,
    }


if __name__ == "__main__":
    # Example usage
    result: Dict[str, Any] = feature_implementation_workflow(
        feature_goal="Create a REST API endpoint for user management",
        repo_path=".",
        config_file="agent.config.yaml"
    )

    print("\n✨ Workflow completed!")
    print(f"Results: {result}")
