#!/bin/bash

# Wagtail Package Scaffolder - Installation Script
# Downloads the skill files from GitHub to an agent-specific project skill directory.

set -e

REPO="https://github.com/nm-packages/wagtail-package-scaffold"
RAW_REPO="https://raw.githubusercontent.com/nm-packages/wagtail-package-scaffold"
BRANCH="main"
SKILL_NAME="wagtail-package-scaffolder"
AGENT=""
TARGET_DIR="."
FORCE=false

usage() {
    cat <<EOF
Wagtail Package Scaffolder installer

Usage:
  bash install.sh [options]

Options:
  -a, --agent codex|claude   Agent to install for
  -t, --target PATH          Target project folder (default: current directory)
  -f, --force                Overwrite an existing skill without prompting
  -h, --help                 Show this help message

Examples:
  bash install.sh --agent codex
  bash install.sh --agent claude --target ./my-new-package
  bash install.sh --agent codex --target /tmp/new-package --force
EOF
}

normalize_agent() {
    case "$1" in
        codex|Codex|CODEX)
            echo "codex"
            ;;
        claude|Claude|CLAUDE|claude-code|Claude-Code|CLAUDE-CODE)
            echo "claude"
            ;;
        *)
            echo ""
            ;;
    esac
}

agent_skill_root() {
    case "$1" in
        codex)
            echo ".codex/skills"
            ;;
        claude)
            echo ".claude/skills"
            ;;
        *)
            echo ""
            ;;
    esac
}

download_file() {
    local source_path="$1"
    local fallback_path="$2"
    local destination="$3"
    local source_url="${RAW_REPO}/${BRANCH}/${source_path}"
    local fallback_url="${RAW_REPO}/${BRANCH}/${fallback_path}"

    if ! curl -fsSL "$source_url" -o "$destination" 2>/dev/null; then
        echo "Could not download ${source_path}; trying legacy source path." >&2
        curl -fsSL "$fallback_url" -o "$destination"
    fi
}

prompt_for_agent() {
    echo "Choose the coding agent to install this skill for:" >&2
    echo "  1) Codex" >&2
    echo "  2) Claude Code" >&2
    printf "Agent [1-2]: " >&2
    read -r choice

    case "$choice" in
        1|codex|Codex|CODEX)
            echo "codex"
            ;;
        2|claude|Claude|CLAUDE|claude-code|Claude-Code|CLAUDE-CODE)
            echo "claude"
            ;;
        *)
            echo ""
            ;;
    esac
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        -a|--agent)
            if [ -z "${2:-}" ]; then
                echo "Error: $1 requires an agent value: codex or claude" >&2
                exit 1
            fi
            AGENT="$(normalize_agent "$2")"
            if [ -z "$AGENT" ]; then
                echo "Error: unsupported agent '$2'. Use codex or claude." >&2
                exit 1
            fi
            shift 2
            ;;
        -t|--target)
            if [ -z "${2:-}" ]; then
                echo "Error: $1 requires a target path" >&2
                exit 1
            fi
            TARGET_DIR="$2"
            shift 2
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Error: unknown option '$1'" >&2
            echo "" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if [ -z "$AGENT" ]; then
    AGENT="$(prompt_for_agent)"
    if [ -z "$AGENT" ]; then
        echo "Installation cancelled: unsupported agent selection."
        exit 1
    fi
fi

SKILL_ROOT="$(agent_skill_root "$AGENT")"
SKILL_DIR="${TARGET_DIR%/}/${SKILL_ROOT}/${SKILL_NAME}"

echo "Installing Wagtail Package Scaffolder skill for ${AGENT}..."
echo ""

mkdir -p "$TARGET_DIR"

if [ -d "${SKILL_DIR}" ]; then
    echo "Skill already exists in ${SKILL_DIR}"
    if [ "$FORCE" = true ]; then
        echo "Overwriting because --force was provided."
    else
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Installation cancelled."
            exit 1
        fi
    fi
    rm -rf "${SKILL_DIR}"
fi

mkdir -p "${SKILL_DIR}/references"

echo "Downloading skill files..."

download_file \
    "skills/wagtail-package-scaffolder/SKILL.md" \
    ".claude/skills/wagtail-package-scaffolder/SKILL.md" \
    "${SKILL_DIR}/SKILL.md"

download_file \
    "skills/wagtail-package-scaffolder/references/file-templates.md" \
    ".claude/skills/wagtail-package-scaffolder/references/file-templates.md" \
    "${SKILL_DIR}/references/file-templates.md"

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
