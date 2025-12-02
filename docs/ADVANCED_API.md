# Advanced API Features

This guide covers advanced API features including webhooks, real-time streaming, and advanced filtering.

## Overview

The AI Agent Framework includes advanced API capabilities:
- **Webhooks**: Event-driven architecture with automatic delivery and retries
- **Event Streaming**: Real-time updates via Server-Sent Events
- **Advanced Filtering**: Complex queries with multiple conditions
- **Full-Text Search**: Search across multiple fields
- **Pagination & Sorting**: Efficient data retrieval

## Webhooks

### Quick Start

Register a webhook to receive events:

```bash
curl -X POST http://localhost:8000/webhooks \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "event_types": ["plan.completed", "task.failed"],
    "secret": "your-secret-key"
  }'
```

### Event Types

Available events:
- `plan.created` - Plan created
- `plan.started` - Plan execution started
- `plan.completed` - Plan completed successfully
- `plan.failed` - Plan failed
- `task.started` - Task started
- `task.completed` - Task completed
- `task.failed` - Task failed
- `conversation.message` - Conversation message

### Webhook Payload

Each webhook receives:

```json
{
  "id": "event-uuid",
  "type": "plan.completed",
  "timestamp": "2025-12-02T10:30:00Z",
  "data": {
    "plan_id": 123,
    "goal": "Create REST API",
    "status": "completed",
    "tasks_completed": 5
  },
  "metadata": {
    "request_id": "req-uuid",
    "source": "api"
  }
}
```

### Headers

Webhook requests include verification headers:

```
X-Webhook-ID: webhook-uuid
X-Event-ID: event-uuid
X-Event-Type: plan.completed
X-Secret: your-secret-key
```

### Delivery Guarantees

- **Automatic Retries**: Up to 3 attempts with exponential backoff
- **Timeout**: 30 seconds per request
- **Verification**: Validate X-Secret header
- **Idempotency**: Event IDs allow duplicate detection

### Python Example

```python
from src.webhooks import WebhookManager, EventType, WebhookEvent

# Initialize manager
webhook_manager = WebhookManager()

# Register webhook
webhook = webhook_manager.register_webhook(
    url="https://your-server.com/webhook",
    event_types=[EventType.PLAN_COMPLETED, EventType.TASK_FAILED],
    secret="your-secret"
)

# Trigger event
event = WebhookEvent(
    type=EventType.PLAN_COMPLETED,
    data={"plan_id": 123, "status": "completed"}
)

await webhook_manager.trigger_event(event)

# Check delivery status
status = webhook_manager.get_delivery_status(webhook.id)
print(status)
```

## Event Streaming (Real-time Updates)

### Server-Sent Events (SSE)

Connect to real-time event stream:

```bash
curl -N http://localhost:8000/events/stream
```

### JavaScript Example

```javascript
const eventSource = new EventSource('/events/stream');

eventSource.addEventListener('plan.completed', (event) => {
    const data = JSON.parse(event.data);
    console.log('Plan completed:', data);
});

eventSource.addEventListener('task.failed', (event) => {
    const data = JSON.parse(event.data);
    console.log('Task failed:', data);
});

eventSource.onerror = (error) => {
    console.error('Stream error:', error);
};
```

### Python Example

```python
from src.webhooks import EventStream, WebhookEvent, EventType

# Create stream
stream = EventStream()

# Subscribe to events
async def on_event(event: WebhookEvent):
    print(f"Event: {event.type} - {event.data}")

stream.subscribe(on_event)

# Emit event
event = WebhookEvent(
    type=EventType.PLAN_COMPLETED,
    data={"plan_id": 123}
)
await stream.emit_event(event)
```

## Advanced Filtering

### Filter Builder

Build complex queries:

```python
from src.query_engine import QueryFilterBuilder, QueryExecutor

# Create filter
filter_builder = QueryFilterBuilder()
query_filter = (
    filter_builder
    .eq("status", "completed")
    .gt("created_at", "2025-12-01")
    .contains("goal", "API")
    .and_operator()
    .sort("created_at", "desc")
    .paginate(limit=10, offset=0)
    .build()
)

# Execute filter
results = QueryExecutor.apply_filter(data, query_filter)
```

### Filter Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `eq` | `eq("status", "active")` | Equals |
| `ne` | `ne("status", "deleted")` | Not equals |
| `gt` | `gt("score", 100)` | Greater than |
| `gte` | `gte("score", 100)` | Greater than or equal |
| `lt` | `lt("score", 100)` | Less than |
| `lte` | `lte("score", 100)` | Less than or equal |
| `contains` | `contains("text", "api")` | Contains string |
| `in` | `in_list("status", ["active", "pending"])` | In list |
| `regex` | `regex("email", ".*@example.com")` | Regex match |

