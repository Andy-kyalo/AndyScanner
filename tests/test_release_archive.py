import unittest

from tools.build_release_archive import safe_member


class TestReleaseArchiveSecurity(unittest.TestCase):
    def test_allows_normal_project_files(self):
        for name in (
            "main.py",
            "backend/scanner_engine.py",
            "tests/test_scanner_pipeline.py",
            "README.md",
            "config/settings.yaml",
        ):
            with self.subTest(name=name):
                self.assertTrue(safe_member(name))

    def test_rejects_environment_files_and_backups(self):
        for name in (
            ".env",
            ".env.local",
            ".env.production",
            "config/.env.backup",
            ".env.backup",
        ):
            with self.subTest(name=name):
                self.assertFalse(safe_member(name))

    def test_rejects_git_and_generated_directories(self):
        for name in (
            ".git/config",
            "backend/__pycache__/module.pyc",
            ".pytest_cache/v/cache/nodeids",
            "node_modules/package/index.js",
            ".venv/lib/module.py",
        ):
            with self.subTest(name=name):
                self.assertFalse(safe_member(name))

    def test_rejects_databases_logs_and_backups(self):
        for name in (
            "database/scanner.db",
            "database/snapshot.sqlite3",
            "logs/scanner.log",
            "reports/scan.log",
            "config/settings.yaml.bak",
            "config/settings.backup",
        ):
            with self.subTest(name=name):
                self.assertFalse(safe_member(name))

    def test_rejects_additional_sensitive_artifacts(self):
        for name in (
            "id_rsa",
            "keys/id_ed25519",
            "config/credentials.json",
            "config/secrets.yaml",
            "certificates/server.pem",
            "keys/private.key",
            "backup/export.p12",
            "database/production.sql",
            "reports/snapshot.dump",
            "config/settings.yaml.old",
            "backend/LOGS/scanner.log",
            "backend/CACHE/data.json",
        ):
            with self.subTest(name=name):
                self.assertFalse(safe_member(name))

    def test_rejects_absolute_and_traversal_paths(self):
        for name in (
            "/etc/passwd",
            "../outside.txt",
            "backend/../../outside.txt",
        ):
            with self.subTest(name=name):
                self.assertFalse(safe_member(name))


if __name__ == "__main__":
    unittest.main()


class TestReleaseArchiveIntegration(unittest.TestCase):
    def setUp(self):
        import tempfile
        from pathlib import Path

        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.script = Path(__file__).resolve().parents[1] / "tools" / "build_release_archive.py"

        for args in (
            ["git", "init", "-q"],
            ["git", "config", "user.email", "test@example.invalid"],
            ["git", "config", "user.name", "Archive Test"],
        ):
            result = self.run_command(args)
            self.assertEqual(result.returncode, 0, result.stderr)

        (self.root / ".gitignore").write_text("dist/\n")
        (self.root / "main.py").write_text("print('fixture')\n")
        (self.root / "backend").mkdir()
        (self.root / "backend" / "scanner.py").write_text("nested=True\n")
        (self.root / "id_rsa").write_text("must not be included\n")
        self.commit_fixture()

    def tearDown(self):
        self.temp.cleanup()

    def run_command(self, args, env=None):
        import subprocess
        return subprocess.run(
            args,
            cwd=self.root,
            capture_output=True,
            text=True,
            env=env,
        )

    def commit_fixture(self):
        result = self.run_command(["git", "add", "-A"])
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_command(["git", "commit", "-qm", "archive fixture"])
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_build_includes_nested_files_and_excludes_sensitive_files(self):
        import zipfile

        result = self.run_command(
            ["python", str(self.script), "dist/release.zip"]
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        output = self.root / "dist" / "release.zip"
        with zipfile.ZipFile(output) as archive:
            names = archive.namelist()
            self.assertIn("main.py", names)
            self.assertIn("backend/scanner.py", names)
            self.assertNotIn("id_rsa", names)
            self.assertIsNone(archive.testzip())
            manifest = archive.read("RELEASE-REVISION.txt").decode()
            expected_revision = self.run_command(
                ["git", "rev-parse", "HEAD"]
            ).stdout.strip()
            self.assertIn(f"Git revision: {expected_revision}", manifest)

        self.assertEqual(
            list(output.parent.glob(".release.zip.*.tmp")),
            [],
        )

    def test_existing_ignored_output_is_preserved(self):
        output = self.root / "dist" / "existing.zip"
        output.parent.mkdir()
        output.write_text("preserve this file")

        result = self.run_command(
            ["python", str(self.script), "dist/existing.zip"]
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("refusing to overwrite", result.stderr)
        self.assertEqual(output.read_text(), "preserve this file")

    def test_dirty_working_tree_is_rejected(self):
        (self.root / "uncommitted.txt").write_text("uncommitted")

        result = self.run_command(
            ["python", str(self.script), "dist/release.zip"]
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("working tree is not clean", result.stderr)
        self.assertFalse((self.root / "dist" / "release.zip").exists())

    def test_invalid_revision_is_rejected(self):
        result = self.run_command(
            [
                "python", str(self.script),
                "--revision", "not-a-real-revision",
                "dist/release.zip",
            ]
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("revision is not a valid commit", result.stderr)
        self.assertFalse((self.root / "dist" / "release.zip").exists())

    def test_failed_build_cleans_temporary_archive(self):
        import os
        import shutil

        real_git = shutil.which("git")
        self.assertIsNotNone(real_git)

        bin_dir = self.base / "bin"
        bin_dir.mkdir()
        wrapper = bin_dir / "git"
        wrapper.write_text(
            "#!/bin/sh\n"
            'if [ "$1" = "-C" ] && [ "$3" = "cat-file" ]; then\n'
            '  echo "simulated blob-read failure" >&2\n'
            "  exit 1\n"
            "fi\n"
            f'exec "{real_git}" "$@"\n'
        )
        wrapper.chmod(0o755)

        env = os.environ.copy()
        env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
        result = self.run_command(
            ["python", str(self.script), "dist/release.zip"],
            env=env,
        )

        output = self.root / "dist" / "release.zip"
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())
        self.assertEqual(
            list(output.parent.glob(".release.zip.*.tmp")),
            [],
        )

    def test_external_output_path_is_rejected(self):
        result = self.run_command(
            ["python", str(self.script), "../outside.zip"]
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("output path must be inside the repository", result.stderr)


if __name__ == "__main__":
    unittest.main()
