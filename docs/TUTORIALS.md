# Agent AI Framework Tutorials

Complete step-by-step tutorials for using the Agent AI Framework in various scenarios.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Building Your First Agent](#building-your-first-agent)
3. [Advanced Planning Strategies](#advanced-planning-strategies)
4. [Integration with External APIs](#integration-with-external-apis)
5. [Webhook Implementation](#webhook-implementation)
6. [Performance Optimization](#performance-optimization)
7. [Deployment to Production](#deployment-to-production)

## Getting Started

### Installation

```bash
# Clone repository
git clone https://github.com/mohamednoorulnaseem/agent_ai.git
cd agent_ai

# Install in development mode
pip install -e .

# Or install from PyPI (once released)
pip install agent-ai
```

### Quick Test

```bash
python quick_test.py
```

Expected output:
```
Starting Agent AI Framework test...
✓ LLM connection successful
✓ Agent initialization successful
✓ Plan creation successful
✓ Task execution successful
✓ All tests passed!
```

## Building Your First Agent

### Step 1: Initialize the Agent

```python
from src.agent.executor import PlanExecutor
from src.llm.openai_like import OpenAILikeLLM

# Initialize LLM
llm = OpenAILikeLLM(
    api_key="sk-your-api-key",
    model="gpt-4",
    base_url="https://api.openai.com/v1"
)

# Initialize agent
agent = PlanExecutor(llm=llm)
```

### Step 2: Create a Simple Plan

```python
from src.agent.planner import Planner

planner = Planner(llm=llm)

# Create a goal
goal = "Write a comprehensive README for my GitHub project"

# Generate plan
plan = planner.create_plan(goal)

print(f"Plan: {plan.goal}")
print(f"Tasks: {len(plan.tasks)}")
for task in plan.tasks:
    print(f"  - {task.description}")
```

### Step 3: Execute Tasks

```python
# Execute the plan
results = agent.execute(plan)

for task_id, result in results.items():
    print(f"Task {task_id}: {result['status']}")
    if result['output']:
        print(f"Output: {result['output']}")
```

### Complete Example

```python
#!/usr/bin/env python3
from src.agent.executor import PlanExecutor
from src.agent.planner import Planner
from src.llm.openai_like import OpenAILikeLLM

def main():
    # Initialize LLM
    llm = OpenAILikeLLM(
        api_key="sk-your-api-key",
        model="gpt-4"
    )
    
    # Create planner and executor
    planner = Planner(llm=llm)
    executor = PlanExecutor(llm=llm)
    
    # Define goal
    goal = "Create a Python web scraper for extracting product prices"
    
    # Create plan
    plan = planner.create_plan(goal)
    
    print(f"Goal: {plan.goal}")
    print(f"Number of tasks: {len(plan.tasks)}")
    print("\nTasks:")
    for i, task in enumerate(plan.tasks, 1):
        print(f"{i}. {task.description}")
    
    # Execute plan
    print("\nExecuting plan...")
    results = executor.execute(plan)
    
    # Display results
    for task_id, result in results.items():
        print(f"\nTask {task_id}:")
        print(f"  Status: {result['status']}")
        print(f"  Output: {result['output'][:100]}...")

if __name__ == "__main__":
    main()
```

## Advanced Planning Strategies

### Multi-Step Planning

```python
# Define a complex goal
goal = """
Analyze sales data, create visualizations, 
and generate a comprehensive report
"""

plan = planner.create_plan(goal)

# The agent will break this into logical steps:
# 1. Load and validate data
# 2. Perform analysis
# 3. Create visualizations
# 4. Generate report
```

### Conditional Task Execution

```python
# Tasks can depend on previous results
plan = planner.create_plan(goal)

# Executor respects dependencies
executor = PlanExecutor(
    llm=llm,
    max_retries=3,
    timeout=300  # 5 minutes
)

results = executor.execute(plan)

# Check for task failures
failed_tasks = [
    task_id for task_id, result in results.items()
    if result['status'] == 'failed'
]

if failed_tasks:
    print(f"Failed tasks: {failed_tasks}")
    # Implement retry or fallback logic
```

### Iterative Refinement

```python
# Start with initial plan
initial_goal = "Improve website performance"
plan_v1 = planner.create_plan(initial_goal)

# Execute and collect feedback
results_v1 = executor.execute(plan_v1)

# Refine based on results
refined_goal = f"""
Improve website performance focusing on:
- Database query optimization
- Caching strategy
- CDN implementation
Based on initial findings
"""

plan_v2 = planner.create_plan(refined_goal)
results_v2 = executor.execute(plan_v2)
```

## Integration with External APIs

### REST API Integration

```python
import httpx
from src.agent.executor import PlanExecutor

# Use custom executor with API capabilities
class APIExecutor(PlanExecutor):
    async def execute_api_task(self, task):
        """Execute tasks that call external APIs"""
        
        url = task.data.get('url')
        method = task.data.get('method', 'GET')
        
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url)
            return response.json()

# Example goal
goal = """
Fetch weather data from API,
analyze trends, and create summary
"""

plan = planner.create_plan(goal)
executor = APIExecutor(llm=llm)
results = executor.execute(plan)
```

### Database Integration

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Create database engine
engine = create_engine('postgresql://user:password@localhost/db')

# Custom executor with database access
class DBExecutor(PlanExecutor):
    def __init__(self, llm, db_engine):
        super().__init__(llm)
        self.db_engine = db_engine
    
    def execute_db_task(self, task):
        """Execute database queries"""
        
        with Session(self.db_engine) as session:
            # Execute task with database context
            query = task.data.get('query')
            results = session.execute(query)
            return results.fetchall()

# Use in planning
goal = """
Query customer database,
analyze purchase patterns,
identify high-value customers
"""

executor = DBExecutor(llm=llm, db_engine=engine)
results = executor.execute(planner.create_plan(goal))
```

### File Processing

```python
import os
from pathlib import Path

def process_files_task():
    """Process files with agent assistance"""
    
    # Define goal
    goal = """
    Process all PDF files in data/input:
    1. Extract text content
    2. Identify key information
    3. Generate summaries
    4. Save to data/output
    """
    
    # Create plan
    plan = planner.create_plan(goal)
    
    # Execute with file context
    input_dir = Path("data/input")
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = executor.execute(plan)
    
    return results

# Run file processing
results = process_files_task()
```

## Webhook Implementation

### Setup Webhooks

```python
from src.webhooks import WebhookManager, EventType, WebhookEvent

# Initialize webhook manager
webhook_manager = WebhookManager()

# Register webhook
webhook = webhook_manager.register_webhook(
    url="https://your-server.com/webhook",
    event_types=[
        EventType.PLAN_COMPLETED,
        EventType.TASK_FAILED
    ],
    secret="your-webhook-secret"
)

print(f"Webhook registered: {webhook.id}")
```

### Receive Webhook Events

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def receive_webhook():
    """Receive webhook events from Agent AI"""
    
    # Verify secret
    secret = "your-webhook-secret"
    signature = request.headers.get('X-Secret')
    
    if not signature:
        return {"error": "Missing signature"}, 401
    
    # Process event
    event_data = request.json
    event_type = event_data['type']
    
    print(f"Received event: {event_type}")
    print(f"Event data: {event_data['data']}")
    
    # Handle different event types
    if event_type == 'plan.completed':
        handle_plan_completed(event_data['data'])
    elif event_type == 'task.failed':
        handle_task_failed(event_data['data'])
    
    return {"status": "received"}, 200

def handle_plan_completed(data):
    """Handle plan completion event"""
    print(f"Plan {data['plan_id']} completed!")
    # Send notification, update database, etc.

def handle_task_failed(data):
    """Handle task failure event"""
    print(f"Task {data['task_id']} failed!")
    # Alert, retry, or escalate

if __name__ == '__main__':
    app.run(port=5000)
```

### Event Streaming

```python
from src.webhooks import EventStream, WebhookEvent, EventType

# Create event stream
stream = EventStream()

# Subscribe to events
async def on_plan_created(event: WebhookEvent):
    print(f"New plan created: {event.data}")

async def on_task_completed(event: WebhookEvent):
    print(f"Task completed: {event.data}")

stream.subscribe(on_plan_created)
stream.subscribe(on_task_completed)

# In your main agent code
plan = planner.create_plan(goal)

event = WebhookEvent(
    type=EventType.PLAN_CREATED,
    data={"plan_id": plan.id, "goal": plan.goal}
)

await stream.emit_event(event)
```

## Performance Optimization

### Enable Caching

```python
from src.caching import MemoryCache, CacheDecorator

# Initialize cache
cache = MemoryCache(
    max_size=1000,
    ttl=3600  # 1 hour
)

# Decorator for caching function results
@CacheDecorator(cache)
def expensive_computation(input_data):
    # This result will be cached
    return perform_analysis(input_data)

# First call: executes function
result1 = expensive_computation(data)

# Second call: returns from cache
result2 = expensive_computation(data)
```

### Profile Performance

```python
from src.performance import PerformanceProfiler, profile_operation

profiler = PerformanceProfiler()

@profile_operation(profiler, "plan_creation")
def create_plan_tracked(goal):
    return planner.create_plan(goal)

# Execute with profiling
plan = create_plan_tracked(goal)

# Get statistics
stats = profiler.get_stats("plan_creation")
print(f"Average time: {stats['duration_ms']['avg']}ms")
print(f"Total calls: {stats['calls']}")
print(f"Memory used: {stats['memory_mb']['avg']}MB")
```

### Optimize Queries

```python
from src.query_engine import QueryFilterBuilder, QueryExecutor, SearchEngine

# Build complex query
filter_builder = QueryFilterBuilder()
query_filter = (
    filter_builder
    .eq("status", "completed")
    .gte("created_at", "2025-12-01")
    .contains("goal", "analysis")
    .sort("created_at", "desc")
    .paginate(limit=10, offset=0)
    .build()
)

# Execute efficiently
results = QueryExecutor.apply_filter(all_plans, query_filter)

# Full-text search
search = SearchEngine(
    searchable_fields=["goal", "description"]
)

search_results = search.search(
    data=all_plans,
    query="performance optimization"
)

print(f"Found {len(search_results)} matching plans")
```

## Deployment to Production

### Docker Deployment

```bash
# Build image
docker build -t agent-ai:latest .

# Run container
docker run -d \
  --name agent-ai \
  -e LLM_API_KEY="sk-your-key" \
  -e REDIS_HOST="redis" \
  -p 8000:8000 \
  agent-ai:latest
```

### Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace agent-ai

# Apply configuration
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/deployment.yaml

# Verify deployment
kubectl get pods -n agent-ai
```

### Health Checks and Monitoring

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness probe"""
    # Check dependencies
    if check_llm_connection() and check_db_connection():
        return jsonify({"status": "ready"}), 200
    return jsonify({"status": "not ready"}), 503

def check_llm_connection():
    """Verify LLM is accessible"""
    try:
        llm.test_connection()
        return True
    except:
        return False

def check_db_connection():
    """Verify database is accessible"""
    try:
        # Test database query
        return True
    except:
        return False
```

### Scaling

```bash
# Scale Kubernetes deployment
kubectl scale deployment agent-ai --replicas=5 -n agent-ai

# Monitor scaling
kubectl get hpa -n agent-ai
kubectl describe hpa agent-ai-hpa -n agent-ai
```

---

## Next Steps

1. **Explore Examples**: Check the `examples.py` file for more use cases
2. **Join Community**: Participate in [GitHub Discussions](https://github.com/mohamednoorulnaseem/agent_ai/discussions)
3. **Read Documentation**: See [Advanced API Features](ADVANCED_API.md)
4. **Deploy**: Follow [Deployment Guide](DEPLOYMENT.md)

## Common Issues

### Issue: Agent not responding

**Solution**: Check LLM connection and API key
```bash
python quick_test.py
```

### Issue: Tasks timeout

**Solution**: Increase timeout in executor
```python
executor = PlanExecutor(llm=llm, timeout=600)  # 10 minutes
```

### Issue: Memory issues

**Solution**: Enable caching and pagination
```python
# Use cache for frequent queries
# Use pagination for large datasets
results = QueryExecutor.apply_filter(data, query_filter)
```

For more help, see [troubleshooting](../README.md#troubleshooting) or open an issue on [GitHub](https://github.com/mohamednoorulnaseem/agent_ai/issues).
