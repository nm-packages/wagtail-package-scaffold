#!/bin/bash

# Wagtail Package Scaffolder - Installation Script
# Downloads the skill files from GitHub to the current directory

set -e

REPO="https://github.com/nm-packages/wagtail-package-scaffold"
BRANCH="main"

echo "📦 Installing Wagtail Package Scaffolder skill..."
echo ""

# Check if .claude directory already exists
if [ -d ".claude/skills/wagtail-package-scaffolder" ]; then
    echo "⚠️  Skill already exists in .claude/skills/wagtail-package-scaffolder"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
    rm -rf .claude/skills/wagtail-package-scaffolder
fi

# Create directory structure
mkdir -p .claude/skills/wagtail-package-scaffolder/references

echo "📥 Downloading skill files..."

# Download SKILL.md
curl -sL "${REPO}/raw/${BRANCH}/.claude/skills/wagtail-package-scaffolder/SKILL.md" \
    -o .claude/skills/wagtail-package-scaffolder/SKILL.md

# Download file-templates.md
curl -sL "${REPO}/raw/${BRANCH}/.claude/skills/wagtail-package-scaffolder/references/file-templates.md" \
    -o .claude/skills/wagtail-package-scaffolder/references/file-templates.md

echo "✅ Installation complete!"
echo ""
echo "The skill is now available in: .claude/skills/wagtail-package-scaffolder/"
echo ""
echo "📝 Usage:"
echo "  Open Claude Code and ask:"
echo "  'Create a Wagtail package called [your-package-name]'"
echo ""
echo "📚 For more info, see: ${REPO}"
