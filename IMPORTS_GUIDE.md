# Complete Imports Guide - Phase 7

## Module Organization & Import Patterns

### Core Module Imports

#### Webhooks & Events
```python
# Event type enumeration
from src.webhooks import EventType

# Available events:
# - EventType.PLAN_CREATED
# - EventType.PLAN_STARTED
# - EventType.PLAN_COMPLETED
# - EventType.PLAN_FAILED
# - EventType.TASK_STARTED
# - EventType.TASK_COMPLETED
# - EventType.TASK_FAILED
# - EventType.CONVERSATION_MESSAGE

# Webhook management
from src.webhooks import WebhookManager, WebhookEvent, WebhookDelivery

# Event streaming (Server-Sent Events)
from src.webhooks import EventStream

# Complete webhook import
from src.webhooks import (
    EventType,
    WebhookManager,
    WebhookEvent,
    WebhookDelivery,
    EventStream
)
```

**Usage Example**:
```python
from src.webhooks import WebhookManager, EventType, WebhookEvent

webhook_manager = WebhookManager()

# Register webhook
webhook = webhook_manager.register_webhook(
    url="https://example.com/webhook",
    event_types=[EventType.PLAN_COMPLETED, EventType.TASK_FAILED],
    secret="your-secret-key"
)

# Trigger event
event = WebhookEvent(
    type=EventType.PLAN_COMPLETED,
    data={"plan_id": 123, "status": "completed"}
)

import asyncio
asyncio.run(webhook_manager.trigger_event(event))

# Stream events
stream = EventStream(webhook_manager)
for event in stream:
    print(f"Received: {event.type}")
```

---

#### Query Engine & Filtering
```python
# Query filter builder
from src.query_engine import QueryFilterBuilder

# Query executor
from src.query_engine import QueryExecutor

# Search engine
from src.query_engine import SearchEngine

# Complete query engine import
from src.query_engine import (
    QueryFilterBuilder,
    QueryExecutor,
    SearchEngine
)
```

**Operators Reference**:
```python
from src.query_engine import QueryFilterBuilder

builder = QueryFilterBuilder()

# Comparison operators
.eq("field", "value")           # Equals
.ne("field", "value")           # Not equals
.gt("field", 10)                # Greater than
.gte("field", 10)               # Greater than or equal
.lt("field", 10)                # Less than
.lte("field", 10)               # Less than or equal

# String operators
.contains("field", "text")      # Contains substring
.in("field", ["a", "b", "c"])   # In list
.regex("field", "^pattern$")    # Regex match

# Logical operators
.and_filter()                   # AND logic
.or_filter()                    # OR logic

# Sorting and pagination
.sort("field", "asc")           # Sort ascending
.sort("field", "desc")          # Sort descending
.paginate(limit=10, offset=0)   # Pagination

.build()                        # Build filter
```

**Usage Example**:
```python
from src.query_engine import QueryFilterBuilder, QueryExecutor, SearchEngine

# Build complex filter
query_filter = (
    QueryFilterBuilder()
    .eq("status", "completed")
    .gte("created_at", "2025-12-01")
    .contains("goal", "API")
    .sort("created_at", "desc")
    .paginate(limit=10, offset=0)
    .build()
)

# Apply filter
results = QueryExecutor.apply_filter(data, query_filter)

# Search
search_engine = SearchEngine()
search_results = search_engine.search(data, "REST API")
```

---

#### Caching System
```python
# In-memory cache
from src.caching import MemoryCache

# Persistent cache
from src.caching import PersistentCache

# Cache decorator
from src.caching import CacheDecorator

# Cache statistics
from src.caching import CacheStatistics

# Complete caching import
from src.caching import (
    MemoryCache,
    PersistentCache,
    CacheDecorator,
    CacheStatistics
)
```

**Usage Example**:
```python
from src.caching import MemoryCache, CacheDecorator

# Create cache instance
cache = MemoryCache(max_size=1000, ttl=3600)

# Use decorator
@CacheDecorator(cache, key_builder=lambda x: f"operation_{x}")
def expensive_operation(data):
    # Expensive computation
    return process_data(data)

# Manual cache operations
cache.set("key", "value", ttl=3600)
value = cache.get("key")
cache.delete("key")
cache.clear()

# Get statistics
stats = cache.get_stats()
print(f"Hits: {stats['hits']}, Misses: {stats['misses']}")
print(f"Hit Rate: {stats['hit_rate']:.2%}")
```

---

#### Performance Profiling
```python
# Performance profiler
from src.performance import PerformanceProfiler

# Profile decorator
from src.performance import profile_operation

# Query optimizer
from src.performance import QueryOptimizer

# Performance statistics
from src.performance import PerformanceStatistics

# Complete performance import
from src.performance import (
    PerformanceProfiler,
    profile_operation,
    QueryOptimizer,
    PerformanceStatistics
)
```

