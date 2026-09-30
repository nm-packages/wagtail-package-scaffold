# Generator and Template Reference

## Executable sources

- `../scripts/scaffold.py`: CLI, input validation, rendering, file checks, replay.
- `../scripts/versions.py`: official source parsing and compatible test triples.
- `../assets/manifest.json`: ordered generated-file paths, template paths, and conditions.
- `../assets/templates/`: maintained templates, including the complete sandbox.

The Markdown reference documents the contract; Python and assets implement it.
Do not interpret this document as instructions to render files manually.

## Configuration

A JSON object accepts the following fields. Unknown fields are errors.

| Field | Default | Behavior |
|---|---|---|
| `package_name` | Required | Lowercase hyphenated distribution name; derived module must be a valid Python identifier and not a keyword. |
| `description` | `A reusable Wagtail package` | One line; escaped for TOML and Python. |
| `author_name` | `Your Name` | The skill offers Git-config defaults. |
| `author_email` | `you@example.com` | One email-like value. |
| `github_username` | `your-github-username` | Letters, digits, hyphens; a leading `@` is removed. |
| `license` | `MIT` | Other licenses fail until a maintained template is added. |
| `test_framework` | `pytest` | `pytest` or Django `unittest`. |
| `include_sandbox` | `true` | Render the sandbox and associated Makefile targets. |
| `include_admin` | `true` | Render a `wagtail_hooks.py` placeholder. |
| `include_models` | `true` | Render a `models.py` placeholder; migration package remains available. |
| `include_blocks` | `false` | Render an example StructBlock and its HTML template. |
| `include_api` | `false` | Render a JSON endpoint, URL configuration, and a generated endpoint test. |
| `wagtail_min` | Latest supported LTS | Must occur in the compatible matrix after applying all minima. |
| `django_min` | Lowest compatible Django for that LTS | Same constraint. |
| `python_min` | Lowest compatible Python for those defaults | Same constraint. |

Boolean fields require actual JSON booleans. Metadata cannot contain control
characters. `--output` always specifies the exact destination; it is not saved
as part of the configuration so replay can target a different directory.

## Version detection

Fresh detection fetches the official Wagtail release schedule and upgrading
compatibility table with a 20-second timeout per request. Release dates and
security-support dates are normalized to ISO dates. Retain released, supported
Wagtail versions, requiring an LTS. Django series without published non-yanked
stable PyPI releases are omitted even if Wagtail documents future compatibility.

Fetch Django's official version-specific installation FAQ tables to validate
Django/Python support. Missing data, malformed tables, and network failures abort
instead of guessing. Table parsers validate headers and cell shapes; upstream
format changes may require parser maintenance.

The saved version data contains:

- `supported_wagtail_versions`: numerically sorted releases with `version`,
  `is_lts`, `release_date`, `support_end`, `django_versions`, and `python_versions`.
- `django_python`: Python compatibility lists for each retained Django series.
- `sources`: official-source URLs and the Django PyPI URL used during detection.

Build triples only when Python and Django both occur in the Wagtail row and the
Python release also occurs in Django's compatibility list. Apply user minima,
then sort by Python, Django, and Wagtail numerically. Both tox and GitHub Actions
use this exact set; Actions uses an explicit `include` matrix. Classifiers use
the Python and Django releases occurring in those triples. Wagtail classifiers
include every distinct major version occurring in the selected triples, sorted
numerically and emitted once (for example, `Framework :: Wagtail :: 7` and
`Framework :: Wagtail :: 8`).

## Rendering and replay

Templates use Python `str.format_map`: `{name}` is a placeholder, `{{` and `}}`
are literal braces. Django template braces therefore need escaping too. Unknown
placeholders fail rendering. User values are substituted once, so literal braces
in descriptions are preserved. Source templates are trusted repository assets.

Render all selected files in manifest order before writing the destination.
Validate Python with `ast.parse` and TOML with `tomllib`; normalize UTF-8 text to
LF and one final newline, including otherwise empty marker files. Stage complete
output before writing. Existing project contents and symlinks are rejected;
optional installer README content is replaced by the package README.

Every generated project stores:

- `.scaffold/config.json`: resolved metadata, options, and version minima.
- `.scaffold/version-data.json`: normalized compatibility snapshot.
- `.scaffold/metadata.json`: schema and generator version, generation date,
  SHA-256 of generator scripts and assets, and hashes of generated files.

Replay validates the snapshot and bundle identity and reproduces the initial
scaffold. It does not fetch sources or capture subsequent project edits. Identical
resolved inputs, date, version data, and bundle produce identical generated file
paths and bytes, including snapshot files. Keep the original bundle or repository
revision for long-term replay. Hashes detect accidental changes, not authenticity.

Generation does not install dependencies. Reproducible scaffold bytes do not
freeze later dependency installations; generated dependency ranges still resolve
against the package index.

## Contributor validation

Run the generator regression tests:

```bash
python3 -m unittest discover -s skills/wagtail-package-scaffolder/tests -v
bash -n install.sh
bash install.sh --help
```

For integration checks, generate disposable projects, install dependencies, and
exercise pytest/unittest, sandbox on/off, API/block options, sandbox checks and
migrations, and distribution builds. Compare fresh generation and offline replay
byte-for-byte. Keep all generated projects outside this repository.
