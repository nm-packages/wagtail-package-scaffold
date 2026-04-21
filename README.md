# Wagtail Package Scaffolder

An agent-agnostic scaffolding skill that generates production-ready Wagtail packages with live version detection and deterministic rendering.

## Features

- **Live version detection** - Automatically fetches current Wagtail/Django/Python compatibility from official sources
- **Deterministic rendering** - Produces stable output for identical inputs, fetched version data, current date, and selected options
- **Complete package structure** - Modern Python packaging with src layout
- **Test matrices** - tox.ini and GitHub Actions configured for all supported version combinations
- **Optional sandbox** - Full Wagtail development site for testing
- **Zero maintenance** - Version data updates automatically at generation time

## Installation

**Security Note**: Before running any installation script, review what it does:
```bash
curl https://raw.githubusercontent.com/nm-packages/wagtail-package-scaffold/main/install.sh | less
```

In your new empty folder where you want to generate a package, install the skill for your coding agent.

For Codex:

```bash
curl -sSL https://raw.githubusercontent.com/nm-packages/wagtail-package-scaffold/main/install.sh | bash -s -- --agent codex
```

For Claude Code:

```bash
curl -sSL https://raw.githubusercontent.com/nm-packages/wagtail-package-scaffold/main/install.sh | bash -s -- --agent claude
```

To install into a specific target folder:

```bash
curl -sSL https://raw.githubusercontent.com/nm-packages/wagtail-package-scaffold/main/install.sh | bash -s -- --agent codex --target ./my-new-package
```

Once installed, ask your coding agent:
```
Create a Wagtail package called wagtail-hello-world
```

The skill is installed into the project-local skill directory for your agent:

- Codex: `.codex/skills/wagtail-package-scaffolder/`
- Claude Code: `.claude/skills/wagtail-package-scaffolder/`

The skill can be removed after it generates the package files.

## Usage

The skill will:
1. Fetch current Wagtail version compatibility
2. Show you detected versions and defaults
3. Ask for each missing package value one at a time, always showing a default answer
4. Generate all files with deterministic ordering, normalized formatting, and proper version support

For identical user inputs, identical fetched version data, the same current date, and the same selected options, the generated output is intended to be byte-for-byte stable.

## Requirements

- An AI coding agent with shell and file access
- Internet connection (for version detection)

## What Gets Generated

- Modern `pyproject.toml` with live version classifiers rendered in stable order
- Complete source structure in `src/` layout
- Test infrastructure (pytest or unittest)
- GitHub Actions CI/CD with version matrix
- `tox.ini` for local testing across Python/Django/Wagtail versions
- Optional Wagtail sandbox site
- Pre-commit hooks and development tools

## Learn More

See [`usage.md`](usage.md) for detailed documentation.
