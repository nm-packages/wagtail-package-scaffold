"""Behavioral regression tests; all artifacts stay in temporary directories."""

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import scaffold
import versions

TODAY = "2026-09-29"
DATA = {
    "supported_wagtail_versions": [
        {
            "version": "7.4",
            "is_lts": True,
            "release_date": "2026-05-04",
            "support_end": "2027-11-02",
            "django_versions": ["5.2", "6.0"],
            "python_versions": ["3.10", "3.12", "3.14"],
        },
        {
            "version": "7.0",
            "is_lts": True,
            "release_date": "2025-05-06",
            "support_end": "2026-11-02",
            "django_versions": ["4.2", "5.2"],
            "python_versions": ["3.9", "3.10", "3.12"],
        },
    ],
    "django_python": {
        "6.0": ["3.12", "3.14"],
        "5.2": ["3.10", "3.12", "3.14"],
        "4.2": ["3.9", "3.10", "3.12"],
    },
    "sources": [versions.RELEASE_URL, versions.COMPATIBILITY_URL],
}


def config(**kwargs):
    return scaffold.normalize_config(
        dict(package_name="wagtail-example", **kwargs),
        versions.validate_data(DATA, TODAY),
    )


def tree(path):
    return {
        file.relative_to(path).as_posix(): file.read_bytes()
        for file in path.rglob("*")
        if file.is_file()
    }


class VersionTests(unittest.TestCase):
    def test_release_dates_lts_future_and_expired(self):
        html = "<table><tr><th>Version</th><th>Release date</th><th>Active support [1]</th><th>Security support [2]</th></tr>"
        for row in [
            ("8.1*", "2 November 2026", "2 February 2027", "4 May 2027"),
            ("7.4 LTS", "4 May 2026", "2 November 2027", "2 November 2027"),
            ("7.0 LTS", "6 May 2025", "2 November 2026", "2 November 2026"),
            ("6.3 LTS", "1 November 2024", "1 May 2026", "1 May 2026"),
        ]:
            html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        rows = versions.parse_releases(html + "</table>", TODAY)
        self.assertEqual([row["version"] for row in rows], ["7.0", "7.4"])
        self.assertTrue(all(row["is_lts"] for row in rows))
        self.assertEqual(rows[0]["release_date"], "2025-05-06")

    def test_footnotes_numeric_sort_and_malformed_data(self):
        self.assertEqual(
            versions.parse_version_list("3.14, 3.9, 3.12[1]"), ["3.9", "3.12", "3.14"]
        )
        self.assertEqual(
            versions.parse_django(
                "<table><tr><th>Django version</th><th>Python versions</th></tr>"
                "<tr><td>5.2</td><td>3.10, 3.14 (added in 5.2.8)</td></tr></table>"
            ),
            {"5.2": ["3.10", "3.14"]},
        )
        with self.assertRaises(ValueError):
            versions.parse_version_list("3.10 through 3.14")
        with self.assertRaises(ValueError):
            versions.parse_releases("<table><th>Changed headers</th></table>", TODAY)

    def test_exact_compatible_triples(self):
        triples = versions.combinations(
            versions.validate_data(DATA, TODAY),
            config(wagtail_min="7.0", django_min="4.2", python_min="3.9"),
        )
        expected = [
            ("3.9", "4.2", "7.0"),
            ("3.10", "4.2", "7.0"),
            ("3.10", "5.2", "7.0"),
            ("3.10", "5.2", "7.4"),
            ("3.12", "4.2", "7.0"),
            ("3.12", "5.2", "7.0"),
            ("3.12", "5.2", "7.4"),
            ("3.12", "6.0", "7.4"),
            ("3.14", "5.2", "7.4"),
            ("3.14", "6.0", "7.4"),
        ]
        self.assertEqual(triples, expected)
        with self.assertRaises(ValueError):
            config(wagtail_min="7.4", django_min="4.2")
        with self.assertRaises(ValueError):
            versions.validate_data({**DATA, "django_python": {}}, TODAY)

    def test_defaults_prefer_latest_supported_lts(self):
        data = versions.validate_data(DATA, TODAY)
        expected = {"wagtail_min": "7.4", "django_min": "5.2", "python_min": "3.10"}
        self.assertEqual(versions.defaults(data), expected)
        # Source order must not affect the selected LTS.
        data["supported_wagtail_versions"].reverse()
        self.assertEqual(versions.defaults(data), expected)
        selected = config()
        triples = versions.combinations(data, selected)
        self.assertTrue(all(versions.version_key(w) >= (7, 4) for _, _, w in triples))
        self.assertTrue(all(versions.version_key(d) >= (5, 2) for _, d, _ in triples))
        generated = scaffold.render(selected, data, TODAY)
        import tomllib

        project = tomllib.loads(generated["pyproject.toml"])["project"]
        self.assertEqual(project["dependencies"], ["Django>=5.2", "wagtail>=7.4"])
        self.assertEqual(project["requires-python"], ">=3.10")

    def test_forthcoming_and_yanked_django_series_are_omitted(self):
        row = copy.deepcopy(DATA["supported_wagtail_versions"][0])
        compatibility = {
            row["version"]: {
                "django_versions": ["5.2", "6.1"],
                "python_versions": ["3.12"],
            }
        }
        replies = {
            versions.RELEASE_URL: "release html",
            versions.COMPATIBILITY_URL: "compatibility html",
            "https://pypi.org/pypi/Django/json": json.dumps(
                {
                    "releases": {
                        "5.2.8": [{"yanked": False}],
                        "6.1rc1": [{"yanked": False}],
                        "6.1": [{"yanked": True}],
                    }
                }
            ),
            "https://docs.djangoproject.com/en/5.2/faq/install/": "django html",
        }
        with (
            patch.object(versions, "fetch", side_effect=replies.__getitem__),
            patch.object(versions, "parse_releases", return_value=[row]),
            patch.object(versions, "parse_compatibility", return_value=compatibility),
            patch.object(versions, "parse_django", return_value={"5.2": ["3.12"]}),
        ):
            result = versions.fetch_data(TODAY)
        self.assertEqual(
            result["supported_wagtail_versions"][0]["django_versions"], ["5.2"]
        )
        self.assertEqual(result["django_python"], {"5.2": ["3.12"]})

    def test_fetch_failure_does_not_guess(self):
        with patch.object(
            versions, "fetch", side_effect=OSError("network unavailable")
        ):
            with self.assertRaises(OSError):
                versions.fetch_data(TODAY)


