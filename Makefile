.PHONY: help install install-dev test test-cov lint format clean docker-build docker-run docker-stop setup pre-commit install-pre-commit

# Default target
help:
	@echo "Available commands:"
	@echo "  install          - Install production dependencies"
	@echo "  install-dev      - Install development dependencies"
	@echo "  setup            - Setup development environment"
	@echo "  test             - Run tests"
	@echo "  test-cov         - Run tests with coverage"
	@echo "  lint             - Run linting checks"
	@echo "  format           - Format code"
	@echo "  clean            - Clean up generated files"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-run       - Run with Docker Compose"
	@echo "  docker-stop      - Stop Docker Compose services"
	@echo "  pre-commit       - Install pre-commit hooks"
	@echo "  install-pre-commit - Install pre-commit tool"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -e ".[dev]"

# Setup development environment
setup: install-dev pre-commit
	@echo "Development environment setup complete!"

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term-missing

# Run linting checks
lint:
	flake8 app/ tests/
	mypy app/
	bandit -r app/ -f json -o bandit-report.json

# Format code
format:
	black app/ tests/
	isort app/ tests/

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "bandit-report.json" -delete
	rm -rf build/ dist/ .eggs/

# Build Docker image
docker-build:
	docker build -t fastapi-blog-api .

# Run with Docker Compose
docker-run:
	docker-compose up -d

# Stop Docker Compose services
docker-stop:
	docker-compose down

# Install pre-commit tool
install-pre-commit:
	pip install pre-commit

# Install pre-commit hooks
pre-commit: install-pre-commit
	pre-commit install

# Run pre-commit on all files
pre-commit-all:
	pre-commit run --all-files

# Database operations
db-init:
	python -c "from app.core.database import init_db; init_db()"

db-reset: clean
	rm -f *.db
	python -c "from app.core.database import init_db; init_db()"

# Development server
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
prod:
	uvicorn app.main:app --host 0.0.0.0 --port 8000

# Check code quality
check: lint test
	@echo "All checks passed!"

# Prepare for commit
prepare: format lint test
	@echo "Code is ready for commit!"

# Security check
security:
	bandit -r app/ -f json -o bandit-report.json
	safety check

# Update dependencies
update-deps:
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt
	pip install --upgrade -e ".[dev]"

# Show project info
info:
	@echo "FastAPI Blog API"
	@echo "Python version: $(shell python --version)"
	@echo "Pip version: $(shell pip --version)"
	@echo "Project location: $(shell pwd)"
