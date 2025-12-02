#!/usr/bin/env python3
"""
AI Agent Framework - Interactive Demo Script

This script demonstrates the core capabilities of the AI Agent Framework
including task planning, execution, conversation management, and API usage.

Run with: python scripts/demo.py
"""

import json
import sys
import time
from typing import Any, Dict, List

# Color codes for terminal output
COLORS = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "END": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{COLORS['BOLD']}{COLORS['BLUE']}{'=' * 60}{COLORS['END']}")
    print(f"{COLORS['BOLD']}{COLORS['BLUE']}{text.center(60)}{COLORS['END']}")
    print(f"{COLORS['BOLD']}{COLORS['BLUE']}{'=' * 60}{COLORS['END']}\n")


def print_section(text: str) -> None:
    """Print a formatted section title."""
    print(f"\n{COLORS['CYAN']}{COLORS['BOLD']}► {text}{COLORS['END']}")
    print(f"{COLORS['CYAN']}{'-' * (len(text) + 2)}{COLORS['END']}\n")


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{COLORS['GREEN']}✓ {text}{COLORS['END']}")


def print_info(text: str) -> None:
    """Print info message."""
    print(f"{COLORS['CYAN']}ℹ {text}{COLORS['END']}")


def print_warning(text: str) -> None:
    """Print warning message."""
    print(f"{COLORS['YELLOW']}⚠ {text}{COLORS['END']}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"{COLORS['RED']}✗ {text}{COLORS['END']}")


def simulate_typing(text: str, delay: float = 0.01) -> None:
    """Simulate typing effect for better UX."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def demo_task_planning() -> None:
    """Demo 1: Task Planning - Breaking down complex goals."""
    print_section("DEMO 1: Task Planning with LLM")

    goal = "Create a REST API for user management with authentication"
    print(f"Goal: {COLORS['BOLD']}{goal}{COLORS['END']}\n")

    print("Planning tasks (simulated)...\n")

    tasks: List[Dict[str, Any]] = [
        {
            "id": 1,
            "title": "Setup FastAPI project structure",
            "description": "Initialize FastAPI app with necessary directories",
            "status": "completed",
        },
        {
            "id": 2,
            "title": "Create User model and database schema",
            "description": "Define User model with SQLAlchemy and create DB migrations",
            "status": "completed",
        },
        {
            "id": 3,
            "title": "Implement authentication endpoints",
            "description": "Create login/signup endpoints with JWT token generation",
            "status": "in_progress",
        },
        {
            "id": 4,
            "title": "Add user CRUD operations",
            "description": "Implement endpoints for Create, Read, Update, Delete operations",
            "status": "pending",
        },
        {
            "id": 5,
            "title": "Setup API documentation",
            "description": "Enable Swagger UI and generate API documentation",
            "status": "pending",
        },
    ]

    for task in tasks:
        status_color = {
            "completed": COLORS["GREEN"],
            "in_progress": COLORS["YELLOW"],
            "pending": COLORS["CYAN"],
        }[task["status"]]

        print(f"  Task {task['id']}: {task['title']}")
        print(f"    Status: {status_color}[{task['status'].upper()}]{COLORS['END']}")
        print(f"    {task['description']}\n")

    print_success("Task planning completed! Ready for execution.\n")


def demo_conversation_management() -> None:
    """Demo 2: Conversation Management - Multi-turn interactions."""
    print_section("DEMO 2: Conversation Management")

    conversation_history = [
        {"role": "user", "content": "Create a REST API for user management"},
        {
            "role": "assistant",
            "content": "I'll help you create a REST API. Let me break this down into tasks.",
        },
        {
            "role": "user",
            "content": "Make sure to include authentication",
        },
        {
            "role": "assistant",
            "content": "Added JWT authentication to the plan. 5 tasks ready.",
        },
        {
            "role": "user",
            "content": "Can you execute the first 3 tasks?",
        },
        {
            "role": "assistant",
            "content": "Executing tasks 1-3 now. This will take about 2 minutes.",
        },
    ]

    print(f"Conversation history ({len(conversation_history)} messages):\n")

    for i, msg in enumerate(conversation_history, 1):
        role_label = f"{COLORS['BOLD']}{msg['role'].upper()}{COLORS['END']}"
        print(f"{i}. {role_label}: {msg['content']}\n")

    print_success(f"Conversation with {len(conversation_history)} messages tracked.\n")


def demo_repository_analysis() -> None:
    """Demo 3: Repository Analysis - Understanding codebases."""
    print_section("DEMO 3: Repository Analysis")

    repo_stats = {
        "total_files": 42,
        "python_files": 28,
        "test_files": 8,
        "documentation_files": 6,
        "total_lines": 5234,
        "average_file_size": 124,
        "largest_file": ("src/api.py", 523),
    }

    print("Repository scan results:\n")
    print(
        f"  Total files: {COLORS['YELLOW']}{repo_stats['total_files']}{COLORS['END']}"
    )
    print(
        f"  Python files: {COLORS['YELLOW']}{repo_stats['python_files']}{COLORS['END']}"
    )
    print(f"  Test files: {COLORS['YELLOW']}{repo_stats['test_files']}{COLORS['END']}")
    print(
        f"  Documentation: {COLORS['YELLOW']}{repo_stats['documentation_files']}{COLORS['END']}"
    )
    print(
        f"  Total lines: {COLORS['YELLOW']}{repo_stats['total_lines']}{COLORS['END']}"
    )
    print(
        f"  Average file size: {COLORS['YELLOW']}{repo_stats['average_file_size']} lines{COLORS['END']}"
    )
    print(
        f"  Largest file: {COLORS['YELLOW']}{repo_stats['largest_file'][0]}{COLORS['END']} "
        f"({repo_stats['largest_file'][1]} lines)\n"
    )

    print_success("Repository analysis completed.\n")


def demo_api_integration() -> None:
    """Demo 4: REST API Integration - Remote access."""
    print_section("DEMO 4: REST API Integration")

    print("Demonstrating REST API endpoints:\n")

    endpoints = [
        {
            "method": "GET",
            "endpoint": "/health",
            "description": "Check API health status",
            "response": {"status": "ok", "version": "0.1.0"},
        },
        {
            "method": "POST",
            "endpoint": "/plans",
            "description": "Create a new plan from a goal",
            "response": {"id": 1, "goal": "Create REST API", "status": "planning"},
        },
        {
            "method": "GET",
            "endpoint": "/plans/1",
            "description": "Get plan details",
            "response": {
                "id": 1,
                "goal": "Create REST API",
                "status": "in_progress",
                "tasks_count": 5,
            },
        },
        {
            "method": "POST",
            "endpoint": "/plans/1/execute",
            "description": "Execute plan tasks",
            "response": {
                "plan_id": 1,
                "executed_tasks": 3,
                "status": "in_progress",
            },
        },
    ]

    for ep in endpoints:
        print(
            f"  {COLORS['BOLD']}{ep['method']:<6}{COLORS['END']} {COLORS['CYAN']}{ep['endpoint']:<20}{COLORS['END']}"
        )
        print(f"    {ep['description']}")
        print(f"    Response: {json.dumps(ep['response'], indent=18)}\n")

    print_success("API integration demonstrated.\n")


def demo_llm_providers() -> None:
    """Demo 5: Multi-provider LLM Support."""
    print_section("DEMO 5: Multi-Provider LLM Support")

    providers = [
        {
            "name": "Ollama",
            "status": "✓ Available locally",
            "models": ["llama2", "mistral", "neural-chat"],
            "setup": "ollama pull llama2",
        },
        {
            "name": "OpenAI",
            "status": "✓ Cloud-based (API key required)",
            "models": ["gpt-4", "gpt-3.5-turbo"],
            "setup": "Set OPENAI_API_KEY environment variable",
        },
        {
            "name": "OpenAI-compatible",
            "status": "✓ Any OpenAI-API compatible endpoint",
            "models": ["Custom models"],
            "setup": "Set custom API_BASE URL",
        },
    ]

    for provider in providers:
        print(f"{COLORS['BOLD']}{provider['name']}{COLORS['END']}")
        print(f"  Status: {provider['status']}")
        print(f"  Available models: {', '.join(provider['models'])}")
        print(f"  Setup: {provider['setup']}\n")

    print_success("Multi-provider LLM support ready.\n")


def demo_code_examples() -> None:
    """Demo 6: Quick Code Examples."""
    print_section("DEMO 6: Quick Code Examples")

    examples = [
        {
            "title": "CLI Usage",
            "code": "python -m src.cli --goal 'Create a REST API' --interactive",
        },
        {
            "title": "API Usage (Python)",
            "code": """import requests
response = requests.post('http://localhost:8000/plans', 
                        json={'goal': 'Create REST API'})
plan = response.json()""",
        },
        {
            "title": "Configuration",
            "code": """# Create agent.config.yaml
llm:
  provider: "ollama"
  model: "llama2"
  api_base: "http://localhost:11434" """,
        },
        {
            "title": "Docker",
            "code": "docker compose up --build\n# Access at http://localhost:8000",
        },
    ]

    for i, example in enumerate(examples, 1):
        print(f"{i}. {COLORS['BOLD']}{example['title']}{COLORS['END']}")
        print(f"   {COLORS['YELLOW']}{example['code']}{COLORS['END']}\n")

    print_success("Code examples ready for reference.\n")


def demo_workflow_templates() -> None:
    """Demo 7: Workflow Templates - Pre-built use cases."""
    print_section("DEMO 7: Workflow Templates")

    templates = [
        {
            "name": "Feature Implementation",
            "description": "Plan and implement a new feature in your codebase",
            "steps": 5,
        },
        {
            "name": "Bug Fix Workflow",
            "description": "Identify, analyze, and fix bugs systematically",
            "steps": 4,
        },
        {
            "name": "Code Refactoring",
            "description": "Improve code structure while maintaining functionality",
            "steps": 6,
        },
        {
            "name": "Test Generation",
            "description": "Automatically generate test cases for your code",
            "steps": 4,
        },
        {
            "name": "Documentation",
            "description": "Generate and update project documentation",
            "steps": 3,
        },
    ]

    for template in templates:
        print(f"• {COLORS['BOLD']}{template['name']}{COLORS['END']}")
        print(f"  {template['description']}")
        print(f"  Steps: {template['steps']}\n")

    print_success(f"Found {len(templates)} pre-built workflow templates.\n")


def show_next_steps() -> None:
    """Show next steps for users."""
    print_section("Next Steps")

    steps = [
        "1. Read the documentation: docs/API.md, docs/DEPLOYMENT.md",
        "2. Configure LLM provider: Create agent.config.yaml",
        "3. Run the application: python -m src.api",
        "4. Try the CLI: python -m src.cli --interactive",
        "5. Check the Swagger UI: http://localhost:8000/docs",
        "6. Deploy with Docker: docker compose up --build",
    ]

    for step in steps:
        print(f"  {COLORS['GREEN']}→{COLORS['END']} {step}")

    print()


def main() -> None:
    """Run the demo."""
    print_header("AI Agent Framework - Interactive Demo")

    print_info("This demo showcases the core capabilities of the AI Agent Framework.\n")

    # Run all demos
    demo_task_planning()
    input(f"{COLORS['BOLD']}Press Enter to continue...{COLORS['END']}")

    demo_conversation_management()
    input(f"{COLORS['BOLD']}Press Enter to continue...{COLORS['END']}")

    demo_repository_analysis()
    input(f"{COLORS['BOLD']}Press Enter to continue...{COLORS['END']}")

    demo_api_integration()
    input(f"{COLORS['BOLD']}Press Enter to continue...{COLORS['END']}")

    demo_llm_providers()
    input(f"{COLORS['BOLD']}Press Enter to continue...{COLORS['END']}")

    demo_code_examples()
    input(f"{COLORS['BOLD']}Press Enter to continue...{COLORS['END']}")

    demo_workflow_templates()

    show_next_steps()

    print_header("Demo Complete!")
    print_success("All features demonstrated successfully!")
    print_info("For more information, visit: https://github.com/mohamednoorulnaseem/agent_ai-")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{COLORS['YELLOW']}Demo interrupted by user.{COLORS['END']}")
        sys.exit(0)
