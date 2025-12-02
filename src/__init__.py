"""
AI Agent - An intelligent agent framework for automated development tasks.

This package provides a complete AI agent system with:
- Task planning using LLMs
- Repository scanning and analysis
- Code patching and modifications
- Conversation history tracking
- Command-line interface for interaction

Example usage:
    from agent_ai.config import load_config_and_llm
    from agent_ai.agent.planner import Planner
    from agent_ai.agent.executor import Executor
    
    config, llm = load_config_and_llm()
    planner = Planner(llm)
    executor = Executor(llm, "/path/to/repo")
    
    tasks = planner.plan("Create a REST API")
    for task in tasks:
        result = executor.execute_task(task)
        print(result)
"""

__version__ = "0.1.0"
__author__ = "AI Agent Team"

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config_and_llm
from agent.planner import Planner, Task
from agent.executor import Executor
from agent.history import ConversationHistory
from llm.base import LLM
from llm.ollama import Ollama
from llm.openai_like import OpenAILike
from repo.scanner import Scanner
from repo.patcher import Patcher

__all__ = [
    "load_config_and_llm",
    "Planner",
    "Task",
    "Executor",
    "ConversationHistory",
    "LLM",
    "Ollama",
    "OpenAILike",
    "Scanner",
    "Patcher",
]
