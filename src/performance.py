"""
Performance profiling and monitoring tools.

Tracks execution time, memory usage, and other performance metrics
for agent operations and API endpoints.
"""

import time
import psutil
import functools
from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class PerformanceMetrics:
    """Performance metrics for an operation."""
    name: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_ms: float = 0.0
    memory_start_mb: float = 0.0
    memory_end_mb: float = 0.0
    memory_delta_mb: float = 0.0
    cpu_percent: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def finish(self) -> None:
        """Mark operation as finished and calculate metrics."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "duration_ms": round(self.duration_ms, 2),
            "memory_delta_mb": round(self.memory_delta_mb, 2),
            "cpu_percent": round(self.cpu_percent, 2),
            "timestamp": self.timestamp,
        }


class PerformanceProfiler:
    """Profile and track performance metrics."""

    def __init__(self, enable_memory_tracking: bool = True):
        """
        Initialize profiler.

        Args:
            enable_memory_tracking: Enable memory tracking (slower)
        """
        self.enable_memory_tracking = enable_memory_tracking
        self.metrics: Dict[str, list] = {}
        self.process = psutil.Process()

    def start_operation(self, name: str) -> PerformanceMetrics:
        """Start tracking an operation."""
        metrics = PerformanceMetrics(name=name)

        if self.enable_memory_tracking:
            mem_info = self.process.memory_info()
            metrics.memory_start_mb = mem_info.rss / (1024 * 1024)

        return metrics

    def finish_operation(self, metrics: PerformanceMetrics) -> None:
        """Finish tracking an operation."""
        metrics.finish()

        if self.enable_memory_tracking:
            mem_info = self.process.memory_info()
            metrics.memory_end_mb = mem_info.rss / (1024 * 1024)
            metrics.memory_delta_mb = metrics.memory_end_mb - metrics.memory_start_mb

        # Try to get CPU percent
        try:
            metrics.cpu_percent = self.process.cpu_percent(interval=0.1)
        except Exception:
            metrics.cpu_percent = 0.0

        # Store metric
        if metrics.name not in self.metrics:
            self.metrics[metrics.name] = []
        self.metrics[metrics.name].append(metrics)

    def get_stats(self, operation_name: str) -> Dict[str, Any]:
        """Get statistics for an operation."""
        if operation_name not in self.metrics:
            return {}

        metrics_list = self.metrics[operation_name]
        durations = [m.duration_ms for m in metrics_list]
        memory_deltas = [m.memory_delta_mb for m in metrics_list]

        return {
            "operation": operation_name,
            "count": len(metrics_list),
            "duration_ms": {
                "min": min(durations),
                "max": max(durations),
                "avg": sum(durations) / len(durations),
                "total": sum(durations),
            },
            "memory_delta_mb": {
                "min": min(memory_deltas) if memory_deltas else 0,
                "max": max(memory_deltas) if memory_deltas else 0,
                "avg": sum(memory_deltas) / len(memory_deltas) if memory_deltas else 0,
            },
        }

    def get_all_stats(self) -> Dict[str, Any]:
        """Get statistics for all operations."""
        return {
            name: self.get_stats(name)
            for name in self.metrics.keys()
        }

    def report(self) -> str:
        """Generate performance report."""
        lines = ["Performance Report", "=" * 60]

        for operation_name in sorted(self.metrics.keys()):
            stats = self.get_stats(operation_name)
            lines.append(f"\n{operation_name}")
            lines.append(f"  Count: {stats['count']}")
            lines.append(
                f"  Duration: {stats['duration_ms']['avg']:.2f}ms "
                f"(min: {stats['duration_ms']['min']:.2f}, "
                f"max: {stats['duration_ms']['max']:.2f})"
            )
            lines.append(
                f"  Memory: {stats['memory_delta_mb']['avg']:.2f}MB "
                f"(min: {stats['memory_delta_mb']['min']:.2f}, "
                f"max: {stats['memory_delta_mb']['max']:.2f})"
            )

        return "\n".join(lines)

    def export_json(self, filepath: str) -> None:
        """Export metrics to JSON file."""
        data = {
            "timestamp": datetime.now().isoformat(),
            "stats": self.get_all_stats(),
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)


def profile_operation(profiler: PerformanceProfiler, name: Optional[str] = None) -> Callable:
    """Decorator to profile a function."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            operation_name = name or func.__name__
            metrics = profiler.start_operation(operation_name)

            try:
                result = func(*args, **kwargs)
                return result
            finally:
                profiler.finish_operation(metrics)

        return wrapper

    return decorator


class QueryOptimizer:
    """Optimize LLM queries through batching and deduplication."""

    def __init__(self):
        """Initialize query optimizer."""
        self.query_cache: Dict[str, str] = {}
        self.batch_size = 5
        self.pending_queries: list = []

    def deduplicate_query(self, query: str) -> str:
        """Check if query is a duplicate and return cached result key."""
        query_hash = str(hash(query))

        if query in self.query_cache:
            return self.query_cache[query]

        self.query_cache[query] = query_hash
        return query_hash

    def batch_queries(self, queries: list) -> list:
        """Batch multiple queries for more efficient processing."""
        batches = []
        for i in range(0, len(queries), self.batch_size):
            batch = queries[i : i + self.batch_size]
            batches.append(batch)

        return batches

    def optimize_query(self, query: str) -> str:
        """Optimize query format for faster processing."""
        # Remove unnecessary whitespace
        query = " ".join(query.split())

        # Convert to lowercase for comparison
        query_lower = query.lower()

        return query_lower
