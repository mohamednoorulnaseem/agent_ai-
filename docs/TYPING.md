# Type Hints Guide

This document describes the type hints strategy for the AI Agent Framework.

## Overview

The project uses Python 3.9+ type hints to ensure:
- Better IDE support and autocomplete
- Earlier detection of type-related bugs
- Clearer function and method contracts
- Easier maintenance and refactoring

## Type Hints Coverage

### Core Modules

| Module       | Coverage | Status      |
| ------------ | -------- | ----------- |
| `src/auth.py`       | 100%     | ✅ Complete |
| `src/cli.py`        | 90%      | ✅ Complete |
| `src/config.py`     | 85%      | ✅ Complete |
| `src/persistence.py`| 95%      | ✅ Complete |
| `src/api.py`        | 80%      | 🔄 Partial  |
| `src/agent/`        | 75%      | 🔄 Partial  |
| `src/llm/`          | 70%      | 🔄 Partial  |
| `src/repo/`         | 65%      | 🔄 Partial  |

## Type Hints Conventions

### Function Arguments and Return Types

All public functions include complete type hints:

```python
from typing import Optional, List, Dict, Any, Tuple

def process_goal(goal: str, max_tasks: int = 50) -> List[str]:
    """Process a goal and return task descriptions."""
    ...

def get_config() -> Dict[str, Any]:
    """Load configuration from file."""
    ...

async def execute_task(task_id: int) -> Tuple[bool, str]:
    """Execute a task and return (success, result)."""
    ...
```

### Class Attributes

Class attributes with type hints:

```python
class TaskManager:
    tasks: Dict[int, Task] = {}
    max_tasks: int = 50
    config: Optional[Config] = None
    
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.created_at: datetime = datetime.now()
```

### Optional Types

Use `Optional[T]` for values that can be `None`:

```python
def find_task(task_id: int) -> Optional[Task]:
    """Find a task by ID, return None if not found."""
    ...

def get_cached_result() -> Optional[Dict[str, Any]]:
    """Get cached result or None if not cached."""
    ...
```

### Union Types

Use `Union[T1, T2]` for values of multiple types:

```python
from typing import Union

def process_input(data: Union[str, int, List[str]]) -> str:
    """Process various input types."""
    ...
```

### Generic Types

Use generic types for collections:

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Cache(Generic[T]):
    def __init__(self) -> None:
        self.items: Dict[str, T] = {}
    
    def get(self, key: str) -> Optional[T]:
        return self.items.get(key)
    
    def set(self, key: str, value: T) -> None:
        self.items[key] = value
```

## Running Type Checks

### With MyPy

```bash
# Check all files
mypy src/

# Check specific file
mypy src/api.py

# Check with strict mode
mypy --strict src/

# Check with configuration
mypy --config-file=mypy.ini src/
```

### With PyRight

```bash
# Check all files
pyright src/

# Check specific file
pyright src/api.py

# Check with strict settings
pyright --outputjson src/
```

### Using Make

```bash
# Type check via Makefile
make type-check

# Run all quality checks (including type checking)
make check
```

## Common Type Hint Patterns

### Callbacks

```python
from typing import Callable

def register_handler(handler: Callable[[str], None]) -> None:
    """Register a callback handler."""
    ...

def execute_with_callback(
    task: Task,
    callback: Callable[[int, str], None]
) -> None:
    """Execute task and call callback with (progress, message)."""
    ...
```

### Variable Arguments

```python
from typing import TypeVar

T = TypeVar('T')

def process_multiple(*items: str) -> List[str]:
    """Process multiple string items."""
    ...

def merge_dicts(**kwargs: Any) -> Dict[str, Any]:
    """Merge multiple keyword arguments."""
    ...
```

### Protocols

```python
from typing import Protocol

class Validator(Protocol):
    def validate(self, data: str) -> bool:
        """Validate data."""
        ...

def validate_input(validator: Validator, data: str) -> bool:
    """Use any object with validate method."""
    return validator.validate(data)
```

### Type Aliases

```python
from typing import TypeAlias

TaskID: TypeAlias = int
TaskDescription: TypeAlias = str
TaskResult: TypeAlias = Dict[str, Any]

def process_task(task_id: TaskID) -> TaskResult:
    """Process a task."""
    ...
```

## IDE Integration

### Visual Studio Code

Add to `.vscode/settings.json`:

```json
{
    "python.linting.mypyEnabled": true,
    "python.linting.mypyArgs": [
        "--strict"
    ],
    "[python]": {
        "editor.defaultFormatter": "ms-python.python"
    }
}
```

### PyCharm

- Settings → Project → Python Interpreter → Package
- Install: `mypy`
- Run: Tools → Python → Run mypy

## Future Improvements

- [ ] Achieve 100% type coverage across all modules
- [ ] Add `mypy.ini` configuration with strict mode
- [ ] Integrate type checking into CI/CD pipeline
- [ ] Document type hints in API documentation
- [ ] Add TypedDict for complex structures
- [ ] Create type stub files (.pyi) for complex modules

## References

- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [PEP 585 - Type Hinting Generics](https://www.python.org/dev/peps/pep-0585/)
- [PEP 586 - Literal Types](https://www.python.org/dev/peps/pep-0586/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [Python typing Module](https://docs.python.org/3/library/typing.html)

---

Last updated: 2025-12-02
