---
name: wagtail-package-scaffolder
description: "Scaffold production-ready Wagtail/Django packages with modern Python tooling. Use when creating new Wagtail packages, Django reusable apps, or Python packages that integrate with Wagtail CMS. Triggers: 'create wagtail package', 'scaffold django app', 'new wagtail extension', 'reusable wagtail app'."
---

# Wagtail Package Scaffolder

Generate production-ready Wagtail packages following current best practices (2024-2025).

## Quick Start

When the user wants to scaffold a Wagtail package:

1. Ask if they want to create files in the current directory (default) or in a `{package_name}/` subdirectory
2. Ask which test framework they prefer: pytest (default) or unittest
3. Gather required variables (see **Input Variables** below)
4. Generate all files using the structures in `references/file-templates.md`
5. Follow the **Generation Workflow** for proper file creation order

**Default behavior**:
- Generate all files in the current working directory unless user requests a subdirectory
- Use pytest for testing unless user prefers unittest

## Input Variables

Collect these from the user before generating:

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `package_name` | Yes | `wagtail-ai-images` | PyPI package name (lowercase, hyphens) |
| `module_name` | Auto | `wagtail_ai_images` | Python module (derived: replace `-` with `_`) |
| `description` | Yes | `AI-powered image generation for Wagtail` | One-line description |
| `author_name` | Yes | `Jane Developer` | Package author |
| `author_email` | Yes | `jane@example.com` | Author email |
| `github_username` | Yes | `janedeveloper` | For repo URLs |
| `wagtail_min` | No | `7.0` | Minimum Wagtail version (default: `7.0`) |
| `django_min` | No | `4.2` | Minimum Django version (default: `4.2`) |
| `python_min` | No | `3.10` | Minimum Python version (default: `3.10`, supports up to `3.13`) |
| `license` | No | `MIT` | License type (default: `MIT`) |
| `include_admin` | No | `true` | Include Wagtail admin integration |
| `include_models` | No | `true` | Include example models |
| `include_blocks` | No | `false` | Include StreamField blocks |
| `include_api` | No | `false` | Include REST API endpoints |
| `test_framework` | No | `pytest` | Testing framework: `pytest` (default) or `unittest` |
| `create_subdirectory` | No | `false` | Create package in `{package_name}/` subdirectory (default: generate in current directory) |

## Generation Workflow

**IMPORTANT**:
- By default, generate all files in the **current working directory**. Only create a subdirectory if `create_subdirectory` is `true`.
- When generating files with conditional sections (marked with `# CONDITIONAL:`), only include the sections that match the user's `test_framework` choice.

Generate files in this order:

### 1. Project Root Files

Generate in current directory (or `{package_name}/` if `create_subdirectory` is true):

```
[current directory or {package_name}/]
├── pyproject.toml          # ALWAYS first - defines the package
├── README.md
├── LICENSE
├── CHANGELOG.md
├── MANIFEST.in
├── .gitignore
├── .pre-commit-config.yaml
├── tox.ini                 # Local testing matrix
└── Makefile
```

### 2. Sandbox Development Site
```
sandbox/
├── manage.py
├── sandbox/
│   ├── __init__.py
│   ├── settings.py         # Full Django/Wagtail settings
│   ├── urls.py
│   └── wsgi.py
├── home/
│   ├── __init__.py
│   ├── models.py           # Basic HomePage model
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── templates/home/home_page.html
└── templates/
    └── base.html
```

The sandbox is a minimal but complete Wagtail site that:
- Imports the package being developed from `src/`
- Runs with SQLite for simplicity
- Includes a basic home app with a HomePage model
- Can be extended to test all package features

### 3. Source Package
```
src/{module_name}/
├── __init__.py             # Version and default_app_config
├── apps.py                 # Django AppConfig
├── wagtail_hooks.py        # Wagtail hooks (if include_admin)
├── models.py               # Models (if include_models)
├── blocks.py               # StreamField blocks (if include_blocks)
├── views.py                # Views (if include_api)
├── urls.py                 # URL routing (if include_api)
├── templates/{module_name}/
│   └── .gitkeep
└── static/{module_name}/
    └── .gitkeep
```

### 4. Test Infrastructure
```
tests/
├── __init__.py
├── conftest.py             # pytest fixtures
├── settings.py             # Django test settings
├── test_models.py          # Model tests (if include_models)
└── urls.py                 # Test URL config
```

### 5. CI/CD & Docs
```
.github/
├── workflows/
│   ├── test.yml            # Run tests on PR
│   └── publish.yml         # Publish to PyPI on release
└── ISSUE_TEMPLATE/
    └── bug_report.md

docs/
├── index.md
├── installation.md
└── configuration.md
```

## File Templates

**MANDATORY**: Read `references/file-templates.md` completely before generating any files. It contains exact templates for every file with proper variable substitution.

## Modern Python Standards

This skill follows 2024-2025 best practices:

- **pyproject.toml only** - No setup.py, setup.cfg, or requirements.txt
- **src layout** - Package code in `src/{module_name}/`
- **Ruff** - For linting AND formatting (replaces Black, isort, flake8)
- **pytest** - With pytest-django for testing
- **GitHub Actions** - For CI/CD
- **pre-commit** - For code quality hooks

## Version Compatibility Matrix

Official compatibility constraints:

**Wagtail Support:**
| Wagtail | Django | Python |
|---------|--------|--------|
| 7.2     | 4.2, 5.1, 5.2 | 3.10, 3.11, 3.12, 3.13, 3.14 |
| 7.1     | 4.2, 5.1, 5.2 | 3.9, 3.10, 3.11, 3.12, 3.13 |
| 7.0 LTS | 4.2, 5.1, 5.2 | 3.9, 3.10, 3.11, 3.12, 3.13 |

**Django Support:**
| Django | Python |
|--------|--------|
| 5.2    | 3.10, 3.11, 3.12, 3.13, 3.14 |
| 5.1    | 3.10, 3.11, 3.12, 3.13 |
| 4.2    | 3.8, 3.9, 3.10, 3.11, 3.12 |

**Important:** Django 4.2 only supports up to Python 3.12. Tests exclude Python 3.13/3.14 with Django 4.2.

## Post-Generation Instructions

After generating all files, provide the user with instructions based on whether a subdirectory was created:

**If files were generated in current directory (create_subdirectory=false):**
```bash
# Initialize git and install
git init
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pre-commit install

# Run tests
pytest

# Run the sandbox site
cd sandbox
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000/admin/ to access Wagtail admin
```

**If files were generated in subdirectory (create_subdirectory=true):**
```bash
# Navigate to package and initialize
cd {package_name}
git init
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pre-commit install

# Run tests
pytest

# Run the sandbox site
cd sandbox
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000/admin/ to access Wagtail admin
```

## Customization Points

Tell the user where to customize:

1. **Add models**: `src/{module_name}/models.py`
2. **Add admin UI**: `src/{module_name}/wagtail_hooks.py`
3. **Add blocks**: `src/{module_name}/blocks.py`
4. **Add templates**: `src/{module_name}/templates/{module_name}/`
5. **Configure settings**: Document in `README.md` and `docs/configuration.md`
