# Phase 3 API Integration Demo

Complete demonstration of the integrated AI Agent framework with advanced Phase 3 features.

## 🚀 Quick Start API Server

```bash
# Start the FastAPI server
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

---

## 📋 API Endpoints (24 Total)

### Health & Info

- `GET /health` - Health check
- `GET /` - API documentation (Swagger UI)
- `GET /redoc` - Alternative documentation (ReDoc)

### Authentication (Phase 3)

- `POST /auth/login` - Get JWT token
- `POST /auth/token` - Generate API key
- `GET /auth/validate` - Validate JWT token

### Planning & Execution

- `POST /plans` - Create a new plan
- `GET /plans` - List all plans
- `GET /plans/{plan_id}` - Get plan details
- `GET /plans/{plan_id}/tasks` - Get plan tasks
- `POST /plans/{plan_id}/execute` - Execute task

### Templates (Phase 3)

- `GET /templates` - List all templates
- `GET /templates/{template_id}` - Get template details
- `GET /templates/search/{query}` - Search templates

### Analytics (Phase 3)

- `GET /analytics` - Get overall analytics
- `GET /analytics/tasks/{task_id}` - Get task-specific analytics
- `GET /analytics/performance` - Get detailed performance metrics

### WebSocket (Phase 3)

- `WS /ws/{client_id}` - Real-time task updates

### Conversation & Scanning

- `GET /conversation` - Get conversation history
- `POST /conversation` - Add message to conversation
- `POST /scan` - Scan repository

### Statistics

- `GET /stats` - Get overall statistics

---

## 🔑 Authentication Examples

### 1. Get JWT Token (Demo Credentials)

**Request:**

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "password": "demo123"
  }'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "user_demo",
  "username": "demo"
}
```

Demo Credentials:

- Username: `demo` | Password: `demo123` (User role)
- Username: `admin` | Password: `admin123` (Admin role)

### 2. Validate Token

**Request:**

```bash
curl -X GET "http://localhost:8000/auth/validate" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

**Response:**

```json
{
  "valid": true,
  "user_id": "user_demo",
  "username": "demo",
  "roles": ["user"]
}
```

### 3. Generate API Key

**Request:**

```bash
curl -X POST "http://localhost:8000/auth/token" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

**Response:**

```json
{
  "api_key": "sk_1764673861_a1b2c3d4e5f6...",
  "created_at": "2025-12-02 10:31:01",
  "expires_at": null
}
```

---

## 📋 Templates API (Phase 3)

### 1. List Available Templates

**Request:**

```bash
curl -X GET "http://localhost:8000/templates" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

**Response:**

```json
[
  {
    "id": "rest_api",
    "name": "REST API Development",
    "description": "Build a production REST API with proper structure and best practices",
    "difficulty": "medium",
    "tags": ["api", "backend", "rest"],
    "task_count": 10
  },
  {
    "id": "web_scraper",
    "name": "Web Scraper",
    "description": "Build an efficient web scraping system",
    "difficulty": "medium",
    "tags": ["web", "scraping", "data"],
    "task_count": 10
  },
  ...
]
```

Available Templates:

1. **rest_api** - REST API Development (10 tasks)
2. **web_scraper** - Web Scraper (10 tasks)
3. **machine_learning** - Machine Learning Pipeline (10 tasks)
4. **react_app** - React Application (10 tasks)
5. **ci_cd_pipeline** - CI/CD Pipeline (10 tasks)
6. **mobile_app** - Mobile Application (10 tasks)
7. **database_design** - Database Design (10 tasks)
8. **documentation** - Documentation (10 tasks)

### 2. Get Template Details

**Request:**

```bash
curl -X GET "http://localhost:8000/templates/rest_api" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

**Response:**

```json
{
  "id": "rest_api",
  "name": "REST API Development",
  "description": "Build a production REST API with proper structure and best practices",
  "difficulty": "medium",
  "tags": ["api", "backend", "rest"],
  "tasks": [
    {
      "id": 1,
      "description": "Design API endpoints and documentation",
      "priority": "high"
    },
    {
      "id": 2,
      "description": "Implement authentication and authorization",
      "priority": "high"
    },
    ...
  ]
}
```

