"""Smoke-test installation of local changes without downloading main."""

import os
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
INSTALLER = SKILL.parents[1] / "install.sh"


class InstallerTests(unittest.TestCase):
    def test_bundle_install_both_agents_and_failed_replacement(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive = root / "bundle.tar.gz"
            with tarfile.open(archive, "w:gz") as bundle:
                for file in SKILL.rglob("*"):
                    if file.is_file() and "__pycache__" not in file.parts:
                        relative = file.relative_to(SKILL)
                        bundle.add(
                            file,
                            arcname=(
                                "wagtail-package-scaffold-main/skills/"
                                f"wagtail-package-scaffolder/{relative.as_posix()}"
                            ),
                        )
            mock_bin = root / "bin"
            mock_bin.mkdir()
            curl = mock_bin / "curl"
            curl.write_text(
                "#!/usr/bin/env python3\nimport os, shutil, sys\n"
                "if os.environ.get('SCAFFOLD_TEST_FAIL'): sys.exit(1)\n"
                "shutil.copyfile(os.environ['SCAFFOLD_TEST_ARCHIVE'], sys.argv[-1])\n"
            )
            curl.chmod(0o755)
            environment = {
                **os.environ,
                "PATH": f"{mock_bin}:{os.environ['PATH']}",
                "SCAFFOLD_TEST_ARCHIVE": str(archive),
            }
            for agent in ("codex", "claude"):
                target = root / f"{agent} path with spaces"
                command = [
                    "bash",
                    str(INSTALLER),
                    "--agent",
                    agent,
                    "--target",
                    str(target),
                    "--force",
                ]
                result = subprocess.run(
                    command, env=environment, capture_output=True, text=True
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                installed = target / f".{agent}/skills/wagtail-package-scaffolder"
                for file in SKILL.rglob("*"):
                    if file.is_file() and "__pycache__" not in file.parts:
                        self.assertEqual(
                            (installed / file.relative_to(SKILL)).read_bytes(),
                            file.read_bytes(),
                        )
                help_result = subprocess.run(
                    ["python3", str(installed / "scripts/scaffold.py"), "--help"],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(help_result.returncode, 0, help_result.stderr)
                before = (installed / "assets/manifest.json").read_bytes()
                failure = subprocess.run(
                    command,
                    env={**environment, "SCAFFOLD_TEST_FAIL": "1"},
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(failure.returncode, 0)
                self.assertEqual(
                    (installed / "assets/manifest.json").read_bytes(), before
                )


if __name__ == "__main__":
    unittest.main()
