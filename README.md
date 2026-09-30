# Wagtail Package Scaffolder

An agent-agnostic skill backed by a deterministic Python generator. Your coding
agent helps choose options; Python validates inputs and renders the package.

## Features

- Live Wagtail and Django compatibility detection without AI table extraction
- Shared, validated Python/Django/Wagtail combinations for tox and GitHub Actions
- Modern Python packaging with a src layout and pytest or Django unittest
- Optional sandbox rendered from repository-maintained templates
- Optional admin/model placeholders, StreamField block, and JSON API example
- Saved configuration and version snapshots for explicit offline replay
- Bundle identity and output hashes to verify reproduction

## Installation

In an empty package directory, install the complete skill bundle for your agent.
Review [install.sh](install.sh) before executing it.

For Codex:

```bash
curl -fsSL https://raw.githubusercontent.com/nm-packages/wagtail-package-scaffold/main/install.sh | bash -s -- --agent codex
```

For Claude Code:

```bash
curl -fsSL https://raw.githubusercontent.com/nm-packages/wagtail-package-scaffold/main/install.sh | bash -s -- --agent claude
```

Use `--target ./my-new-package` to install elsewhere and `--force` to replace an
existing installation. The installer downloads scripts, templates, and their
manifest together from one GitHub archive.

Then ask your agent:

```text
Create a Wagtail package called wagtail-hello-world
```

The skill asks one missing question at a time with a concrete default, then calls
Python to generate files. It is installed in
`.codex/skills/wagtail-package-scaffolder/` or
`.claude/skills/wagtail-package-scaffolder/`.

## Requirements

- Python 3.11+ to run the generator; no third-party generator dependencies
- An AI coding agent with shell/file access for the conversational workflow
- Internet access for fresh compatibility detection

The generator can also be invoked directly with JSON inputs. Generated packages
have their own Python minimum, derived from the selected compatibility data.

## Reproducibility

Every package includes `.scaffold/config.json`, `.scaffold/version-data.json`,
and `.scaffold/metadata.json`. Keep these files and access to the original skill
bundle or its Git revision.

```bash
python3 /path/to/original/skill/scripts/scaffold.py replay \
    /path/to/project/.scaffold --output /path/to/new-empty-directory
```

Replay makes no network requests and uses the original generation date. Matching
inputs and the same generator/template bundle produce identical generated paths
and bytes. Changed snapshots or a different bundle cause an error. Replay
recreates the initial scaffold; it does not restore later project edits or freeze
future dependency installations.

## Contributor checks

```bash
python3 -m unittest discover -s skills/wagtail-package-scaffolder/tests -v
bash -n install.sh
bash install.sh --help
```

See [usage.md](usage.md) for configuration and direct command examples, and the
[generator reference](skills/wagtail-package-scaffolder/references/file-templates.md)
for rendering and version-detection rules. Official documentation formats and
sandbox compatibility still require maintenance as upstream projects evolve.
