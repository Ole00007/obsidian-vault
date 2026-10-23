# Obsidian Access — Hermes Primary, VS Code Fallback

## Decision

**Best fit: Hermes.** Obsidian is the durable knowledge and memory layer used by the Hermes crew, so Hermes should own the vault connection and normal read/write workflow. The VS Code agent is the fallback installer and troubleshooter when Hermes is unavailable, broken after an update, or unable to complete setup.

This does **not** automatically connect the Obsidian vault to Perplexity. There are two separate connections:

| Connection | Owner | Purpose |
|---|---|---|
| Hermes ↔ local Obsidian vault | Hermes | Crew memory, notes, handoffs, project context |
| Perplexity ↔ selected Obsidian material | Perplexity connector or a shared cloud folder | Research and strategic planning using selected notes |

## Recommended Design

1. Give Hermes filesystem access only to the existing vault, or preferably a bounded `Hermes-Agent` folder first.
2. Start read-only, verify search and reading, then test writing with one disposable note.
3. Keep secrets out of the vault and logs.
4. For Perplexity, reuse a supported Google Drive or Dropbox connector for a selected export/shared folder. Do not expose the entire private vault by default.
5. Consider a custom remote Model Context Protocol (MCP) connector only later; it adds hosting, authentication, and security work.

**MCP:** Model Context Protocol, a standard that lets an agent call external tools. Example: Hermes calls a filesystem tool restricted to one vault folder.

## Prompt A — Hermes Primary

Paste into the lead Hermes setup/operations agent.

```text
CONTEXT

You are the primary owner of the Hermes-to-Obsidian connection on my MacBook. Obsidian is the durable knowledge layer for the Hermes crew. VS Code is only the fallback installer/troubleshooter.

Do not create a second vault. Do not move, rename, mass-edit, index externally, or delete existing notes. Do not reveal note contents, API keys, credentials, or personal data in logs.

TASK

Safely connect the active Hermes profile to my existing Obsidian vault.

PHASE 1 — READ-ONLY DISCOVERY
1. Identify the active Hermes profile and its configuration/environment paths.
2. Locate candidate Obsidian vaults by finding `.obsidian` directories. Show paths only; do not read note contents yet.
3. Ask me to choose the correct vault if more than one exists.
4. Inspect the installed Hermes version, available Obsidian skill, filesystem tools, MCP support, Node.js, npm, and npx.
5. Recommend the simplest supported route:
   - First choice: Hermes filesystem-based Obsidian skill with OBSIDIAN_VAULT_PATH.
   - Second choice: a filesystem MCP server restricted to the selected vault or `Hermes-Agent` subfolder.
   - Do not add a REST API plugin or third-party MCP server unless the first two routes cannot meet the requirement.
6. Show the plan and exact files that would change. Wait for my approval before editing configuration.

PHASE 2 — BACKUP AND CONFIGURE
After approval:
1. Make timestamped backups of every Hermes configuration or environment file to be edited.
2. Verify the backups are readable.
3. Configure access to the exact approved vault path. Prefer starting with a `Hermes-Agent` subfolder.
4. Never print secret values.
5. Reload or restart only the affected Hermes profile/service.

PHASE 3 — VERIFY
1. Confirm the connector/tool is registered.
2. Run a read-only listing of the approved folder.
3. Read one note that I explicitly approve.
4. With my approval, create one disposable test note inside `Hermes-Agent/Connection Tests/`.
5. Read it back, make one surgical append, verify it in Obsidian, then offer to delete only that test note.
6. Run Перекрёстный тест: independently verify that access is restricted to the approved folder and that no unrelated config or notes changed.

STOP CONDITIONS
Stop and ask me before:
- choosing between multiple vaults
- installing an Obsidian community plugin
- exposing the vault over HTTP or a network
- storing an API key
- granting write access outside the approved folder
- deleting or moving any existing note
- changing another Hermes profile
- using sudo or changing macOS security settings

DELIVERABLE
Return:
- active Hermes profile
- selected vault and allowed subfolder
- connection method
- backup paths
- files changed
- tools registered
- read and write test results
- Перекрёстный тест result
- rollback steps
- whether Perplexity still needs a separate shared-folder connector

End exactly:
Done | [result]
Next | [one concrete action]
Risks | [remaining risks or None]
```

## Prompt B — VS Code Fallback

Use only if Hermes is down or Prompt A cannot run.

```text
CONTEXT

Hermes is the primary owner of my Obsidian workflow, but it is currently unavailable or unable to complete the connection. You are the VS Code fallback full-stack/setup agent. Your job is to restore or configure the Hermes-to-Obsidian bridge without replacing Hermes memory, profiles, orchestration, or agent design.

TASK

Diagnose and prepare the Hermes-to-Obsidian connection on this MacBook.

1. Inspect only: Hermes version/status, active profile paths, Node/npm/npx, candidate `.obsidian` vault paths, Hermes Obsidian skill, and MCP configuration.
2. Do not read note contents during discovery.
3. Prefer the native filesystem-based Hermes Obsidian skill; otherwise use the official filesystem MCP server restricted to one approved folder.
4. Show the diagnosis, proposed method, exact files to edit, and rollback. Wait for my approval before configuration edits.
5. After approval, back up and verify affected config files, make the smallest change, reload Hermes MCP/tools, and run the same read/write/Перекрёстный тест defined in the primary prompt.
6. Produce a handoff that Hermes can read when it returns. Do not create a competing VS Code memory system.

HARD STOPS
Ask me before selecting a vault, enabling write access, installing an Obsidian plugin, exposing a local/network API, handling a secret, deleting a note, using sudo, or changing macOS security.

End exactly:
Done | [result]
Next | [one concrete action]
Risks | [remaining risks or None]
```

## Perplexity Access Later

For Perplexity research, sync only an approved folder such as `Obsidian Vault/Shared-With-Perplexity/` to Google Drive or Dropbox, then connect that cloud service in Perplexity. This creates a controlled research handoff without granting Perplexity access to the complete private vault.

Official references:
- Hermes MCP guide: https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes
- Hermes MCP reference: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
- Perplexity file connectors: https://www.perplexity.ai/help-center/en/articles/10672063-introduction-to-file-connectors-for-enterprise-organizations
- Perplexity custom remote connectors: https://www.perplexity.ai/help-center/en/articles/13915507-adding-custom-remote-connectors
