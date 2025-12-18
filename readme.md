# Installing the Wagtail Package Scaffolder Skill for Claude Code

## Quick Install

1. **Unzip** `wagtail-package-scaffolder-claude-code.zip` in your project root (or any directory where you want the skill available)

2. **Verify** the structure looks like:
   ```
   your-project/
   └── .claude/
       └── skills/
           └── wagtail-package-scaffolder/
               ├── SKILL.md
               └── references/
                   └── file-templates.md
   ```

3. **Use it** by asking Claude Code:
   - "Scaffold a new Wagtail package called wagtail-markdown-editor"
   - "Create a Wagtail package for me"
   - "New wagtail extension"

## Manual Install

If you prefer, just copy the files manually:

```bash
# From your project root
mkdir -p .claude/skills/wagtail-package-scaffolder/references

# Copy the files (adjust source path as needed)
cp SKILL.md .claude/skills/wagtail-package-scaffolder/
cp file-templates.md .claude/skills/wagtail-package-scaffolder/references/
```

## How It Works

When you ask Claude Code to scaffold a Wagtail package, it will:

1. **Detect the skill** from the `.claude/skills/` directory
2. **Read SKILL.md** for the workflow
3. **Ask you for variables** (package name, author, etc.)
4. **Read the templates** from `references/file-templates.md`
5. **Generate all files** with your values substituted

## Example Usage

```
You: Create a wagtail package called wagtail-ai-assistant

Claude Code: I'll scaffold a Wagtail package for you. I need a few details:
- Description: 
- Author name:
- Author email:
- GitHub username:
...

[Claude generates all files]
```

## Customizing

Edit the files in `.claude/skills/wagtail-package-scaffolder/` to:
- Add your default author info
- Change version requirements
- Add/remove features
- Modify templates

The skill files are just markdown - easy to read and modify!
