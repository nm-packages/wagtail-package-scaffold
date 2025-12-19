# Wagtail Package Scaffolding Skill

A Claude Code skill for scaffolding production-ready Wagtail packages with modern Python tooling and best practices.

## What This Skill Does

This skill generates a complete, production-ready Wagtail package structure with:

- **Modern Python packaging** - Uses `pyproject.toml` with Flit, following 2024-2025 standards
- **Comprehensive testing** - pytest with full Django/Wagtail integration
- **Code quality tools** - Ruff for linting and formatting, pre-commit hooks
- **CI/CD workflows** - GitHub Actions for testing and PyPI publishing
- **Development sandbox** - Complete Wagtail site for testing your package
- **Documentation** - README, installation guide, configuration docs
- **Version compatibility** - Supports Wagtail 7.0-7.2, Django 4.2/5.1/5.2, Python 3.10-3.14

## Quick Start

### Prerequisites

- Claude Code CLI installed
- This skill installed in your project's `.claude/skills/` directory

### Usage

1. **Navigate to your desired location**:
   ```bash
   cd /path/to/your/workspace
   ```

2. **Ask Claude Code to scaffold a package**:
   ```
   Scaffold a new Wagtail package called wagtail-my-feature
   ```

3. **Answer the prompts**:
   - Package description
   - Author information
   - GitHub username
   - Test framework (pytest or unittest)
   - Whether to create in current directory or subdirectory

4. **Initialize and start developing**:
   ```bash
   # If generated in current directory
   git init
   python -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   pre-commit install

   # Run tests
   pytest

   # Start the sandbox site
   cd sandbox
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

## Generated Package Structure

```
[current directory or package-name/]
├── pyproject.toml              # Modern Python packaging config
├── README.md                   # Package documentation
├── LICENSE                     # MIT License
├── CHANGELOG.md               # Version history
├── MANIFEST.in                # Package manifest
├── .gitignore                 # Git ignore rules
├── .pre-commit-config.yaml    # Code quality hooks
├── tox.ini                    # Local testing matrix
├── Makefile                   # Convenience commands
├── src/                       # Source code (src layout)
│   └── your_package/
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py          # Example Wagtail page model
│       ├── wagtail_hooks.py   # Admin integration
│       ├── templates/
│       └── static/
├── sandbox/                   # Development Wagtail site
│   ├── manage.py
│   ├── sandbox/               # Django settings
│   ├── home/                  # Home app with example page
│   └── templates/
├── tests/                     # Test suite
│   ├── conftest.py
│   ├── settings.py
│   ├── test_models.py
│   └── urls.py
├── .github/
│   └── workflows/
│       ├── test.yml           # CI testing
│       └── publish.yml        # PyPI publishing
└── docs/
    ├── index.md
    ├── installation.md
    └── configuration.md
```

## Features

### Testing Matrix

The generated package includes both **tox** for local testing and **GitHub Actions** for CI:

#### Local Testing with Tox

Test locally across all version combinations:
```bash
# Test all combinations (35 environments)
tox

# Test specific Python version
tox -e py312-django51-wagtail72

# Test all Python 3.12 combinations
tox -e py312

