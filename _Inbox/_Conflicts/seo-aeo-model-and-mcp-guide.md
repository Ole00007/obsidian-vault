# SEO-AEO Agent — Model Selection & MCP Stack Guide
> Agent: seo-aeo-expert | Updated: June 2026

---

## 1. Best Model for seo-aeo-expert

### Verdict: Update the roster

Based on current tool-calling benchmarks, the original roster for `seo-aeo-expert` used `google/gemini-3-pro-preview` as default. The research below recommends an update.

| Priority | Model | Why | Cost (input/output per 1M tokens) |
|---|---|---|---|
| **Default** | `google/gemini-3.5-flash` | #1 on tool-calling benchmarks (June 2026), massive 1M context, strong multimodal, best price/performance ratio for a research+execution agent | $1.50 / $9.00 |
| **Fallback 1** | `google/gemini-3.1-pro` | #1 on APEX-Agents (33.5%), BrowseComp (85.9%), MCP Atlas (69.2%) — best deep-research model at non-Opus price | $2.00 / $12.00 |
| **Fallback 2** | `perplexity/sonar-pro` | Real-time SERP data, AI-citation monitoring, web-grounded answers — ideal when live search data is needed | low / per-query |

### Why not Gemini 3 Pro Preview (original default)?

`gemini-3-pro-preview` is a strong research model but Gemini 3.5 Flash now outscores it on all three tool-calling benchmarks that matter for an SEO agent (APEX-Agents, BrowseComp, MCP Atlas) at a lower price point. For a 24/7 execution agent making hundreds of tool calls daily, the cost difference is material.

### Why not Claude or GPT-5?

- Claude Opus 4.8: #2 on tool-calling but costs $5/$25 — 3× the price of Gemini 3.5 Flash for marginal gain on SEO workflows.
- GPT-5.5: Best all-round model but $5/$30 — only justified for the most complex multi-step reasoning, not routine SEO execution.
- GPT-5.3 Codex: Better fit for coding agents (lexflow-builder, backend-developer) than research/execution.

### Cost model for a 24/7 SEO agent

A typical SEO agent session (audit + keyword research + 1 content brief + reporting) uses ~50,000 tokens.

| Model | Cost per session | Cost per 30 days (2 sessions/day) |
|---|---|---|
| gemini-3.5-flash (default) | ~$0.04 | ~$2.40 |
| gemini-3.1-pro (fallback 1) | ~$0.07 | ~$4.20 |
| claude-sonnet-4.6 | ~$0.18 | ~$10.80 |
| gpt-5.5 | ~$0.70 | ~$42.00 |

**Gemini 3.5 Flash is the clear winner for a cost-sensitive, tool-heavy, 24/7 agent.**

---

## 2. Updated Model Roster for seo-aeo-expert

```
Default:    google/gemini-3.5-flash
Fallback 1: google/gemini-3.1-pro
Fallback 2: perplexity/sonar-pro
```

> Note: Update the agents-model-roster.md Space file accordingly.

---

## 3. Hermes MCP Stack — What Is Already Built In

### 3.1 Hermes native built-in tools (no MCP server needed)

These work out of the box with just an API key in `config.yaml`:

| Tool | What it does | API key needed |
|---|---|---|
| **Firecrawl** | Website crawling, structured data extraction, full-page scraping | `FIRECRAWL_API_KEY` |
| **Tavily** | AI-optimised web search, real-time results | `TAVILY_API_KEY` |
| **Exa** | Neural web search, research-grade retrieval | `EXA_API_KEY` |
| **Parallel** | Multi-source search aggregation | `PARALLEL_API_KEY` |
| **Shell execution** | Run CLI commands (curl, Python scripts, etc.) | none (enable + approval policy) |
| **Image generation** | FAL.ai text-to-image | `FAL_API_KEY` |
| **Code execution** | Inline Python/shell | none (enable in config) |

**Firecrawl is built in natively** — no MCP server process to install. Just add the API key.

### 3.2 MCP Catalog (one-click install via `hermes mcp`)

Hermes now ships a native MCP catalog (added May 2026). Run `hermes mcp` for an interactive picker. Vetted servers include:

| MCP Server | Package | Relevance to SEO-AEO agent |
|---|---|---|
| Playwright / Browser | `@playwright/mcp` | Full browser automation: SERP screenshots, AI Overview capture, crawl JS-rendered pages |
| GitHub | `@modelcontextprotocol/server-github` | Push schema fixes, sitemap updates, content briefs as PRs |
| Filesystem | `@modelcontextprotocol/server-filesystem` | Read/write local content files, logs, audit reports |
| n8n | via catalog | Trigger external workflows, CRM updates, email sequences |
| Linear | via catalog | Create fix tickets for frontend/backend developers |

### 3.3 DataForSEO — Status

**DataForSEO does not have a pre-built Hermes MCP entry yet.** However, DataForSEO exposes a REST API and you have two clean options:

