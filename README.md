<p align="center"><img src="assets/logo-256.png" alt="Mantle Chat" width="80" height="80" /></p>

# Mantle Chat for Cursor and Grok Bot

Ask your AI assistant to find things in [Mantle Chat](https://mantle.chat), organize your workspace, save writing in a new canvas, and get help from your saved agents.

**Preview:** find the connection and skills on [Cursor Directory](https://cursor.directory/plugins/mantle-chat), or [connect Mantle in Cursor manually](docs/connecting.md#optional-connect-mcp-tools-in-cursor-manually). The official marketplace listing is not available yet, and Grok Bot setup is still being tested. Available features depend on your account permissions.

## What you can do

- **Find your work.** Browse workspaces, folders, chats, channels, canvases, agents, and tasks.
- **Ask an agent.** Send a prompt to a saved Mantle agent, read its answer, or cancel the request.
- **Save your writing.** Put a poem, meeting notes, or a draft into a new canvas. A canvas is a document in your workspace.
- **Read and share updates.** Read recent messages or canvas content when enabled, and send a plain-text message to a channel.
- **Keep things organized.** Create folders, blank chats, channels, and canvases. Rename items, archive or restore them, and move them into folders.
- **Manage your workspace.** Change its name or icon, delete items, and update workspace access settings using your assistant’s confirmation controls.
- **Update an agent draft.** Prepare changes, review them, and save them to a draft. Publish separately in Mantle.
- **Check task progress.** See whether recent runs completed, failed, or are still running.

Try asking:

> “Create a Planning folder and move this channel into it.”
>
> “Write a short poem and save it in a new canvas.”
>
> “Ask my Research agent to summarize this question.”
>
> “Read the latest messages in Product feedback.”

## Connect your account

1. Open [Mantle Chat on Cursor Directory](https://cursor.directory/plugins/mantle-chat) and choose **Add to Cursor**. This adds the Mantle connection; the **Skills** tab provides the two optional instruction files.
2. Choose **Connect** or **Authorize** in Cursor, then sign in to Mantle in your browser.
3. Ask your assistant to list your workspaces and choose the one to use.

You need a Mantle account with access to that workspace. You never need to paste passwords or API keys into the conversation. See [connecting and troubleshooting](docs/connecting.md) for setup options.

## You stay in control

Mantle checks your permissions for each action. Confirm permanent deletions and workspace visibility or indexing changes in your connected assistant. There is no separate Mantle approval page. Your client’s automatic-run settings may skip confirmation prompts. Deleting a folder keeps its contents and moves them to the workspace root. Archiving a canvas turns off its public share links; restoring it does not turn them back on.

Information you retrieve is shared with your AI assistant. A saved agent can use its configured tools, including tools that change connected services. Read [how your data is handled](docs/privacy.md).

The plugin can add text when creating a canvas, but cannot rewrite an existing canvas. It also cannot send chat messages, move items between workspaces, manage members or billing, delete entire workspaces, or start scheduled tasks. See the [tool reference](docs/tools.md) for the full scope.

## Help

- [Connecting and troubleshooting](docs/connecting.md)
- [Tool reference](docs/tools.md)
- [Learn about Mantle Chat](https://docs.mantle.chat)
- [Example Grok Bot instructions](docs/grok-bot-template.md)
- [Contributing](CONTRIBUTING.md) · [Report a security issue](SECURITY.md)

Contact [support@mantle.chat](mailto:support@mantle.chat).

This plugin is [MIT-licensed](LICENSE). [Mantle service terms](https://mantle.chat/terms) and your client's terms apply separately.
