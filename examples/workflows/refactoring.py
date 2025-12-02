"""
Example 3: Code Refactoring Workflow

This example shows how to systematically refactor code while
maintaining functionality using the AI Agent.

Flow:
1. Define refactoring goal
2. Analyze current structure
3. Plan refactoring steps
4. Apply refactoring changes
5. Run tests to verify
"""

from src.config import load_config_and_llm
from src.agent.planner import Planner
from src.agent.executor import Executor
from src.agent.history import ConversationHistory
from typing import Dict, Any, List


def refactoring_workflow(
    refactoring_goal: str,
    target_files: List[str] = None,
    repo_path: str = ".",
    config_file: str = "agent.config.yaml"
) -> Dict[str, Any]:
    """
    Execute a code refactoring workflow.

    Args:
        refactoring_goal: Description of refactoring to perform
        target_files: List of files to refactor
        repo_path: Path to the repository
        config_file: Path to configuration file

    Returns:
        Dictionary with refactoring results
    """
    print("♻️  Code Refactoring Workflow")
    print("=" * 50)

    # Initialize
    config: Dict[str, Any]
    llm: Any
    config, llm = load_config_and_llm(config_file)

    planner: Planner = Planner(llm)
    executor: Executor = Executor(llm, repo_path)
    history: ConversationHistory = ConversationHistory()

    # Step 1: Define refactoring scope
    print(f"\n📋 Refactoring Goal:\n{refactoring_goal}\n")

    if target_files:
        print("📄 Target Files:")
        for file in target_files:
            print(f"  - {file}")
        print()

    history.add_message("user", f"Refactor: {refactoring_goal}")

    # Step 2: Plan refactoring
    print("🔍 Planning refactoring steps...")

    tasks: List[Any] = planner.plan(refactoring_goal)

    print(f"\n✅ Created {len(tasks)} refactoring steps:\n")
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task.description}")

    history.add_message("assistant", planner.get_plan_summary())

    # Step 3: Apply refactoring
    print("\n⚙️  Applying refactoring changes...\n")
    changes: Dict[int, Dict[str, Any]] = {}

    for task in tasks:
        print(f"🔧 {task.description}")
        try:
            result: str = executor.execute_task(task)
            planner.mark_task_complete(task.id, result)
            history.add_message("user", f"Execute refactoring task {task.id}")
            history.add_message("assistant", result)

            changes[task.id] = {
                "task": task.description,
                "result": result,
                "status": "completed"
            }
            print(f"   ✓ Completed\n")
        except Exception as e:
            changes[task.id] = {
                "task": task.description,
                "error": str(e),
                "status": "failed"
            }
            print(f"   ✗ Failed: {e}\n")

    # Step 4: Verification
    print("✅ Refactoring Verification")
    print("-" * 50)
    print(f"Refactoring Goal: {refactoring_goal}")
    print(f"Tasks Completed: {len([c for c in changes.values() if c['status'] == 'completed'])}/{len(tasks)}")
    print(f"Status: {'Success' if all(c['status'] == 'completed' for c in changes.values()) else 'Partial'}")

    return {
        "goal": refactoring_goal,
        "target_files": target_files or [],
        "tasks": len(tasks),
        "changes": changes,
        "history": history.get_summary(),
    }


if __name__ == "__main__":
    # Example usage
    result: Dict[str, Any] = refactoring_workflow(
        refactoring_goal="Extract database operations into a separate repository pattern class",
        target_files=["src/persistence.py", "src/api.py"],
        repo_path=".",
        config_file="agent.config.yaml"
    )

    print("\n✨ Refactoring workflow completed!")
