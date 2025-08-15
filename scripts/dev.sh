#!/bin/bash

# Development script for FastAPI Blog API

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install Python 3.8+ first."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_status "Python $PYTHON_VERSION detected"
}

# Check if virtual environment exists
check_venv() {
    if [ ! -d "venv" ]; then
        print_warning "Virtual environment not found. Creating one..."
        python3 -m venv venv
        print_status "Virtual environment created"
    fi
}

# Activate virtual environment
activate_venv() {
    source venv/bin/activate
    print_status "Virtual environment activated"
}

# Install dependencies
install_deps() {
    print_status "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_status "Dependencies installed"
}

# Check environment file
check_env() {
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Creating from template..."
        if [ -f "env.example" ]; then
            cp env.example .env
            print_warning "Please edit .env file with your configuration"
        else
            print_error "env.example not found. Please create .env file manually."
            exit 1
        fi
    fi
}

# Run the application
run_app() {
    print_status "Starting FastAPI application..."
    python -m app.main
}

# Run tests
run_tests() {
    print_status "Running tests..."
    pytest tests/ -v
}

# Format code
format_code() {
    print_status "Formatting code..."
    black app/ tests/
    isort app/ tests/
}

# Lint code
lint_code() {
    print_status "Linting code..."
    flake8 app/ tests/
    mypy app/
}

# Show help
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     - Set up the development environment"
    echo "  run       - Run the application"
    echo "  test      - Run tests"
    echo "  format    - Format code"
    echo "  lint      - Lint code"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup"
    echo "  $0 run"
    echo "  $0 test"
}

# Main script logic
case "${1:-help}" in
    "setup")
        print_status "Setting up development environment..."
        check_python
        check_venv
        activate_venv
        install_deps
        check_env
        print_status "Development environment setup complete!"
        print_status "Run 'source venv/bin/activate' to activate the virtual environment"
        ;;
    "run")
        check_venv
        activate_venv
        check_env
        run_app
        ;;
    "test")
        check_venv
        activate_venv
        run_tests
        ;;
    "format")
        check_venv
        activate_venv
        format_code
        ;;
    "lint")
        check_venv
        activate_venv
        lint_code
        ;;
    "help"|*)
        show_help
        ;;
esac
