# Contributing

This plugin contains the Mantle MCP connection, two assistant skills, and documentation. Keep contributions focused on those features.

## Run the checks

Use Python 3.10+; no package installation is needed:

```sh
python3 scripts/validate_plugin.py
python3 -m unittest discover -s tests -p '*_test.py'
```

CI also scans Git history and package files with Gitleaks. To run those scans with your own Gitleaks installation:

```sh
gitleaks git --redact --log-opts=--all .
gitleaks dir --redact .
```

Do not commit scanner reports or credentials. Use made-up data in examples and screenshots.

## Submit a change

- Keep the connection pointed at the documented public Mantle MCP URL. Do not add credentials, command launchers, or other servers.
- Match tool instructions to the connected server's schema. Preserve the draft review step and handling of untrusted tool text.
- Write documentation in plain language. Put technical details in the tool reference rather than the quick start.
- Include a short explanation and check results in your pull request. Follow [testing](docs/testing.md) for connection and workflow changes.
- The validator checks an explicit list of public package files. Add a file to that list only after reviewing its contents for publication.

Contributions are distributed under the repository's [MIT license](LICENSE). Confirm you have the rights to contributed code and assets. Report security issues through [SECURITY.md](SECURITY.md).