**Usage Example**:
```python
from src.performance import PerformanceProfiler, profile_operation

# Create profiler
profiler = PerformanceProfiler()

# Profile with decorator
@profile_operation(profiler, "my_operation")
def my_function(data):
    return process_data(data)

# Get statistics
stats = profiler.get_stats("my_operation")
print(f"Duration: {stats['duration_ms']['avg']}ms")
print(f"Memory: {stats['memory_mb']['avg']}MB")
print(f"Calls: {stats['calls']}")

# Export metrics
metrics_json = profiler.export_metrics()

# Query optimizer
optimizer = QueryOptimizer()
optimized_query = optimizer.optimize_query(original_query)
```

---

#### Version Management
```python
# Version info
from src import __version__

# Access version
print(__version__)  # Returns current version
```

---

## Framework Imports

### Base Classes & Interfaces
```python
# Core agent framework (from existing project)
from agent.executor import Executor
from agent.planner import Planner
from agent.history import History

# LLM support
from llm.base import LLMBase
from llm.openai_like import OpenAILikeLLM
from llm.ollama import OllamaLLM

# Repository tools
from repo.scanner import Scanner
from repo.patcher import Patcher
```

### API Module
```python
# FastAPI application
from api import create_app, get_app

# Authentication
from auth import verify_token, create_token

# Configuration
from config import load_config, get_settings
```

---

## Infrastructure Files Organization

### Kubernetes Manifests
```
k8s/
├── deployment.yaml    # Agent AI deployment with HPA
├── service.yaml       # Service definitions and configuration
└── configmap.yaml     # ConfigMaps and Secrets
```

**Deployment via Kubernetes**:
```bash
# Create namespace
kubectl create namespace agent-ai

# Apply manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/configmap.yaml

# Check status
kubectl get pods -n agent-ai
kubectl get services -n agent-ai

# Scale if needed
kubectl scale deployment agent-ai --replicas=5 -n agent-ai
```

### Terraform Configuration
```
terraform/
├── main.tf         # AWS VPC, EKS, RDS, ElastiCache, ECR
├── variables.tf    # Input variables
└── outputs.tf      # Output values
```

**Deployment via Terraform**:
```bash
cd terraform

# Plan infrastructure
terraform plan

# Apply infrastructure
terraform apply

# Get outputs
terraform output

# Destroy infrastructure
terraform destroy
```

### Docker Compose Stack
```yaml
# docker-compose.prod.yml contains:
# - agent-ai (main application)
# - postgres (database)
# - redis (caching)
# - prometheus (metrics)
# - grafana (visualization)
# - jaeger (tracing)
# - nginx (reverse proxy)
```

**Deployment via Docker Compose**:
```bash
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Documentation Files Organization

### Primary Documentation
```
docs/
├── RELEASE.md                    # Release workflow automation
├── PERFORMANCE.md                # Caching and optimization
├── ADVANCED_API.md               # Webhooks, streaming, filtering
├── DEPLOYMENT.md                 # Production deployment guide
├── DOCKER_COMPOSE_PROD.md       # Docker Compose setup
└── TUTORIALS.md                  # Learning path (7 modules)
```

### Project Level Documentation
```
├── MASTER_SUMMARY.md             # Executive summary
├── PHASE_7_COMPLETION_REPORT.md  # Detailed metrics and status
├── PROJECT_SUMMARY.md            # Project overview and recommendations
├── CASE_STUDIES.md               # 5 enterprise examples
├── DISCUSSIONS.md                # GitHub Discussions guide
└── PHASE_7_INDEX.md             # This index (start here!)
```

### Getting Started
```
├── README.md                     # Project overview
├── QUICK_START_GUIDE.md          # 5-minute setup
└── GETTING_STARTED.md            # Detailed getting started
```

---

## Common Import Patterns

### Pattern 1: Complete Feature Import
```python
# Webhook with all components
from src.webhooks import (
    EventType,
    WebhookManager,
    WebhookEvent,
    WebhookDelivery,
    EventStream
)
```

### Pattern 2: Selective Imports
```python
# Just what you need
from src.query_engine import QueryFilterBuilder
from src.caching import MemoryCache
from src.performance import profile_operation
```

### Pattern 3: Decorator-Based
```python
# Using decorators
from src.caching import CacheDecorator
from src.performance import profile_operation

@profile_operation(profiler, "operation_name")
@CacheDecorator(cache)
def my_function():
    pass
```

### Pattern 4: Manager Objects
```python
# Using manager pattern
from src.webhooks import WebhookManager
from src.performance import PerformanceProfiler
from src.query_engine import SearchEngine

webhook_manager = WebhookManager()
profiler = PerformanceProfiler()
search = SearchEngine()
```

---

## Type Hints & Dataclasses

### Webhook Types
```python
from src.webhooks import WebhookEvent, WebhookDelivery

# WebhookEvent has:
event: WebhookEvent = WebhookEvent(
    type=EventType.PLAN_COMPLETED,
    data={"plan_id": 123},
    timestamp="2025-12-02T10:30:00Z"
)