### 3. Search Templates

**Request:**

```bash
curl -X GET "http://localhost:8000/templates/search/web" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

**Response:**

```json
{
  "query": "web",
  "results": [
    {
      "id": "web_scraper",
      "name": "Web Scraper",
      "description": "Build an efficient web scraping system",
      "difficulty": "medium",
      "tags": ["web", "scraping", "data"]
    }
  ]
}
```

---

## 📊 Analytics API (Phase 3)

### 1. Get Overall Analytics

**Request:**

```bash
curl -X GET "http://localhost:8000/analytics" \
  -H "Authorization: Bearer {ADMIN_TOKEN}"
```

**Response:**

```json
{
  "total_executions": 42,
  "average_success_rate": 95.2,
  "tasks_analyzed": 15,
  "performance_report": {
    "total_executions": 42,
    "total_successful": 40,
    "total_failed": 2,
    "overall_success_rate": 95.2,
    "average_execution_time": 2.35,
    "total_results_length": 45320
  }
}
```

### 2. Get Task-Specific Analytics

**Request:**

```bash
curl -X GET "http://localhost:8000/analytics/tasks/1" \
  -H "Authorization: Bearer {ADMIN_TOKEN}"
```

**Response:**

```json
{
  "task_id": 1,
  "execution_count": 5,
  "success_count": 5,
  "success_rate": 100.0,
  "avg_duration": 2.45,
  "min_duration": 1.8,
  "max_duration": 3.2,
  "total_results_length": 4500
}
```

### 3. Get Performance Metrics

**Request:**

```bash
curl -X GET "http://localhost:8000/analytics/performance" \
  -H "Authorization: Bearer {ADMIN_TOKEN}"
```

**Response:**

```json
{
  "performance_report": {
    "total_executions": 42,
    "total_successful": 40,
    "total_failed": 2,
    "overall_success_rate": 95.2,
    "average_execution_time": 2.35,
    "total_results_length": 45320
  },
  "trending_tasks": [
    {
      "task_id": 3,
      "execution_count": 12,
      "success_rate": 100.0
    },
    {
      "task_id": 1,
      "execution_count": 5,
      "success_rate": 100.0
    }
  ],
  "hourly_summary": {...},
  "daily_summary": {...}
}
```

---

## 🔌 WebSocket Real-time Updates

### Connect to WebSocket

```bash
# Using websocat (install with: cargo install websocat)
websocat ws://localhost:8000/ws/client1

# Or using Node.js ws client
npm install -g ws
wscat -c ws://localhost:8000/ws/client1
```

### Subscribe to Events

**Send:**

```json
{
  "action": "subscribe",
  "topic": "plan_1"
}
```

**Response:**

```json
{
  "type": "subscribed",
  "topic": "plan_1"
}
```

### Receive Task Events

When tasks execute, you'll receive events like:

```json
{
  "event": "task_started",
  "plan_id": 1,
  "task_id": 2,
  "description": "Implement authentication",
  "timestamp": "2025-12-02T10:31:45.123456"
}
```

Event Types:

- `task_started` - Task execution began
- `task_progress` - Progress update during execution
- `task_completed` - Task successfully completed
- `task_failed` - Task execution failed
- `plan_updated` - Plan status changed

---

## 🎯 Planning & Execution

### 1. Create a Plan

**Request:**

```bash
curl -X POST "http://localhost:8000/plans" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a REST API",
    "repo_path": "."
  }'
```

**Response:**

```json
{
  "plan_id": 1,
  "goal": "Build a REST API",
  "tasks": 5,
  "status": "created"
}
```

### 2. Get Plan Details

**Request:**

```bash
curl -X GET "http://localhost:8000/plans/1" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

### 3. Execute Task

**Request:**

