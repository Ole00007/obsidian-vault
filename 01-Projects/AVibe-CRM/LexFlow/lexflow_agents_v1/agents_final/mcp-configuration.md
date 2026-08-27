# MCP Configuration — LexTaskFlow Hermes Stack

> Master MCP configuration document. Owner: operator-installer.
> All MCP installs, filters, and approvals are gated by operator-installer before activation.

---

## What is an MCP

A Model Context Protocol (MCP) server gives an agent structured access to an external system
(filesystem, database, browser, API) through a standardised tool-call interface.
Each MCP must be explicitly installed, filtered, and assigned to agents in hermes-config.

---

## MCP Installation Principle

- Minimum blast radius: only the tools each agent actually needs are allowed.
- Every MCP has an allowed_agents list. Agents not on the list cannot call it.
- Every MCP has a allowed_tools filter. Agents receive only the tools they need.
- Destructive tools (write, delete, send, deploy) require confirmation from operator-installer
  unless the agent is explicitly marked autonomous=true for that tool.
- Human-in-the-loop: irreversible actions (delete production data, send mass email, live ad spend)
  always surface to operator before executing unless otherwise stated in agent's soul.

---

## MCP Stack Overview

| # | MCP Name | Status | Priority | Agents |
|---|---|---|---|---|
| 1 | filesystem | INSTALLED | P0 | All agents |
| 2 | postgresql | INSTALLED | P0 | lexflow-builder, backend-developer, data-analyst, sales-crm, qa-tester |
| 3 | github | INSTALLED | P0 | lexflow-builder, backend-developer, frontend-developer, devops-agent, qa-tester |
| 4 | resend/email | PENDING INSTALL | P1 | email-campaign, sales-crm, customer-rel-manager |
| 5 | playwright | PENDING INSTALL | P1 | devops-agent, qa-tester, ads-expert, marketing-analyst, agency-growth |
| 6 | google-workspace | PENDING OAUTH | P1 | agency-growth, personal-assistant, content-creator |
| 7 | perplexity-search | CONFIGURED | P1 | All agents (Sonar API) |
| 8 | notion/drive | PENDING INSTALL | P2 | librarian, memory-curator |
| 9 | railway | PENDING INSTALL | P1 | devops-agent |
| 10 | netlify | PENDING INSTALL | P1 | devops-agent, frontend-developer |
| 11 | cloudflare | PENDING INSTALL | P2 | devops-agent |
| 12 | google-ads | PENDING INSTALL | P3 | ads-expert |
| 13 | meta-ads | PENDING INSTALL | P3 | ads-expert |
| 14 | instagram | PENDING INSTALL | P3 | customer-rel-manager |
| 15 | twilio-whatsapp | PENDING INSTALL | P3 | customer-rel-manager |

---

## 1. filesystem

