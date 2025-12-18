# File Templates Reference

Complete templates for all generated files. Substitute variables using `{variable_name}` syntax.

---

## pyproject.toml

```toml
[build-system]
requires = ["flit_core>=3.4,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "{package_name}"
version = "0.1.0"
description = "{description}"
readme = "README.md"
license = {{ file = "LICENSE" }}
authors = [
    {{ name = "{author_name}", email = "{author_email}" }}
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Framework :: Django :: {django_min}",
    "Framework :: Wagtail",
    "Framework :: Wagtail :: {wagtail_min[0]}",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: {license} License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: {python_min}",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
]
requires-python = ">={python_min}"
dependencies = [
    "Django>={django_min}",
    "wagtail>={wagtail_min}",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.5",
    "pytest-cov>=4.0",
    "ruff>=0.4",
    "pre-commit>=3.5",
    "build>=1.0",
    "twine>=5.0",
]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.0",
]

[project.urls]
Homepage = "https://github.com/{github_username}/{package_name}"
Documentation = "https://github.com/{github_username}/{package_name}#readme"
Repository = "https://github.com/{github_username}/{package_name}.git"
Changelog = "https://github.com/{github_username}/{package_name}/blob/main/CHANGELOG.md"
Issues = "https://github.com/{github_username}/{package_name}/issues"

[tool.flit.module]
name = "{module_name}"

[tool.flit.sdist]
include = [
    "CHANGELOG.md",
    "LICENSE",
]
exclude = [
    ".*",
    "tests/",
    "docs/",
]

[tool.ruff]
target-version = "py{python_min_nodot}"
line-length = 88
src = ["src"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "DJ",     # flake8-django
]
ignore = [
    "E501",   # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["{module_name}"]
known-third-party = ["django", "wagtail"]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "tests.settings"
python_files = ["test_*.py"]
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["src/{module_name}"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
]
```

---

## README.md

```markdown
# {package_name}

[![PyPI version](https://badge.fury.io/py/{package_name}.svg)](https://badge.fury.io/py/{package_name})
[![Test](https://github.com/{github_username}/{package_name}/actions/workflows/test.yml/badge.svg)](https://github.com/{github_username}/{package_name}/actions/workflows/test.yml)
[![License: {license}](https://img.shields.io/badge/License-{license}-blue.svg)](LICENSE)

{description}

## Requirements

- Python {python_min}+
- Django {django_min}+
- Wagtail {wagtail_min}+

## Installation

```bash
pip install {package_name}
```

Add to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "{module_name}",
    # ...
]
```

## Quick Start

```python
# Example usage - customize this section
from {module_name} import ...
```

## Configuration

Add to your Django settings:

```python
# Optional settings with defaults
{module_name_upper}_SETTING = "value"
```

## Documentation