### API Query Syntax

Query string format:

```
/api/plans?filter[status]=active&filter[goal]~=API&sort=-created_at&limit=10&offset=0
```

### Complex Filtering Example

```bash
# Find completed plans created after Dec 1 with "API" in goal
curl "http://localhost:8000/plans?filter[status]=completed&filter[created_at]>=2025-12-01&filter[goal]~=API&sort=-created_at&limit=20"
```

## Full-Text Search

### Search Example

```python
from src.query_engine import SearchEngine

# Create search engine
search = SearchEngine(
    searchable_fields=["goal", "description", "status"]
)

# Search data
results = search.search(
    data=plans,
    query="REST API",
    fields=["goal", "description"]
)

# Faceted search
facets = search.faceted_search(
    data=plans,
    query="REST API",
    facet_field="status"
)
# Returns: {
#   "active": [...],
#   "completed": [...],
#   "failed": [...]
# }
```

### API Endpoint

```bash
# Search plans
curl "http://localhost:8000/plans/search?q=REST%20API"

# Search with facets
curl "http://localhost:8000/plans/search?q=REST%20API&facet=status"
```

## Combining Features

### Webhook with Filtering

```python
# Register webhook for specific events
webhook = webhook_manager.register_webhook(
    url="https://your-server.com/webhook",
    event_types=[EventType.PLAN_COMPLETED],
    secret="secret"
)

# Only trigger for completed plans
filter_builder = QueryFilterBuilder()
query_filter = (
    filter_builder
    .eq("status", "completed")
    .gte("score", 80)
    .build()
)

# Emit filtered events
if QueryExecutor.apply_filter([plan], query_filter):
    await webhook_manager.trigger_event(event)
```

### Search + Stream

```python
# Create filtered stream
stream = EventStream()
search = SearchEngine()

# Subscribe with filtering
async def on_event_filtered(event):
    # Filter events by search
    if "API" in event.data.get("goal", ""):
        print(f"Relevant event: {event}")

stream.subscribe(on_event_filtered)
```

## Error Handling

### Webhook Failures

```python
# Check delivery status
status = webhook_manager.get_delivery_status(webhook_id)

if status['failed'] > 0:
    print(f"Failed deliveries: {status['failed']}")
    
# Retry failed deliveries
for delivery in webhook_manager.deliveries:
    if delivery.status_code >= 500:
        await webhook_manager._deliver_webhook(
            webhook_manager.webhooks[delivery.webhook_id],
            event,
            delivery
        )
```

### Filter Errors

```python
try:
    results = QueryExecutor.apply_filter(data, query_filter)
except ValueError as e:
    print(f"Invalid filter: {e}")
```

## Performance Considerations

### Webhook Optimization

- Batch similar events
- Use appropriate TTLs
- Monitor delivery times
- Implement exponential backoff

### Filtering Optimization

- Index frequently filtered fields
- Use pagination for large datasets
- Cache filter results
- Optimize regex patterns

### Streaming Optimization

- Use connection pooling
- Implement backpressure
- Limit event history
- Clean up stale streams

## Rate Limiting

Webhook deliveries are rate-limited:

```python
# Per webhook: 100 requests/minute
# Per event type: 1000 requests/minute
# Total: 10000 requests/minute
```

Configure in `agent.config.yaml`:

```yaml
webhooks:
  rate_limit:
    per_webhook: 100
    per_minute: 10000
  retry_policy:
    max_attempts: 3
    backoff_multiplier: 2
    initial_delay_seconds: 60
```

## Monitoring

### Webhook Health

```python
# Get overall webhook health
health = {
    "total_webhooks": len(webhook_manager.list_webhooks()),
    "active_webhooks": len(webhook_manager.list_webhooks(active_only=True)),
    "total_deliveries": len(webhook_manager.deliveries),
    "successful_rate": successful / total
}
```

### Filter Performance

```python
from src.performance import PerformanceProfiler

profiler = PerformanceProfiler()

@profile_operation(profiler, "filter_execution")
def apply_filters(data, filters):
    return QueryExecutor.apply_filter(data, filters)

# Monitor
stats = profiler.get_stats("filter_execution")
print(f"Avg filter time: {stats['duration_ms']['avg']:.2f}ms")
```

---

For questions, see [API Reference](API.md) or [Supporting Documentation](../README.md).