Status: INSTALLED
Scope: ~/hermes-workspace/ (read+write), ~/agents_final/ (read-only for non-librarian)
Allowed agents: ALL

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "/Users/operator/hermes-workspace"],
      "env": {}
    }
  }
}
```

Tool filters per agent role:
- All agents: read_file, list_directory, search_files
- librarian, memory-curator, operator-installer: + write_file, create_directory, move_file
- All dev agents (lexflow-builder, backend-developer, frontend-developer): + write_file

---

## 2. postgresql

Status: INSTALLED
Database: LexTaskFlow Railway PostgreSQL
Connection: Via DATABASE_URL (Railway private network)
Allowed agents: lexflow-builder, backend-developer, data-analyst, sales-crm, qa-tester

```json
{
  "mcpServers": {
    "postgresql": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
               "${DATABASE_URL}"],
      "env": {
        "DATABASE_URL": "${RAILWAY_DATABASE_URL}"
      }
    }
  }
}
```

Tool filters per agent:
- data-analyst, qa-tester: query (SELECT only — no writes, enforced)
- backend-developer, lexflow-builder: query (full), execute_migration (with diff review)
- sales-crm: query (contacts table SELECT only)

---

## 3. github

Status: INSTALLED
Repo: LexTaskFlow monorepo (owner/lexflow)
Allowed agents: lexflow-builder, backend-developer, frontend-developer, devops-agent, qa-tester

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Tool filters per agent:
- All: get_file_contents, list_branches, get_commit, search_code, list_pull_requests
- backend-developer, frontend-developer, lexflow-builder: + create_or_update_file,
  create_pull_request, create_branch
- devops-agent: + all workflow tools
- qa-tester: + create_issue (bug report), add_pull_request_review_comment

---

## 4. resend/email

Status: PENDING INSTALL
Priority: P1 — install next
Allowed agents: email-campaign, sales-crm, customer-rel-manager

```json
{
  "mcpServers": {
    "resend": {
      "command": "npx",
      "args": ["-y", "resend-mcp-server"],
      "env": {
        "RESEND_API_KEY": "${RESEND_API_KEY}"
      }
    }
  }
}
```

Tool filters:
- email-campaign: send_email, create_broadcast, get_email_stats, update_contact, remove_contact
- sales-crm: send_email (follow-up sequences only, operator-approved template IDs)
- customer-rel-manager: send_email (off-hours acknowledgement only)

Note: Transactional email (5 Resend triggers already in Flask API) is NOT managed via MCP.
The Resend MCP is for marketing, drip, and follow-up sequences only.

Install command:
```bash
npx @modelcontextprotocol/server-resend
# OR
npm install -g resend-mcp-server
```

---

## 5. playwright

Status: PENDING INSTALL
Priority: P1
Allowed agents: devops-agent, qa-tester, ads-expert, marketing-analyst, agency-growth

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"]
    }
  }
}
```

Tool filters:
- qa-tester: browser_navigate, browser_click, browser_fill, browser_screenshot, browser_evaluate
- devops-agent: browser_navigate, browser_screenshot (smoke test)
- marketing-analyst, agency-growth: browser_navigate, browser_screenshot, browser_evaluate
  (competitor research, GSC data collection)
- ads-expert: browser_navigate, browser_screenshot (ad preview, competitor ad review)

Install command:
```bash
npx playwright install chromium
npx @modelcontextprotocol/server-playwright
```

---

## 6. google-workspace

Status: PENDING OAUTH
Priority: P1
Allowed agents: agency-growth, personal-assistant, content-creator

OAuth scopes required:
- calendar.readonly, calendar.events (personal-assistant)
- drive.file (content-creator — Drive drafts folder only)
- gmail.readonly, gmail.send (customer-rel-manager, when added)
- searchconsole.readonly (agency-growth — GSC only)

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gdrive"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}",
        "GOOGLE_REDIRECT_URI": "http://localhost:3000/oauth/callback"
      }
    }
  }
}
```

OAuth setup steps:
1. Create OAuth 2.0 Client in Google Cloud Console (project: lexflow-ops)
2. Add scopes (calendar, drive, gsc)
3. Complete OAuth flow in Hermes (127.0.0.1 redirect)
4. Store refresh token in Railway env vars (GOOGLE_REFRESH_TOKEN)

---

## 7. perplexity-search

Status: CONFIGURED (Sonar API available to all agents)
Priority: P1 (configured)
Allowed agents: ALL

Every agent has a `perplexity-lookup` skill that calls Sonar API directly.
No separate MCP installation required — API key is in Railway env vars.

```python
# Sonar API call pattern used in all agents
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["PERPLEXITY_API_KEY"],
    base_url="https://api.perplexity.ai"
)

response = client.chat.completions.create(
    model="sonar-pro",
    messages=[{"role": "user", "content": query}]
)
```

Fallback chain if sonar-pro fails:
1. sonar (faster, lower cost)
2. sonar-reasoning (chain-of-thought)

---

## 8. notion/drive

Status: PENDING INSTALL
Priority: P2
Allowed agents: librarian, memory-curator

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "${NOTION_API_KEY}"
      }
    }
  }
}
```

Note: Obtain Notion integration token from https://www.notion.so/my-integrations
Share the target workspace pages with the integration before using.

---

## 9. railway

