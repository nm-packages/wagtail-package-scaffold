#!/usr/bin/env python3
"""Deterministic Wagtail package generator (Python 3.11+, standard library only)."""

import argparse
import ast
import hashlib
import json
import keyword
import os
import re
import tempfile
import tomllib
from datetime import date
from pathlib import Path

from versions import combinations, defaults, fetch_data, validate_data, version_key

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_VERSION = 1
GENERATOR_VERSION = "1.0.0"
OPTIONS = {
    "include_admin": True,
    "include_models": True,
    "include_blocks": False,
    "include_api": False,
    "include_sandbox": True,
}
METADATA = {
    "description": "A reusable Wagtail package",
    "author_name": "Your Name",
    "author_email": "you@example.com",
    "github_username": "your-github-username",
    "license": "MIT",
    "test_framework": "pytest",
}


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def read_json(path):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON field: {key}")
            result[key] = value
        return result

    return json.loads(
        Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_object
    )


def fingerprint():
    """Include executable code, manifest, and every template in the bundle identity."""
    files = sorted(
        list((ROOT / "assets").rglob("*")) + list((ROOT / "scripts").glob("*.py"))
    )
    digest = hashlib.sha256()
    for path in files:
        if path.is_file():
            digest.update(path.relative_to(ROOT).as_posix().encode() + b"\0")
            digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def normalize_config(raw, data):
    if not isinstance(raw, dict):
        raise ValueError("Configuration must be a JSON object")
    allowed = {"package_name", *METADATA, *OPTIONS, *defaults(data)}
    if set(raw) - allowed:
        raise ValueError(f"Unknown configuration fields: {sorted(set(raw) - allowed)}")
    config = {**METADATA, **OPTIONS, **defaults(data), **raw}
    name = config.get("package_name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("package_name must be lowercase words separated by hyphens")
    module = name.replace("-", "_")
    if not module.isidentifier() or keyword.iskeyword(module):
        raise ValueError("Package name must produce a valid Python module identifier")
    for field in METADATA:
        value = config[field]
        if (
            not isinstance(value, str)
            or not value.strip()
            or any(ord(c) < 32 for c in value)
        ):
            raise ValueError(
                f"{field} must be nonempty text without control characters"
            )
        config[field] = value.strip()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", config["author_email"]):
        raise ValueError("author_email must be a single email-like value")
    config["github_username"] = config["github_username"].lstrip("@")
    if not re.fullmatch(r"[A-Za-z0-9-]+", config["github_username"]):
        raise ValueError("Invalid GitHub username")
    if config["license"] != "MIT":
        raise ValueError("Only MIT has a maintained license template")
    if config["test_framework"] not in ("pytest", "unittest"):
        raise ValueError("test_framework must be pytest or unittest")
    for field in OPTIONS:
        if type(config[field]) is not bool:
            raise ValueError(f"{field} must be a JSON boolean")
    for field in defaults(data):
        version_key(config[field])
    combinations(data, config)
    return config


def next_minor(version):
    major, minor = version_key(version)
    return f"{major}.{minor + 1}"


def context(config, data, today):
    matrix = combinations(data, config)
    module = config["package_name"].replace("-", "_")
    python_versions = sorted({p for p, _, _ in matrix}, key=version_key)
    django_versions = sorted({d for _, d, _ in matrix}, key=version_key)
    wagtail_versions = sorted({w for _, _, w in matrix}, key=version_key)
    pytest = config["test_framework"] == "pytest"
    test_deps = (
        ["pytest>=8.0", "pytest-django>=4.5", "pytest-cov>=4.0"]
        if pytest
        else ["coverage>=7.0"]
    )
    result = {
        **config,
        "module_name": module,
        "module_name_camel": "".join(part.capitalize() for part in module.split("_")),
        "module_name_upper": module.upper(),
        "package_title": " ".join(
            part.capitalize() for part in config["package_name"].split("-")
        ),
        "python_min_nodot": config["python_min"].replace(".", ""),
        "wagtail_major": config["wagtail_min"].split(".")[0],
        "date": today,
        "year": today[:4],
        "description_literal": json.dumps(config["description"], ensure_ascii=False),
        "test_dependencies": "\n".join(f'    "{dep}",' for dep in test_deps),
        "tox_test_dependencies": "\n".join(f"    {dep}" for dep in test_deps),
        "pytest_ini_options": '[tool.pytest.ini_options]\nDJANGO_SETTINGS_MODULE = "tests.settings"\npython_files = ["test_*.py"]\ntestpaths = ["tests"]\npythonpath = ["."]\naddopts = "-v --tb=short"'
        if pytest
        else "",
        "coverage_command_line": "",
        "test_command": "pytest" if pytest else "python test_manage.py test",
        "make_test_command": "pytest" if pytest else "python test_manage.py test",
        "github_test_command": "pytest --cov --cov-report=xml"
        if pytest
        else "coverage run test_manage.py test && coverage xml",
        "tox_commands": f"    pytest --cov={module} --cov-report=term-missing --cov-report=html"
        if pytest
        else "    coverage run test_manage.py test\n    coverage report\n    coverage html",
        "lint_paths": "src tests sandbox" if config["include_sandbox"] else "src tests",
        "django_classifiers": "\n".join(
            f'    "Framework :: Django :: {v}",' for v in django_versions
        ),
        "python_classifiers": "\n".join(
            f'    "Programming Language :: Python :: {v}",' for v in python_versions
        ),
        "coverage_python": matrix[0][0],
        "coverage_django": matrix[0][1],
        "coverage_wagtail": matrix[0][2],
    }
    # The complete include matrix cannot produce unsupported Django/Wagtail pairs.
    result["github_matrix"] = "        include:\n" + "\n".join(
        f'          - python-version: "{p}"\n            django-version: "{d}"\n            wagtail-version: "{w}"'
        for p, d, w in matrix
    )
    rows = []
    for p in python_versions:
        for d in django_versions:
            ws = [w.replace(".", "") for py, dj, w in matrix if py == p and dj == d]
            if ws:
                selector = ws[0] if len(ws) == 1 else "{" + ",".join(ws) + "}"
                rows.append(
                    f"    py{p.replace('.', '')}-django{d.replace('.', '')}-wagtail{selector}"
                )
    result["tox_envlist"] = "\n".join(rows)
    result["tox_deps"] = "\n".join(
        f"    {label}{v.replace('.', '')}: {distribution}>={v},<{next_minor(v)}"
        for label, distribution, values in (
            ("django", "Django", django_versions),
            ("wagtail", "wagtail", wagtail_versions),
        )
        for v in values
    )
    result["api_view"] = "# Add your views here"
    if config["include_api"]:
        result["api_view"] = (
            "from django.http import JsonResponse\nfrom django.views import View\n\n\n"
            f"class {result['module_name_camel']}APIView(View):\n"
            "    def get(self, request):\n"
            f'        return JsonResponse({{"package": "{config["package_name"]}"}})'
        )
    result["package_url_pattern"] = (
        f'urlpatterns.insert(0, path("{module}/", include("{module}.urls")))'
        if config["include_api"]
        else ""
    )
    feature_tests = []
    if config["include_api"]:
        if pytest:
            feature_tests.append(
                "    def test_api(self, client):\n"
                f'        response = client.get("/{module}/api/")\n'
                "        assert response.status_code == 200\n"
                f'        assert response.json() == {{"package": "{config["package_name"]}"}}'
            )
        else:
            feature_tests.append(
                "    def test_api(self):\n"
                f'        response = self.client.get("/{module}/api/")\n'
                "        self.assertEqual(response.status_code, 200)\n"
                f'        self.assertEqual(response.json(), {{"package": "{config["package_name"]}"}})'
            )
    if config["include_blocks"]:
        feature_tests.append(
            "    def test_block_template(self):\n"
            f"        from {module}.blocks import {result['module_name_camel']}Block\n\n"
            f"        block = {result['module_name_camel']}Block()\n"
            '        value = block.to_python({"title": "Example", "text": "", "image": None})\n'
            + (
                '        assert "Example" in block.render(value)'
                if pytest
                else '        self.assertIn("Example", block.render(value))'
            )
        )
    result["feature_tests"] = "\n\n".join(feature_tests)
    sandbox = config["include_sandbox"]
    result["sandbox_phony_targets"] = " sandbox migrate superuser" if sandbox else ""
    result["sandbox_help_lines"] = (
        '\t@echo "  make sandbox    - Run the sandbox development server"\n'
        '\t@echo "  make migrate    - Apply sandbox migrations"\n'
        '\t@echo "  make superuser  - Create a sandbox administrator"'
        if sandbox
        else ""
    )
    result["sandbox_targets"] = (
        "sandbox:\n\tcd sandbox && python manage.py runserver\n\n"
        "migrate:\n\tcd sandbox && python manage.py migrate\n\n"
        "superuser:\n\tcd sandbox && python manage.py createsuperuser"
        if sandbox
        else ""
    )
    return result


def render(config, data, today):
    values = context(config, data, today)
    files = {}
    for entry in read_json(ROOT / "assets/manifest.json"):
        if entry.get("option") and not config[entry["option"]]:
            continue
        if (
            entry.get("test_framework", config["test_framework"])
            != config["test_framework"]
        ):
            continue
        path = entry["path"].format_map(values)
        relative = Path(path)
        if relative.is_absolute() or ".." in relative.parts or path in files:
            raise ValueError(f"Invalid/duplicate output path: {path}")
        local_values = dict(values)
        if path == "pyproject.toml":
            for field in ("description", "author_name", "author_email"):
                local_values[field] = json.dumps(values[field], ensure_ascii=False)[
                    1:-1
                ]
        template = (ROOT / "assets/templates" / entry["template"]).read_text(
            encoding="utf-8"
        )
        rendered = template.format_map(local_values)
        rendered = (
            rendered.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"
        )
        # Check placeholders in templates through format_map; literal braces in
        # Django templates, CSS, tox selectors and user text are valid output.
        if path.endswith(".py"):
            ast.parse(rendered, filename=path)
        elif path.endswith(".toml"):
            tomllib.loads(rendered)
        files[path] = rendered
    return files


def clean_target(target):
    """Permit only installed scaffolding resources and optional installer docs."""
    if target.is_symlink():
        raise ValueError("Output directory must not be a symlink")
    if not target.exists():
        return
    if not target.is_dir():
        raise ValueError("Output path is not a directory")
    skill_roots = [
        Path(".codex/skills/wagtail-package-scaffolder"),
        Path(".claude/skills/wagtail-package-scaffolder"),
        Path("skills/wagtail-package-scaffolder"),
    ]
    for path in target.rglob("*"):
        relative = path.relative_to(target)
        if path.is_symlink():
            raise ValueError(f"Output contains a symlink: {relative}")
        allowed = any(
            relative == root
            or root in relative.parents
            or (path.is_dir() and relative in root.parents)
            for root in skill_roots
        )
        allowed |= (
            len(relative.parts) == 1
            and path.is_file()
            and relative.name.lower()
            in {
                "readme.md",
                "usage.md",
                "install.sh",
            }
        )
        if not allowed:
            raise ValueError(f"Output directory contains existing files: {relative}")


def write_project(target, config, data, today):
    clean_target(target)
    files = render(config, data, today)
    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "generator_version": GENERATOR_VERSION,
        "bundle_sha256": fingerprint(),
        "date": today,
        "files_sha256": {
            path: hashlib.sha256(body.encode()).hexdigest()
            for path, body in files.items()
        },
    }
    files[".scaffold/config.json"] = json_text(config)
    files[".scaffold/version-data.json"] = json_text(data)
    files[".scaffold/metadata.json"] = json_text(snapshot)
    # Validate and stage everything before changing the destination.
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".scaffold-stage-", dir=target.parent
    ) as temp:
        stage = Path(temp)
        for path, body in files.items():
            destination = stage / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(body, encoding="utf-8", newline="\n")
        if not target.exists():
            os.replace(stage, target)
        else:
            clean_target(target)
            # Only README.md is an allowed preexisting output file.
            for path in files:
                destination = target / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                os.replace(stage / path, destination)
    print(f"Generated {len(files)} files in {target}")
    print("Saved replay inputs in .scaffold/ (keep these with your project).")
    print('Next: python -m venv .venv; activate it; pip install -e ".[dev]"')
    print(
        f"Tests: {'pytest' if config['test_framework'] == 'pytest' else 'python test_manage.py test'}"
    )
    if config["include_sandbox"]:
        print("Sandbox: make migrate, make superuser, make sandbox")


