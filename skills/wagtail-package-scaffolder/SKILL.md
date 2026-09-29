---
name: wagtail-package-scaffolder
description: "Scaffold reusable Wagtail/Django packages using a deterministic Python generator. Use when creating a new Wagtail package or reusable Wagtail app, or replaying a saved scaffold."
---

# Wagtail Package Scaffolder

Help the user choose package options, then run the bundled Python generator.
Python owns version retrieval, validation, compatibility matrices, template
rendering, sandbox creation, and replay. Do not generate or edit scaffold files
with AI to work around a generator failure; report the error and resolve its cause.

## Requirements and entry point

Use Python 3.11+ and the `scripts/scaffold.py` beside this skill. Resolve its
absolute path from the installed skill directory (`.codex/skills/`,
`.claude/skills/`, or the repository's `skills/` layout). The generator uses only
the standard library. Internet access is required for fresh version detection;
explicit snapshot replay makes no network requests.

Read [references/file-templates.md](references/file-templates.md) when you need
configuration fields, replay details, or generator behavior. The executable
manifest and templates are in `assets/`; the agent does not need to read them
before invoking the generator.

## Interaction

Ask exactly one unresolved question per message. Include a concrete default in
its wording, put the recommended multiple-choice answer first, and skip values
already supplied by the user. Accept an empty answer, `default`, or `use default`
as that question's default. Convert yes/no answers to JSON booleans.

Ask in this order:

1. Version defaults or custom constraints (custom: Wagtail, Django, Python minima separately).
2. Package name.
3. Description.
4. Author name.
5. Author email.
6. GitHub username.
7. License (MIT is the only maintained license template).
8. Output location (current directory by default; a requested subdirectory is passed as `--output`).
9. Test framework (`pytest` by default; `unittest` is supported).
10. Sandbox (`true`).
11. Admin hooks (`true`), models placeholder (`true`), StreamField block (`false`), JSON API example (`false`), each separately.
12. Cleanup confirmation after successful generation (default: no).

Derive the package-name default from the current directory basename: lowercase,
replace spaces/underscores with hyphens, remove other characters, collapse repeated
hyphens, and trim hyphens. Use `wagtail-example-package` if it does not match
`^[a-z0-9]+(-[a-z0-9]+)*$` or cannot produce a valid Python module identifier.
Use `A reusable Wagtail package` for description. Use `git config user.name` and
`git config user.email` for author defaults, falling back to `Your Name` and
`you@example.com`. Derive GitHub owner from the remote when available; otherwise
slugify the author's name or use `your-github-username`.

## Generate a new package

1. Choose a clean destination. The generator permits only the installed skill
   and optional `README.md`, `usage.md`, and `install.sh`; other existing content
   or symlinks cause an error. Do not bypass this check or overwrite a project.
2. Create a temporary working directory **outside the destination** for JSON
   input files. Fetch version data once, using the session's current date:

   ```bash
   python3 /absolute/path/to/skill/scripts/scaffold.py versions \
       --date YYYY-MM-DD --output /temporary/path/version-data.json
   ```

   The command prints recommended minima. Show the retained Wagtail versions,
   support dates, and defaults from the saved JSON before asking the version
   question. Do not extract tables with prompts or substitute remembered data.
3. Collect missing inputs and write a JSON configuration in the temporary
   directory. Validate custom minima against the fetched data; the generator
   requires each minimum to occur in the resulting compatible matrix.
4. Invoke the generator with those exact inputs:

   ```bash
   python3 /absolute/path/to/skill/scripts/scaffold.py generate \
       --config /temporary/path/config.json \
       --versions /temporary/path/version-data.json \
       --date YYYY-MM-DD --output /absolute/path/to/destination
   ```

5. Report success only when the command exits successfully. Explain how to
   install development dependencies, run `make test`, and, when enabled, run
   `make migrate`, `make superuser`, and `make sandbox`. Explain source edit
   points and that optional models/admin files start as placeholders.
6. Keep the generated `.scaffold/` directory: it stores configuration, version
   data, date, output hashes, and generator/template identity for replay.

Sandbox files come from repository-maintained templates. Do not install Wagtail
or run `wagtail start` during scaffolding.

## Replay

When the user requests reproduction, use their saved `.scaffold/` directory:

```bash
python3 /absolute/path/to/skill/scripts/scaffold.py replay \
    /original/project/.scaffold --output /new/clean/destination
```

Replay uses the original date and saved inputs without network access. It rejects
an altered input snapshot or a different generator/template bundle. Keep an
original bundle or Git revision available; do not bypass identity verification.
Replay recreates the initial scaffold, not later source edits.

## Cleanup

After successful generation, ask whether to remove the installed skill directory
and installer docs (`usage.md` and `install.sh`), defaulting to no. Remove only
those named resources after an affirmative answer. Keep `.scaffold/` and the
package README. Explain that replay still requires access to the original bundle.
