.PHONY: help install dev test lint format clean build publish sandbox migrate superuser

help:
	@echo "Available commands:"
	@echo "  make install    - Install the package"
	@echo "  make dev        - Install with dev dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Format code"
	@echo "  make clean      - Remove build artifacts"
	@echo "  make build      - Build package"
	@echo "  make publish    - Publish to PyPI"
	@echo ""
	@echo "Sandbox commands:"
	@echo "  make sandbox    - Run the sandbox development server"
	@echo "  make migrate    - Run sandbox migrations"
	@echo "  make superuser  - Create sandbox superuser"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	ruff check src tests sandbox

format:
	ruff format src tests sandbox
	ruff check --fix src tests sandbox

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean
	python -m build

publish: build
	twine upload dist/*

# Sandbox commands
sandbox:
	cd sandbox && python manage.py runserver

migrate:
	cd sandbox && python manage.py migrate

superuser:
	cd sandbox && python manage.py createsuperuser
