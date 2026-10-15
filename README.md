<p align="center"><img src="assets/logo-256.png" alt="Mantle Chat" width="80" height="80" /></p>

# Mantle Chat for AI assistants

Ask your AI assistant to find things in [Mantle Chat](https://mantle.chat), organize your workspace, save writing in a new canvas, and get help from your saved agents.

Connect from Cursor, or try the preview setup for Claude, Codex, ChatGPT, and OpenCode. [Choose your assistant](docs/clients.md). Official directory listings are not available yet. The new client setups and Grok Bot are still being tested; available features depend on your account permissions.

## What you can do

- **Find your work.** Browse workspaces, folders, chats, channels, canvases, agents, and tasks.
- **Ask an agent.** Send a prompt to a saved Mantle agent, read its answer, or cancel the request.
- **Save your writing.** Save meeting notes, a project brief, or a draft in a new canvas. A canvas is a document in your workspace.
- **Read and share updates.** Read recent messages or canvas content when enabled, and send a plain-text message to a channel.
- **Keep things organized.** Create folders, blank chats, channels, and canvases. Rename items, archive or restore them, and move them into folders.
- **Manage your workspace.** Change its name or icon, delete items, and update workspace access settings using your assistant’s confirmation controls.
- **Update an agent draft.** Prepare changes, review them, and save them to a draft. Publish separately in Mantle.
- **Check task progress.** See whether recent runs completed, failed, or are still running.

Try asking:

> “Create a Planning folder and move this channel into it.”
>
> “Summarize this conversation and save it in a new Mantle canvas.”
>
> “Ask my Research agent to summarize this question.”
>
> “Read the latest messages in Product feedback.”

## Connect your account

1. Follow the [setup for your assistant](docs/clients.md). Cursor users can start with **Add to Cursor** on [Cursor Directory](https://cursor.directory/plugins/mantle-chat).
2. Choose **Connect** or **Authorize**, then sign in to Mantle in your browser.
3. Ask your assistant to list your workspaces and choose the one to use.

You need a Mantle account with access to that workspace. You never need to paste passwords or API keys into the conversation. See [connecting and troubleshooting](docs/connecting.md) for setup options.

## You stay in control

Mantle checks your permissions for each action. Before posting a channel message, permanently deleting an item, or changing workspace visibility or indexing, your assistant must show an approval card or confirmation form. Review the exact message, item, or settings and approve it there. If your assistant cannot show an approval, use Mantle for that action. There is no separate Mantle approval page. Deleting a folder keeps its contents and moves them to the workspace root. Archiving a canvas turns off its public share links; restoring it does not turn them back on.

Information you retrieve is shared with your AI assistant. You can call saved agents with no tools or with explicitly selected read-only tools. Agents that can change connected services must be run directly in Mantle. Read [how your data is handled](docs/privacy.md).

The plugin can add text when creating a canvas, but cannot rewrite an existing canvas. It can post plain-text messages to channels you choose, as your signed-in Mantle user. It cannot send messages into individual chats, move items between workspaces, manage members or billing, delete entire workspaces, or start scheduled tasks. See the [tool reference](docs/tools.md) for the full scope.

## Help

- [Connecting and troubleshooting](docs/connecting.md)
- [Setup for Claude, Codex, ChatGPT, and OpenCode](docs/clients.md)
- [Tool reference](docs/tools.md)
- [Learn about Mantle Chat](https://docs.mantle.chat)
- [Privacy policy](https://mantle.chat/privacy) · [Contact support](https://mantle.chat/contact)
- [Example Grok Bot instructions](docs/grok-bot-template.md)
- [Contributing](CONTRIBUTING.md) · [Report a security issue](SECURITY.md)

Contact [support@mantle.chat](mailto:support@mantle.chat).

This plugin is [MIT-licensed](LICENSE). [Mantle service terms](https://mantle.chat/terms) and your client's terms apply separately.
