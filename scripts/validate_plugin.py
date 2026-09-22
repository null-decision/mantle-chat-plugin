#!/usr/bin/env python3
"""Validate this repository's intentionally URL-only plugin contracts.

Offline, standard-library only. Not a general client schema or secret scanner.
"""

import json
import re
import sys
from pathlib import Path, PurePosixPath


PUBLIC_FILES = frozenset({
    ".claude-plugin/marketplace.json",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".cursor-plugin/plugin.json",
    ".mcp.json",
    ".github/workflows/validate.yml",
    ".gitignore",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "assets/logo-256.png",
    "assets/logo.svg",
    "docs/clients.md",
    "docs/connecting.md",
    "docs/grok-bot-template.md",
    "docs/privacy.md",
    "docs/testing.md",
    "docs/tools.md",
    "examples/opencode-v1.json",
    "examples/opencode-v2.json",
    "mcp.json",
    "scripts/validate_plugin.py",
    "skills/edit-mantle-agent/SKILL.md",
    "skills/use-mantle/SKILL.md",
    "tests/validate_plugin_test.py",
})


class ValidationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ValidationError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "JSON contains a duplicate key")
        result[key] = value
    return result


def package_path(root, value):
    require(isinstance(value, str) and bool(value), "Package path must be a string")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts and "\\" not in value,
            "Package path must be relative and stay inside the repository")
    target = root / path
    require(target.resolve().is_relative_to(root), "Package path escapes the repository")
    require(target.exists(), f"Missing package file or directory: {value}")
    return target


def read_json(root, path):
    try:
        return json.loads(package_path(root, path).read_text(encoding="utf-8"),
                          object_pairs_hook=unique_object)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValidationError(f"Invalid JSON: {path}") from error


