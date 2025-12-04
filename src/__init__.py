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

__author__ = "AI Agent Team"

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Core configuration and agent framework
from config import load_config_and_llm
from agent.planner import Planner, Task
from agent.executor import Executor
from agent.history import ConversationHistory
from llm.base import LLM
from llm.ollama import Ollama
from llm.openai_like import OpenAILike
from repo.scanner import Scanner
from repo.patcher import Patcher

# Phase 7 exports (webhooks, query engine, caching, performance)
from .webhooks import (
    EventType,
    WebhookManager,
    WebhookEvent,
    WebhookDelivery,
    EventStream,
)
from .query_engine import (
    QueryFilterBuilder,
    QueryExecutor,
    SearchEngine,
)
from .caching import (
    MemoryCache,
    PersistentCache,
    CacheDecorator,
    CacheStatistics,
)
from .performance import (
    PerformanceProfiler,
    profile_operation,
    QueryOptimizer,
    PerformanceStatistics,
)
from .advanced_pro import (
    CircuitBreaker,
    RateLimiter,
    RequestSignature,
    AdaptiveCaching,
    DistributedTracing,
    AdvancedAnalytics,
    AdvancedMetrics,
)

# Prefer package version from src/__version__.py when available
try:
    from .__version__ import __version__ as _pkg_version
    __version__ = _pkg_version
except Exception:
    __version__ = "0.1.0"

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
    # Phase 7 exports
    "EventType",
    "WebhookManager",
    "WebhookEvent",
    "WebhookDelivery",
    "EventStream",
    "QueryFilterBuilder",
    "QueryExecutor",
    "SearchEngine",
    "MemoryCache",
    "PersistentCache",
    "CacheDecorator",
    "CacheStatistics",
    "PerformanceProfiler",
    "profile_operation",
    "QueryOptimizer",
    "PerformanceStatistics",
    # Advanced Pro Features
    "CircuitBreaker",
    "RateLimiter",
    "RequestSignature",
    "AdaptiveCaching",
    "DistributedTracing",
    "AdvancedAnalytics",
    "AdvancedMetrics",
    "__version__",
]