# WebhookDelivery has:
delivery: WebhookDelivery
delivery.webhook_id
delivery.delivery_id
delivery.status  # "pending", "delivered", "failed"
delivery.attempts
delivery.next_retry
```

### Query Filter Types
```python
from src.query_engine import QueryFilter

# QueryFilter attributes:
query_filter: QueryFilter
query_filter.filters      # List of filter conditions
query_filter.sort_field   # Sort by field
query_filter.sort_order   # "asc" or "desc"
query_filter.limit        # Result limit
query_filter.offset       # Result offset
```

### Performance Types
```python
from src.performance import PerformanceStatistics

# Statistics have:
stats: PerformanceStatistics
stats.duration_ms         # {"avg": 50, "min": 10, "max": 100}
stats.memory_mb           # {"avg": 25, "min": 10, "max": 50}
stats.calls               # 1000
stats.errors              # 5
stats.error_rate          # 0.005
```

---

## Dependency Graph

```
Phase 7 Modules Dependencies:

src/webhooks.py
  └── Uses: asyncio, datetime, dataclasses, uuid

src/query_engine.py
  └── Uses: re (regex), dataclasses, typing

src/caching.py
  └── Uses: time, json, os, functools, collections

src/performance.py
  └── Uses: time, psutil, statistics, functools

src/__version__.py
  └── Standalone: version string

Framework Integration:
  └── All modules integrate with: api.py, config.py
```

---

## Quick Reference Table

| Module | Purpose | Main Classes | Learn From |
|--------|---------|--------------|-----------|
| `webhooks.py` | Event-driven | `WebhookManager`, `EventType`, `EventStream` | [docs/ADVANCED_API.md](../docs/ADVANCED_API.md) |
| `query_engine.py` | Filtering & Search | `QueryFilterBuilder`, `QueryExecutor`, `SearchEngine` | [docs/ADVANCED_API.md](../docs/ADVANCED_API.md) |
| `caching.py` | Performance | `MemoryCache`, `PersistentCache`, `CacheDecorator` | [docs/PERFORMANCE.md](../docs/PERFORMANCE.md) |
| `performance.py` | Profiling | `PerformanceProfiler`, `profile_operation` | [docs/PERFORMANCE.md](../docs/PERFORMANCE.md) |
| `__version__.py` | Versioning | `__version__` | [docs/RELEASE.md](../docs/RELEASE.md) |

---

## Integration Examples

### Example 1: Complete Pipeline
```python
from src.webhooks import WebhookManager, EventType
from src.query_engine import QueryFilterBuilder, QueryExecutor
from src.caching import MemoryCache, CacheDecorator
from src.performance import PerformanceProfiler, profile_operation

# Setup
webhook_manager = WebhookManager()
cache = MemoryCache(max_size=1000)
profiler = PerformanceProfiler()

# Build operation with all features
@profile_operation(profiler, "full_pipeline")
@CacheDecorator(cache)
def process_with_features(data):
    # Build query
    query = QueryFilterBuilder().eq("status", "active").build()
    
    # Execute query
    results = QueryExecutor.apply_filter(data, query)
    
    # Trigger event
    import asyncio
    asyncio.run(webhook_manager.trigger_event(
        WebhookEvent(EventType.PLAN_COMPLETED, {"count": len(results)})
    ))
    
    return results

# Use it
results = process_with_features(data)
print(profiler.get_stats("full_pipeline"))
```

### Example 2: API Endpoint
```python
from fastapi import FastAPI
from src.webhooks import WebhookManager
from src.query_engine import QueryFilterBuilder

app = FastAPI()
webhook_manager = WebhookManager()

@app.post("/api/events")
async def register_webhook(url: str, events: list[str]):
    from src.webhooks import EventType
    
    event_types = [EventType[e] for e in events]
    webhook = webhook_manager.register_webhook(url, event_types)
    return {"webhook_id": webhook.id}

@app.get("/api/search")
async def search(status: str = None, limit: int = 10):
    query = QueryFilterBuilder().eq("status", status).paginate(limit=limit).build()
    # Execute query and return results
    return {"results": []}
```

---

## Next Steps

1. **Start Simple**: Import single modules and explore
2. **Read Documentation**: Each module has a guide in `docs/`
3. **Follow Tutorials**: [docs/TUTORIALS.md](../docs/TUTORIALS.md) has step-by-step examples
4. **Deploy**: Use Docker, Kubernetes, or Terraform from Infrastructure section
5. **Monitor**: Use Performance Profiling and Webhook events
6. **Scale**: Follow the [CASE_STUDIES.md](../CASE_STUDIES.md) patterns

---

**For more information:**
- [PHASE_7_INDEX.md](PHASE_7_INDEX.md) - Complete index
- [docs/TUTORIALS.md](docs/TUTORIALS.md) - Learning path
- [docs/ADVANCED_API.md](docs/ADVANCED_API.md) - API examples
