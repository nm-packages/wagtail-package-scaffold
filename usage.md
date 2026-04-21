# Wagtail Package Scaffolder

## Quick Install

The `skills` folder is already installed in this project. Verify the structure looks like:

```text
your-project/
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

If you prefer, copy the files manually:

```bash
# From your project root
mkdir -p skills/wagtail-package-scaffolder/references

# Copy the files, adjusting source paths as needed
cp SKILL.md skills/wagtail-package-scaffolder/
cp file-templates.md skills/wagtail-package-scaffolder/references/
```

For tools that require a vendor-specific skill directory, copy `skills/wagtail-package-scaffolder/` into that tool's expected skill location.

## How It Works

When you ask an agent to scaffold a Wagtail package, it will:

1. **Read the skill** from the `skills/wagtail-package-scaffolder/` directory
2. **Read SKILL.md** for the workflow
3. **Fetch current version compatibility** from official Wagtail sources:
   - Release schedule from GitHub wiki
   - Compatibility matrix from Wagtail docs
   - Determines supported Wagtail, Django, and Python versions
4. **Display detected versions** and allow you to confirm or customize
5. **Ask you for package details** (name, description, author, etc.)
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
[1] Use recommended defaults
[2] Specify custom version constraints

You: 1

Agent: Great! Now I need a few more details:
- Description: AI-powered assistant for Wagtail CMS
- Author name: Jane Developer
- Author email: jane@example.com
- GitHub username: janedeveloper
...

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

Edit the files in `skills/wagtail-package-scaffolder/` to:

- Add your default author info to prompts
- Modify file templates
- Add/remove generated files
- Change project structure

Version requirements are fetched dynamically from official Wagtail sources at generation time. This ensures generated packages always support current Wagtail versions without manual updates to the skill.

## Requirements

- An AI coding agent with shell and file access
- Internet connection for version detection

## Learn More

- Skill configuration: `skills/wagtail-package-scaffolder/SKILL.md`
- File templates: `skills/wagtail-package-scaffolder/references/file-templates.md`
- Wagtail docs: https://docs.wagtail.org
