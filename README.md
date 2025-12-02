# AI Agent Framework 🤖

An intelligent agent framework for automated development tasks powered by LLMs.

## 📁 Project Structure

```
agent_ai-/
├── README.md                 # This file (main documentation)
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── agent.config.yaml        # Agent configuration template
│
├── src/                     # Source code
│   ├── __init__.py
│   ├── api.py              # REST API endpoints
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration loader
│   ├── analytics.py        # Performance analytics
│   ├── auth.py             # Authentication & JWT
│   ├── persistence.py      # Database layer (SQLite)
│   ├── templates.py        # Workflow templates
│   ├── examples.py         # Usage examples
│   ├── tests.py            # Unit and integration tests
│   ├── websocket_support.py # Real-time WebSocket updates
│   │
│   ├── agent/              # Core agent framework
│   │   ├── planner.py      # Task planning (LLM-driven)
│   │   ├── executor.py     # Task execution
│   │   └── history.py      # Conversation tracking
│   │
│   ├── llm/                # LLM provider integrations
│   │   ├── base.py         # Base LLM interface
│   │   ├── ollama.py       # Ollama (local)
│   │   ├── openai_like.py  # OpenAI-compatible APIs
│   │   └── mock.py         # Mock LLM for testing
│   │
│   └── repo/               # Repository tools
│       ├── scanner.py      # Codebase analysis
│       └── patcher.py      # Safe code patching
│
├── docs/                   # Documentation
│   ├── README.md           # Main docs (moved here)
│   ├── README.docker.md    # Docker setup guide
│   └── LICENSE             # MIT License
│
├── scripts/                # Utility scripts (for future use)
│
└── .github/                # GitHub workflows (CI/CD)
    └── workflows/
        └── ci.yml
```

## ✨ Features

### Phase 1: Core Framework

- **Smart Planning**: Break down complex goals into actionable tasks using LLM
- **Code Execution**: Execute tasks with repository access and code patching
- **Conversation History**: Track and manage multi-turn conversations
- **Repository Tools**: Scan codebases and apply targeted changes safely
- **Multiple LLM Support**: Works with Ollama, OpenAI, and OpenAI-like APIs
- **Interactive CLI**: Easy command-line interface

### Phase 2: Production Ready

- **REST API**: 10+ endpoints for plan management and execution
- **Database Persistence**: SQLite backend for data survival
- **Web Integration**: FastAPI server for remote access

### Phase 3: Enterprise Features 🚀

- **Real-time Updates**: WebSocket support for live task monitoring
- **Authentication**: JWT tokens + API key management
- **Task Templates**: 8+ predefined workflow templates
- **Performance Analytics**: Track execution metrics and trending tasks
- **24 REST Endpoints**: Comprehensive API coverage

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/mohamednoorulnaseem/agent_ai-.git
cd agent_ai-

# Install dependencies
pip install -r requirements.txt

# (Optional) For development
pip install -e .
```

### 2. Configure LLM

Create `agent.config.yaml`:

```yaml
llm:
  provider: "ollama" # or "openai_like"
  model: "llama2"
  api_base: "http://localhost:11434"
  temperature: 0.0
  top_p: 1.0
```

### 3. Run via CLI

```bash
# Plan a goal
python -m src.cli --goal "Create a REST API for user management"

# Interactive mode
python -m src.cli --interactive
```

### 4. Run via REST API

```bash
# Start the server
python -m src.api

# API will be available at http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

### 5. Run with Docker (Recommended)

```bash
docker compose up --build
# Access at http://localhost:8000
```

## 📖 Documentation

- **[Main Docs](docs/README.md)** — Detailed usage, architecture, examples
- **[Docker Setup](docs/README.docker.md)** — Docker and Compose instructions
- **[License](docs/LICENSE)** — MIT License

## ⚙️ Configuration

All settings are in `agent.config.yaml`:

```yaml
llm:
  provider: "ollama"
  model: "llama2"
  api_base: "http://localhost:11434"
  temperature: 0.0

agent:
  max_tasks: 50
  max_history: 100
  task_timeout: 300

repository:
  ignore_dirs: [".git", "__pycache__", "node_modules"]
  code_extensions: [".py", ".js", ".ts"]

logging:
  level: "INFO"
  console: true
```

## 🔌 Supported LLMs

| Provider             | Config                  | Notes                          |
| -------------------- | ----------------------- | ------------------------------ |
| **Ollama**           | `provider: ollama`      | Local, no API key needed       |
| **OpenAI**           | `provider: openai_like` | API key required               |
| **Other compatible** | `provider: openai_like` | Any OpenAI-compatible endpoint |

## 🧪 Testing

```bash
# Run all tests
python -m pytest src/tests.py -v

# Run specific test
python -m pytest src/tests.py::TestPlanner -v
```

## 🐳 Docker Commands

```bash
# Build and run
docker compose up --build -d

# View logs
docker compose logs -f

# Stop containers
docker compose down

# Clean up
docker image prune -f && docker volume prune -f
```

See [Docker guide](docs/README.docker.md) for more details.

## 🤝 Contributing

Contributions welcome! Please ensure:

- Code follows PEP 8 style guide
- Functions have docstrings
- Tests are included for new features
- All tests pass

## 📄 License

MIT License — See [LICENSE](docs/LICENSE) for details.

## 🆘 Support

For issues or questions, please open an issue on [GitHub](https://github.com/mohamednoorulnaseem/agent_ai-).

---

**Happy automating!** 🚀