Status: PENDING INSTALL
Priority: P1
Allowed agents: devops-agent

```json
{
  "mcpServers": {
    "railway": {
      "command": "npx",
      "args": ["-y", "railway-mcp"],
      "env": {
        "RAILWAY_TOKEN": "${RAILWAY_API_TOKEN}"
      }
    }
  }
}
```

Get token: Railway dashboard → Account Settings → Tokens → New Token
Allowed tools: get_deployments, get_service_logs, deploy, rollback
Blocked: delete_service, delete_database (irreversible — requires human approval)

---

## 10. netlify

Status: PENDING INSTALL
Priority: P1
Allowed agents: devops-agent, frontend-developer

```json
{
  "mcpServers": {
    "netlify": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-netlify"],
      "env": {
        "NETLIFY_AUTH_TOKEN": "${NETLIFY_AUTH_TOKEN}",
        "NETLIFY_SITE_ID": "${NETLIFY_SITE_ID}"
      }
    }
  }
}
```

Get token: Netlify dashboard → User Settings → Applications → New Access Token
Site ID: Netlify site dashboard → Site configuration → Site ID

---

## 11. cloudflare

Status: PENDING INSTALL (depends on custom domain purchase)
Priority: P2
Allowed agents: devops-agent

Install after: custom domain purchased and DNS points to Netlify/Railway.
Use: DNS management, SSL, WAF rules, performance (Cloudflare Pro or Free).

---

## 12–13. google-ads / meta-ads

Status: PENDING INSTALL
Priority: P3 (after first ad campaigns approved by operator)
Allowed agents: ads-expert only

Note: Both require operator to approve ad budget before these MCPs are activated.
Activation of these MCPs is an irreversible spend trigger — requires human confirmation.

---

## 14–15. instagram / twilio-whatsapp

Status: PENDING INSTALL
Priority: P3 (after Phase 2 scope confirmed)
Allowed agents: customer-rel-manager

Instagram MCP: requires Meta Developer App and Instagram Business Account
Twilio WhatsApp: requires Twilio API key, WhatsApp Business number verified

---

## MCP Installation Runbook

Run in order. Each step verified before proceeding to next.

### Phase 1 (Now — P1)
1. Verify filesystem MCP working across all agents
2. Verify postgresql MCP (SELECT query from data-analyst)
3. Verify github MCP (list_branches on lexflow repo)
4. Install playwright (npx playwright install chromium)
5. Install resend MCP (npm install -g resend-mcp-server or npx)
6. Complete Google Workspace OAuth (Calendar + GSC + Drive)
7. Install railway MCP (npx railway-mcp)
8. Install netlify MCP

### Phase 2 (After Phase 1 stable)
9. Install notion MCP (get NOTION_API_KEY)
10. Set up Cloudflare (after domain purchased)
11. Configure instagram MCP (after Meta Developer App created)

### Phase 3 (After operator approves ad spend)
12. Google Ads API MCP (budget-gated)
13. Meta Ads MCP (budget-gated)
14. Twilio WhatsApp MCP (after WhatsApp Business verified)

---

## Hermes MCP Config File Location

Hermes stores MCP config at:
~/Library/Application Support/Hermes/mcp_config.json (macOS)
OR defined per agent in hermes-workspace/agent_configs/

After every MCP install: restart Hermes gateway via dashboard Restart Gateway button.

---

## Security Rules

1. All API keys stored as env vars. Never in code, never in agent MD, never in chat.
2. Production DATABASE_URL: only backend-developer, lexflow-builder, data-analyst, qa-tester.
3. Railway/Netlify deploy tokens: devops-agent only.
4. RESEND_API_KEY: email-campaign, backend-developer (transactional triggers).
5. PERPLEXITY_API_KEY: all agents (read-only Sonar queries — no spend risk).
6. Ad platform tokens: ads-expert only. Activation requires operator approval.
7. Google OAuth refresh token: stored in Railway env vars, not in any agent MD file.

## Links
- Parent: [[agents_final-INDEX]]
- Related: [[qa-tester]]
