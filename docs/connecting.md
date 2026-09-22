# Connect Mantle Chat

You need a Mantle account, access to a workspace, and permission to install plugins in your AI client. Editing an agent also requires permission to change that agent.

The community preview is available on [Cursor Directory](https://cursor.directory/plugins/mantle-chat). The official marketplace listing is not available yet. Grok Bot setup is still being tested.

For Claude, Codex, ChatGPT, or OpenCode, start with [Choose your assistant](clients.md). The account selection and troubleshooting advice below applies to all clients.

## Connect through Cursor Directory

1. Open [Mantle Chat on Cursor Directory](https://cursor.directory/plugins/mantle-chat).
2. In **MCP Servers**, choose **Add to Cursor** and review the connection. It should be named `mantle-chat` and use `https://api.mantle.chat/mcp`.
3. Connect the server in Cursor and complete the browser sign-in.

This adds the tools. To add the workflow instructions too, open the listing's **Skills** tab and copy each complete skill into its own file:

- `~/.cursor/skills/use-mantle/SKILL.md`
- `~/.cursor/skills/edit-mantle-agent/SKILL.md`

Restart Cursor and check **Customize → Skills**. These files are local to your computer; see [Cursor's skills guide](https://cursor.com/docs/skills) to use them with Cloud Agents. If Mantle is already connected, keep that connection rather than adding a duplicate.

## Official plugin installation

When the plugin is available in your account, find **Mantle Chat** in Cursor or Grok Bot's **Plugins** list and add it. Choose **Connect** or **Authorize** and finish signing in through your browser.

This installation option is not available yet. If you belong to a team, your administrator may also need to allow the plugin. Contact [support@mantle.chat](mailto:support@mantle.chat) about availability.

Never paste a password, browser cookie, access token, or API key into the conversation.

## Choose a workspace

Ask your assistant to list your workspaces and choose the intended one. If workspace discovery is unavailable and it asks for an ID:

1. Open the workspace in Mantle.
2. Look for `/w/` in the page URL.
3. Copy the ID immediately after `/w/`, stopping at the next slash.

An ID identifies the workspace; it does not grant access to it. Use your own account and a workspace you have permission to access.

Your assistant's Mantle connection can use a different account from the Mantle website open in your browser. Check the returned workspace names before creating or changing anything. To switch accounts, disconnect and sign in again with the intended Mantle account.

## Optional: connect MCP tools in Cursor manually

This option connects the tools without installing the plugin's workflow instructions. If the plugin is already installed, keep that connection rather than adding a duplicate.

Merge this entry into your user-level Cursor MCP configuration at `~/.cursor/mcp.json`, preserving any existing servers:

```json
{
  "mcpServers": {
    "mantle-chat": {
      "url": "https://api.mantle.chat/mcp"
    }
  }
}
```

Complete the browser sign-in when prompted. No token belongs in this file. This configuration is for Cursor; use the Plugins interface for Grok Bot.

## Troubleshooting

| Problem | What to try |
| --- | --- |
| Mantle Chat is missing from Plugins | Check availability with support and your team administrator. |
| Sign-in does not finish | Reopen the connection's sign-in page. If it still fails, contact support. |
| Access denied | Check that you signed in with the right account and have access to the selected workspace or agent. |
| My usual workspaces are missing | Check which Mantle account you connected. Reconnect with the intended account; a different workspace ID will not switch accounts. |
| A draft has changed or is locked | Open the review link in Mantle and check the latest draft before trying again. |
| A request is temporarily unavailable | Wait for the suggested retry time. Avoid repeatedly submitting the same edit. |

For support, include the client version, what you were trying to do, and the error code or request ID if shown. Remove account details from screenshots and never send credentials or raw response dumps.

## Disconnect

Remove or disconnect Mantle Chat from your client's Plugins settings. This does not undo completed changes or remove information already returned in a conversation. If you suspect someone else has access to your connection, contact support for help revoking it.