def validate(root):
    root = Path(root).resolve()
    # Check symlinks before reading any content outside the checkout.
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in relative.parts):
            continue
        require(not path.is_symlink(), f"Symlinks are not allowed: {relative}")
        require(not (path.name == ".env" or path.name.startswith(".env.") or
                     path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}),
                f"Credential-like file is not allowed: {relative}")
        if path.is_file():
            require(relative.as_posix() in PUBLIC_FILES,
                    f"File needs publication review before inclusion: {relative}")

    for name in sorted(PUBLIC_FILES):
        require(package_path(root, name).is_file(), f"Missing public package file: {name}")

    manifest = read_json(root, ".cursor-plugin/plugin.json")
    require(isinstance(manifest, dict), "Manifest must be an object")
    allowed = {"name", "version", "description", "author", "homepage", "repository",
               "license", "keywords", "logo", "skills", "mcpServers"}
    require(set(manifest) <= allowed, "Unexpected manifest field; review package capabilities")
    require(manifest.get("name") == "mantle-chat", "Unexpected plugin identity")
    require(isinstance(manifest.get("version"), str) and
            re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", manifest["version"]),
            "Version must have major.minor.patch form")
    require(isinstance(manifest.get("description"), str) and manifest["description"].strip(),
            "A description is required")
    require(manifest.get("license") == "MIT", "Review changes to the MIT license")
    require(manifest.get("homepage") == "https://mantle.chat", "Unexpected homepage")
    require(manifest.get("repository") ==
            "https://github.com/null-decision/mantle-chat-plugin", "Unexpected repository")
    author = manifest.get("author")
    require(isinstance(author, dict) and author.get("name") == "Mantle Chat", "Missing publisher")
    require(set(author) <= {"name", "email"}, "Unexpected author metadata")
    require(author.get("email") == "support@mantle.chat", "Use the public support contact")
    keywords = manifest.get("keywords")
    require(isinstance(keywords, list) and bool(keywords) and
            all(isinstance(word, str) and word.strip() for word in keywords), "Invalid keywords")
    logo = package_path(root, manifest.get("logo"))
    require(logo.is_file(), "Logo must be a committed file")
    require(manifest.get("skills") == "skills/", "Skills must be explicitly discoverable")
    require(manifest.get("mcpServers") == "mcp.json", "MCP config must be explicit")

    mcp = read_json(root, "mcp.json")
    require(mcp == {"mcpServers": {"mantle-chat": {"url": "https://api.mantle.chat/mcp"}}},
            "MCP must contain exactly one production HTTPS URL; no credentials or commands")
    shared_mcp = read_json(root, ".mcp.json")
    require(shared_mcp == {"mcpServers": {"mantle-chat": {
        "type": "http", "url": "https://api.mantle.chat/mcp"}}},
        "Claude/Codex MCP must contain only the public HTTP connection")

    metadata_fields = {"name", "version", "description", "author", "homepage", "repository", "license", "keywords"}
    for client in ("claude", "codex"):
        adapter = read_json(root, f".{client}-plugin/plugin.json")
        adapter_fields = metadata_fields | {"skills", "mcpServers"}
        if client == "codex":
            adapter_fields |= {"interface"}
        require(isinstance(adapter, dict) and set(adapter) == adapter_fields,
                f"Unexpected {client} manifest fields")
        require(all(adapter[field] == manifest[field] for field in metadata_fields),
                f"{client} identity, version, and metadata must match Cursor")
        require(adapter["skills"] == "./skills/" and adapter["mcpServers"] == "./.mcp.json",
                f"{client} must use the reviewed shared skills and connection")
        if client == "codex":
            interface = adapter["interface"]
            required_interface = {"displayName", "shortDescription", "longDescription", "developerName",
                                  "category", "capabilities", "websiteURL", "privacyPolicyURL",
                                  "termsOfServiceURL", "defaultPrompt", "brandColor", "composerIcon", "logo", "logoDark"}
            require(isinstance(interface, dict) and set(interface) == required_interface,
                    "Unexpected Codex presentation metadata")
            require(interface["displayName"] == "Mantle Chat" and interface["developerName"] == "Mantle Chat",
                    "Unexpected Codex publisher")
            require(interface["category"] == "Productivity" and interface["capabilities"] == ["Read", "Write"],
                    "Review changes to Codex capabilities")
            for field, url in {"websiteURL": "https://mantle.chat", "privacyPolicyURL": "https://mantle.chat/privacy",
                               "termsOfServiceURL": "https://mantle.chat/terms"}.items():
                require(interface[field] == url, "Unexpected Codex public URL")
            for field in ("shortDescription", "longDescription"):
                require(isinstance(interface[field], str) and interface[field].strip(), "Missing Codex description")
            prompts = interface["defaultPrompt"]
            require(isinstance(prompts, list) and 1 <= len(prompts) <= 3 and
                    all(isinstance(prompt, str) and 1 <= len(prompt) <= 128 for prompt in prompts),
                    "Codex needs one to three short starter prompts")
            require(isinstance(interface["brandColor"], str) and
                    re.fullmatch(r"#[0-9A-Fa-f]{6}", interface["brandColor"]), "Invalid brand color")
            for field in ("composerIcon", "logo", "logoDark"):
                require(interface[field] == "./assets/logo-256.png", "Use the reviewed PNG logo")
                require(package_path(root, interface[field]).is_file(), "Missing Codex logo")

    marketplace = read_json(root, ".claude-plugin/marketplace.json")
    require(marketplace == {"name": "mantle-chat", "description": "Mantle Chat tools and skills for your workspace.",
        "owner": manifest["author"], "plugins": [{
        "name": "mantle-chat", "source": "./", "description": manifest["description"], "version": manifest["version"]}]},
        "Claude marketplace must point only to this package and release")

    opencode_server = {"mantle-chat": {"type": "remote", "url": "https://api.mantle.chat/mcp"}}
    for version, servers in ((1, opencode_server), (2, {"servers": opencode_server})):
        require(read_json(root, f"examples/opencode-v{version}.json") == {
            "$schema": "https://opencode.ai/config.json", "mcp": servers},
            f"OpenCode {version} example must use its own format and only the public endpoint")

    for directory in ("hooks", "commands", "agents", "rules"):
        require(not (root / directory).exists(), f"Unexpected executable/instruction surface: {directory}")
    for alternate in ("plugin.json", ".cursor-plugin/marketplace.json"):
        require(not (root / alternate).exists(), f"Unexpected alternate discovery file: {alternate}")

    skills_root = package_path(root, "skills/")
    expected_skills = {"use-mantle", "edit-mantle-agent"}
    require({path.name for path in skills_root.iterdir()} == expected_skills,
            "Expected exactly the two reviewed skill directories")
    for name in sorted(expected_skills):
        text = package_path(root, f"skills/{name}/SKILL.md").read_text(encoding="utf-8")
        parts = text.split("---", 2)
        require(len(parts) == 3 and parts[0] == "" and parts[2].strip(), "Missing skill frontmatter/body")
        # This project uses a restricted frontmatter style; a full YAML parser is unnecessary.
        header = parts[1]
        require(re.findall(r"^name: (.+)$", header, re.M) == [name], "Skill name must match its folder")
        require(re.findall(r"^description: (.+)$", header, re.M) == [">-"],
                "Use a folded skill description")
        require(bool(re.search(r"^  \S.+$", header, re.M)), "Missing skill description text")
        require(re.findall(r"^(\w+):", header, re.M) == ["name", "description"],
                "Unexpected skill metadata")

    # Verify local Markdown destinations (external URLs and intra-page anchors are out of scope).
    markdown_files = [root / name for name in ("README.md", "SECURITY.md", "CONTRIBUTING.md", "CHANGELOG.md")]
    markdown_files += list((root / "docs").glob("*.md"))
    for path in markdown_files:
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", link) or link.startswith("#"):
                continue
            destination = path.parent / link.split("#", 1)[0]
            require(destination.resolve().is_relative_to(root) and destination.exists(),
                    f"Broken or escaping local link in {path.relative_to(root)}")


if __name__ == "__main__":
    try:
        require(len(sys.argv) <= 2, "Usage: validate_plugin.py [plugin-directory]")
        validate(Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[1])
    except (ValidationError, OSError) as error:
        print(f"Plugin validation failed: {error}", file=sys.stderr)
        sys.exit(1)
    print("Plugin package validation passed (offline; live compatibility not assessed).")
