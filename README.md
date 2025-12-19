# Wagtail Package Scaffolder

A Claude Code skill that generates production-ready Wagtail packages with dynamic version detection.

## Features

- 🔄 **Dynamic version detection** - Automatically fetches current Wagtail/Django/Python compatibility from official sources
- 📦 **Complete package structure** - Modern Python packaging with src layout
- 🧪 **Test matrices** - tox.ini and GitHub Actions configured for all supported version combinations
- 🏗️ **Optional sandbox** - Full Wagtail development site for testing
- ⚡ **Zero maintenance** - Version data updates automatically at generation time

## Installation

### Option 1: Quick Install (Recommended)

In your new empty folder where you want to generate a package:

```bash
curl -sSL https://raw.githubusercontent.com/nickmoreton/claude-code-wagtail-package-scaffolder/main/install.sh | bash
```

Or download and run the script:

```bash
curl -O https://raw.githubusercontent.com/nickmoreton/claude-code-wagtail-package-scaffolder/main/install.sh
chmod +x install.sh
./install.sh
```

### Option 2: Manual Download

Download only the `.claude/` folder (the skill files):

```bash
# Download the repository ZIP
curl -L https://github.com/nickmoreton/claude-code-wagtail-package-scaffolder/archive/refs/heads/main.zip -o skill.zip

# Extract only the .claude directory
unzip -j skill.zip "claude-code-wagtail-package-scaffolder-main/.claude/skills/wagtail-package-scaffolder/*" -d .claude/skills/wagtail-package-scaffolder/
unzip -j skill.zip "claude-code-wagtail-package-scaffolder-main/.claude/skills/wagtail-package-scaffolder/references/*" -d .claude/skills/wagtail-package-scaffolder/references/

# Clean up
rm skill.zip

echo "✅ Skill installed in .claude/skills/wagtail-package-scaffolder/"
```

**Note**: Only the `.claude/` folder is required - you don't need any other files from the repository.

### Using the Skill

Once installed, run Claude Code and ask:
```
Create a Wagtail package called [your-package-name]
```

## Usage

The skill will:
1. Fetch current Wagtail version compatibility
2. Show you detected versions and defaults
3. Ask for package details (name, description, author, etc.)
4. Generate all files with proper version support

## Requirements

- Claude Code CLI
- Internet connection (for version detection)

## What Gets Generated

- Modern `pyproject.toml` with dynamic version classifiers
- Complete source structure in `src/` layout
- Test infrastructure (pytest or unittest)
- GitHub Actions CI/CD with version matrix
- `tox.ini` for local testing across Python/Django/Wagtail versions
- Optional Wagtail sandbox site
- Pre-commit hooks and development tools

## Learn More

See [`claude_code_skill.md`](claude_code_skill.md) for detailed documentation.
