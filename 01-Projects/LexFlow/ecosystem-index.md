# LexFlow Ecosystem Index

> **Purpose:** Single renewable index of the LexFlow agentic ecosystem — profiles, repos,
> deployments, MCP, cron, kanban, standards, blockers. This is the canonical text index.
> The structured cross-platform export (6-sheet `.xlsx`) is a derived companion, not a second
> source of truth.
>
> **Renewal cadence:** manual, per the Quality Manifesto §9 reminder. Do NOT automate.
> **Last renewed:** 2026-09-19 (frontend-developer-lovable_react)
> **Next renewal:** 2026-09-20 (manual)

---

## HOW TO RENEW (read this first)

1. Update `Last renewed` / `Next renewal` at the top.
2. Refresh each section below against the live system — do not copy stale values:
   - Profiles: `ls ~/.hermes/profiles/`
   - Repos: `gh repo list Ole00007` + local `~/projects` / `Desktop/projects/services/LEGAL`
   - Deployments: `npx wrangler pages deployment list --project-name lexflow-site` + Railway dashboard
   - MCP: read each profile's `config.yaml` `mcp_servers:` block
   - Cron: `hermes cron list` (per profile) — verify jobs actually fire
   - Kanban: `hermes kanban list` — mark done/blocked/ready
3. Verify live endpoints return 200 (do not trust stale URLs — several legacy hosts are dead).
4. Append a row to the **Renewal log** at the bottom.
5. If a section is unchanged, write "unchanged" — do not re-type it.

---

## 1. Profiles (24)
admy_ceo · ads-expert · agency-growth · backend-dev · chatbot_builder · chatseo-agent ·
content-creator · crm-outreach-agent · customer-rel-manager · email-digest-agent ·
frontend-developer-lovable_react · gsc-agent · marketing-analyst · memory-curator ·
operator-installer · personal-assistant · sales-crm · seo-aeo-expert · seo-cron-agent ·
seo-swarm-agent · smoothy_op_dir · telegram-utility-agent · tester

## 2. Repositories
- Website: github.com/Ole00007/lexflow-website (PUBLIC). Branches: main, feat/heading-align-cta-merge, content/humanization-20260917.
- CRM: github.com/Ole00007/lexflow-crm (branch lexflow_hermes_v1). Local: Desktop/projects/services/LEGAL/aLEXy.
- **⚠️ TWO separate frontend surfaces — do not conflate (see §2a):**
  - **Single-page LP** → github.com/Ole00007/LexFlow-landing, local `~/projects/LEGAL_backup/LexFlow-landing` (migrated from `~/LexFlow-landing`, Repo Root Rule §8).
  - **Multi-page site** → local `/Users/olesiarasing/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site` (55+ HTML incl blog + articles; on Cloudflare via `wrangler.toml`).
- Others (9 public): LexFlow-MVP, LexFlow-Chatbot, LexBillFlow, LexTaskFlow, etc. — verify live.

