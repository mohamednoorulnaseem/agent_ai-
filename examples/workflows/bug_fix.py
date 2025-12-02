"""
Example 2: Bug Fix Workflow

This example demonstrates a systematic approach to identifying,
analyzing, and fixing bugs using the AI Agent.

Flow:
1. Describe the bug/issue
2. Agent analyzes the codebase
3. Identify root cause
4. Generate fix
5. Execute fix and test
"""

from src.config import load_config_and_llm
from src.agent.planner import Planner
from src.agent.executor import Executor
from src.agent.history import ConversationHistory
from typing import Dict, Any, List


def bug_fix_workflow(
    bug_description: str,
    affected_file: str = None,
    repo_path: str = ".",
    config_file: str = "agent.config.yaml"
) -> Dict[str, Any]:
    """
    Execute a bug fix workflow.

    Args:
        bug_description: Description of the bug to fix
        affected_file: Optional path to affected file
        repo_path: Path to the repository
        config_file: Path to configuration file

    Returns:
        Dictionary with bug fix results
    """
    # Initialize
    print("🐛 Bug Fix Workflow")
    print("=" * 50)

    config: Dict[str, Any]
    llm: Any
    config, llm = load_config_and_llm(config_file)

    planner: Planner = Planner(llm)
    executor: Executor = Executor(llm, repo_path)
    history: ConversationHistory = ConversationHistory()

    # Step 1: Analyze bug
    print(f"\n📝 Bug Description:\n{bug_description}\n")

    if affected_file:
        print(f"📄 Affected File: {affected_file}\n")

    history.add_message("user", f"Fix bug: {bug_description}")

    # Step 2: Plan bug fix
    bug_goal: str = f"Identify and fix: {bug_description}"
    print("🔍 Planning bug fix steps...")

    tasks: List[Any] = planner.plan(bug_goal)

    print(f"\n✅ Created {len(tasks)} bug fix tasks:\n")
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task.description}")

    history.add_message("assistant", planner.get_plan_summary())

    # Step 3: Execute fix steps
    print("\n⚙️  Executing fix steps...\n")
    fix_results: Dict[int, str] = {}

    for task in tasks:
        print(f"🔧 {task.description}")
        try:
            result: str = executor.execute_task(task)
            fix_results[task.id] = result
            planner.mark_task_complete(task.id, result)
            history.add_message("user", f"Execute task {task.id}")
            history.add_message("assistant", result)
            print(f"   ✓ Completed\n")
        except Exception as e:
            print(f"   ✗ Failed: {e}\n")
            fix_results[task.id] = f"Failed: {str(e)}"

    # Step 4: Generate report
    print("📋 Bug Fix Report")
    print("-" * 50)
    summary: Dict[str, Any] = history.get_summary()
    print(f"Bug: {bug_description}")
    print(f"Status: {'Fixed' if len(fix_results) == len(tasks) else 'Partial Fix'}")
    print(f"Steps Completed: {len(fix_results)}/{len(tasks)}")

    return {
        "bug": bug_description,
        "affected_file": affected_file,
        "tasks": len(tasks),
        "completed": len(fix_results),
        "results": fix_results,
        "summary": summary,
    }


if __name__ == "__main__":
    # Example usage
    result: Dict[str, Any] = bug_fix_workflow(
        bug_description="API returns 500 error when creating user with duplicate email",
        affected_file="src/api.py",
        repo_path=".",
        config_file="agent.config.yaml"
    )

    print("\n✨ Bug fix workflow completed!")
