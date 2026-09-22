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

    def test_standalone_skill_cannot_depend_on_outside_files(self):
        with (self.root / "skills/use-mantle/SKILL.md").open("a") as output:
            output.write("\n[Outside](../../docs/tools.md)\n")
        self.assert_rejected()

    def test_missing_skill_resource_is_rejected(self):
        with (self.root / "skills/use-mantle/SKILL.md").open("a") as output:
            output.write("\n[Missing](references/missing.md)\n")
        self.assert_rejected()

    def test_skill_dependency_cannot_redirect_or_add_credentials(self):
        for name in ("use-mantle", "edit-mantle-agent"):
            path = self.root / f"skills/{name}/agents/openai.yaml"
            original = path.read_text()
            for altered in (
                original.replace("https://api.mantle.chat/mcp", "https://example.invalid/mcp"),
                original + '      headers: {Authorization: "Bearer EXAMPLE_ONLY"}\n',
                original + '    - type: "mcp"\n      value: "unreviewed-server"\n',
            ):
                with self.subTest(skill=name):
                    path.write_text(altered)
                    self.assert_rejected()
                    path.write_text(original)

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

    def test_adapter_version_mismatch_is_rejected(self):
        for client in ("claude", "codex"):
            with self.subTest(client=client):
                path = self.root / f".{client}-plugin/plugin.json"
                original = path.read_text()
                self.rewrite(path.relative_to(self.root), lambda data: data.update(version="9.9.9"))
                self.assert_rejected()
                path.write_text(original)

    def test_adapter_cannot_load_another_connection_or_skill_path(self):
        for client in ("claude", "codex"):
            for field in ("skills", "mcpServers"):
                with self.subTest(client=client, field=field):
                    path = self.root / f".{client}-plugin/plugin.json"
                    original = path.read_text()
                    self.rewrite(path.relative_to(self.root), lambda data: data.update({field: "../outside"}))
                    self.assert_rejected()
                    path.write_text(original)

    def test_shared_mcp_rejects_credentials_and_commands(self):
        path = self.root / ".mcp.json"
        original = path.read_text()
        for extra in ({"headers": {"Authorization": "Bearer EXAMPLE_ONLY"}}, {"command": "sh"},
                      {"url": "https://example.invalid/mcp"}):
            with self.subTest(extra=extra):
                self.rewrite(".mcp.json", lambda data: data["mcpServers"]["mantle-chat"].update(extra))
                self.assert_rejected()
                path.write_text(original)

    def test_claude_marketplace_cannot_redirect_installation(self):
        self.rewrite(".claude-plugin/marketplace.json", lambda data: data["plugins"][0].update(
            source={"source": "url", "url": "https://example.invalid/plugin.git"}))
        self.assert_rejected()

    def test_codex_cannot_add_hooks_or_apps(self):
        path = self.root / ".codex-plugin/plugin.json"
        original = path.read_text()
        for field in ("hooks", "apps"):
            with self.subTest(field=field):
                self.rewrite(path.relative_to(self.root), lambda data: data.update({field: "./extra.json"}))
                self.assert_rejected()
                path.write_text(original)

    def test_codex_cannot_load_external_assets(self):
        self.rewrite(".codex-plugin/plugin.json", lambda data: data["interface"].update(
            logo="https://example.invalid/logo.png"))
        self.assert_rejected()

    def test_opencode_examples_reject_credentials_and_extra_plugins(self):
        for version in (1, 2):
            path = self.root / f"examples/opencode-v{version}.json"
            original = path.read_text()
            with self.subTest(version=version, change="headers"):
                data = json.loads(original)
                servers = data["mcp"] if version == 1 else data["mcp"]["servers"]
                servers["mantle-chat"]["headers"] = {"Authorization": "Bearer EXAMPLE_ONLY"}
                path.write_text(json.dumps(data))
                self.assert_rejected()
                path.write_text(original)
            with self.subTest(version=version, change="plugin"):
                self.rewrite(path.relative_to(self.root), lambda data: data.update(plugin=["unreviewed-package"]))
                self.assert_rejected()
                path.write_text(original)

    def test_opencode_versions_are_not_interchangeable(self):
        (self.root / "examples/opencode-v2.json").write_text(
            (self.root / "examples/opencode-v1.json").read_text())
        self.assert_rejected()


if __name__ == "__main__":
    unittest.main()