def load_replay(directory):
    snapshot = Path(directory)
    metadata = read_json(snapshot / "metadata.json")
    if not isinstance(metadata, dict) or set(metadata) != {
        "schema_version",
        "generator_version",
        "bundle_sha256",
        "date",
        "files_sha256",
    }:
        raise ValueError("Invalid replay metadata fields")
    if metadata.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unsupported replay schema")
    if (
        metadata.get("generator_version") != GENERATOR_VERSION
        or metadata.get("bundle_sha256") != fingerprint()
    ):
        raise ValueError("Replay requires the original generator/template bundle")
    today = metadata["date"]
    if date.fromisoformat(today).isoformat() != today:
        raise ValueError("Invalid replay date")
    data = validate_data(read_json(snapshot / "version-data.json"), today)
    config = normalize_config(read_json(snapshot / "config.json"), data)
    rendered = render(config, data, today)
    hashes = {
        path: hashlib.sha256(body.encode()).hexdigest()
        for path, body in rendered.items()
    }
    if hashes != metadata.get("files_sha256"):
        raise ValueError("Replay inputs do not match the saved output hashes")
    return config, data, today


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    versions = sub.add_parser("versions", help="Fetch compatibility data as JSON")
    versions.add_argument("--date", default=date.today().isoformat())
    versions.add_argument("--output", type=Path)
    generate = sub.add_parser("generate", help="Generate from a JSON configuration")
    generate.add_argument("--config", required=True, type=Path)
    generate.add_argument(
        "--versions",
        type=Path,
        help="Explicit saved version data; otherwise fetch live",
    )
    generate.add_argument("--date", default=date.today().isoformat())
    generate.add_argument("--output", default=Path.cwd(), type=Path)
    replay = sub.add_parser(
        "replay",
        help="Reproduce a project from its .scaffold directory without network access",
    )
    replay.add_argument("snapshot", type=Path)
    replay.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == "replay":
            clean_target(args.output.absolute())
            config, data, today = load_replay(args.snapshot)
            write_project(args.output.absolute(), config, data, today)
            return
        today = args.date
        if date.fromisoformat(today).isoformat() != today:
            raise ValueError("Date must use YYYY-MM-DD")
        if args.command == "versions":
            data = fetch_data(today)
            if args.output:
                if args.output.exists():
                    raise ValueError("Version output file already exists")
                args.output.write_text(json_text(data), encoding="utf-8", newline="\n")
                print(json_text(defaults(data)), end="")
            else:
                print(json_text(data), end="")
        else:
            clean_target(args.output.absolute())
            data = (
                validate_data(read_json(args.versions), today)
                if args.versions
                else fetch_data(today)
            )
            config = normalize_config(read_json(args.config), data)
            write_project(args.output.absolute(), config, data, today)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
