import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_openai_package import build


class OpenAIPackageTest(unittest.TestCase):
    def test_update_keeps_identity_and_includes_explicit_oauth_without_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "plugin.zip"
            build(ROOT, output, "existing-mantle-listing")
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(set(archive.namelist()), {
                    ".codex-plugin/plugin.json", ".mcp.json", "assets/logo-256.png",
                    "skills/use-mantle/SKILL.md", "skills/use-mantle/agents/openai.yaml",
                    "skills/edit-mantle-agent/SKILL.md", "skills/edit-mantle-agent/agents/openai.yaml",
                })
                manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
                self.assertEqual(manifest["name"], "existing-mantle-listing")
                self.assertEqual(manifest["mcpServers"], "./.mcp.json")
                server = json.loads(archive.read(".mcp.json"))["mcpServers"]["mantle-chat"]
                self.assertEqual(server, {
                    "type": "http", "url": "https://api.mantle.chat/mcp",
                    "extensions": {"com.openai": {"auth": {"type": "oauth", "client": {"mode": "cimd"}}}},
                })

    def test_invalid_package_identity_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "plugin.zip"
            with self.assertRaises(ValueError):
                build(ROOT, output, "../bad")
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