### 2a. Two frontend surfaces — precise identity (2026-09-19)
| # | Surface | Local path | Repo / remote | Current HEAD (verified) | Deploy target | Conflation trap |
|---|---|---|---|---|---|---|
| A | **Single-page LP** (this upgrade brief's target) | `~/projects/LEGAL_backup/LexFlow-landing` (branch `main`; migrated from old `~/LexFlow-landing` which **no longer exists**) | `github.com/Ole00007/LexFlow-landing.git` | `55d5488` (2026-09-16: every CRM entry link → `/admin/panel`) | Netlify `poetic-kleicha-28d058` (deploy coordinated by operator-installer) | Brief at `lexflow-landing-upgrade-brief.md` named operator-installer's path but file lives under `smoothy_op_dir` profile |
| B | **Multi-page site** (deployed) | `/Users/olesiarasing/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site` | (not git-tracked 1:1 — untracked only; Cloudflare `wrangler.toml` + `_redirects`) | `4e526a0` (add `_redirects` 301 `/ -> /lexflow-index`) | Cloudflare Pages `lexflow-site` → `lexflow-site.pages.dev` | Has duplicate `(1)` backups (e.g. `lexflow-faq (1).html`) — those are stale backups, not the served files |

**Verified 2026-09-19 from live repo state:** Single-page LP has **0 legacy `web-production-ab54f` refs, 8 current `web-production-031a6` refs**, Romanelli premium style committed (`52f1bc6`), all 3 post-freeze Sept-16 fixes present. Multi-page site `git status` = **untracked-only** (probes, `wrangler.toml`, `src/`, `templates/` pre-deploy backups); **all tracked pages untouched** — no edits/deploys made by any agent since Sept 8. Both opened locally :8090 (LP) and :8091 (multi-page), all pages HTTP 200.

## 3. Deployments
- Cloudflare Pages `lexflow-site` → https://lexflow-site.pages.dev
  - Production: main @ 0a6f5bd (deploy 1cba771c). ORIGIN = https://lexflow-site.pages.dev (single source, build-lang-sites.py:42).
  - Deploy dir = dist/ (templates/build-dist.py). Build = build-lang-sites.py && build-dist.py.
- Railway CRM: web-production-031a6.up.railway.app (self-names "aLEXy" but IS LexFlow Production). Legacy ab54f host: do not link.

## 4. MCP servers
- composio (smoothy_op_dir): RESOLVED — session tool-router URL + x-api-key header. Refresh session when stale; do not block on durable OAuth route. Key env: MCP_COMPOSIO_API_KEY.
- obsidian-mcp: stdio via npx obsidian-mcp.

## 5. Cron / scheduled
- Daily LexFlow status (operator-installer): job 2573e20ab61f, 09:00 — update CRM project status + schedule unfinished tasks. (Verify it fires — was not visible in frontend profile's cronjob list.)

## 6. Kanban — open / blocked (2026-09-17)
- t_3c7158f8 [OVERRIDE] DoD §5 deployed w/o passing (operator-installer) — blocked
- t_7bf4de1f /api/public/intake (backend-dev) — blocked on Ole D1–D4
- t_051169c7 legal placeholders + P.IVA (operator-installer) — blocked on legal
- t_d6065167 / t_85d62411 aLEXy naming + intake + CORS (operator-installer) — blocked
- t_8c6d4642 verify EN capability claims vs CRM (operator-installer) — blocked
- t_62cbf086 Alessia widget → real intake (operator-installer) — blocked on UX sign-off
- t_167704c8 Carrozzeria 2DI vault sync (memory-curator) — blocked
- t_cc1f371c Composio RESOLVED (smoothy) — ready
- t_e8b10ba0 Composio account confirm (admy_ceo) — ready

## 7. Standards / hard rules
- LEXFLOW-Quality-Manifesto.md (candidate; override clause permanent)
- HARD RULE (all agents): no parallel source of truth / no duplicate registries unless vitally necessary (explain+flag)
- SEO/AEO/GEO audit standard: ~/Obsidian/03-Resources/Reference-General/seo-aeo-space-upgrade-audit-standard.md

## 8. Blockers
1. Legal identity (P.IVA, entity, address, PEC) — pending from Ole; gates "promotion" + fills placeholders.
2. Cloudflare Git integration — dashboard-native connect (prod branch main, build cmd, ORIGIN in CF env).
3. /api/public/intake — blocked on Ole D1–D4.
4. aLEXy naming correction in CRM.

## 9. Content export (humanization)
- Branch content/humanization-20260917, folder content-export-20260917/ (19 pages, 3038 blocks). Re-import by content_id.

---

## Renewal log
| Date | Renewed by | Key changes |
|---|---|---|
| 2026-09-17 | frontend-developer-lovable_react | Initial; Composio resolved; prod @0a6f5bd; daily status cron added |
| 2026-09-19 | frontend-developer-lovable_react | Added §2a — precise split of the TWO frontend surfaces (single-page LP vs multi-page site), live paths/HEADs/refs verified; noted LP repo relocated to `~/projects/LEGAL_backup/` |

## Links
- Parent: [[LexFlow]]
- Related: [[LEXFLOW-Quality-Manifesto]] · [[seo-aeo-space-upgrade-audit-standard]]
