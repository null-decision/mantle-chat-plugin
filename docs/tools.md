# MCP tool reference

The connected server's tool definitions are the source of truth for input types, limits, and available features. Some tools require separate organization permissions. If a tool is missing or access is denied, ask your administrator; reconnecting does not grant extra access.

## Available tools

Use `list_workspaces` first. The other tools take the selected `workspace_id`; resolve resource IDs from list results rather than guessing them.

| Area | Tools | What they do |
| --- | --- | --- |
| Workspaces | `list_workspaces`, `get_workspace`, `update_workspace_profile` | Find accessible workspaces; change a name or icon as an owner or admin. |
| Folders | `list_folders`, `get_folder`, `create_folder`, `update_folder`, `set_item_folder` | Create and rename folders; place a chat, channel, or canvas in a folder or the workspace root. |
| Chats | `list_chats`, `get_chat`, `create_chat`, `update_chat_title`, `set_chat_archived`, `list_chat_messages` | Browse metadata, create blank chats, replace titles, archive/restore, and read recent text when permitted. |
| Channels | `list_channels`, `get_channel`, `create_channel`, `update_channel`, `set_channel_archived`, `list_channel_messages`, `send_channel_message` | Manage channels, read recent text, and send plain-text messages when permitted. |
| Canvases | `list_canvases`, `get_canvas`, `get_canvas_content`, `create_canvas`, `update_canvas`, `set_canvas_archived` | Create canvases with optional text, change their name/details, archive/restore, and read current content when permitted. |
| Deletion | `delete_resource` | Permanently delete one folder, chat, channel, or canvas after confirmation in the connected app. |
| Access settings | `get_workspace_settings`, `update_workspace_settings` | Inspect or change workspace visibility and search/knowledge indexing with owner/admin access. |
| Agents | `list_agents`, `get_agent`, `call_agent`, `get_agent_response`, `cancel_agent_response` | Find saved agents, send a private prompt, poll the answer, or cancel. |
| Agent drafts | `propose_agent_changes`, `apply_agent_changes_to_draft` | Prepare typed changes and apply an agreed proposal to a draft. |
| Tasks | `list_tasks`, `get_task`, `list_runs`, `get_run` | Read task metadata and run status. |

## Safe requests and retries

Use each tool's advertised pagination and bounds. Where a result returns `{ items, nextCursor }`, pass `nextCursor` as `cursor` with the same workspace and filters; null ends the list. Do not call a partial page the full inventory. Content tools may have different limits.

Creation and channel-message tools require `idempotency_key`. Reuse the same key and exact arguments when retrying an uncertain request. Use a new key for a distinct action. Agent calls also use a retry key. Update and folder-placement tools require `expected_updated_at` from the latest resource result. Refresh after a conflict and review any replacement change.

Deletion and workspace access-setting changes run directly after confirmation in the connected app. Use the exact target/settings, current `expected_updated_at`, and a stable `idempotency_key`. Retry with the same key and arguments after a lost response. Mantle rejects stale versions, missing permissions, and reused keys with different arguments. No separate Mantle approval page is involved. Client settings determine whether a confirmation prompt appears; automatic-run modes may skip it. Deleting a folder moves its contents to the workspace root. Archiving a canvas revokes active public share links.

`call_agent` starts a private single-turn agent request. Poll with `get_agent_response` using the returned response ID. Reading answers requires separate permission; only the originating user and connection can access the response. Answer content expires after 24 hours. Agents may use configured tools that read or change connected services.

## Content and limits

Chat metadata excludes titles, snippets, and messages. Separate content tools return bounded chat/channel text or current canvas content when authorized. Message content omits authors, attachments, reactions, citations, reasoning, and tool traces. Canvas reads omit edit history and collaborators. Agent/task metadata excludes hidden instructions, credentials, task prompts, and task-run output. Arbitrary names, descriptions, and message text can still contain sensitive information.

`create_canvas` accepts optional `content`: initial plain text from 1 to 16,000 characters. It preserves line and paragraph breaks. Markdown and HTML remain literal text. Omit `content` to create a blank canvas; `description` is a short description, not the document body. Keep the same text and retry key after an uncertain creation. When permitted, use `get_canvas_content` to read back the saved document.

`update_canvas` changes a name, description, or icon; it does not change the document body. Rewriting existing canvas content, chat-message sending, rich channel attachments/mentions, cross-workspace moves, workspace deletion, member/role management, billing, and scheduled-task execution are outside this release.

## Draft edits

The `changes` object accepts these optional sections; send only requested fields:

| Section | Fields |
| --- | --- |
| `metadata` | `name`, `description`, `icon`, `icon_fit_mode` |
| `model` | `model_id`, `system_instructions`, `temperature`, `max_tool_steps` |
| `tools` | `mcp_server_ids`, `mcp_selected_tools`, `managed_tool_provider_ids`, `managed_selected_tools` |
| `workspace` | `folder_id`, `pinned`, `shared_with_workspace` |

Consult the live schema for types and bounds. Omitting a field preserves it; null explicitly clears a nullable field. Tool arrays/maps are replacement values, not instructions to append. Workspace fields control placement/sharing inside the selected workspace.

For example, the *changes fragment* for a rename is:

```json
{
  "metadata": {
    "name": "Research Assistant"
  }
}
```

Provide this under `changes`, alongside the real IDs resolved from the user's authorized workspace. This fragment is not a complete tool call.

Proposal summaries use camelCase: `changeSetId`, `agentId`, `workspaceId`, `draftId`, `baseVersion`, `draftVersion`, `changedFields`, `resolveUrl`, and `status`. They do not return the proposed full content. Display the exact submitted values and the server's field list; direct the user to Mantle for the complete review.

After agreement, pass the returned `changeSetId` as **`change_set_id`** to the apply tool. Status is `proposed`, `applied_to_draft`, or `already_applied`. None means published. Proposal creation is non-idempotent; applying the same change set is idempotent. Stop on version conflicts, locks, or validation failures and re-review any replacement proposal.

`system_instructions` is write-capable in this contract even though existing instructions are not returned. Never infer or reconstruct hidden current text. Only transmit new instructions deliberately provided or approved for this edit.

## Errors

Tool failures include a safe error code and message, with a next step or retry delay when available. HTTP responses carry an `X-Request-Id` header for support and may include `WWW-Authenticate` or `Retry-After`. Share only the error code and request ID when contacting support. Avoid raw payloads and arbitrary links. Validate review URLs against the configured Mantle frontend origin before presenting them.
