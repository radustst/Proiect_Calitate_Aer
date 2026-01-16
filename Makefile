.PHONY: install install-dev test lint format clean run train help

# Default target
help:
	@echo "Available commands:"
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linting checks"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Remove cache and build files"
	@echo "  make run          - Run the Streamlit application"
	@echo "  make train        - Train the ML model"
	@echo "  make all          - Install, lint, test, and run"

# Install production dependencies
install:
	pip install -e .

# Install development dependencies
install-dev:
	pip install -e ".[dev]"
	pre-commit install

# Run tests with coverage
test:
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# Run linting checks
lint:
	flake8 src/ tests/
	mypy src/
	black --check src/ tests/
	isort --check-only src/ tests/

# Format code
format:
	black src/ tests/
	isort src/ tests/

# Clean cache and build files
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Run the Streamlit application
run:
	streamlit run src/app.py

# Train the ML model
train:
	python src/model.py

# Run everything
all: install-dev lint test run
