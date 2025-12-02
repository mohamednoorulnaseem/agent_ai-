.PHONY: help build run stop down logs test lint clean install dev prod format check

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help:
	@echo "$(BLUE)=== AI Agent Framework - Development Commands ===$(NC)"
	@echo ""
	@echo "$(GREEN)Setup & Installation:$(NC)"
	@echo "  make install          Install dependencies"
	@echo "  make install-dev      Install dev dependencies (includes linting, testing)"
	@echo ""
	@echo "$(GREEN)Docker Commands:$(NC)"
	@echo "  make build            Build Docker image"
	@echo "  make run              Start containers (build if needed)"
	@echo "  make stop             Stop running containers"
	@echo "  make down             Stop and remove containers"
	@echo "  make logs             View container logs (live)"
	@echo "  make restart          Restart containers"
	@echo "  make clean-docker     Remove images and volumes"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  make test             Run all tests"
	@echo "  make test-coverage    Run tests with coverage report"
	@echo "  make lint             Run code quality checks (pylint, flake8)"
	@echo "  make format           Format code with black"
	@echo "  make check            Run all checks (lint, format check, type check)"
	@echo ""
	@echo "$(GREEN)Cleanup:$(NC)"
	@echo "  make clean            Remove __pycache__, .pytest_cache, etc."
	@echo "  make clean-all        Deep clean: remove build artifacts, caches, Docker"
	@echo ""

# Installation
install:
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 pylint mypy pre-commit
	@echo "$(GREEN)✓ Development dependencies installed$(NC)"

# Docker commands
build:
	docker compose build
	@echo "$(GREEN)✓ Docker image built$(NC)"

run: build
	docker compose up -d
	@echo "$(GREEN)✓ Containers started$(NC)"
	@echo "$(BLUE)API available at: http://localhost:8000$(NC)"
	@echo "$(BLUE)Swagger UI: http://localhost:8000/docs$(NC)"

stop:
	docker compose stop
	@echo "$(GREEN)✓ Containers stopped$(NC)"

down:
	docker compose down
	@echo "$(GREEN)✓ Containers removed$(NC)"

restart: stop run
	@echo "$(GREEN)✓ Containers restarted$(NC)"

logs:
	docker compose logs -f

clean-docker:
	docker compose down -v
	docker image prune -f
	docker volume prune -f
	@echo "$(GREEN)✓ Docker cleanup complete$(NC)"

# Testing & Quality
test:
	python -m pytest src/tests.py -v
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-coverage:
	python -m pytest src/tests.py -v --cov=src --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated (see htmlcov/index.html)$(NC)"

lint:
	flake8 src/ --max-line-length=100 --ignore=E501,W503
	pylint src/ --disable=C0111,C0103,R0913,R0914
	@echo "$(GREEN)✓ Linting completed$(NC)"

format:
	black src/ --line-length=100
	@echo "$(GREEN)✓ Code formatted$(NC)"

check: lint
	black src/ --check --line-length=100 || (echo "$(YELLOW)Run 'make format' to fix formatting$(NC)" && exit 1)
	@echo "$(GREEN)✓ All checks passed$(NC)"

# Cleanup
clean:
	find src -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find src -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find src -type f -name "*.pyc" -delete
	find src -type f -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	@echo "$(GREEN)✓ Cache and temporary files cleaned$(NC)"

clean-all: clean clean-docker
	rm -rf build/ dist/ src/*.egg-info
	@echo "$(GREEN)✓ Complete cleanup done$(NC)"

# Development shortcuts
dev:
	@echo "$(BLUE)Starting development environment...$(NC)"
	python -m src.api

dev-interactive:
	@echo "$(BLUE)Starting interactive CLI...$(NC)"
	python -m src.cli --interactive

# Additional helpers
status:
	@echo "$(BLUE)Repository Status:$(NC)"
	@git status --short
	@echo ""
	@echo "$(BLUE)Container Status:$(NC)"
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker not running"
