"""
Command-line interface for the AI Agent.
Main entry point for interacting with the agent system.
"""

import argparse
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config_and_llm
from agent.planner import Planner
from agent.executor import Executor
from agent.history import ConversationHistory
def setup_parser() -> argparse.ArgumentParser:
    """Set up command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="AI Agent for automated development tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --goal "Create a REST API for user management"
  %(prog)s --goal "Fix all linting errors" --repo /path/to/repo
  %(prog)s --plan "Parse user input and plan tasks"
        """,
    )
    
    parser.add_argument(
        "--goal",
        type=str,
        help="High-level goal to accomplish",
    )
    
    parser.add_argument(
        "--plan",
        type=str,
        help="Create a plan for a specific goal",
    )
    
    parser.add_argument(
        "--execute",
        type=int,
        help="Execute task by ID",
    )
    
    parser.add_argument(
        "--repo",
        type=str,
        default=".",
        help="Path to repository (default: current directory)",
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default="agent.config.yaml",
        help="Path to configuration file (default: agent.config.yaml)",
    )
    
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive mode",
    )
    
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan repository and display summary",
    )
    
    parser.add_argument(
        "--history",
        action="store_true",
        help="Display conversation history",
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    
    return parser


def cmd_plan(planner: Planner, goal: str, history: ConversationHistory) -> list:
    """Plan a goal into tasks."""
    print(f"\nPlanning goal: {goal}")
    print("-" * 50)
    
    history.add_message("user", goal)
    tasks = planner.plan(goal)
    
    print(f"\nCreated {len(tasks)} tasks:\n")
    for task in tasks:
        print(f"[{task.id}] {task.description}")
    
    history.add_message("assistant", planner.get_plan_summary())
    
    return tasks


def cmd_execute(executor: Executor, task_id: int, planner: Planner, history: ConversationHistory):
    """Execute a specific task."""
    if task_id not in planner.tasks:
        print(f"Task {task_id} not found")
        return
    
    task = planner.tasks[task_id]
    
    print(f"\nExecuting task {task_id}: {task.description}")
    print("-" * 50)
    
    result = executor.execute_task(task)
    planner.mark_task_complete(task_id, result)
    
    print(result)
    
    history.add_message("user", f"Execute task {task_id}")
    history.add_message("assistant", result)
    
    print("\n✓ Task completed")


def cmd_scan(executor: Executor):
    """Scan repository."""
    print("Scanning repository...")
    print("-" * 50)
    
    info = executor.scanner.scan_repository()
    print(info)


def cmd_history(history: ConversationHistory):
    """Display conversation history."""
    summary = history.get_summary()
    print("\nConversation History:")
    print("-" * 50)
    print(f"Total Messages: {summary['total_messages']}")
    print(f"User Messages: {summary['user_messages']}")
    print(f"Assistant Messages: {summary['assistant_messages']}")
    print(f"Created At: {summary['created_at']}")
    
    if summary['last_message']:
        print(f"\nLast Message: {summary['last_message']['role']}")
        print(f"Content: {summary['last_message']['content'][:100]}...")


def interactive_mode(planner: Planner, executor: Executor, history: ConversationHistory):
    """Run interactive mode."""
    print("\n" + "=" * 50)
    print("AI Agent - Interactive Mode")
    print("=" * 50)
    print("Commands:")
    print("  plan <goal>      - Create a plan for a goal")
    print("  exec <task_id>   - Execute a specific task")
    print("  show plan        - Display current plan")
    print("  scan             - Scan repository")
    print("  history          - Show conversation history")
    print("  exit             - Exit interactive mode")
    print("=" * 50 + "\n")
    
    while True:
        try:
            user_input = input("agent> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                return

            if user_input.lower() == "help":
                print("Available commands: plan <goal>, exec <task_id>, show plan, scan, history, exit")
                continue
            
            elif user_input.lower() == "scan":
                cmd_scan(executor)
            
            elif user_input.lower() == "history":
                cmd_history(history)
            
            elif user_input.lower() == "show plan":
                print(planner.get_plan_summary())
            
            elif user_input.lower().startswith("plan "):
                goal = user_input[5:].strip()
                cmd_plan(planner, goal, history)
            
            elif user_input.lower().startswith("exec "):
                try:
                    task_id = int(user_input[5:].strip())
                    cmd_execute(executor, task_id, planner, history)
                except ValueError:
                    print("Invalid task ID")
            
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main entry point."""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Load configuration
    try:
        config, llm = load_config_and_llm(args.config)
    except FileNotFoundError:
        print(f"Error: Configuration file '{args.config}' not found")
        print("Please create an agent.config.yaml file with LLM settings")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)
    
    # Resolve repository path
    repo_path = os.path.abspath(args.repo)
    if not os.path.isdir(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist")
        sys.exit(1)
    
    # Initialize components
    planner = Planner(llm)
    executor = Executor(llm, repo_path)
    history = ConversationHistory()
    
    if args.verbose:
        print(f"Configuration: {args.config}")
        print(f"Repository: {repo_path}")
        print(f"LLM Provider: {config.get('llm', {}).get('provider')}")
    
    # Execute commands
    try:
        if args.scan:
            cmd_scan(executor)
        
        elif args.plan:
            cmd_plan(planner, args.plan, history)
        
        elif args.goal:
            tasks = cmd_plan(planner, args.goal, history)
            if tasks:
                print("\nFirst task ready for execution")
                print(f"Run: agent --execute {tasks[0].id} --repo {args.repo}")
        
        elif args.execute:
            cmd_execute(executor, args.execute, planner, history)
        
        elif args.history:
            cmd_history(history)
        
        elif args.interactive:
            interactive_mode(planner, executor, history)
            # Normal completion of interactive mode
            sys.exit(0)
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # If we reach here normally, exit with success
    sys.exit(0)


if __name__ == "__main__":
    main()
