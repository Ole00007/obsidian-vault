# MCP Rollout Plan — LexTaskFlow Hermes Stack
> Owner: operator-installer | Config file: `~/.hermes/config.yaml`
> After every install: run `hermes restart` then `/reload-mcp` inside chat.

---

## How Hermes loads MCP servers

Hermes reads `~/.hermes/config.yaml` at startup. Each `mcp_servers` entry is spawned as a subprocess. Tools register automatically alongside built-in Hermes tools. The model calls them like any other skill.

Verify any server loaded correctly:
```bash
hermes tools list | grep -i mcp
# or ask inside chat: "Tell me which MCP-backed tools are available right now."
```

Check logs if a server fails to start:
```bash
cat ~/.hermes/logs/mcp-<servername>.log
grep -i mcp ~/.hermes/logs/agent.log
```

---

## DAY 1 — Install today (after agentic setup complete)

### 1. filesystem
**Purpose:** Read/write project files. Typed operations: list_files, read_file, write_file
**Agents:** lexflow-builder, agency-growth, librarian, content-creator

**Install:**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

**config.yaml block:**
```yaml
mcp_servers:
  filesystem:
    command: npx
    args:
      - "@modelcontextprotocol/server-filesystem"
      - "/Users/operator/hermes-workspace"
    tools:
      include:
        - list_directory
        - read_file
        - write_file
        - create_directory
        - move_file
        - search_files
      resources: false
      prompts: false
    enabled: true
```

**Security:** Root scoped to `hermes-workspace` only — never `/` or `~`. Write access: librarian, content-creator, lexflow-builder. Others: read-only (enforced in each agent soul).

**Verify:**
```bash
hermes tools list | grep filesystem
```

---

### 2. github
**Purpose:** Repo management — issues, commits, PRs, CI status
**Agents:** lexflow-builder (full), operator-installer (audit/read)

**Install:**
```bash
npm install -g @modelcontextprotocol/server-github
```

Get token: GitHub → Settings → Developer Settings → Fine-grained token
Scopes: `contents:read`, `issues:write`, `pull_requests:write`, `actions:read`

**config.yaml block:**
```yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
    tools:
      include:
        - get_file_contents
        - list_branches
        - get_commit
        - search_code
        - list_pull_requests
        - create_pull_request
        - create_or_update_file
        - create_branch
        - list_issues
        - create_issue
        - update_issue
        - get_pull_request_status
      resources: false
      prompts: false
    enabled: true
```

**operator-installer** uses read-only subset only (enforced in soul): `get_file_contents`, `list_branches`, `get_commit`, `search_code`, `list_issues`

**Verify:**
```bash
hermes tools list | grep github
```

---

### 3. postgres
**Purpose:** LexFlow DB — schema queries, migrations, CRM/task reads
**Agents:** lexflow-builder, sales-crm, customer-rel-manager

**Install:**
```bash
npm install -g @modelcontextprotocol/server-postgres
```

**CRITICAL: Create read-only DB user first (Railway shell or psql):**
```sql
CREATE USER hermes_readonly WITH PASSWORD 'your_readonly_password';
GRANT CONNECT ON DATABASE lexflow TO hermes_readonly;
GRANT USAGE ON SCHEMA public TO hermes_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO hermes_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO hermes_readonly;
```

**config.yaml block (two servers — read-only + read-write):**
```yaml
mcp_servers:
  postgres-readonly:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-postgres"
      - "postgresql://hermes_readonly:${PG_READONLY_PASSWORD}@${PG_HOST}:5432/lexflow"
    tools:
      include: [query]
      resources: false
      prompts: false
    enabled: true

  postgres-rw:
    command: npx
    args:
      - "-y"
      - "@modelcontextprotocol/server-postgres"
      - "${DATABASE_URL}"
    tools:
      include: [query, execute_migration]
      resources: false
      prompts: false
    enabled: true
```

**Agents:**
- `postgres-readonly`: sales-crm (contacts), customer-rel-manager (contact lookup), data-analyst (all SELECTs), qa-tester
- `postgres-rw`: lexflow-builder, backend-developer (migrations with diff review)

**Verify (inside hermes chat):**
```
Run: SELECT table_name FROM information_schema.tables WHERE table_schema='public';
```

---

### 4. playwright
**Purpose:** Browser automation — site audit, scraping, UI testing
**Agents:** agency-growth, lexflow-builder, marketing-analyst

**Install:**
```bash
npm install -g @executeautomation/playwright-mcp-server
npx playwright install chromium
```

Alternative (official):
```bash
npx @playwright/mcp init
```

**config.yaml block:**
```yaml
mcp_servers:
  playwright:
    command: npx
    args: ["-y", "@executeautomation/playwright-mcp-server"]
    tools:
      include:
        - browser_navigate
        - browser_click
        - browser_fill
        - browser_screenshot
        - browser_evaluate
        - browser_get_text
        - browser_wait_for
      resources: false
      prompts: false
    enabled: true
```

