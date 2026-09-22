"""Regression checks for accidental expansion of the URL-only package boundary."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate_plugin import ValidationError, validate


class PluginValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "plugin"
        shutil.copytree(Path(__file__).resolve().parents[1], self.root,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "node_modules"))

    def rewrite(self, name, edit):
        path = self.root / name
        data = json.loads(path.read_text())
        edit(data)
        path.write_text(json.dumps(data))

    def assert_rejected(self):
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_reviewed_package_is_valid(self):
        validate(self.root)

    def test_endpoint_changes_are_rejected(self):
        for url in ("http://api.mantle.chat/mcp", "https://example.invalid/mcp",
                    "https://api.mantle.chat.evil.example/mcp", "https://api.mantle.chat/mcp?key=example"):
            with self.subTest(url=url):
                self.rewrite("mcp.json", lambda data: data["mcpServers"]["mantle-chat"].update(url=url))
                self.assert_rejected()

    def test_embedded_auth_is_rejected(self):
        self.rewrite("mcp.json", lambda data: data["mcpServers"]["mantle-chat"].update(
            headers={"Authorization": "Bearer EXAMPLE_ONLY"}))
        self.assert_rejected()

    def test_command_launcher_is_rejected(self):
        self.rewrite("mcp.json", lambda data: data["mcpServers"]["mantle-chat"].update(command="sh"))
        self.assert_rejected()

    def test_additional_server_is_rejected(self):
        self.rewrite("mcp.json", lambda data: data["mcpServers"].update(other={"url": "https://example.com"}))
        self.assert_rejected()

    def test_duplicate_json_keys_are_rejected(self):
        (self.root / "mcp.json").write_text('{"mcpServers": {}, "mcpServers": {}}')
        self.assert_rejected()

    def test_path_traversal_and_absolute_paths_are_rejected(self):
        for logo in ("../outside.svg", "/tmp/logo.svg"):
            with self.subTest(logo=logo):
                self.rewrite(".cursor-plugin/plugin.json", lambda data: data.update(logo=logo))
                self.assert_rejected()

    def test_symlink_is_rejected(self):
        (self.root / "assets" / "outside").symlink_to(Path(self.temp.name))
        self.assert_rejected()

    def test_new_hook_surface_is_rejected(self):
        (self.root / "hooks").mkdir()
        self.assert_rejected()

    def test_credential_file_is_rejected(self):
        (self.root / ".env.local").write_text("EXAMPLE_ONLY=true")
        self.assert_rejected()

    def test_skill_identity_mismatch_is_rejected(self):
        path = self.root / "skills/use-mantle/SKILL.md"
        path.write_text(path.read_text().replace("name: use-mantle", "name: unrelated"))
        self.assert_rejected()

    def test_broken_documentation_link_is_rejected(self):
        with (self.root / "README.md").open("a") as output:
            output.write("\n[Missing](docs/missing.md)\n")
        self.assert_rejected()

    def test_unreviewed_note_is_rejected(self):
        (self.root / "docs/notes.md").write_text("Notes that have not been reviewed for publication.")
        self.assert_rejected()

    def test_unreviewed_attachment_is_rejected(self):
        (self.root / "assets/recording.txt").write_text("An unreviewed attachment.")
        self.assert_rejected()


if __name__ == "__main__":
    unittest.main()