**Option A — HTTP Tool (easiest, no MCP server needed):**
Define DataForSEO as a custom HTTP tool directly in Hermes `config.yaml`:
```yaml
tools:
  dataforseo:
    type: http
    base_url: https://api.dataforseo.com/v3
    auth:
      type: basic
      username: YOUR_EMAIL
      password: YOUR_API_KEY
```
The agent can then call DataForSEO endpoints directly (keyword data, SERP, difficulty scores).

**Option B — Custom MCP server:**
Build a lightweight Node.js or Python MCP server wrapping DataForSEO endpoints.
Use `hermes mcp add dataforseo --transport stdio` to register it.
This gives the agent a clean tool interface with named functions like `get_keyword_volume`, `get_serp_data`, `get_backlinks`.

### 3.4 Google Search Console — Status

**Google Search Console does not have a default Hermes preset either.** Options:

**Option A — Official Google Search Console MCP (community):**
```bash
npx @modelcontextprotocol/server-google-search-console
```
Configure OAuth2 credentials, then:
```bash
hermes mcp add gsc --transport stdio --command "npx @modelcontextprotocol/server-google-search-console"
```

**Option B — Direct API via HTTP Tool:**
Use the Google Search Console REST API with a service account JSON key:
```yaml
tools:
  google_search_console:
    type: http
    base_url: https://searchconsole.googleapis.com/v1
    auth:
      type: oauth2_service_account
      key_file: /path/to/service-account.json
```
Gives the agent direct access to impressions, clicks, positions, crawl errors, and index coverage.

---

## 4. Full MCP Stack Recommendation for seo-aeo-expert

| Tool | Install method | Priority |
|---|---|---|
| Firecrawl | Built-in (add API key) | 🔴 Essential — page scraping |
| Tavily or Exa | Built-in (add API key) | 🔴 Essential — web research |
| Google Search Console | HTTP Tool or GSC MCP | 🔴 Essential — ranking data |
| DataForSEO | HTTP Tool in config.yaml | 🟠 High — keyword volumes, SERP, difficulty |
| Playwright/Browser | `hermes mcp` catalog | 🟠 High — SERP screenshots, AI Overview capture |
| GitHub | `hermes mcp` catalog | 🟡 Medium — schema/sitemap PRs |
| Filesystem | `hermes mcp` catalog | 🟡 Medium — audit reports, content briefs |
| Linear or n8n | `hermes mcp` catalog | 🟡 Medium — ticket dispatch to other agents |
| Perplexity Sonar API | HTTP Tool or Fallback 1 model | 🟡 Medium — AI citation monitoring |

---

## 5. Recommended `config.yaml` additions for seo-aeo-expert

```yaml
# seo-aeo-expert tool config block
model: google/gemini-3.5-flash
fallback_models:
  - google/gemini-3.1-pro
  - perplexity/sonar-pro

tools:
  web_search:
    enabled: true
    provider: firecrawl        # built-in
    api_key: ${FIRECRAWL_API_KEY}
  
  secondary_search:
    enabled: true
    provider: exa              # built-in
    api_key: ${EXA_API_KEY}
  
  google_search_console:
    type: http
    base_url: https://searchconsole.googleapis.com/v1
    auth:
      type: oauth2_service_account
      key_file: /opt/secrets/gsc-service-account.json
  
  dataforseo:
    type: http
    base_url: https://api.dataforseo.com/v3
    auth:
      type: basic
      username: ${DATAFORSEO_EMAIL}
      password: ${DATAFORSEO_KEY}
  
  shell:
    enabled: true
    approval_policy: auto      # allow autonomous execution

mcp_servers:
  - name: browser
    command: npx @playwright/mcp
  - name: github
    command: npx @modelcontextprotocol/server-github
    env:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
  - name: filesystem
    command: npx @modelcontextprotocol/server-filesystem
    args: ["/opt/data/seo-reports"]
```

---

## 6. Summary Decision Table

| Question | Answer |
|---|---|
| Best default model | `google/gemini-3.5-flash` (#1 tool-calling benchmark, June 2026) |
| Best fallback 1 | `google/gemini-3.1-pro` (best deep-research + MCP Atlas score) |
| Best fallback 2 | `perplexity/sonar-pro` (live SERP + AI citation data) |
| Is Firecrawl built into Hermes? | ✅ Yes — native built-in, just add API key |
| Is DataForSEO built into Hermes? | ❌ No — add as HTTP Tool in config.yaml (easiest) |
| Is Google Search Console built into Hermes? | ❌ No — add as HTTP Tool with service account OAuth2 |
| Is there an MCP catalog in Hermes? | ✅ Yes — since May 2026, run `hermes mcp` for one-click installs |
| Can Playwright/Browser be added via catalog? | ✅ Yes — one-click from catalog |

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[Hermes_Obsidian_Windows_Install_Guide]]