**Agent tool access:**
- agency-growth: `browser_navigate`, `browser_screenshot`, `browser_get_text` (competitor research, GSC UI)
- lexflow-builder: all tools (smoke tests, debugging)
- marketing-analyst: `browser_navigate`, `browser_screenshot`, `browser_get_text` (competitor audit)
- qa-tester: all tools (E2E UI testing)

**Verify (inside hermes chat):**
```
Open https://muzloto-apr-1f8f19.netlify.app/ and take a screenshot.
```

---

### 5. telegram
**Purpose:** Telegram bot — send_message, receive_update, set_webhook
**Agents:** telegram-utility (all tools), customer-rel-manager (send_message only)

**Install:**
```bash
npx -y mcp-telegram-bot
```

Get token: @BotFather → /newbot (or use existing token already in Hermes gateway)
Store in env only: `TELEGRAM_BOT_TOKEN`

**config.yaml block:**
```yaml
mcp_servers:
  telegram:
    command: npx
    args: ["-y", "mcp-telegram-bot"]
    env:
      TELEGRAM_BOT_TOKEN: "${TELEGRAM_BOT_TOKEN}"
    tools:
      include:
        - send_message
        - receive_update
        - set_webhook
        - get_chat
        - get_updates
      resources: false
      prompts: false
    enabled: true
```

**Security:** Bot token in env only — never logged or returned as tool output. `set_webhook` requires operator confirmation (irreversible network change).

**Verify:**
```
Send a test message to my Telegram chat ID: [your_chat_id]
```

---

## DAY 2 — Next session

### 6. resend
**Purpose:** Email automation — send_email, list_templates, trigger_sequence
**Agents:** sales-crm, customer-rel-manager

**Install:**
```bash
npx -y @resend/mcp
```

Get API key: https://resend.com/api-keys

**config.yaml block:**
```yaml
mcp_servers:
  resend:
    command: npx
    args: ["-y", "@resend/mcp"]
    env:
      RESEND_API_KEY: "${RESEND_API_KEY}"
    tools:
      include:
        - send_email
        - list_emails
        - get_email
        - list_domains
        - create_broadcast
        - list_broadcasts
      resources: false
      prompts: false
    enabled: true
```

**Important:** The 5 Flask transactional triggers (intake, assignment, status, deadline, digest) are NOT managed via this MCP. This MCP is for marketing and drip sequences only. Do not duplicate transactional sends.

---

### 7. google-workspace
**Purpose:** Gmail + Calendar + Drive + Docs — send_email, create_event, upload_doc
**Agents:** personal-assistant (calendar), agency-growth (GSC), content-creator (Drive), librarian (Drive)

**Install:**
```bash
npm install -g @modelcontextprotocol/server-gdrive
```

**One-time OAuth setup:**
```
1. https://console.cloud.google.com → New project: lexflow-ops
2. Enable: Gmail API, Calendar API, Drive API, Search Console API
3. Create OAuth 2.0 Client ID → Desktop app → download credentials.json
4. Save to: ~/.hermes/google-credentials.json
5. Run auth flow:
```
```bash
npx @modelcontextprotocol/server-gdrive auth \
  --credentials ~/.hermes/google-credentials.json \
  --scopes "https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/webmasters.readonly"
```
```
6. Complete browser OAuth → token saved to ~/.hermes/google-token.json
```

**config.yaml block:**
```yaml
mcp_servers:
  google-workspace:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-gdrive"]
    env:
      GOOGLE_CREDENTIALS_PATH: "/Users/operator/.hermes/google-credentials.json"
      GOOGLE_TOKEN_PATH: "/Users/operator/.hermes/google-token.json"
    tools:
      include:
        - list_files
        - read_file
        - create_file
        - send_email
        - list_events
        - create_event
        - search_console_query
      resources: false
      prompts: false
    enabled: true
```

**Agent tool access:**
- personal-assistant: `list_events`, `create_event`
- agency-growth: `search_console_query` (GSC read-only)
- content-creator: `list_files`, `create_file` (Drive drafts folder)
- librarian: `list_files`, `create_file`, `read_file` (documentation Drive backup)

---

### 8. perplexity
**Purpose:** AI research — search, summarise, fact-check
**Primary agents:** marketing-analyst, agency-growth
**Note:** All agents already call Sonar API directly via `perplexity-lookup` skill. This MCP formally registers it as a Hermes tool.

**Install:**
```bash
npx -y @ppl-ai/mcp
```

Get key: https://console.perplexity.ai → API Keys

**config.yaml block:**
```yaml
mcp_servers:
  perplexity:
    command: npx
    args: ["-y", "@ppl-ai/mcp"]
    env:
      PERPLEXITY_API_KEY: "${PERPLEXITY_API_KEY}"
    tools:
      include: [search, summarize, fact_check]
      resources: false
      prompts: false
    enabled: true
```

Model: `sonar-pro` (default). Fallback: `sonar` → `sonar-reasoning`

---

## Complete config.yaml — copy-paste ready

