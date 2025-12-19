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

2. **FETCH VERSION COMPATIBILITY**: Query official Wagtail sources for current version support (see **Dynamic Version Detection** section below)
   - Fetch release schedule and compatibility matrix
   - Display detected versions to user
   - Allow user to confirm defaults or specify custom constraints

3. Ask if they want to create files in the current directory (default) or in a `{package_name}/` subdirectory
4. Ask which test framework they prefer: pytest (default) or unittest
5. Ask if they want to include a sandbox development site (default: yes)
6. Gather required variables (see **Input Variables** below)
7. Generate all files using the structures in `references/file-templates.md`
8. Follow the **Generation Workflow** for proper file creation order

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
| `wagtail_min` | No | (dynamic) | Minimum Wagtail version (default: detected oldest LTS from official sources) |
| `django_min` | No | (dynamic) | Minimum Django version (default: minimum for detected oldest LTS) |
| `python_min` | No | (dynamic) | Minimum Python version (default: minimum for detected oldest LTS) |
| `license` | No | `MIT` | License type (default: `MIT`) |
| `include_admin` | No | `true` | Include Wagtail admin integration |
| `include_models` | No | `true` | Include example models |
| `include_blocks` | No | `false` | Include StreamField blocks |
| `include_api` | No | `false` | Include REST API endpoints |
| `test_framework` | No | `pytest` | Testing framework: `pytest` (default) or `unittest` |
| `include_sandbox` | No | `true` | Include sandbox development site (default: `true`) |
| `create_subdirectory` | No | `false` | Create package in `{package_name}/` subdirectory (default: generate in current directory) |

## Dynamic Version Detection

**IMPORTANT**: Execute these steps before collecting user input to ensure current version compatibility data.

### Step 1: Fetch Wagtail Release Schedule

Use the WebFetch tool to retrieve the current release schedule:

- **URL**: https://github.com/wagtail/wagtail/wiki/Release-schedule
- **Prompt**: "Extract the release schedule table showing Version, Release Date, and Security Support end dates. Return as a JSON array with fields: version (string), is_lts (boolean), support_end (date in YYYY-MM-DD format). Only include versions where the Release Date is today or earlier (today is 2025-12-19)."
- Parse the response into structured data
- Filter to keep only versions where `support_end >= today's date`

**Expected output format**:
```json
{
  "versions": [
    {"version": "7.2", "is_lts": false, "support_end": "2026-05-04"},
    {"version": "7.1", "is_lts": false, "support_end": "2026-02-02"},
    {"version": "7.0", "is_lts": true, "support_end": "2026-11-02"}
  ]
}
```

### Step 2: Fetch Wagtail-Django-Python Compatibility Matrix

Use the WebFetch tool to retrieve the compatibility matrix:

- **URL**: https://docs.wagtail.org/en/stable/releases/upgrading.html
- **Prompt**: "Extract the compatibility matrix table showing which Django and Python versions are supported by each Wagtail version. Return as JSON object where keys are Wagtail versions (as strings like '7.0', '7.1', etc.) and values contain arrays of Django versions and Python versions supported by that Wagtail version."
- Parse the response into structured data

**Expected output format**:
```json
{
  "7.2": {
    "django": ["4.2", "5.1", "5.2"],
    "python": ["3.10", "3.11", "3.12", "3.13", "3.14"]
  },
  "7.1": {
    "django": ["4.2", "5.1", "5.2"],
    "python": ["3.9", "3.10", "3.11", "3.12", "3.13"]
  },
  "7.0": {
    "django": ["4.2", "5.1", "5.2"],
    "python": ["3.9", "3.10", "3.11", "3.12", "3.13"]
  }
}
```

### Step 3: Build Complete Version Data Structure

Merge the fetched data from Steps 1 and 2 into a unified structure:

1. Take the currently supported Wagtail versions from Step 1
2. For each version, add its Django and Python compatibility from Step 2
3. Build lists of all unique Django and Python versions across all supported Wagtail versions
4. Structure the data as follows:

```json
{
  "supported_wagtail_versions": [
    {
      "version": "7.0",
      "is_lts": true,
      "support_end": "2026-11-02",
      "django_versions": ["4.2", "5.1", "5.2"],
      "python_versions": ["3.9", "3.10", "3.11", "3.12", "3.13"]
    },
    {
      "version": "7.1",
      "is_lts": false,
      "support_end": "2026-02-02",
      "django_versions": ["4.2", "5.1", "5.2"],
      "python_versions": ["3.9", "3.10", "3.11", "3.12", "3.13"]
    },
    {
      "version": "7.2",
      "is_lts": false,
      "support_end": "2026-05-04",
      "django_versions": ["4.2", "5.1", "5.2"],
      "python_versions": ["3.10", "3.11", "3.12", "3.13", "3.14"]
    }
  ],
  "all_django_versions": ["4.2", "5.1", "5.2"],
  "all_python_versions": ["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"],
  "defaults": {
    "wagtail_min": "7.0",
    "django_min": "4.2",
    "python_min": "3.9"
  }
}
```

**Logic for calculating defaults**:
- `wagtail_min`: Select the **oldest LTS version** from the supported versions list
- `django_min`: Select the minimum Django version supported by the chosen `wagtail_min`
- `python_min`: Select the minimum Python version supported by the chosen `wagtail_min`

