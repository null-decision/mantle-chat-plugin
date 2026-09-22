# How your data is handled

Connecting the plugin lets your AI assistant request information and perform authorized actions in your Mantle account. Mantle checks your access for each request.

## Information shared with your assistant

The plugin can return workspace and folder names, channel and canvas details, agent and task summaries, run status, timestamps, and resource IDs. Separate permissions allow reading recent chat/channel text and current canvas content. An agent call can return the answer to the prompt you sent.

Chat metadata does not include titles or snippets. Message reads omit authors, attachments, reactions, citations, reasoning, and tool traces. Canvas reads omit edit history and collaborators. The tools do not return stored agent instructions, knowledge files, credentials, task prompts, or task-run output. Names, descriptions, messages, documents, and agent answers can still contain sensitive information.

## Changes and agent calls

New canvas text, requested edits, and channel messages are sent to Mantle. Completed changes remain after you disconnect the plugin. New agent instructions or tool settings may be submitted as part of an agent draft edit; publishing remains separate in Mantle.

A saved agent may use its configured tools to read or change connected services. Consider those tool permissions before requesting a call. Private agent responses belong to the user and connection that created them; answer content expires after 24 hours in Mantle. That expiry does not remove copies already returned to your assistant.

Permanent deletions and workspace visibility or indexing changes use the connected app’s confirmation controls. There is no separate Mantle approval page. Automatic-run settings may skip client prompts; Mantle still enforces current access, operation permissions, and version checks.

## Sign-in and privacy choices

Sign in through the browser connection flow. The plugin files contain no passwords or API keys. Never paste credentials into chat. Choosing a workspace does not grant new permissions; use an account whose access is appropriate for the work.

Information returned by Mantle may be included in your AI conversation and processed by your client and its model providers. Their privacy settings and retention policies apply. The plugin package has no separate data store or tracking code.

See [Mantle's privacy policy](https://mantle.chat/privacy) for the hosted service. For help disconnecting, revoking access, or making a privacy request, contact [support@mantle.chat](mailto:support@mantle.chat).