Full documentation is available at [GitHub]({https://github.com/{github_username}/{package_name}}).

## Development

```bash
# Clone and install
git clone https://github.com/{github_username}/{package_name}.git
cd {package_name}
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

This project is licensed under the {license} License - see the [LICENSE](LICENSE) file for details.
```

---

## src/{module_name}/__init__.py

```python
"""
{description}
"""

__version__ = "0.1.0"

default_app_config = "{module_name}.apps.{module_name_camel}Config"
```

---

## src/{module_name}/apps.py

```python
from django.apps import AppConfig


class {module_name_camel}Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{module_name}"
    label = "{module_name}"
    verbose_name = "{package_title}"

    def ready(self):
        pass  # Import signals here if needed
```

---

## src/{module_name}/models.py (if include_models)

```python
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class {module_name_camel}Page(Page):
    """
    Example page model - customize or replace as needed.
    """

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "{package_title} Page"
        verbose_name_plural = "{package_title} Pages"
```

---

## src/{module_name}/wagtail_hooks.py (if include_admin)

```python
from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_menu_item():
    return MenuItem(
        "{package_title}",
        "/admin/{module_name}/",
        icon_name="cog",
        order=10000,
    )


# Uncomment to add custom admin URLs
# @hooks.register("register_admin_urls")
# def register_admin_urls():
#     from django.urls import path
#     from . import views
#     return [
#         path("{module_name}/", views.index, name="{module_name}_index"),
#     ]
```

---

## src/{module_name}/blocks.py (if include_blocks)

```python
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class {module_name_camel}Block(blocks.StructBlock):
    """
    Example StreamField block - customize as needed.
    """

    title = blocks.CharBlock(required=True, max_length=255)
    text = blocks.RichTextBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        template = "{module_name}/blocks/{module_name}_block.html"
        icon = "placeholder"
        label = "{package_title} Block"
```

---

## src/{module_name}/views.py (if include_api)

```python
from django.http import JsonResponse
from django.views import View


class {module_name_camel}APIView(View):
    """
    Example API view - customize as needed.
    """

    def get(self, request):
        return JsonResponse({{"status": "ok", "data": []}})
```

---

## src/{module_name}/urls.py (if include_api)

```python
from django.urls import path

from . import views

app_name = "{module_name}"

urlpatterns = [
    path("api/", views.{module_name_camel}APIView.as_view(), name="api"),
]
```

---

## Sandbox Development Site

The sandbox is a complete Wagtail site for developing and testing the package locally.

### sandbox/manage.py

```python
#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sandbox.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
```

---

### sandbox/sandbox/__init__.py

```python
# Sandbox Wagtail site for {package_name} development
```

---

### sandbox/sandbox/settings.py

```python
import os
import sys
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent

# Add the src directory to the path so the package can be imported
sys.path.insert(0, str(PROJECT_DIR / "src"))

SECRET_KEY = "sandbox-secret-key-not-for-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # Local apps
    "home",
    # The package being developed
    "{module_name}",
    # Wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "sandbox.urls"

TEMPLATES = [
    {{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {{
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        }},
    }},
]

WSGI_APPLICATION = "sandbox.wsgi.application"

DATABASES = {{
    "default": {{
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }}
}}

AUTH_PASSWORD_VALIDATORS = []  # Disabled for development convenience

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Wagtail settings
WAGTAIL_SITE_NAME = "{package_title} Sandbox"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# Search backend (simple database backend for development)
WAGTAILSEARCH_BACKENDS = {{
    "default": {{
        "BACKEND": "wagtail.search.backends.database",
    }}
}}
```

---

### sandbox/sandbox/urls.py

```python
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]

# Include package URLs if they exist
try:
    from {module_name} import urls as package_urls
    urlpatterns.append(path("{module_name}/", include(package_urls)))
except ImportError:
    pass

# Wagtail catch-all (must be last)
urlpatterns.append(path("", include(wagtail_urls)))

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

### sandbox/sandbox/wsgi.py

```python
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sandbox.settings")

application = get_wsgi_application()
```

---

### sandbox/home/__init__.py

```python
# Home app for sandbox site
```

---

### sandbox/home/models.py

```python
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    """
    The home page for the sandbox site.
    Extend this to test your package features.
    """

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    # Restrict what pages can be created under home
    # subpage_types = []  # Uncomment to restrict child pages

    class Meta:
        verbose_name = "Home Page"
```

---

### sandbox/home/migrations/__init__.py

```python
```

---

### sandbox/home/migrations/0001_initial.py

```python
from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0094_alter_page_locale"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomePage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("body", wagtail.fields.RichTextField(blank=True)),
            ],
            options={{
                "verbose_name": "Home Page",
            }},
            bases=("wagtailcore.page",),
        ),
    ]
```

---

### sandbox/home/templates/home/home_page.html

```html
{{% extends "base.html" %}}
{{% load wagtailcore_tags %}}

{{% block content %}}
<article>
    <h1>{{{{ page.title }}}}</h1>

    <div class="intro">
        {{{{ page.body|richtext }}}}
    </div>

    <hr>

    <section class="package-test">
        <h2>Test {package_title}</h2>
        <p>
            This sandbox site is for developing and testing the
            <strong>{package_name}</strong> package.
        </p>
        <p>
            Edit this template at
            <code>sandbox/home/templates/home/home_page.html</code>
            to add package-specific test content.
        </p>
    </section>
</article>
{{% endblock %}}
```

---

### sandbox/templates/base.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{% block title %}}{{{{ page.title }}}} | {package_title} Sandbox{{% endblock %}}</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            color: #333;
        }}
        h1, h2, h3 {{ color: #1a1a1a; }}
        a {{ color: #007bff; }}
        code {{
            background: #f4f4f4;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-size: 0.9em;
        }}
        .intro {{ font-size: 1.1em; color: #555; }}
        hr {{ border: none; border-top: 1px solid #eee; margin: 2rem 0; }}
        .package-test {{
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }}
    </style>
    {{% block extra_css %}}{{% endblock %}}
</head>
<body>
    <nav>
        <a href="/">Home</a> |
        <a href="/admin/">Wagtail Admin</a>
    </nav>

    <main>
        {{% block content %}}{{% endblock %}}
    </main>

    <footer style="margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #eee; color: #666;">
        <p>{package_title} Sandbox &mdash; Development Environment</p>
    </footer>

    {{% block extra_js %}}{{% endblock %}}
</body>
</html>
```

