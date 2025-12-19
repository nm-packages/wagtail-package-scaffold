---
name: wagtail-package-scaffolder
description: "Scaffold production-ready Wagtail/Django packages with modern Python tooling. Use when creating new Wagtail packages, Django reusable apps, or Python packages that integrate with Wagtail CMS. Triggers: 'create wagtail package', 'scaffold django app', 'new wagtail extension', 'reusable wagtail app'."
---

# Wagtail Package Scaffolder

Generate production-ready Wagtail packages following current best practices (2024-2025).

## Quick Start

When the user wants to scaffold a Wagtail package:

1. **GUARDRAIL CHECK**: Verify the directory is clean before proceeding
   - Check if any files exist besides: `.claude/`, `claude_code_install.md`, `readme.md` (case-insensitive)
   - If other files exist, abort with an error message: "The directory contains existing files. This skill only works in a clean directory with just the .claude folder and optional readme.md/claude_code_install.md files. Please run this skill in an empty directory or a new subdirectory."
   - Only proceed if the directory is clean

2. Ask if they want to create files in the current directory (default) or in a `{package_name}/` subdirectory
3. Ask which test framework they prefer: pytest (default) or unittest
4. Ask if they want to include a sandbox development site (default: yes)
5. Gather required variables (see **Input Variables** below)
6. Generate all files using the structures in `references/file-templates.md`
7. Follow the **Generation Workflow** for proper file creation order

**Default behavior**:
- Generate all files in the current working directory unless user requests a subdirectory
- Use pytest for testing unless user prefers unittest
- Include sandbox development site unless user opts out

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
| `include_sandbox` | No | `true` | Include sandbox development site (default: `true`) |
| `create_subdirectory` | No | `false` | Create package in `{package_name}/` subdirectory (default: generate in current directory) |

## Generation Workflow

**IMPORTANT**:
- By default, generate all files in the **current working directory**. Only create a subdirectory if `create_subdirectory` is `true`.
- When generating files with conditional sections (marked with `# CONDITIONAL:`), only include the sections that match the user's `test_framework` choice.
- If `include_sandbox` is `false`, skip the entire sandbox generation section (section 2) and omit sandbox-related commands from the Makefile (sandbox, migrate, superuser targets).

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
├── test_manage.py          # Django management wrapper for tests
├── .gitignore
├── .pre-commit-config.yaml
├── tox.ini                 # Local testing matrix
└── Makefile
```

### 2. Sandbox Development Site (if include_sandbox is true)

**IMPORTANT**: The sandbox is generated using the official `wagtail start` command.

To generate the sandbox:

1. **Create and activate a temporary virtual environment** for running the wagtail command:
   ```bash
   python -m venv .venv-temp
   source .venv-temp/bin/activate  # or .venv-temp\Scripts\activate on Windows
   ```

2. **Install Wagtail** in the temporary environment:
   ```bash
   pip install wagtail
   ```

3. **Run the wagtail start command**:
   ```bash
   wagtail start sandbox
   ```

4. **Deactivate and remove the temporary environment**:
   ```bash
   deactivate
   rm -rf .venv-temp
   ```

The `wagtail start sandbox` command creates a complete Wagtail site structure with:
- Full Django/Wagtail settings
- A home app with a basic HomePage model
- All necessary configuration files
- Template structure
- Migrations

**Post-generation modifications**:
After running `wagtail start sandbox`, you MUST make the following modifications:

1. **Remove unnecessary files** created by `wagtail start`:
   - Delete `.dockerignore` (if exists)
   - Delete `Dockerfile` (if exists)
   - Delete `requirements.txt` (if exists)

   These files are not needed since the package uses `pyproject.toml` for dependency management and doesn't require Docker configuration.

2. **Consolidate settings files** (if `wagtail start` created multiple settings files):
   - If `sandbox/sandbox/settings/` directory exists with `base.py`, `dev.py`, and `production.py`:
     - Copy any development-specific settings from `dev.py` into `base.py`
     - Remove `dev.py` and `production.py`
     - Rename `settings/base.py` to `settings.py` in the `sandbox/sandbox/` directory
     - Remove the now-empty `settings/` directory
   - Ensure `DEBUG = True` is set in the settings file for easy development

3. **Update the settings file** (`sandbox/sandbox/settings.py`) to integrate the package:

   a. Add the src directory to the Python path (add after the BASE_DIR/PROJECT_DIR definitions):
   ```python
   import sys
   PROJECT_DIR = BASE_DIR.parent
   sys.path.insert(0, str(PROJECT_DIR / "src"))
   ```

   b. Add the package to INSTALLED_APPS. Insert `"{module_name}"` in the INSTALLED_APPS list after "home" and before the Wagtail apps:
   ```python
   INSTALLED_APPS = [
       # Local apps
       "home",
       # The package being developed
       "{module_name}",
       # Wagtail apps
       "wagtail.contrib.forms",
       # ... rest of Wagtail apps
   ```

**Note**: Only generate the sandbox if `include_sandbox` is `true`. If the user opts out, skip this entire section.

### 3. Source Package
```
src/{module_name}/
├── __init__.py             # Version and default_app_config
├── apps.py                 # Django AppConfig
├── models.py               # Models (empty placeholder)
├── views.py                # Views (empty placeholder)
├── wagtail_hooks.py        # Wagtail hooks (empty placeholder)
├── blocks.py               # StreamField blocks (if include_blocks)
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
├── test_models.py          # Placeholder model tests
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
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pre-commit install

# Run tests
{test_command}  # pytest or python test_manage.py test depending on test_framework
```

**If sandbox was included, also tell the user:**
```bash
# To run the sandbox development server:
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
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pre-commit install

# Run tests
{test_command}  # pytest or python test_manage.py test depending on test_framework
```

**If sandbox was included, also tell the user:**
```bash
# To run the sandbox development server:
cd sandbox
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# Visit http://localhost:8000/admin/ to access Wagtail admin
```

## Cleanup Scaffolding Files

After providing all post-generation instructions, inform the user about cleanup:

**IMPORTANT**: Use the AskUserQuestion tool to ask the user if they want to remove the scaffolding files.

Tell the user:
"Now that your package is scaffolded, the following files/folders are no longer needed for developing or using the package:
- `.claude/` - Contains the scaffolding skill (no longer needed)
- `claude_code_install.md` - Claude Code installation instructions (no longer needed)

Would you like me to remove these files to keep your package clean?"

If the user agrees (answers yes):
1. Remove the `.claude/` directory and all its contents
2. Remove the `claude_code_install.md` file (if it exists)
3. Confirm the removal with a brief message

If the user declines:
1. Acknowledge their choice
2. Remind them they can manually delete these files anytime with:
   ```bash
   rm -rf .claude
   rm -f claude_code_install.md
   ```

## Customization Points

Tell the user where to customize:

1. **Add models**: `src/{module_name}/models.py` (empty placeholder ready for your models)
2. **Add views**: `src/{module_name}/views.py` (empty placeholder ready for your views)
3. **Add Wagtail hooks**: `src/{module_name}/wagtail_hooks.py` (empty placeholder ready for your hooks)
4. **Add blocks**: `src/{module_name}/blocks.py` (if `include_blocks` is enabled)
5. **Add templates**: `src/{module_name}/templates/{module_name}/`
6. **Configure settings**: Document in `README.md` and `docs/configuration.md`