```yaml
# ~/.hermes/config.yaml
# LexTaskFlow MCP Stack v1.0 — June 2026

mcp_servers:

  # DAY 1

  filesystem:
    command: npx
    args: ["@modelcontextprotocol/server-filesystem", "/Users/operator/hermes-workspace"]
    tools:
      include: [list_directory, read_file, write_file, create_directory, move_file, search_files]
      resources: false
      prompts: false
    enabled: true

  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "${GITHUB_TOKEN}"
    tools:
      include: [get_file_contents, list_branches, get_commit, search_code,
                list_pull_requests, create_pull_request, create_or_update_file,
                create_branch, list_issues, create_issue, update_issue]
      resources: false
      prompts: false
    enabled: true

  postgres-readonly:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-postgres",
           "postgresql://hermes_readonly:${PG_READONLY_PASSWORD}@${PG_HOST}:5432/lexflow"]
    tools:
      include: [query]
      resources: false
      prompts: false
    enabled: true

  postgres-rw:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    tools:
      include: [query, execute_migration]
      resources: false
      prompts: false
    enabled: true

  playwright:
    command: npx
    args: ["-y", "@executeautomation/playwright-mcp-server"]
    tools:
      include: [browser_navigate, browser_click, browser_fill, browser_screenshot,
                browser_evaluate, browser_get_text, browser_wait_for]
      resources: false
      prompts: false
    enabled: true

  telegram:
    command: npx
    args: ["-y", "mcp-telegram-bot"]
    env:
      TELEGRAM_BOT_TOKEN: "${TELEGRAM_BOT_TOKEN}"
    tools:
      include: [send_message, receive_update, set_webhook, get_chat, get_updates]
      resources: false
      prompts: false
    enabled: true

  # DAY 2

  resend:
    command: npx
    args: ["-y", "@resend/mcp"]
    env:
      RESEND_API_KEY: "${RESEND_API_KEY}"
    tools:
      include: [send_email, list_emails, get_email, list_domains,
                create_broadcast, list_broadcasts]
      resources: false
      prompts: false
    enabled: true

  google-workspace:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-gdrive"]
    env:
      GOOGLE_CREDENTIALS_PATH: "/Users/operator/.hermes/google-credentials.json"
      GOOGLE_TOKEN_PATH: "/Users/operator/.hermes/google-token.json"
    tools:
      include: [list_files, read_file, create_file, send_email,
                list_events, create_event, search_console_query]
      resources: false
      prompts: false
    enabled: true

  perplexity:
    command: npx
    args: ["-y", "@ppl-ai/mcp"]
    env:
      PERPLEXITY_API_KEY: "${PERPLEXITY_API_KEY}"
    tools:
      include: [search, summarize, fact_check]
      resources: false
      prompts: false
    enabled: true
```

---

## Commands reference

```bash
# After any config change:
hermes restart
# OR inside chat:
/reload-mcp

# Verify all loaded tools:
hermes tools list | grep mcp

# Per-server logs:
cat ~/.hermes/logs/mcp-filesystem.log
cat ~/.hermes/logs/mcp-github.log
cat ~/.hermes/logs/mcp-postgres-readonly.log
cat ~/.hermes/logs/mcp-playwright.log
cat ~/.hermes/logs/mcp-telegram.log

# Disable without removing:
# Set  enabled: false  then hermes restart

# Add interactively (if supported):
hermes mcp add <name> --command npx --args "..."
hermes mcp test <name>
```

---

## Security checklist before going live

- [ ] All API keys in `env:` block only — never in `args:` (visible in process listings)
- [ ] filesystem root = `hermes-workspace` only (not `~`, not `/`)
- [ ] postgres: `hermes_readonly` user created and tested before wiring agents
- [ ] postgres-rw: only lexflow-builder and backend-developer
- [ ] telegram bot token in env only — never logged, never returned in tool output
- [ ] github token: fine-grained (not classic), minimum scopes
- [ ] google-workspace: scopes = calendar + drive.file + gmail.send + webmasters.readonly only
- [ ] resend: no `delete_contact` or `delete_domain` in include list
- [ ] playwright: no `browser_clear_cookies` unless explicitly needed
- [ ] After every MCP install: `/reload-mcp` → `hermes tools list` to confirm

---

## Phase 3 — budget-gated (do not install until operator approves)

| MCP | Install command | Gate |
|---|---|---|
| railway | `npx railway-mcp` | RAILWAY_API_TOKEN provided |
| netlify | `npx @modelcontextprotocol/server-netlify` | NETLIFY_AUTH_TOKEN provided |
| notion | `npx @modelcontextprotocol/server-notion` | NOTION_API_KEY provided |
| google-ads | `npx @google-ads/mcp` | Ad budget approved |
| meta-ads | `npx meta-ads-mcp` | Ad budget approved |
| twilio-whatsapp | `npx twilio-mcp` | WhatsApp Business number verified |
| cloudflare | `npx @cloudflare/mcp-server-cloudflare` | Custom domain purchased |
| instagram | via Meta Developer App | Phase 2 scope confirmed |

## Links
- Parent: [[lexflow_new_agents_mcp-INDEX]]
- Related: [[qa-tester]]
