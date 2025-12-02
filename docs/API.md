# API Documentation

Complete reference for the AI Agent Framework REST API.

## 📋 Table of Contents

- [Authentication](#authentication)
- [Base URL](#base-url)
- [Endpoints](#endpoints)
- [Error Handling](#error-handling)
- [Examples](#examples)

---

## Authentication

### Methods

The API supports multiple authentication methods:

#### 1. API Key (Header)
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/plans
```

#### 2. JWT Bearer Token
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:8000/api/plans
```

#### 3. JWT Cookie (for web clients)
- Token is automatically sent as `httponly` cookie
- No need to add headers

### Get JWT Token

**Endpoint:** `POST /auth/login`

**Request:**
```json
{
  "username": "user",
  "password": "password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

## Base URL

```
http://localhost:8000
```

For production, update to your domain:
```
https://agent-api.yourdomain.com
```

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.2.0",
  "timestamp": "2025-12-02T19:50:00Z"
}
```

---

### 2. Plans

#### Create Plan

**POST** `/api/v1/plans`

Create a new plan for a goal.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json
```

**Request:**
```json
{
  "goal": "Create a REST API for user management",
  "repository_path": "/path/to/repo",
  "max_tasks": 10
}
```

**Response:**
```json
{
  "id": "plan_12345",
  "goal": "Create a REST API for user management",
  "status": "planning",
  "tasks": [],
  "created_at": "2025-12-02T19:50:00Z",
  "updated_at": "2025-12-02T19:50:00Z"
}
```

**Status Codes:**
- `201 Created` — Plan created successfully
- `400 Bad Request` — Invalid request
- `401 Unauthorized` — Missing or invalid token

---

#### List Plans

**GET** `/api/v1/plans`

List all plans.

**Query Parameters:**
- `status` (optional): `planning`, `executing`, `completed`, `failed`
- `skip` (optional): Number of plans to skip (default: 0)
- `limit` (optional): Max plans to return (default: 10)

**Response:**
```json
{
  "plans": [
    {
      "id": "plan_12345",
      "goal": "Create a REST API for user management",
      "status": "planning",
      "task_count": 5,
      "created_at": "2025-12-02T19:50:00Z"
    }
  ],
  "total": 1
}
```

---

#### Get Plan Details

**GET** `/api/v1/plans/{plan_id}`

Get detailed information about a specific plan.

**Response:**
```json
{
  "id": "plan_12345",
  "goal": "Create a REST API for user management",
  "status": "executing",
  "tasks": [
    {
      "id": "task_1",
      "description": "Create User model",
      "status": "completed",
      "result": "Model created in models/user.py"
    }
  ],
  "created_at": "2025-12-02T19:50:00Z",
  "updated_at": "2025-12-02T19:55:00Z"
}
```

---

#### Execute Plan

**POST** `/api/v1/plans/{plan_id}/execute`

Start executing a plan.

**Request:**
```json
{
  "sequential": true
}
```

**Response:**
```json
{
  "plan_id": "plan_12345",
  "status": "executing",
  "current_task": "task_1",
  "message": "Execution started"
}
```

---

#### Cancel Plan

**POST** `/api/v1/plans/{plan_id}/cancel`

Cancel a running plan.

**Response:**
```json
{
  "plan_id": "plan_12345",
  "status": "cancelled",
  "message": "Plan cancelled successfully"
}
```

---

### 3. Tasks

#### Get Task

**GET** `/api/v1/tasks/{task_id}`

Get details of a specific task.

**Response:**
```json
{
  "id": "task_1",
  "plan_id": "plan_12345",
  "description": "Create User model",
  "status": "completed",
  "result": "Model created successfully",
  "error": null,
  "created_at": "2025-12-02T19:50:00Z",
  "completed_at": "2025-12-02T19:51:00Z"
}
```

---

#### Update Task

**PUT** `/api/v1/tasks/{task_id}`

Manually update a task status.

**Request:**
```json
{
  "status": "completed",
  "result": "Task completed successfully"
}
```

**Response:**
```json
{
  "id": "task_1",
  "status": "completed",
  "result": "Task completed successfully",
  "updated_at": "2025-12-02T19:52:00Z"
}
```

---

### 4. Repository

#### Scan Repository

**POST** `/api/v1/repository/scan`

Scan repository structure and code files.

**Request:**
```json
{
  "path": "/path/to/repo",
  "extensions": [".py", ".js", ".ts"]
}
```

**Response:**
```json
{
  "repository": {
    "path": "/path/to/repo",
    "files_count": 42,
    "directories_count": 8,
    "size_mb": 5.2
  },
  "files": [
    {
      "path": "src/main.py",
      "size": 2048,
      "language": "python"
    }
  ]
}
```

---

#### Get Code File

**GET** `/api/v1/repository/files?path=src/main.py`

Get content of a specific code file.

**Response:**
```json
{
  "path": "src/main.py",
  "content": "import os\n\ndef main():\n    pass",
  "size": 2048,
  "language": "python"
}
```

---

### 5. Analytics

#### Get Performance Metrics

**GET** `/api/v1/analytics/metrics`

Get performance and usage metrics.

**Response:**
```json
{
  "total_plans": 42,
  "total_tasks": 257,
  "completed_plans": 38,
  "success_rate": 90.5,
  "average_execution_time_seconds": 125,
  "total_execution_time_seconds": 5250
}
```

---

#### Get Task Trends

**GET** `/api/v1/analytics/trends?days=7`

Get usage trends over time.

**Query Parameters:**
- `days` (optional): Number of days to analyze (default: 7)

**Response:**
```json
{
  "trend": [
    {
      "date": "2025-11-26",
      "plans_created": 5,
      "tasks_completed": 28,
      "success_rate": 88.5
    },
    {
      "date": "2025-11-27",
      "plans_created": 7,
      "tasks_completed": 35,
      "success_rate": 91.2
    }
  ]
}
```

---

### 6. WebSocket (Real-time Updates)

**WS** `/ws/plans/{plan_id}`

Connect to WebSocket for real-time plan execution updates.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/plans/plan_12345');

ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log('Status:', update.status);
  console.log('Current task:', update.current_task);
};
```

**Message Format:**
```json
{
  "type": "task_update",
  "plan_id": "plan_12345",
  "task_id": "task_1",
  "status": "completed",
  "message": "Task completed successfully",
  "timestamp": "2025-12-02T19:51:00Z"
}
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message",
  "error_code": "INVALID_REQUEST",
  "timestamp": "2025-12-02T19:50:00Z"
}
```

### Common Status Codes

| Code | Meaning |
|------|---------|
| `200` | OK - Request succeeded |
| `201` | Created - Resource created |
| `400` | Bad Request - Invalid request format |
| `401` | Unauthorized - Authentication failed |
| `403` | Forbidden - Permission denied |
| `404` | Not Found - Resource not found |
| `409` | Conflict - Resource already exists |
| `429` | Too Many Requests - Rate limit exceeded |
| `500` | Internal Server Error - Server error |

### Example Error Response

```json
{
  "detail": "Plan not found",
  "error_code": "NOT_FOUND",
  "timestamp": "2025-12-02T19:50:00Z"
}
```

---

## Examples

### Example 1: Create and Execute a Plan

```bash
# 1. Authenticate
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"password"}' \
  | jq -r '.access_token')

# 2. Create a plan
PLAN=$(curl -X POST http://localhost:8000/api/v1/plans \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Add user authentication to the API",
    "repository_path": "/path/to/repo",
    "max_tasks": 10
  }' | jq -r '.id')

# 3. Get plan details
curl http://localhost:8000/api/v1/plans/$PLAN \
  -H "Authorization: Bearer $TOKEN"

# 4. Execute the plan
curl -X POST http://localhost:8000/api/v1/plans/$PLAN/execute \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"sequential": true}'

# 5. Monitor progress with WebSocket
wscat -c ws://localhost:8000/ws/plans/$PLAN
```

### Example 2: Using Python Client

```python
import requests
import json

BASE_URL = "http://localhost:8000"
TOKEN = "your_jwt_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Create a plan
response = requests.post(
    f"{BASE_URL}/api/v1/plans",
    json={
        "goal": "Fix all linting errors",
        "repository_path": "/path/to/repo"
    },
    headers=headers
)
plan = response.json()
print(f"Plan created: {plan['id']}")

# Get plan status
response = requests.get(
    f"{BASE_URL}/api/v1/plans/{plan['id']}",
    headers=headers
)
print(f"Status: {response.json()['status']}")
```

### Example 3: JavaScript/Node.js

```javascript
const fetch = require('node-fetch');

const BASE_URL = 'http://localhost:8000';
const token = 'your_jwt_token';

async function createPlan(goal, repoPath) {
  const response = await fetch(`${BASE_URL}/api/v1/plans`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      goal,
      repository_path: repoPath,
      max_tasks: 10
    })
  });
  
  return response.json();
}

async function main() {
  const plan = await createPlan(
    'Add error handling',
    '/path/to/repo'
  );
  console.log('Plan:', plan);
}

main();
```

---

## Rate Limiting

The API implements rate limiting:

- **Without authentication**: 100 requests/hour per IP
- **With authentication**: 1000 requests/hour per user

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640962800
```

---

## Versioning

The API uses URL-based versioning:

- Current version: `v1`
- URL pattern: `/api/v1/...`

Future versions will be available as `/api/v2/...`, etc.

---

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/mohamednoorulnaseem/agent_ai-)
- Check the [main documentation](../README.md)
- See [Contributing guide](./CONTRIBUTING.md)
