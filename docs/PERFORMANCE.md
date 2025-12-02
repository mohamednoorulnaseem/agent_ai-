# Performance Optimization Guide

This guide covers performance optimization strategies for the AI Agent Framework.

## Overview

Performance optimization focuses on:
- **Response Time**: Reduce latency of API endpoints
- **Memory Usage**: Minimize memory footprint
- **CPU Efficiency**: Optimize CPU utilization
- **LLM Costs**: Reduce API calls through caching and batching

## Built-in Optimization Features

### 1. Caching System

The framework includes a multi-level caching system:

#### Memory Cache
```python
from src.caching import MemoryCache

cache = MemoryCache(max_size_mb=100, default_ttl_seconds=3600)

# Manual caching
cache.set("key", "value", ttl_seconds=1800)
result = cache.get("key")

# Using decorator
from src.caching import CacheDecorator

@CacheDecorator(cache, ttl_seconds=300)
def expensive_function(arg):
    return compute_result(arg)
```

#### Persistent Cache
```python
from src.caching import PersistentCache

persistent_cache = PersistentCache(cache_dir=".cache")
persistent_cache.set("key", "value", ttl_seconds=86400)  # 24 hours
```

### 2. Performance Profiling

Track performance metrics:

```python
from src.performance import PerformanceProfiler, profile_operation

profiler = PerformanceProfiler(enable_memory_tracking=True)

@profile_operation(profiler, name="task_execution")
def execute_task(task):
    return task.execute()

# Get statistics
stats = profiler.get_stats("task_execution")
print(profiler.report())

# Export metrics
profiler.export_json("metrics.json")
```

### 3. Query Optimization

Optimize LLM queries:

```python
from src.performance import QueryOptimizer

optimizer = QueryOptimizer()

# Deduplicate queries
query_id = optimizer.deduplicate_query("same query")

# Batch multiple queries
queries = ["query1", "query2", "query3"]
batches = optimizer.batch_queries(queries)

# Optimize query format
optimized = optimizer.optimize_query(query)
```

## Configuration for Performance

### Environment Variables

```bash
# Cache settings
export AGENT_CACHE_MAX_SIZE_MB=100
export AGENT_CACHE_TTL_SECONDS=3600
export AGENT_PERSISTENT_CACHE=true

# Performance tracking
export AGENT_ENABLE_PROFILING=true
export AGENT_MEMORY_TRACKING=false

# LLM optimization
export AGENT_LLM_BATCH_SIZE=5
export AGENT_QUERY_DEDUPLICATION=true
```

### Configuration File

```yaml
# agent.config.yaml

performance:
  cache:
    enabled: true
    max_size_mb: 100
    default_ttl_seconds: 3600
    persistent: true
    persistent_dir: .cache

  profiling:
    enabled: false  # Enable for production monitoring
    memory_tracking: false  # Slower, but detailed
    export_interval_seconds: 3600

  optimization:
    query_deduplication: true
    query_batching: true
    batch_size: 5
    response_compression: true

llm:
  # Use smaller models for cost optimization
  model: "llama2-7b"  # Faster than larger models
  
  # Cache LLM responses
  response_cache_ttl: 3600
```

## Performance Best Practices

### 1. Enable Caching

```python
# Bad: No caching, repeated computation
result1 = agent.plan("Create API")
result2 = agent.plan("Create API")  # Same computation again

# Good: With caching
from src.caching import MemoryCache, CacheDecorator

cache = MemoryCache()

@CacheDecorator(cache, ttl_seconds=3600)
def plan_with_cache(goal):
    return agent.plan(goal)

result1 = plan_with_cache("Create API")
result2 = plan_with_cache("Create API")  # Cached, instant
```

### 2. Batch Queries

```python
# Bad: Sequential API calls
for task in tasks:
    result = llm.query(f"Execute: {task}")

# Good: Batch queries
from src.performance import QueryOptimizer

optimizer = QueryOptimizer()
queries = [f"Execute: {task}" for task in tasks]
batches = optimizer.batch_queries(queries)

for batch in batches:
    results = llm.query_batch(batch)
```

### 3. Monitor Performance

```python
# Enable profiling in production
from src.performance import PerformanceProfiler

profiler = PerformanceProfiler(enable_memory_tracking=False)

# Profile critical operations
@profile_operation(profiler)
def api_endpoint():
    return process_request()

# Export metrics periodically
import schedule
schedule.every(1).hour.do(
    lambda: profiler.export_json("metrics.json")
)
```

