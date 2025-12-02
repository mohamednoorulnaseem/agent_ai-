# Getting Started with AI Agent

Quick start guide for the AI Agent framework.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd agent_ai
pip install -r requirements.txt
```

### Step 2: Configure LLM

Edit `agent.config.yaml`:

```yaml
llm:
  provider: "mock" # or "ollama", "openai_like"
  model: "mock"
  api_base: "http://localhost:11434"
```

For **Ollama** (local):

```yaml
llm:
  provider: "ollama"
  model: "llama2"
  api_base: "http://localhost:11434"
```

For **OpenAI**:

```yaml
llm:
  provider: "openai_like"
  model: "gpt-4"
  api_base: "https://api.openai.com/v1"
  api_key: "your-api-key"
```

## Usage

### 1. Interactive Mode

Start the interactive CLI:

```bash
python cli.py --interactive
```

Commands:

- `exec <task_id>` - Execute a task
- `show plan` - Display current plan
- `scan` - Scan repository
- `history` - Show conversation history
- `exit` - Exit

Example:

```
agent> plan Create a REST API for user management
agent> show plan
agent> exit
```

### 2. Command-Line Mode

Single command execution:

```bash
# Plan a goal
python cli.py --goal "Create a data pipeline"

# Scan repository
python cli.py --scan

# View help
python cli.py --help
```

from agent_ai import load_config_and_llm, Planner, Executor

# Load configuration

config, llm = load_config_and_llm()

# Create planner

planner = Planner(llm)

# Plan a goal

tasks = planner.plan("Build a web scraper")

# Create executor

executor = Executor(llm, ".")

# Execute tasks

for task in tasks:
result = executor.execute_task(task)
planner.mark_task_complete(task.id, result)
print(result)

````

### 4. REST API

Start the API server:

```bash
python -m uvicorn agent_ai.api:app --reload

Create a plan:

```bash
curl -X POST "http://localhost:8000/plans" \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Build a REST API",
    "repo_path": "."
  }'
````

Access Swagger UI: `http://localhost:8000/docs`

### 5. Run Tests

Execute unit tests:

```bash
python tests.py
```

### 6. Run Examples

See practical examples:

```bash
python examples.py
```

## Common Use Cases

### Use Case 1: Plan a Project

```bash
python cli.py --goal "Create a machine learning pipeline for image classification"
```

This will:

1. Break down the goal into specific tasks
2. Display the plan
3. Suggest next steps

### Use Case 2: Analyze Repository

```bash
python cli.py --scan --verbose
```

This will:

1. Scan your repository structure
2. Count files by language
3. Identify key directories

### Use Case 3: Full Workflow

```python
from agent_ai import *

# Initialize
config, llm = load_config_and_llm()
planner = Planner(llm)
executor = Executor(llm, "my_project")
history = ConversationHistory()

# Track conversation
history.add_message("user", "Plan the project")

# Plan
goal = "Create a REST API"
tasks = planner.plan(goal)
history.add_message("assistant", planner.get_plan_summary())

# Execute
for task in tasks[:3]:
    result = executor.execute_task(task)
    planner.mark_task_complete(task.id, result)
    history.add_message("assistant", result)

# Review
print(history.get_summary())
```

## Troubleshooting

### Issue: "No module named 'agent_ai'"

**Solution:** Install in editable mode:

```bash
pip install -e .
```

### Issue: "Error: Configuration file 'agent.config.yaml' not found"

**Solution:** Make sure you're in the `agent_ai` directory and the config file exists.

### Issue: "Connection refused" when using Ollama

**Solution:** Make sure Ollama is running:

```bash
ollama serve
```

### Issue: "OpenAI API Key not found"

**Solution:** Set the environment variable:

```bash
export OPENAI_API_KEY="your-key-here"
```

Or configure in `agent.config.yaml`:

```yaml
api_key: "your-key-here"
```

## Next Steps

1. **Explore Examples** - Run `python examples.py` to see various use cases
2. **Read Documentation** - Check `README.md` for detailed documentation
3. **Run Tests** - Execute `python tests.py` to verify installation
4. **API Exploration** - Start the API server and visit `http://localhost:8000/docs`
5. **Customize** - Modify configuration and extend for your needs

## Project Structure

```
agent_ai/
├── agent/                  # Core agent logic
│   ├── planner.py         # Task planning
│   ├── executor.py        # Task execution
│   └── history.py         # Conversation tracking
├── llm/                    # LLM providers
│   ├── base.py            # Base class
│   ├── ollama.py          # Ollama integration
│   ├── openai_like.py     # OpenAI integration
│   └── mock.py            # Mock for testing
├── repo/                   # Repository tools
│   ├── scanner.py         # Code analysis
│   └── patcher.py         # Code modification
├── cli.py                 # Command-line interface
├── config.py              # Configuration loading
├── persistence.py         # Database layer
├── api.py                 # REST API
├── tests.py               # Unit tests
├── examples.py            # Usage examples
└── agent.config.yaml      # Configuration file
```

## Key Concepts

### Task Planning

The planner uses an LLM to break down complex goals into specific, actionable tasks.

### Task Execution

The executor runs tasks and can interact with the codebase through the repository tools.

### Conversation History

All interactions are tracked, enabling multi-turn workflows and better context.

### Persistence

Plans and executions are stored in a SQLite database for later retrieval and analysis.

### Repository Scanning

The scanner analyzes code structure and can identify files for modification.

### Code Patching

The patcher safely applies changes to files with automatic backups.

## Tips and Best Practices

1. **Use Clear Goals** - Specific goals produce better task plans
2. **Review Plans** - Always check the generated plan before execution
3. **Start with Mock LLM** - Test with mock LLM before using real APIs
4. **Monitor Execution** - Check conversation history after execution
5. **Backup Important Files** - Enable backups in configuration
6. **Use Interactive Mode** - For exploratory work and debugging
7. **Batch Operations** - Use API for automated workflows

## Support and Feedback

For issues or questions:

1. Check the troubleshooting section above
2. Review the documentation files
3. Run the examples for reference
4. Check test cases for API usage

## Resources

- **README.md** - Full project documentation
- **API_DOCUMENTATION.md** - REST API reference
- **examples.py** - Practical usage examples
- **tests.py** - Unit test cases
- **config.py** - Configuration management

## License

MIT License - See LICENSE file for details