```bash
curl -X POST "http://localhost:8000/plans/1/execute" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": 1,
    "task_id": 1
  }'
```

---

## 📊 Conversation History

### Get Conversation History

**Request:**

```bash
curl -X GET "http://localhost:8000/conversation?limit=50" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

### Add Message

**Request:**

```bash
curl -X POST "http://localhost:8000/conversation" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "user",
    "content": "Build a web scraper for news sites"
  }'
```

---

## 🔍 Repository Scanning

**Request:**

```bash
curl -X POST "http://localhost:8000/scan" \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -d "repo_path=."
```

**Response:**

```json
{
  "repository": ".",
  "info": {
    "total_files": 36,
    "total_python_files": 23,
    "total_lines_of_code": 4096,
    "programming_languages": ["Python"],
    "directory_tree": {...}
  }
}
```

---

## 🧪 Integration Testing

### Test Workflow: Complete User Journey

```bash
#!/bin/bash

# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"

# 2. List Templates
curl -s -X GET "http://localhost:8000/templates" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# 3. Get Specific Template
curl -s -X GET "http://localhost:8000/templates/rest_api" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# 4. Create Plan
PLAN=$(curl -s -X POST "http://localhost:8000/plans" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"goal":"Build API","repo_path":"."}')

echo "Plan: $PLAN"
PLAN_ID=$(echo $PLAN | jq -r '.plan_id')

# 5. Get Plan Details
curl -s -X GET "http://localhost:8000/plans/$PLAN_ID" \
  -H "Authorization: Bearer $TOKEN" | jq '.'

# 6. Check Analytics
curl -s -X GET "http://localhost:8000/analytics" \
  -H "Authorization: Bearer $(curl -s -X POST "http://localhost:8000/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')" | jq '.'
```

---

## 🛡️ Security Features

### Role-Based Access Control

**User Role:**

- Can create plans, execute tasks, view templates, conversation

**Admin Role:**

- Can do everything + access /analytics endpoints

### JWT Token

- Auto-expiring tokens (60 minutes default)
- Bearer authentication via Authorization header
- Stateless validation using HS256 algorithm

### API Keys

- Generate persistent API keys
- Revoke keys as needed
- Track key usage and expiration

---

## 📈 Performance Metrics

The analytics system tracks:

- **Execution Count** - How many times a task has run
- **Success Rate** - Percentage of successful executions
- **Duration** - Execution time (min, max, average)
- **Result Size** - Size of outputs generated
- **Trending** - Most-used tasks
- **Hourly/Daily** - Time-based aggregations

---

## 🔧 Configuration

API configuration is in `agent.config.yaml`:

```yaml
llm:
  provider: mock # mock, ollama, or openai_like
  model: gpt-4
  api_base: http://localhost:11434
  api_key: ""
  temperature: 0.7
  top_p: 0.95
```

---

## 📚 Further Reading

- REST API: `/plans`, `/templates`, `/analytics` endpoints
- WebSocket: Real-time `/ws/{client_id}` updates
- Authentication: JWT and API key management
- Analytics: Performance tracking and reporting
- Examples: See `examples.py` and `test_agent.py`

---

## ✅ Complete Feature Checklist

### Phase 1 (Core)

- [x] Task Planner
- [x] Task Executor
- [x] Conversation History
- [x] Repository Scanner
- [x] File Patcher

### Phase 2 (Integration)

- [x] REST API (10 endpoints)
- [x] Database Persistence
- [x] CLI Interface
- [x] Unit Tests (26 tests)
- [x] Examples & Documentation

### Phase 3 (Advanced)

- [x] WebSocket Real-time Updates
- [x] JWT Authentication + API Keys
- [x] Task Templates (8 templates)
- [x] Performance Analytics
- [x] API Integration (24 total endpoints)

---

## 🎉 Ready to Use!

The framework is now production-ready with:

- 24 REST API endpoints
- Real-time WebSocket support
- Comprehensive authentication
- 8 reusable templates
- Performance monitoring
- Full documentation

Start the server and explore! 🚀
