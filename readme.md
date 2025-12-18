# wagtail-heelo-world

[![PyPI version](https://badge.fury.io/py/wagtail-heelo-world.svg)](https://badge.fury.io/py/wagtail-heelo-world)
[![Test](https://github.com/nickmoreton/wagtail-heelo-world/actions/workflows/test.yml/badge.svg)](https://github.com/nickmoreton/wagtail-heelo-world/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A hello world package for Wagtail

## Requirements

- Python 3.10+
- Django 4.2+
- Wagtail 7.0+

## Installation

```bash
pip install wagtail-heelo-world
```

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_heelo_world",
    # ...
]
```

## Quick Start

```python
# Example usage - customize this section
from wagtail_heelo_world import ...
```

## Configuration

Add to your Django settings:

```python
# Optional settings with defaults
WAGTAIL_HEELO_WORLD_SETTING = "value"
```

## Documentation

Full documentation is available at [GitHub](https://github.com/nickmoreton/wagtail-heelo-world).

## Development

```bash
# Clone and install
git clone https://github.com/nickmoreton/wagtail-heelo-world.git
cd wagtail-heelo-world
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install

# Run tests
pytest

# Run linting
ruff check src tests
ruff format src tests
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
