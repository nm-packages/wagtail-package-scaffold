# Usage

## Conversational scaffolding

Install the skill in an empty project directory, then ask:

```text
Create a Wagtail package called wagtail-hello-world
```

The agent fetches compatibility data through Python and offers version defaults.
It asks each missing metadata or feature question separately, with a default.
Python generates files once the choices are collected.

Defaults include pytest, MIT licensing, a sandbox, and empty models/admin hook
files. StreamField blocks and the JSON API example are optional. Both options
include working templates or endpoint code and generated tests. Other licenses
are rejected until a maintained license template is supplied.

Output goes to the current directory unless you choose another destination.
Only installed skill resources and optional installer docs may already exist;
existing projects and symlinks are rejected. The package README replaces any
installer README in that directory.

## Direct Python commands

Use Python 3.11+ and resolve the script path for your installation. For example:

```bash
SCAFFOLD_SCRIPT="$PWD/.codex/skills/wagtail-package-scaffolder/scripts/scaffold.py"
SCAFFOLD_INPUT_DIR="$(mktemp -d)"
python3 "$SCAFFOLD_SCRIPT" versions --output "$SCAFFOLD_INPUT_DIR/version-data.json"
```

Input files must be outside the generation destination. Create
`$SCAFFOLD_INPUT_DIR/config.json` with a JSON object such as:

```json
{
  "package_name": "wagtail-hello-world",
  "description": "A reusable Wagtail package",
  "author_name": "Jane Developer",
  "author_email": "jane@example.com",
  "github_username": "janedeveloper",
  "license": "MIT",
  "test_framework": "pytest",
  "include_sandbox": true,
  "include_admin": true,
  "include_models": true,
  "include_blocks": false,
  "include_api": false
}
```

Only `package_name` is mandatory; missing fields receive documented defaults.
The direct CLI uses placeholder author defaults, while the skill offers values
from Git configuration. Boolean values must be JSON booleans, not strings.

```bash
python3 "$SCAFFOLD_SCRIPT" generate \
    --config "$SCAFFOLD_INPUT_DIR/config.json" \
    --versions "$SCAFFOLD_INPUT_DIR/version-data.json" \
    --output /path/to/clean/destination
```

Omit `--versions` to fetch live data as part of generation. The `versions` and
`generate` commands accept `--date YYYY-MM-DD`; use the same explicit date for
both when running a controlled reproduction check. Otherwise they use today's
local date. Network or parsing errors abort; there is no automatic cached fallback.

Custom `wagtail_min`, `django_min`, and `python_min` fields must each occur in the
valid test matrix after applying all minima. The default Wagtail minimum is the
oldest currently supported LTS. Compatibility with future, unpublished Django
series is omitted.

## Generated output

- Root packaging, README, MIT license, changelog, Makefile, and development config
- `src/<module_name>/` with AppConfig, migration package, static/template directories
- `tests/` with settings and pytest or Django unittest tests
- `.github/` with CI, publishing workflow, and a bug-report template
- `docs/` and `mkdocs.yml`
- Optional `sandbox/` with Wagtail settings, home page model, templates, and migrations
- `.scaffold/` with resolved inputs and reproduction metadata

Admin/model options create placeholder files ready for your implementation.
The API option creates `/<module_name>/api/`, returning the package name as JSON.
The block option includes a StructBlock and its HTML template. Sandbox generation
runs no external project generator and installs no dependencies.

## Develop the package

In the generated project:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
# Initialize Git if needed before installing hooks:
git init
pre-commit install
make test
make build
```

For a sandbox:

```bash
make migrate
make superuser
make sandbox
```

Visit [the sandbox admin](http://localhost:8000/admin/) or
[the home page](http://localhost:8000/). The sandbox migration creates a HomePage
and a default localhost site.

`make test-all` runs tox across the supported matrix. Missing local Python
interpreters are skipped. CI uses the same compatible triples. Development
settings and their fixed secret keys are intended for local use.

## Explicit replay

Keep `.scaffold/` and the original generator/template bundle. Reproduce the
initial scaffold in a new clean directory:

```bash
python3 /path/to/original/skill/scripts/scaffold.py replay \
    /original/project/.scaffold --output /new/clean/destination
```

Replay validates configuration, compatibility data, original date, bundle
identity, and expected output hashes. It makes no network requests. If the bundle
has changed, retrieve the original Git revision rather than bypassing the check.
Edits to a generated project's source do not change the saved initial scaffold;
replay does not copy those edits.

You can use `generate` with edited configuration and explicit version data to
create a new variant in another directory. This is a new generation, not replay.
Keep its new `.scaffold/` snapshot too.

## Customize or maintain the generator

Edit `assets/templates/` and `assets/manifest.json` for output changes, and
`scripts/` for validation and compatibility logic. Templates use `{variable}`
placeholders with doubled literal braces. Changing scripts or assets changes
bundle identity. Read the
[generator reference](skills/wagtail-package-scaffolder/references/file-templates.md)
before adding fields or conditional files.

After generation, the agent offers to remove the installed skill, `usage.md`, and
`install.sh`. Cleanup defaults to no and requires an affirmative answer. Preserve
`.scaffold/` and another copy of the original bundle if you want future replay.
