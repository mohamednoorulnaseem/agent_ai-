# AI Agent Framework

An intelligent agent framework for automated development tasks powered by LLMs.

## ✨ Features

### Phase 1: Core Framework

- **Smart Planning**: Break down complex goals into actionable tasks using LLM
- **Code Execution**: Execute tasks with access to repository scanning and code patching
- **Conversation History**: Track and manage multi-turn conversations
- **Repository Tools**: Scan codebases and apply targeted code changes
- **Multiple LLM Support**: Works with Ollama, OpenAI, and OpenAI-like APIs
- **Interactive CLI**: Command-line interface for easy interaction

### Phase 2: Production Ready

- **REST API**: 10 endpoints for plan management and execution
- **Database Persistence**: SQLite backend for data survival
- **Web Integration**: FastAPI server for remote access

### Phase 3: Enterprise Features (NEW! 🚀)

- **Real-time Updates**: WebSocket support for live task monitoring
- **Authentication**: JWT tokens + API key management
- **Task Templates**: 8 predefined workflow templates
- **Performance Analytics**: Track execution metrics and trending tasks
- **24 REST Endpoints**: Comprehensive API coverage

## Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install pyyaml requests openai
   ```

3. Create a configuration file `agent.config.yaml`:
   ```yaml
   llm:
     provider: "ollama" # or "openai_like"
     model: "llama2"
     api_base: "http://localhost:11434"
     temperature: 0.0
     top_p: 1.0
   ```

## Usage

### Command Line

```bash
# Plan a goal
python -m agent_ai.cli --goal "Create a REST API for user management"

# Scan repository
python -m agent_ai.cli --scan

# Execute a task
python -m agent_ai.cli --execute 1

# Interactive mode
python -m agent_ai.cli --interactive

# With custom config and repository
python -m agent_ai.cli --goal "Fix linting errors" --repo /path/to/repo --config custom.yaml
```

### Programmatic Usage

```python
from agent_ai import load_config_and_llm, Planner, Executor

# Load configuration and LLM
config, llm = load_config_and_llm("agent.config.yaml")

# Create planner and executor
planner = Planner(llm)
executor = Executor(llm, "/path/to/repo")

# Plan a goal
tasks = planner.plan("Implement user authentication")

# Execute tasks
for task in tasks:
    result = executor.execute_task(task)
    planner.mark_task_complete(task.id, result)
    print(result)

# View summary
print(planner.get_plan_summary())
```

## Architecture

### Components

- **Planner** (`agent/planner.py`): Breaks goals into tasks
- **Executor** (`agent/executor.py`): Executes tasks and manages results
- **History** (`agent/history.py`): Tracks conversation messages
- **Scanner** (`repo/scanner.py`): Analyzes repository structure
- **Patcher** (`repo/patcher.py`): Applies code changes safely
- **LLM Providers** (`llm/`): Supports multiple LLM backends

### Configuration

Configuration is loaded from `agent.config.yaml`:

```yaml
llm:
  provider: "ollama" # LLM provider
  model: "llama2" # Model name
  api_base: "http://localhost:11434" # API endpoint
  temperature: 0.0 # Creativity (0=deterministic, 1=creative)
  top_p: 1.0 # Nucleus sampling

agent:
  max_tasks: 50 # Maximum tasks per plan
  max_history: 100 # Maximum conversation messages
  task_timeout: 300 # Task timeout in seconds

repository:
  ignore_dirs: [".git", "__pycache__", "node_modules"]
  code_extensions: [".py", ".js", ".ts"]

logging:
  level: "INFO"
  console: true
```

## Supported LLMs

### Ollama (Local)

```yaml
llm:
  provider: "ollama"
  model: "llama2"
  api_base: "http://localhost:11434"
```

### OpenAI

```yaml
llm:
  provider: "openai_like"
  model: "gpt-4"
  api_base: "https://api.openai.com/v1"
  api_key: "your-api-key"
```

### Other OpenAI-compatible APIs

```yaml
llm:
  provider: "openai_like"
  model: "your-model"
  api_base: "https://your-api-endpoint"
  api_key: "your-api-key"
```

## Workflow

1. **Plan**: Define a high-level goal
2. **Break Down**: Agent plans the goal into tasks
3. **Scan**: Agent scans the repository
4. **Execute**: Agent executes each task using the LLM
5. **Apply**: Changes are applied safely with backups
6. **Track**: Conversation history is maintained

## Examples

### Example 1: Create a REST API

```bash
python -m agent_ai.cli --goal "Create a FastAPI REST API for managing todos with CRUD operations"
```

### Example 2: Fix Code Issues

```bash
python -m agent_ai.cli --goal "Find all Python files with unused imports and remove them"
```

### Example 3: Add Documentation

```bash
python -m agent_ai.cli --goal "Add comprehensive docstrings to all functions in src/utils.py"
```

## Safety Features

- **Backups**: Automatic backups before modifying files
- **Validation**: Configuration validation before execution
- **Limits**: Task and history size limits to prevent resource exhaustion
- **Permissions**: Safe file system operations with error handling
- **Timeouts**: Configurable task execution timeouts

## Development

### Adding a New LLM Provider

1. Create a new class in `llm/`:

   ```python
   from agent_ai.llm.base import LLM

   class YourProvider(LLM):
       def completion(self, messages, **kwargs):
           # Implementation here
           pass
   ```

2. Register in `config.py`:
   ```python
   elif provider == "your_provider":
       llm = YourProvider(...)
   ```

## Contributing

Contributions are welcome! Please ensure:

- Code follows PEP 8 style guide
- All functions have docstrings
- Error handling is comprehensive
- Tests are included for new features

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
