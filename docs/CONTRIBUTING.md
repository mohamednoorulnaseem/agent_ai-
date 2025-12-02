# Contributing to AI Agent Framework

Thank you for your interest in contributing to the AI Agent Framework! This document provides guidelines and instructions for contributing.

## 🎯 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/agent_ai-.git
cd agent_ai-
```

### 2. Set Up Development Environment

```bash
# Install development dependencies
make install-dev

# Or manually:
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 pylint mypy pre-commit
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/your-bug-fix-name
```

## 📋 Development Workflow

### Code Style & Quality

We follow **PEP 8** with some customizations:

```bash
# Format code with black (100-char line length)
make format

# Run linting checks
make lint

# Run all quality checks
make check
```

### Testing

All new features must include tests:

```bash
# Run tests
make test

# Run tests with coverage report
make test-coverage

# Run specific test file
python -m pytest src/tests.py::TestClassName -v
```

### Common Development Tasks

```bash
# Start the application for testing
make run

# View logs
make logs

# Stop containers
make stop

# Clean up temporary files
make clean
```

## 📝 Commit Guidelines

Use clear, descriptive commit messages:

```bash
# Good examples:
git commit -m "feat: add WebSocket support for real-time updates"
git commit -m "fix: resolve null pointer exception in task executor"
git commit -m "refactor: improve code organization in planner module"
git commit -m "docs: add API endpoint documentation"
git commit -m "test: add unit tests for scanner module"

# Avoid:
git commit -m "fixed stuff"
git commit -m "changes"
git commit -m "WIP"
```

**Commit message format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `docs`: Documentation changes
- `chore`: Maintenance, dependency updates
- `perf`: Performance improvements

## 🔧 Adding New Features

### 1. Create a Feature Branch

```bash
git checkout -b feature/awesome-feature
```

### 2. Implement Your Feature

- Follow existing code patterns
- Add type hints to functions
- Write clear docstrings
- Keep functions focused and testable

Example:

```python
def process_task(task_id: str, config: dict) -> dict:
    """
    Process a task and return results.
    
    Args:
        task_id: Unique task identifier
        config: Configuration dictionary
        
    Returns:
        Dictionary containing task results
        
    Raises:
        ValueError: If task_id is empty
        RuntimeError: If processing fails
    """
    if not task_id:
        raise ValueError("task_id cannot be empty")
    
    # Implementation here
    return {"status": "success", "task_id": task_id}
```

### 3. Write Tests

Create tests in `src/tests.py` or appropriate test module:

```python
import pytest
from src.your_module import your_function

class TestYourFeature:
    """Tests for your feature."""
    
    def test_basic_functionality(self):
        """Test basic functionality."""
        result = your_function("input")
        assert result is not None
        assert result["status"] == "success"
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError):
            your_function("")
```

### 4. Check Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Run tests with coverage
make test-coverage
```

### 5. Create a Pull Request

- Push to your fork: `git push origin feature/awesome-feature`
- Create PR on GitHub with clear description
- Link related issues (if any): `Closes #123`
- Describe what changed and why

**PR template:**

```markdown
## Description
Brief description of changes

## Related Issue
Closes #(issue number)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested this:
- Test A: ...
- Test B: ...

## Checklist
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
```

## 🐛 Bug Reports

If you find a bug:

1. **Check existing issues** — It may already be reported
2. **Create a detailed report** with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment info (OS, Python version, etc.)
   - Relevant code or error messages

Example:

```markdown
## Bug: Agent fails to parse repository with symlinks

**Environment:**
- OS: Windows 10
- Python: 3.11
- Version: 0.2.0

**Steps to reproduce:**
1. Create a repository with symlinked directories
2. Run `python -m src.cli --scan`
3. Error occurs in scanner.py line 45

**Expected:** Scanner should skip symlinks gracefully
**Actual:** ValueError raised

**Error message:**
```
ValueError: Cannot resolve symlink path
```
```

## 📚 Documentation

When adding features, update relevant documentation:

- **Code comments** — Explain WHY, not WHAT
- **Docstrings** — Follow Google/NumPy style
- **README.md** — Update if user-facing
- **docs/** — Add detailed docs if significant feature

## 🚀 Release Process

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create release notes
4. Tag release: `git tag -a v0.3.0 -m "Release 0.3.0"`
5. Push: `git push origin --tags`

## ❓ Questions?

- Check existing issues and discussions
- Read the [main README](../README.md)
- Read the [architecture docs](./ARCHITECTURE.md) (if available)
- Open a discussion on GitHub

## Code of Conduct

- Be respectful and inclusive
- Assume good intent
- Provide constructive feedback
- Welcome diverse perspectives

---

Thank you for contributing! 🙏