# Test specific Django version across all Python versions
tox -e py{310,311,312,313}-django51-wagtail72
```

#### CI Testing

GitHub Actions workflows automatically test against:
- **Python versions**: 3.10, 3.11, 3.12, 3.13, 3.14
- **Django versions**: 4.2 (LTS), 5.1, 5.2
- **Wagtail versions**: 7.0 (LTS), 7.1, 7.2

**Note**: Test matrix respects compatibility constraints:
- Django 4.2 only supports up to Python 3.12
- Python 3.14 only supported in Wagtail 7.2+

This creates **35 valid test combinations** ensuring comprehensive compatibility.

### Modern Python Standards

- **pyproject.toml only** - No setup.py, setup.cfg, or requirements.txt
- **src layout** - Package code in `src/{module_name}/`
- **Ruff** - Fast linting and formatting (replaces Black, isort, flake8)
- **Testing framework choice** - pytest (default) or Django unittest
- **Flit** - Simple, modern build backend
- **pre-commit** - Automated code quality checks

### Testing Framework Options

Choose between two testing approaches:

**pytest** (default):
- Modern, feature-rich testing framework
- Clean test syntax with fixtures
- Excellent Django integration via pytest-django
- Powerful assertions and detailed output
- Parallel test execution support

**unittest** (Django's built-in):
- Standard Django testing approach
- No additional testing dependencies
- Full Django TestCase features
- Familiar to Django developers
- Built-in coverage support

### Sandbox Development Site

Every package includes a fully functional Wagtail site for testing:
- SQLite database (easy setup)
- Example HomePage model
- Admin access at `/admin/`
- Imports your package from `src/` for live development

## Configuration Options

When scaffolding, you can customize:

| Option | Default | Description |
|--------|---------|-------------|
| **Package name** | Required | PyPI package name (e.g., `wagtail-my-feature`) |
| **Description** | Required | One-line package description |
| **Author info** | Git config | Name and email from git |
| **GitHub username** | Required | For repository URLs |
| **Wagtail version** | 7.0 | Minimum Wagtail version |
| **Django version** | 4.2 | Minimum Django version |
| **Python version** | 3.10 | Minimum Python version |
| **License** | MIT | Package license |
| **Include admin** | Yes | Wagtail admin integration |
| **Include models** | Yes | Example page model |
| **Include blocks** | No | StreamField blocks |
| **Include API** | No | REST API endpoints |
| **Test framework** | pytest | Testing framework: `pytest` or `unittest` |
| **Create subdirectory** | No | Generate in current directory or subdirectory |

## Example Commands

The generated Makefile includes helpful commands:

```bash
make install    # Install the package
make dev        # Install with dev dependencies
make test       # Run tests (current environment)
make test-all   # Run tests across all Python/Django/Wagtail versions (tox)
make lint       # Run linting
make format     # Format code
make sandbox    # Run sandbox development server
make migrate    # Run sandbox migrations
make superuser  # Create sandbox superuser
make build      # Build package for distribution
make publish    # Publish to PyPI
```

## Local Testing with Tox

The generated `tox.ini` includes **35 test environments** matching the CI matrix:

### Available Tox Environments

**Test environments** (format: `py{version}-django{version}-wagtail{version}`):
- `py310-django42-wagtail70` through `py312-django42-wagtail72` (Django 4.2)
- `py310-django51-wagtail70` through `py313-django51-wagtail72` (Django 5.1)
- `py310-django52-wagtail70` through `py314-django52-wagtail72` (Django 5.2)

**Utility environments**:
- `tox -e lint` - Run ruff linting
- `tox -e format` - Format code with ruff
- `tox -e docs` - Build documentation

### Example Usage

```bash
# Run all 35 test environments (requires all Python versions installed)
tox

# Test specific combination
tox -e py312-django51-wagtail72

# Test all Django 4.2 combinations with Python 3.10
tox -e py310-django42-wagtail{70,71,72}

# Run tests for Python 3.12 across all Django/Wagtail versions
tox -e py312

# Parallel testing (faster)
tox -p auto

# Run lint and format checks
tox -e lint,format
```

**Tip**: Use `skip_missing_interpreters = true` in `tox.ini` to skip Python versions you don't have installed locally.

## Development Workflow

1. **Scaffold the package** using this skill
2. **Develop in the sandbox**: Run `make sandbox` and test features in the browser
3. **Write tests**: Add tests in `tests/`
4. **Test locally**: Run `make test` (quick) or `make test-all` (comprehensive with tox)
5. **Customize models**: Extend or replace the example models
6. **Add admin UI**: Customize `wagtail_hooks.py`
7. **Document**: Update README and docs
8. **Publish**: Create a GitHub release to trigger PyPI publishing

## Version Compatibility

The skill follows official compatibility matrices:

**Wagtail Support:**
| Wagtail | Django | Python |
|---------|--------|--------|
| 7.2     | 4.2, 5.1, 5.2 | 3.10-3.14 |
| 7.1     | 4.2, 5.1, 5.2 | 3.9-3.13 |
| 7.0 LTS | 4.2, 5.1, 5.2 | 3.9-3.13 |

**Django Support:**
| Django | Python |
|--------|--------|
| 5.2    | 3.10-3.14 |
| 5.1    | 3.10-3.13 |
| 4.2    | 3.8-3.12 |

## Customizing the Skill

The skill files are located in `.claude/skills/wagtail-package-scaffolder/`:

- **SKILL.md** - Main skill instructions and workflow
- **references/file-templates.md** - All file templates with variable substitution

You can modify these files to:
- Change default versions
- Add custom templates
- Modify the generated structure
- Add your own default settings

## Trigger Phrases

Ask Claude Code to scaffold a package with phrases like:
- "Scaffold a new Wagtail package called wagtail-xyz"
- "Create a Wagtail package for me"
- "New wagtail extension"
- "Generate a reusable Wagtail app"

## Support

For issues or questions:
- Check the generated package's README
- Review the [Wagtail documentation](https://docs.wagtail.org/)
- See the skill source in `.claude/skills/wagtail-package-scaffolder/`

## License

This skill and generated packages default to MIT License. You can change the license during package generation or modify it afterward.

---

**Note**: When you scaffold a new package, this README will be replaced with the generated package's README. The skill files in `.claude/skills/` remain unchanged.
