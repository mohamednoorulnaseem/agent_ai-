# AI Agent API Documentation

## Overview

The AI Agent REST API provides HTTP endpoints for planning, execution, and management of AI-driven development tasks.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. This should be added for production use.

## Endpoints

### Health Check

#### `GET /health`

Check API health and configuration.

**Response:**

```json
{
  "status": "healthy",
  "llm_provider": "mock",
  "version": "0.1.0"
}
```

### Plans

#### `POST /plans`

Create a new plan from a goal.

**Request:**

```json
{
  "goal": "Build a REST API for user management",
  "repo_path": "."
}
```

**Response:**

```json
{
  "plan_id": 1,
  "goal": "Build a REST API for user management",
  "tasks": 5,
  "status": "created"
}
```

**Status Codes:**

- `200`: Plan created successfully
- `400`: Invalid request

---

#### `GET /plans`

List all plans.

**Query Parameters:**

- `limit` (int, optional): Maximum number of plans to return (default: 50)

**Response:**

```json
{
  "plans": [
    {
      "id": 1,
      "goal": "Build a REST API",
      "created_at": "2025-12-02 10:30:00",
      "status": "active"
    }
  ],
  "total": 1
}
```

---

#### `GET /plans/{plan_id}`

Get details of a specific plan.

**Response:**

```json
{
  "plan": {
    "id": 1,
    "goal": "Build a REST API",
    "created_at": "2025-12-02 10:30:00",
    "status": "active"
  },
  "tasks": [
    {
      "id": 1,
      "plan_id": 1,
      "task_id": 1,
      "description": "Create project structure",
      "priority": 0,
      "created_at": "2025-12-02 10:30:00"
    }
  ],
  "statistics": {
    "plan": {...},
    "total_tasks": 5,
    "completed_tasks": 0,
    "total_executions": 0
  }
}
```

---

#### `GET /plans/{plan_id}/tasks`

Get tasks for a plan.

**Response:**

```json
{
  "plan_id": 1,
  "tasks": [
    {
      "id": 1,
      "plan_id": 1,
      "task_id": 1,
      "description": "Create project structure",
      "priority": 0,
      "completed": false,
      "result": null,
      "created_at": "2025-12-02 10:30:00"
    }
  ]
}
```

---

### Execution

#### `POST /plans/{plan_id}/execute`

Execute a task within a plan.

**Request:**

```json
{
  "plan_id": 1,
  "task_id": 1
}
```

**Response:**

```json
{
  "success": true,
  "result": "Task queued for execution",
  "execution_id": 1
}
```

**Status Codes:**

- `200`: Task queued successfully
- `404`: Plan or task not found
- `400`: Invalid request

---

### Conversation

#### `GET /conversation`

Get conversation history.

**Query Parameters:**

- `limit` (int, optional): Maximum messages to return (default: 100)

**Response:**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Create a REST API",
      "created_at": "2025-12-02 10:30:00"
    },
    {
      "role": "assistant",
      "content": "I'll help you create a REST API...",
      "created_at": "2025-12-02 10:30:05"
    }
  ],
  "total": 2
}
```

---

#### `POST /conversation`

Add a message to conversation history.

**Request:**

```json
{
  "role": "user",
  "content": "What's the next step?"
}
```

**Response:**

```json
{
  "status": "saved"
}
```

---

### Repository

#### `POST /scan`

Scan a repository.

**Query Parameters:**

- `repo_path` (str, optional): Repository path (default: ".")

**Response:**

```json
{
  "repository": ".",
  "info": "Repository: .\nTotal Files: 32\n..."
}
```

---

### Statistics

#### `GET /stats`

Get overall system statistics.

**Response:**

```json
{
  "total_plans": 10,
  "completed_plans": 3,
  "active_sessions": 2,
  "total_messages": 45,
  "llm_provider": "mock"
}
```

---

## Error Handling

All errors return a JSON response with details:

```json
{
  "detail": "Plan not found"
}
```

**Common Status Codes:**

- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

---

## Example Usage

### Python

```python
import requests

# Create a plan
response = requests.post(
    "http://localhost:8000/plans",
    json={
        "goal": "Build a web scraper",
        "repo_path": "."
    }
)
plan = response.json()
plan_id = plan["plan_id"]

# Get plan details
response = requests.get(f"http://localhost:8000/plans/{plan_id}")
details = response.json()

# Execute a task
response = requests.post(
    f"http://localhost:8000/plans/{plan_id}/execute",
    json={
        "plan_id": plan_id,
        "task_id": 1
    }
)

# Get conversation history
response = requests.get("http://localhost:8000/conversation")
messages = response.json()
```

### cURL

```bash
# Create a plan
curl -X POST "http://localhost:8000/plans" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a web scraper",
    "repo_path": "."
  }'

# Get statistics
curl -X GET "http://localhost:8000/stats"

# Get conversation history
curl -X GET "http://localhost:8000/conversation?limit=50"
```

### JavaScript

```javascript
// Create a plan
const response = await fetch("http://localhost:8000/plans", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    goal: "Build a web scraper",
    repo_path: ".",
  }),
});

const plan = await response.json();
console.log("Plan created:", plan);

// Get statistics
const statsResponse = await fetch("http://localhost:8000/stats");
const stats = await statsResponse.json();
console.log("Statistics:", stats);
```

---

## Running the API Server

### Installation

```bash
pip install -r requirements.txt
```

### Start Server

```bash
python -m uvicorn agent_ai.api:app --reload
```

Or with a different host/port:

```bash
python -m uvicorn agent_ai.api:app --host 0.0.0.0 --port 8000
```

### Access Swagger UI

Navigate to:

```
http://localhost:8000/docs
```

---

## Rate Limiting

Currently not implemented. Recommended for production.

---

## Versioning

API version: `0.1.0`

Current stability: **Alpha**

---

## Future Enhancements

- [ ] Authentication (JWT tokens)
- [ ] Rate limiting
- [ ] WebSocket support for real-time updates
- [ ] Batch operations
- [ ] File upload/download endpoints
- [ ] Advanced filtering and search
- [ ] Webhook support for task completion