### 4. Optimize LLM Calls

```yaml
# Use smaller, faster models
llm:
  model: "llama2"  # Fast, 7B parameters
  # OR
  model: "mistral"  # Fast, 7B parameters

# Reduce context length
agent:
  max_context_tokens: 2000  # Smaller context
  max_history: 10  # Fewer messages
```

## Performance Benchmarks

Run benchmarks to measure improvements:

```bash
# Run performance benchmarks
python -m benchmarks.agent_benchmarks

# With specific configuration
AGENT_ENABLE_PROFILING=true python -m benchmarks.agent_benchmarks
```

Expected performance metrics:

| Operation | Uncached | Cached | Improvement |
|-----------|----------|--------|-------------|
| Plan generation | 5000ms | 50ms | 100x |
| API response | 2000ms | 100ms | 20x |
| Task execution | 3000ms | 500ms | 6x |

## Troubleshooting Performance

### High Memory Usage

**Symptoms**: Process memory growing continuously

**Solutions**:
1. Reduce cache size: `AGENT_CACHE_MAX_SIZE_MB=50`
2. Disable persistent cache: `AGENT_PERSISTENT_CACHE=false`
3. Enable memory tracking to identify leaks
4. Reduce history size: `max_history: 5`

### Slow API Responses

**Symptoms**: Endpoints returning slowly (>1000ms)

**Solutions**:
1. Enable caching for endpoints
2. Batch LLM queries
3. Use smaller LLM models
4. Reduce context length

### High LLM Costs

**Symptoms**: Excessive API billing

**Solutions**:
1. Enable query deduplication
2. Cache responses with longer TTL
3. Use local models (Ollama) instead of API
4. Batch queries to reduce calls

## Advanced Optimization

### Custom Caching Strategy

```python
class CustomCache:
    def __init__(self):
        self.memory_cache = MemoryCache(max_size_mb=50)
        self.persistent_cache = PersistentCache(".cache")

    def get(self, key):
        # Try memory first (fastest)
        result = self.memory_cache.get(key)
        if result is not None:
            return result

        # Try persistent cache (slower but survives restart)
        result = self.persistent_cache.get(key)
        if result is not None:
            self.memory_cache.set(key, result)
            return result

        return None

    def set(self, key, value, ttl=None):
        self.memory_cache.set(key, value, ttl)
        self.persistent_cache.set(key, value, ttl * 24 if ttl else None)
```

### Custom Profiling

```python
from src.performance import PerformanceProfiler

class DetailedProfiler(PerformanceProfiler):
    def analyze_bottlenecks(self):
        """Identify performance bottlenecks."""
        stats = self.get_all_stats()
        
        for op_name, stats in stats.items():
            avg_duration = stats['duration_ms']['avg']
            
            if avg_duration > 1000:
                print(f"⚠️  Slow: {op_name} ({avg_duration:.0f}ms)")
            
            if avg_duration > 5000:
                print(f"🔴 Very Slow: {op_name} ({avg_duration:.0f}ms)")
```

## Monitoring in Production

### Collect Metrics

```python
import logging
from src.performance import PerformanceProfiler

profiler = PerformanceProfiler()
logger = logging.getLogger(__name__)

# Log metrics periodically
import schedule

def log_metrics():
    stats = profiler.get_all_stats()
    logger.info(f"Performance stats: {stats}")

schedule.every(1).hour.do(log_metrics)
```

### Dashboard Integration

Export metrics to monitoring tools:

```python
# Export to Prometheus
def export_prometheus(profiler):
    stats = profiler.get_all_stats()
    
    for op_name, stat in stats.items():
        print(f"agent_duration_ms{{operation='{op_name}'}} {stat['duration_ms']['avg']}")

# Export to InfluxDB
def export_influxdb(profiler, client):
    stats = profiler.get_all_stats()
    
    for op_name, stat in stats.items():
        client.write_points([{
            "measurement": "agent_performance",
            "tags": {"operation": op_name},
            "fields": {
                "duration_ms": stat['duration_ms']['avg'],
                "memory_mb": stat['memory_delta_mb']['avg'],
            }
        }])
```

## References

- [Performance Profiling](../benchmarks/agent_benchmarks.py)
- [Caching System](../src/caching.py)
- [Performance Module](../src/performance.py)
- [Configuration Guide](./API.md#configuration)

---

For questions, see [Contributing Guide](CONTRIBUTING.md) or [Support](../SECURITY.md).
