# Report a security issue

Please report suspected vulnerabilities privately to [support@mantle.chat](mailto:support@mantle.chat), with **Plugin security report** in the subject.

Include the affected plugin version, what happened, and steps to reproduce using made-up data. Add a request ID if available. Do not include passwords, tokens, customer data, or private conversation contents in a public issue.

If a credential may have been exposed, revoke it with the service that issued it. Deleting a file or uninstalling the plugin does not revoke a credential.

## Scope

Reports about this plugin's connection settings, skills, or Mantle MCP behavior are welcome. For issues in Cursor, Grok Bot, or another service, contact that provider as well.

The plugin connects to `https://api.mantle.chat/mcp`. Mantle enforces account and resource permissions. The skills guide the assistant to treat returned text as data and to get agreement before applying draft changes; they do not replace those permissions.

See [data handling](docs/privacy.md) and [connection help](docs/connecting.md).