---

## tests/conftest.py

```python
import pytest
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {{
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }}


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {{
        "title": "Test Title",
        "body": "<p>Test content</p>",
    }}
```

---

## tests/settings.py

```python
SECRET_KEY = "test-secret-key-not-for-production"
DEBUG = True

DATABASES = {{
    "default": {{
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }}
}}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    # The package being tested
    "{module_name}",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {{
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {{
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        }},
    }},
]

STATIC_URL = "/static/"
WAGTAIL_SITE_NAME = "Test Site"
WAGTAILADMIN_BASE_URL = "http://localhost:8000"
```

---

## tests/urls.py

```python
from django.urls import include, path
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path("admin/", include(wagtailadmin_urls)),
    path("", include(wagtail_urls)),
]

# Include package URLs if they exist
try:
    from {module_name} import urls as package_urls
    urlpatterns.insert(0, path("{module_name}/", include(package_urls)))
except ImportError:
    pass
```

---

## tests/test_models.py (if include_models)

```python
import pytest
from django.test import TestCase
from wagtail.models import Page

from {module_name}.models import {module_name_camel}Page


@pytest.mark.django_db
class Test{module_name_camel}Page:
    def test_can_create_page(self, django_db_setup):
        """Test that the page model can be instantiated."""
        page = {module_name_camel}Page(
            title="Test Page",
            slug="test-page",
            body="<p>Test content</p>",
        )
        assert page.title == "Test Page"
        assert page.body == "<p>Test content</p>"

    def test_page_verbose_name(self):
        """Test the model's verbose name."""
        assert {module_name_camel}Page._meta.verbose_name == "{package_title} Page"
```

---

## .github/workflows/test.yml

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["{python_min}", "3.11", "3.12"]
        django-version: ["{django_min}", "5.0"]
        wagtail-version: ["{wagtail_min}", "6.3"]
        exclude:
          # Add version exclusions as needed
          - django-version: "5.0"
            wagtail-version: "5.2"

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{{{ matrix.python-version }}}}
        uses: actions/setup-python@v5
        with:
          python-version: ${{{{ matrix.python-version }}}}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install Django~=${{{{ matrix.django-version }}}}.0
          pip install wagtail~=${{{{ matrix.wagtail-version }}}}.0
          pip install -e ".[dev]"

      - name: Run tests
        run: pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '{python_min}' && matrix.django-version == '{django_min}'
```

---

## .github/workflows/publish.yml

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write  # For trusted publishing

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "{python_min}"

      - name: Install build tools
        run: pip install build

      - name: Build package
        run: python -m build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

---

## .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.10
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

---

## .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
ENV/

# Testing
.tox/
.nox/
.coverage
.coverage.*
htmlcov/
.pytest_cache/
.hypothesis/

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Django / Sandbox
*.log
local_settings.py
db.sqlite3
sandbox/db.sqlite3
sandbox/media/
sandbox/staticfiles/

# Distribution
*.tar.gz
*.whl
```

---

## LICENSE (MIT example)

```text
MIT License

Copyright (c) {year} {author_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - {date}

### Added
- Initial release
- Basic package structure
- Core functionality
```

---

## MANIFEST.in

```text
include LICENSE
include README.md
include CHANGELOG.md
recursive-include src/{module_name}/templates *
recursive-include src/{module_name}/static *
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

---

## Makefile

```makefile
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
	find . -type d -name __pycache__ -exec rm -rf {{}} +

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
```

---

## Variable Transformation Rules

When applying templates, transform variables as follows:

| Source | Transformation | Example |
|--------|----------------|---------|
| `{package_name}` | As-is | `wagtail-ai-images` |
| `{module_name}` | Replace `-` with `_` | `wagtail_ai_images` |
| `{module_name_camel}` | PascalCase | `WagtailAiImages` |
| `{module_name_upper}` | SCREAMING_SNAKE | `WAGTAIL_AI_IMAGES` |
| `{package_title}` | Title Case | `Wagtail AI Images` |
| `{python_min_nodot}` | Remove dot | `310` |
| `{wagtail_min[0]}` | Major version | `6` |
| `{year}` | Current year | `2025` |
| `{date}` | YYYY-MM-DD | `2025-01-15` |
