# Choose your assistant

Mantle connects through MCP, a standard that lets your assistant use tools in your Mantle account. You sign in through your browser. Never paste a password, access token, or API key into chat or a configuration file.

These are preview installation options. Cursor has been tested with browser sign-in and creating and reading a canvas. Claude, Codex, ChatGPT, OpenCode, and Grok Bot still need complete connection and workflow testing. Package validation alone does not prove a connection works. Official directory listings are not available yet.

If you already have a Mantle connection in your assistant, use it instead of adding a second one. After connecting, ask **“Show my Mantle workspaces”** and check which account and workspace you are using before making changes.

## Cursor

Use [Mantle Chat on Cursor Directory](https://cursor.directory/plugins/mantle-chat), or follow the [manual setup](connecting.md#optional-connect-mcp-tools-in-cursor-manually). The community listing provides the connection and two optional skills.

## Claude Code

The repository includes a Claude plugin with the connection and both skills. After this package version is available on the repository's default branch, add the Mantle marketplace and install the plugin:

```text
/plugin marketplace add null-decision/mantle-chat-plugin
/plugin install mantle-chat@mantle-chat
```

Open `/mcp`, select the Mantle connection, and finish browser sign-in. Use `/mantle-chat:use-mantle` for workspace help or `/mantle-chat:edit-mantle-agent` for agent draft changes. Team policy may restrict installation.

This is a direct installation from Mantle's repository. It does not mean the plugin is listed or endorsed in Anthropic's directory. See [Claude's plugin guide](https://code.claude.com/docs/en/plugins).

## Claude.ai and Cowork

For tools without installing skills, open Claude's **Customize → Connectors**, choose the option to add a custom connector, and enter:

```text
https://api.mantle.chat/mcp
```

Connect and complete the Mantle sign-in. Custom connectors and plugin installation can depend on your plan, client, or administrator's settings. A future directory listing will provide the normal install flow; do not look for a published Mantle listing yet. See [Claude's custom connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

## Codex

The plugin adds the Mantle tools and both skills. After this package version is available on the repository's default branch, install it from Mantle's marketplace:

```sh
codex plugin marketplace add null-decision/mantle-chat-plugin
codex plugin add mantle-chat@mantle-chat
```

Start a new Codex session to load the plugin and complete browser sign-in when prompted. This installs from Mantle's repository; it does not mean the plugin is listed or endorsed in OpenAI's directory.

If you only want the tools, use a direct MCP connection instead:

```sh
codex mcp add mantle-chat --url https://api.mantle.chat/mcp
codex mcp login mantle-chat
```

Complete the browser sign-in, then start a new Codex session. Your organization may control which connections are allowed.

A direct MCP connection does not install the two skills. Choose one installation method to avoid duplicate Mantle connections. The public OpenAI directory installation will become available after review and publication. See [Codex MCP setup](https://developers.openai.com/codex/mcp).

## ChatGPT

If your account has developer mode and permission to add custom MCP connections, add a connection with the URL below and select OAuth authentication:

```text
https://api.mantle.chat/mcp
```

Complete sign-in, enable the connection in a conversation, and ask for your Mantle workspaces. This is an early testing option, not the normal directory installation. Availability depends on your account and workspace settings. See [OpenAI's connection guide](https://developers.openai.com/plugins/deploy/connect-chatgpt).

## OpenCode

Check your version with `opencode --version`. Merge the matching example into your existing `opencode.json`, preserving other settings:

- OpenCode 1.x: [V1 example](../examples/opencode-v1.json). The server is directly under `mcp`.
- OpenCode 2.x: [V2 example](../examples/opencode-v2.json). The server is under `mcp.servers`.

Both examples connect only to `https://api.mantle.chat/mcp` and contain no credentials. Then run:

```sh
opencode mcp auth mantle-chat
opencode mcp list
```

Finish browser sign-in. When Mantle shows as connected, start a conversation and ask for your workspaces. For the optional skills, copy each complete skill directory from this repository into `.opencode/skills/` in the project where you want to use it. Review existing files before copying; do not overwrite another skill with the same name.

See the official [V1 MCP guide](https://opencode.ai/docs/mcp-servers/), [V2 MCP guide](https://opencode.ai/v2/docs/mcp-servers/), and [skills guide](https://opencode.ai/v2/docs/skills/).

## Grok Bot

Grok Bot setup is still being tested. A community Cursor listing does not automatically install the plugin in Grok Bot. See the [Grok Bot instructions](grok-bot-template.md) for the intended workflow and current limitations.

## If something goes wrong

See [connection troubleshooting](connecting.md#troubleshooting), the [tool reference](tools.md), and [how data is handled](privacy.md). Contact [support@mantle.chat](mailto:support@mantle.chat) with your client version and a redacted description of the problem.
