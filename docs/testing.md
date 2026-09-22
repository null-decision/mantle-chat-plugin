# Testing the plugin

## Package checks

Run with Python 3.10+:

```sh
python3 scripts/validate_plugin.py
python3 -m unittest discover -s tests -p '*_test.py'
```

These offline checks validate the public file list, manifest, connection settings, skill metadata, and documentation links. They do not test browser sign-in or the hosted service.

The checks cover the Cursor, Claude, and Codex manifests, the Claude marketplace, and both OpenCode examples. They reject additional endpoints, embedded credentials, command launchers, mismatched package identities/versions, and unreviewed files.

With Claude Code installed, also validate its plugin and marketplace:

```sh
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

## Try a local copy in Claude Code

From the package directory, run `claude --plugin-dir .`. Inspect `/mcp` and the two namespaced skills before signing in. This does not install the package into the public directory. Test a normal marketplace installation separately before claiming that install path works.

## Other clients

Follow [Choose your assistant](clients.md). Keep a separate result for each client and version; do not count a successful Cursor connection as proof that another client works. Test the actual OpenCode version that matches each example. Check both OAuth consent and the resulting Mantle account, then test token refresh, reconnect, and revocation.

## Try a local copy in Cursor

Copy `.cursor-plugin`, `mcp.json`, `assets`, and `skills` into a new `~/.cursor/plugins/local/mantle-chat` folder. Check for an existing installation before copying. Include the hidden `.cursor-plugin` folder; leave out `.git`, logs, and credentials.

Restart Cursor and inspect Customize. You should see one Mantle connection and two skills. Team policy may restrict local imports, and an installed marketplace copy with the same name takes precedence. See [Cursor's local plugin instructions](https://cursor.com/docs/plugins).

For Grok Bot, test through the Plugins interface using a plugin available to your account. The local Cursor folder does not install a Grok Bot plugin.

## Check the user experience

Use test accounts and made-up data. Record the plugin version, client version, and result for each case:

- Connect from a fresh account and complete browser sign-in.
- Select a workspace, find an agent, and check a task's recent runs.
- Check empty lists and more than one page of results.
- Confirm inaccessible items do not return data or allow changes.
- Prepare a rename, review it, and apply it to the draft. Confirm the live agent is unchanged.
- Check that unrelated fields stay unchanged and a conflicting edit asks for another review.
- Confirm an uncertain write does not create repeated proposals.
- Put an instruction to perform an unrelated action in a test item's description. Confirm the assistant treats it as data.
- Create a folder, blank chat, channel, and canvas; retry each with the same key and confirm no duplicates.
- Create a canvas with a short poem in `content`; read it back and check the text and paragraph breaks. Retry with the same key and content and confirm there is only one canvas. Check that a short `description` is not mistaken for the document body.
- Check the connected Mantle account when the assistant lists different workspaces from the Mantle website. Reconnecting with another account must not expose the first account's private items.
- Move an item into a folder; check a stale revision fails without changing it.
- Read message/canvas content with and without the relevant permission.
- Send a plain-text channel message; retry it and confirm only one message exists.
- Call a saved agent, poll its answer, and cancel another call. Confirm a different connection cannot read it.
- Confirm deletion and workspace access changes inside the client, with the exact target/settings visible and no separate Mantle approval page. Check stale-version and permission denials, same-key retries without repeated changes, and rejection of changed arguments under the same key. Record how automatic-run settings affect prompts.
- Verify a revoked connection no longer works.
- If sharing a bot template, import it with another account and confirm the recipient must use their own connection.

Run these checks in every client you claim to support before claiming compatibility. Coordinate account changes with the test account's owner and keep credentials out of screenshots and reports.
