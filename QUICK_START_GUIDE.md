# Quick Start Guide - Phase 3 Ready System

**Status:** ✅ Production Ready | **Version:** 0.3.0

---

## 🚀 Start in 3 Steps

### Step 1: Install Dependencies

```bash
cd c:\Users\moham\agent_ai
pip install -r requirements.txt
```

### Step 2: Start the API Server

```bash
python -m uvicorn api:app --reload --port 8000
```

### Step 3: Access the API

Open browser: **http://localhost:8000/docs**

---

## 🔑 Authentication

### Get a Token

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user_id": "user_demo",
  "username": "demo"
}
```

### Use Token in Requests

```bash
curl -H "Authorization: Bearer {ACCESS_TOKEN}" \
  http://localhost:8000/templates
```

---

## 📋 Basic Operations

### 1. List Templates

```bash
curl -H "Authorization: Bearer {TOKEN}" \
  http://localhost:8000/templates
```

**8 Available Templates:**

- REST API Development (10 tasks)
- Web Scraper (10 tasks)
- Machine Learning Pipeline (10 tasks)
- React Application (10 tasks)
- CI/CD Pipeline (10 tasks)
- Mobile Application (10 tasks)
- Database Design (10 tasks)
- Documentation (10 tasks)

### 2. Search Templates

```bash
curl -H "Authorization: Bearer {TOKEN}" \
  "http://localhost:8000/templates/search/api"
```

### 3. Get Template Details

```bash
curl -H "Authorization: Bearer {TOKEN}" \
  http://localhost:8000/templates/rest_api
```

### 4. Create a Plan

```bash
curl -X POST "http://localhost:8000/plans" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a REST API",
    "repo_path": "."
  }'
```

### 5. View Analytics

```bash
# Get overall analytics (admin only)
curl -H "Authorization: Bearer {ADMIN_TOKEN}" \
  http://localhost:8000/analytics

# Get task-specific metrics
curl -H "Authorization: Bearer {ADMIN_TOKEN}" \
  "http://localhost:8000/analytics/tasks/1"
```

---

## 🌐 WebSocket Real-time Monitoring

### Connect to WebSocket

```bash
# Using websocat (install: cargo install websocat)
websocat ws://localhost:8000/ws/client1

# Or using Node.js ws
npm install -g ws
wscat -c ws://localhost:8000/ws/client1
```

### Subscribe to Events

Send JSON:

```json
{
  "action": "subscribe",
  "topic": "plan_1"
}
```

### Receive Events

When tasks execute:

```json
{
  "event": "task_started",
  "plan_id": 1,
  "task_id": 2,
  "description": "Implement authentication",
  "timestamp": "2025-12-02T10:31:45.123456"
}
```

---

## 🧪 Test Everything

### Run Integration Test

```bash
python test_phase3_integration.py
```

**Expected Output:**

```
[PASS] Authentication System
[PASS] WebSocket Real-time Support
[PASS] Task Templates
[PASS] Analytics Engine
[PASS] API Integration
[PASS] Core System Compatibility

Total: 6/6 tests passed
```

---

## 📚 API Endpoints Reference

### Health Check

```
GET /health
```

### Authentication (3 endpoints)

```
POST /auth/login
POST /auth/token
GET /auth/validate
```

### Planning (5 endpoints)

```
POST /plans
GET /plans
GET /plans/{id}
GET /plans/{id}/tasks
POST /plans/{id}/execute
```

### Templates (3 endpoints - NEW!)

```
GET /templates
GET /templates/{id}
GET /templates/search/{query}
```

### Analytics (3 endpoints - NEW!)

```
GET /analytics
GET /analytics/tasks/{id}
GET /analytics/performance
```

### WebSocket (1 endpoint - NEW!)

```
WS /ws/{client_id}
```

### Conversation (2 endpoints)

```
GET /conversation
POST /conversation
```

### Repository (1 endpoint)

```
POST /scan
```

### Statistics (1 endpoint)

```
GET /stats
```

---

## 🔒 Security

### Demo Accounts

**User Account (Limited Access)**

```
Username: demo
Password: demo123
Permissions: plans, templates, conversation
```

**Admin Account (Full Access)**

```
Username: admin
Password: admin123
Permissions: everything + analytics
```

### Authentication Methods

1. **JWT Tokens** - 60-minute expiry
2. **API Keys** - Persistent, revocable
3. **Bearer Token** - In Authorization header

---

## 📊 System Components

### 6 Core Modules

- Planner - Break goals into tasks
- Executor - Execute tasks
- History - Track conversations
- Scanner - Analyze repositories
- Patcher - Apply code changes
- Config - LLM configuration

### 4 Phase 3 Modules

- websocket_support - Real-time updates
- auth - Authentication
- templates - Workflow templates
- analytics - Performance metrics

### Storage

- SQLite database for persistence
- Conversation history
- Plan and task tracking
- Execution metrics

---

## 🛠️ Configuration

Edit `agent.config.yaml`:

```yaml
llm:
  provider: "mock" # mock, ollama, or openai_like
  model: "gpt-4"
  api_base: "http://localhost:11434"
  temperature: 0.7
  top_p: 0.95
```

### LLM Providers

- **mock** - Testing without external services
- **ollama** - Local LLM (Llama2, etc)
- **openai_like** - OpenAI or compatible APIs

---

## 📈 Monitoring

### View Performance Metrics

```bash
curl -H "Authorization: Bearer {ADMIN_TOKEN}" \
  http://localhost:8000/analytics/performance
```

Response includes:

- Total executions
- Success rates
- Trending tasks
- Hourly/daily summaries

### Track Individual Tasks

```bash
curl -H "Authorization: Bearer {ADMIN_TOKEN}" \
  "http://localhost:8000/analytics/tasks/1"
```

---

## 🐛 Troubleshooting

### API Won't Start

```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use different port
python -m uvicorn api:app --port 8001
```

### Import Errors

```bash
# Reinstall package
pip install -e . --force-reinstall
```

### WebSocket Connection Fails

```bash
# Check WebSocket is enabled in FastAPI
# Try with: ws://localhost:8000/ws/test_client
```

---

## 📞 Support

### Documentation Files

- `FINAL_SUMMARY.md` - Executive summary
- `API_DEMO_PHASE3.md` - Complete API examples
- `GETTING_STARTED.md` - Detailed setup
- `API_DOCUMENTATION.md` - Endpoint reference
- `README.md` - Project overview

### Test Files

- `test_phase3_integration.py` - Integration tests
- `test_agent.py` - Agent demonstration
- `examples.py` - Usage examples

---

## ✨ You're All Set!

The system is production-ready. Start with:

```bash
# 1. Start API server
python -m uvicorn api:app --reload --port 8000

# 2. Open browser
# http://localhost:8000/docs

# 3. Login with demo/demo123

# 4. Try templates or create a plan
```

**Happy developing! 🚀**

---

_AI Agent Framework v0.3.0 | Phase 3 Complete | December 2, 2025_
