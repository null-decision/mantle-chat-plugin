#!/usr/bin/env python3
"""Build a credential-free ZIP for OpenAI's plugin submission portal."""

import argparse
import json
import re
import zipfile
from pathlib import Path

from validate_plugin import validate


def build(root, output, package_name=None):
    root = Path(root).resolve()
    validate(root)
    manifest = json.loads((root / ".codex-plugin/plugin.json").read_text())
    if package_name is not None:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", package_name):
            raise ValueError("Use the exact package name shown in your existing OpenAI listing")
        manifest["name"] = package_name
    manifest["interface"]["supportURL"] = "https://mantle.chat/contact"
    mcp = {"mcpServers": {"mantle-chat": {
        "type": "http",
        "url": "https://api.mantle.chat/mcp",
        "extensions": {"com.openai": {"auth": {
            "type": "oauth", "client": {"mode": "cimd"}
        }}}
    }}}
    files = [root / "assets/logo-256.png"]
    files.extend(sorted((root / "skills").rglob("*")))
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(".codex-plugin/plugin.json", json.dumps(manifest, indent=2) + "\n")
        archive.writestr(".mcp.json", json.dumps(mcp, indent=2) + "\n")
        for path in files:
            if path.is_file():
                archive.write(path, path.relative_to(root).as_posix())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="ZIP destination outside this repository")
    parser.add_argument("--package-name", help="Existing OpenAI package name, when updating a migrated listing")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.output.resolve().is_relative_to(root):
        parser.error("Write the ZIP outside this repository")
    build(root, args.output, args.package_name)
    print(f"Created {args.output}")
