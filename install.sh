#!/bin/bash

# Wagtail Package Scaffolder - Installation Script
# Downloads the skill files from GitHub to the current directory

set -e

REPO="https://github.com/nm-packages/wagtail-package-scaffold"
BRANCH="main"
SKILL_DIR="skills/wagtail-package-scaffolder"

echo "Installing Wagtail Package Scaffolder skill..."
echo ""

if [ -d "${SKILL_DIR}" ]; then
    echo "Skill already exists in ${SKILL_DIR}"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 1
    fi
    rm -rf "${SKILL_DIR}"
fi

mkdir -p "${SKILL_DIR}/references"

echo "Downloading skill files..."

curl -sL "${REPO}/raw/${BRANCH}/skills/wagtail-package-scaffolder/SKILL.md" \
    -o "${SKILL_DIR}/SKILL.md"

curl -sL "${REPO}/raw/${BRANCH}/skills/wagtail-package-scaffolder/references/file-templates.md" \
    -o "${SKILL_DIR}/references/file-templates.md"

echo "Installation complete!"
echo ""
echo "The skill is now available in: ${SKILL_DIR}/"
echo ""
echo "Usage:"
echo "  Ask your coding agent:"
echo "  'Create a Wagtail package called [your-package-name]'"
echo ""
echo "For more info, see: ${REPO}"
echo ""

if [ -f "install.sh" ]; then
    echo "Cleaning up installation script..."
    rm -f install.sh
fi
