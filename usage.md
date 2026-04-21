# Wagtail Package Scaffolder

## Quick Install

Install the skill into the project-local skill directory for your coding agent.

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

For Codex, verify the structure looks like:

```text
your-project/
└── .codex/
    └── skills/
        └── wagtail-package-scaffolder/
            ├── SKILL.md
            └── references/
                └── file-templates.md
```

For Claude Code, verify the structure looks like:

```text
your-project/
└── .claude/
    └── skills/
        └── wagtail-package-scaffolder/
            ├── SKILL.md
            └── references/
                └── file-templates.md
```

Use it by asking your coding agent:

- "Scaffold a new Wagtail package called wagtail-hello-world"
- "Create a Wagtail package for me"
- "New wagtail extension"

Depending on your prompt content, the agent will guide you through the full process. For example, if you do not specify a package name it will ask for one.

## Manual Install

If you prefer, copy the files manually into your agent's project-local skill directory.

For Codex:

```bash
# From your project root
mkdir -p .codex/skills/wagtail-package-scaffolder/references

# Copy the files, adjusting source paths as needed
cp SKILL.md .codex/skills/wagtail-package-scaffolder/
cp file-templates.md .codex/skills/wagtail-package-scaffolder/references/
```

For Claude Code:

```bash
# From your project root
mkdir -p .claude/skills/wagtail-package-scaffolder/references

# Copy the files, adjusting source paths as needed
cp SKILL.md .claude/skills/wagtail-package-scaffolder/
cp file-templates.md .claude/skills/wagtail-package-scaffolder/references/
```

## How It Works

When you ask an agent to scaffold a Wagtail package, it will:

1. **Read the skill** from the project-local skill directory:
   - Codex: `.codex/skills/wagtail-package-scaffolder/`
   - Claude Code: `.claude/skills/wagtail-package-scaffolder/`
2. **Read SKILL.md** for the workflow
3. **Fetch current version compatibility** from official Wagtail sources:
   - Release schedule from GitHub wiki
   - Compatibility matrix from Wagtail docs
   - Determines supported Wagtail, Django, and Python versions
4. **Display detected versions** and ask whether to use the recommended defaults or customize them
5. **Ask for each missing package value one at a time**, always showing a default answer
6. **Read the templates** from `references/file-templates.md`
7. **Generate all files dynamically** with:
   - Your values substituted
   - Current version compatibility in dependencies
   - Test matrices for all supported version combinations
   - Appropriate classifiers for PyPI

## Example Usage

```text
You: Create a wagtail package called wagtail-ai-assistant

Agent: I'll scaffold a Wagtail package for you. Let me first fetch
current Wagtail version compatibility data...

Wagtail Version Compatibility Detected

Currently Supported Wagtail Versions:
  - [latest version] - supported until [date]
  - [version] - supported until [date]
  - [LTS version] (recommended) - supported until [date]

Django Versions: [LTS], [current versions]
Python Versions: [supported versions]

Recommended Defaults:
  - Minimum Wagtail: [oldest LTS for long-term stability]
  - Minimum Django: [LTS version]
  - Minimum Python: [oldest supported by LTS Wagtail]

Would you like to:
[1] Use recommended defaults (default)
[2] Specify custom version constraints

You: 1

Agent: Description [default: A reusable Wagtail package]?

You: AI-powered assistant for Wagtail CMS

Agent: Author name [default: Jane Developer]?

You: use default

Agent: Author email [default: jane@example.com]?

You: jane@example.com

Agent: GitHub username [default: janedeveloper]?

You: janedeveloper

Agent: License [default: MIT]?

You: use default

Agent: Output location [default: current directory]?

You: use default

Agent: Test framework [default: pytest]?

You: use default

Agent: Include a sandbox development site [default: yes]?

You: use default

Agent: Include Wagtail admin integration [default: yes]?

You: use default

Agent: Include example models [default: yes]?

You: use default

Agent: Include StreamField blocks [default: no]?

You: use default

Agent: Include REST API endpoints [default: no]?

You: use default

[The agent generates all files with current version data]
```

## What Gets Generated

The skill creates a complete, production-ready package:

### Package Structure

- `pyproject.toml` - Modern Python packaging with dynamic version classifiers
- `src/{module_name}/` - Source code in src layout
- `tests/` - Test infrastructure (pytest or unittest)
- `sandbox/` - Full Wagtail development site (optional)
- `.github/workflows/` - CI/CD with version matrix testing
- `tox.ini` - Local testing across all supported version combinations
- `docs/` - Documentation structure
- `Makefile` - Development commands
- Pre-commit hooks and linting configuration

### Version-Smart Features

- **Test matrices** automatically include all valid Python/Django/Wagtail combinations
- **Exclusion rules** prevent testing incompatible version combinations
- **PyPI classifiers** list all currently supported framework versions
- **Dependencies** specify minimum versions based on oldest LTS

## Customizing

Edit the installed files in `.codex/skills/wagtail-package-scaffolder/` or `.claude/skills/wagtail-package-scaffolder/` to:

- Add your default author info to prompts
- Modify file templates
- Add/remove generated files
- Change project structure

Version requirements are fetched dynamically from official Wagtail sources at generation time. This ensures generated packages always support current Wagtail versions without manual updates to the skill.

## Requirements

- An AI coding agent with shell and file access
- Internet connection for version detection

## Learn More

- Skill configuration: `.codex/skills/wagtail-package-scaffolder/SKILL.md` or `.claude/skills/wagtail-package-scaffolder/SKILL.md`
- File templates: `.codex/skills/wagtail-package-scaffolder/references/file-templates.md` or `.claude/skills/wagtail-package-scaffolder/references/file-templates.md`
- Wagtail docs: https://docs.wagtail.org
