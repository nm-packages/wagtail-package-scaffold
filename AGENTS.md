# Repository Guidelines

## Project Structure & Module Organization

This repository distributes an agent-agnostic Wagtail package scaffolding skill. The workflow lives in `skills/wagtail-package-scaffolder/SKILL.md`; Python generation lives in `skills/wagtail-package-scaffolder/scripts/`; executable templates and the ordered manifest live in `skills/wagtail-package-scaffolder/assets/`. `skills/wagtail-package-scaffolder/references/file-templates.md` documents configuration and rendering rules. `install.sh` installs these files for Codex or Claude Code. `README.md` and `usage.md` explain installation and usage.

Directories such as `src/`, `tests/`, `sandbox/`, and package static assets belong to generated projects; they are not present in this repository.

## Build, Test, and Development Commands

- `bash -n install.sh`: check installer syntax without executing it.
- `bash install.sh --help`: inspect supported arguments.
- `bash install.sh --agent codex --target /tmp/scaffold-check`: smoke-test installation in a disposable directory; use `--agent claude` for Claude Code. Downloads come from GitHub's `main` branch, so this does not validate local template edits.

Run `python3 -m unittest discover -s skills/wagtail-package-scaffolder/tests -v` for generator regression checks. There is no repository build. To validate template changes, scaffold a disposable project using the edited generator. Within that generated project, `make dev` installs development dependencies, `make test` runs tests, `make test-all` runs tox, and `make build` creates distribution artifacts.

## Coding Style & Naming Conventions

Use descriptive Markdown headings and fenced code blocks with language labels. Match the installer's four-space indentation and quote shell path variables. Python templates use four-space indentation and configure Ruff with an 88-character line limit; generated projects also include pre-commit hooks.

Use hyphenated distribution names such as `wagtail-hello-world` and underscore module names such as `wagtail_hello_world`. Preserve template placeholders, escaped braces, section ordering, and conditional rendering rules.

## Testing Guidelines

Exercise pytest (the default) and Django unittest output when changing test templates. Generated tests use `tests/test_*.py`; coverage reporting is configured without a minimum percentage requirement. Check sandbox-enabled and sandbox-disabled output when relevant.

Verify generated files contain no unresolved placeholders, use LF endings and one final newline, and remain identical for fixed inputs, version data, date, and options.

## Commit & Pull Request Guidelines

1. Before making changes for each new piece of work, always create and check out a focused branch from the currently checked-out branch. Use `git switch -c <task-branch>` without switching to another base branch first. Name the branch for its task, such as `feat/add-template-option`, `fix/installer-path-handling`, or `docs/update-contributor-guide`. Never make changes directly on the repository's default branch or `main`. Keep unrelated changes on separate branches.
2. Present completed changes and validation results for developer review. Commit only after the developer has reviewed and explicitly approved the changes; address requested revisions before committing.
3. Before opening a pull request, prepare its title and detailed description and ask the developer for approval. Open the PR only after approval. Include the problem addressed, changes made, resulting behavior, validation performed, relevant issue links, and any limitations or follow-up work.

Use short imperative commit subjects, following history. Update usage documentation when prompts, installer arguments, or generated output change.

The root `.gitignore` ignores files by default. Explicitly allow or force-add intended new contributor files; keep generated projects and local agent settings out of commits.