### Step 4: Generate Exclusion Rules

Based on the version_data structure, generate exclusion rules for incompatible version combinations:

**Known incompatibilities to check**:
1. **Django-Python incompatibilities**:
   - Django 4.2 only supports Python up to 3.12 (exclude 3.13, 3.14)
   - Django 5.1 may not support Python 3.14 (check compatibility matrix)

2. **Wagtail-Python incompatibilities**:
   - Check each Wagtail version's Python support
   - If a Python version is supported by newer Wagtail but not older, add exclusion
   - Example: Python 3.14 is only in Wagtail 7.2+, so exclude with 7.0 and 7.1

**Generate exclusions array**:
```json
{
  "exclusions": [
    {"python": "3.13", "django": "4.2", "reason": "Django 4.2 max is Python 3.12"},
    {"python": "3.14", "django": "4.2", "reason": "Django 4.2 max is Python 3.12"},
    {"python": "3.14", "wagtail": "7.0", "reason": "Python 3.14 only in Wagtail 7.2+"},
    {"python": "3.14", "wagtail": "7.1", "reason": "Python 3.14 only in Wagtail 7.2+"}
  ]
}
```

Add this to the version_data structure.

### Step 5: Display Version Information to User

Show a clear summary of the detected versions with the option to override:

```
📊 Wagtail Version Compatibility Detected

Currently Supported Wagtail Versions:
  • 7.2 (latest) - supported until May 4, 2026
  • 7.1 - supported until February 2, 2026
  • 7.0 LTS (recommended) - supported until November 2, 2026

Django Versions: 4.2 (LTS), 5.1, 5.2
Python Versions: 3.9, 3.10, 3.11, 3.12, 3.13, 3.14

Recommended Defaults:
  • Minimum Wagtail: 7.0 (oldest LTS for long-term stability)
  • Minimum Django: 4.2 (LTS)
  • Minimum Python: 3.9 (oldest supported by Wagtail 7.0)

ℹ️ These versions will be used in:
  - pyproject.toml dependencies and classifiers
  - tox.ini test matrix (all compatible combinations)
  - GitHub Actions CI (testing across versions)
  - Documentation requirements

Would you like to:
[1] Use recommended defaults
[2] Specify custom version constraints
```

**If user chooses option 1**: Proceed with the detected defaults

**If user chooses option 2**:
- Prompt for custom `wagtail_min`, `django_min`, `python_min`
- Validate against the compatibility matrix
- Warn if specified versions are incompatible or not currently supported
- Update the defaults in version_data

### Step 6: Error Handling

**If WebFetch fails** (network error, timeout, rate limiting):
```
❌ Unable to fetch current version data from official Wagtail sources.
Error: {error_message}

Cannot proceed with package generation without current version compatibility data.

This is likely a temporary network issue. Please try again in a few moments.

If the problem persists:
1. Check your internet connection
2. Verify the Wagtail wiki and docs are accessible:
   - https://github.com/wagtail/wagtail/wiki/Release-schedule
   - https://docs.wagtail.org/en/stable/releases/upgrading.html
3. Try again later when the services are available

Package generation has been aborted.
```

**If parsing fails** (unexpected page format):
```
❌ Successfully fetched data but unable to parse version compatibility information.
The page format may have changed since this skill was last updated.

Cannot proceed with package generation without accurate version data.

Please report this issue at:
https://github.com/wagtail/claude-code-wagtail-package-scaffolder/issues

Include this information:
- Date: {current_date}
- Error: Unable to parse version data
- URLs attempted:
  - https://github.com/wagtail/wagtail/wiki/Release-schedule
  - https://docs.wagtail.org/en/stable/releases/upgrading.html

Package generation has been aborted.
```

**Important**: Do not proceed with package generation if version data cannot be fetched and parsed successfully. Accurate version compatibility information is critical for generating a working package.

## Generation Workflow

**IMPORTANT**:
- By default, generate all files in the **current working directory**. Only create a subdirectory if `create_subdirectory` is `true`.
- **Version-dependent content is GENERATED DYNAMICALLY** based on the fetched version_data structure from the Dynamic Version Detection section.
- For files with "DYNAMIC GENERATION" comments in the templates, follow the generation algorithms provided in `references/file-templates.md`.
- Simple variables (package_name, author_name, etc.) use standard `{variable}` substitution.
- Complex version content (classifiers, tox envlist, GitHub Actions matrix) requires programmatic generation during file creation.
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

## Version Compatibility

Version compatibility is **dynamically detected** at generation time by fetching current data from official Wagtail sources:

- **Release Schedule**: https://github.com/wagtail/wagtail/wiki/Release-schedule
- **Compatibility Matrix**: https://docs.wagtail.org/en/stable/releases/upgrading.html

The skill automatically:
1. Fetches currently supported Wagtail versions
2. Determines compatible Django and Python versions
3. Generates appropriate exclusion rules for test matrices
4. Uses the oldest LTS version as the default minimum

**Note**: Version data is always fetched fresh at generation time to ensure packages support current versions. If version data cannot be fetched, package generation will abort with an error message.

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