class GeneratorTests(unittest.TestCase):
    def test_all_framework_sandbox_and_feature_choices_replay(self):
        data = versions.validate_data(DATA, TODAY)
        with tempfile.TemporaryDirectory() as temp:
            for framework in ("pytest", "unittest"):
                for sandbox in (True, False):
                    for features in (True, False):
                        with self.subTest(
                            framework=framework, sandbox=sandbox, features=features
                        ):
                            chosen = config(
                                test_framework=framework,
                                include_sandbox=sandbox,
                                include_api=features,
                                include_blocks=features,
                                include_admin=features,
                                include_models=features,
                            )
                            label = f"{framework}-{sandbox}-{features}"
                            destination, replay = (
                                Path(temp) / label,
                                Path(temp) / (label + "-replay"),
                            )
                            scaffold.write_project(destination, chosen, data, TODAY)
                            with patch.object(
                                versions,
                                "fetch",
                                side_effect=AssertionError("network used"),
                            ):
                                inputs = scaffold.load_replay(destination / ".scaffold")
                                scaffold.write_project(replay, *inputs)
                            self.assertEqual(tree(destination), tree(replay))
                            files = tree(destination)
                            self.assertEqual("sandbox/manage.py" in files, sandbox)
                            self.assertEqual(
                                "tests/conftest.py" in files, framework == "pytest"
                            )
                            self.assertEqual(
                                "src/wagtail_example/urls.py" in files, features
                            )
                            self.assertEqual(
                                "src/wagtail_example/models.py" in files, features
                            )
                            self.assertEqual(
                                "src/wagtail_example/wagtail_hooks.py" in files,
                                features,
                            )
                            for body in files.values():
                                self.assertNotIn(b"\r", body)
                                self.assertTrue(body.endswith(b"\n"))
                                self.assertFalse(body.endswith(b"\n\n"))

    def test_metadata_escaping_and_literal_braces(self):
        chosen = config(
            description='Quotes " and \\ and {literal} and triple """',
            author_name='Author "Quoted"',
        )
        files = scaffold.render(chosen, versions.validate_data(DATA, TODAY), TODAY)
        import tomllib

        metadata = tomllib.loads(files["pyproject.toml"])["project"]
        self.assertEqual(metadata["description"], chosen["description"])
        self.assertEqual(metadata["authors"][0]["name"], chosen["author_name"])
        self.assertIn("{literal}", files["README.md"])

    def test_invalid_config(self):
        for fields in [
            {"package_name": "class"},
            {"package_name": "3-invalid"},
            {"include_api": "false"},
            {"license": "Apache-2.0"},
            {"author_email": "bad"},
            {"description": "new\nline"},
            {"unrecognized": True},
        ]:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                scaffold.normalize_config(
                    {"package_name": "wagtail-example", **fields}, DATA
                )

    def test_existing_files_and_symlinks_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "target"
            target.mkdir()
            existing = target / "important.py"
            existing.write_text("keep me\n")
            before = tree(target)
            with self.assertRaises(ValueError):
                scaffold.write_project(target, config(), DATA, TODAY)
            self.assertEqual(tree(target), before)
            existing.unlink()
            (target / "linked").symlink_to(Path(temp))
            with self.assertRaises(ValueError):
                scaffold.clean_target(target)

    def test_installed_skill_is_allowed_other_agent_files_are_not(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)
            skill = target / ".codex/skills/wagtail-package-scaffolder"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("installed\n")
            (target / "README.md").write_text("installer docs\n")
            scaffold.clean_target(target)
            (target / ".codex/config.toml").write_text("unrelated\n")
            with self.assertRaises(ValueError):
                scaffold.clean_target(target)

    def test_replay_rejects_changed_bundle_and_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "generated"
            scaffold.write_project(
                target, config(), versions.validate_data(DATA, TODAY), TODAY
            )
            snapshot = target / ".scaffold"
            with patch.object(scaffold, "fingerprint", return_value="different"):
                with self.assertRaises(ValueError):
                    scaffold.load_replay(snapshot)
            changed = json.loads((snapshot / "config.json").read_text())
            changed["description"] = "Changed"
            (snapshot / "config.json").write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                scaffold.load_replay(snapshot)

    def test_template_error_leaves_destination_untouched(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "absent"
            with patch.object(
                scaffold, "render", side_effect=KeyError("missing_placeholder")
            ):
                with self.assertRaises(KeyError):
                    scaffold.write_project(target, config(), DATA, TODAY)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
