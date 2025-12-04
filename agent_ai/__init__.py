"""
Agent AI Framework - Advanced Professional Edition

A production-ready AI agent platform with enterprise features,
comprehensive infrastructure support, and advanced optimizations.

VERSION: 1.0.0
STATUS: Production Ready
"""

from src import __version__
from src.api import create_app
from src.agent.executor import PlanExecutor
from src.agent.planner import Planner
from src.caching import MemoryCache, PersistentCache, CacheDecorator
from src.performance import PerformanceProfiler, profile_operation, QueryOptimizer
from src.query_engine import QueryFilterBuilder, QueryExecutor, SearchEngine
from src.webhooks import EventType, EventStream, WebhookManager

__all__ = [
    "__version__",
    "create_app",
    "PlanExecutor",
    "Planner",
    "MemoryCache",
    "PersistentCache",
    "CacheDecorator",
    "PerformanceProfiler",
    "profile_operation",
    "QueryOptimizer",
    "QueryFilterBuilder",
    "QueryExecutor",
    "SearchEngine",
    "EventType",
    "EventStream",
    "WebhookManager",
]

__title__ = "Agent AI Framework"
__description__ = "Enterprise-grade AI agent platform with advanced features"
__url__ = "https://github.com/mohamednoorulnaseem/agent_ai"
__author__ = "Mohamed Noor Ulnaseem"
__license__ = "Apache 2.0"
__version__ = "1.0.0"
