# LexFlow / AVIBE Ecosystem — Cross-Platform Project Index **v3**

**Generated:** 2026-09-16 (Europe/Rome) — supersedes v2 (2026-08-28, `LexFlow_Ecosystem_Index.md`)
**Companion file:** `LexFlow_Ecosystem_Index_v3_2026-09-16.xlsx` (6 sheets: Master Index, Live Endpoints (Verified), GitHub Repos (Live), Local Repos, Obsidian Vault, Gaps & Blockers)
**Vault mirror:** `~/Obsidian/_Inbox/LexFlow-Ecosystem-Index-v3-2026-09-16.md`

## What changed vs v2

| # | v2 said | v3 (verified 2026-09-16) |
|---|---|---|
| 1 | Railway status was "last documented, not confirmed right now" | Every endpoint below was probed live with `curl` on 2026-09-16 |
| 2 | `lexflow-mvp-production.up.railway.app` was "the" CRM | It answers **404 on `/`**; the live CRM is **`web-production-031a6.up.railway.app`** (200, serves "aLEXy – Legal Intake & Status Suite") |
| 3 | Netlify LP documented as `poetic-kleicha.netlify.app` / `lexflow-landing.netlify.app` | **Both 404.** The real legacy LP is **`poetic-kleicha-28d058.netlify.app`** (200) — older docs dropped the `-28d058` suffix |
| 4 | "11 GitHub repos" | **9 public repos** enumerable unauthenticated; the 2 private repos in v2 (`avibe-agency-mvp`, `lextaskflow-e953c3e7`) are no longer visible without a token — not confirmed deleted |
| 5 | LexFlow landing "auto-deploying to Netlify" (implied current) | The **new** multi-page web-site has **no git remote and no deploy config** — it deploys nowhere yet. Only the **legacy** LP is live on Netlify |
| 6 | Vault "8 of 177 notes use `[[wikilinks]]`" | Vault auto-linked 2026-08-26: **210/226 notes linked**, per-folder hubs, 409 edges; vault is a git repo (`Ole00007/obsidian-vault`) |

## The four-layer truth model (unchanged)

```
Local code repos  →  GitHub (deployed truth)  →  Obsidian vault (knowledge)  →  Hindsight avibe-hq (long-term memory)
```

Each layer answers a different question: repos = what the code is; GitHub = what is pushed;
vault = what we know and decided; Hindsight = what survives across sessions.

---

## A. LexFlow product family

| Project | Type | Local path | GitHub | Deploy platform | Live URL | Status (2026-09-16) |
|---|---|---|---|---|---|---|
| **LexFlow CRM (aLEXy intake & status suite)** | Flask app, multi-tenant, RLS in progress | `~/Desktop/projects/services/LEGAL/LEXFLOW Production/lexflow-crm` | `Ole00007/lexflow-crm` (pushed 2026-09-04) | **Railway** | `https://web-production-031a6.up.railway.app/` → **200** | LIVE. `/login?ws=lexflow` 200, `/admin/panel` 200, `/kanban` 200. Public intake contract **not enabled** (`POST /api/public/intake` 404) |
| **LexFlow Web-Site (marketing, trilingual EN/IT/RU)** | Static HTML, generated `it/`+`ru/`, agent surface | `~/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site` | **none** | **none chosen** | **not deployed** | HEAD `88f6cc9`, 31 modified files in flight, 74 placeholder-domain files. Blocked on domain + host choice (Ole → Cloudflare) |
| **LexFlow legacy landing page (LP)** | Single-page HTML + Alessia widget | `~/Projects/LEGAL_backup/LexFlow-landing` (git → `Ole00007/LexFlow-landing`, HEAD `47ed616`, has `netlify.toml`) | `Ole00007/LexFlow-landing` (pushed 2026-09-02) | **Netlify** | `https://poetic-kleicha-28d058.netlify.app/` → **200** ("LexFlow — Studio Legale X") | LIVE legacy surface. Frozen by Ole — reference only. **Moved:** the old `~/LexFlow-landing` path in older docs is stale — the repo now lives under `~/Projects/LEGAL_backup/`. Live deploy sha256 == `origin/main:index.html` |
| **LexFlow Chatbot (empathic secretary)** | Flask, `/chat` POST | `~/Projects/LEGAL_backup/LexFlow-Chatbot` (`server.py`, Procfile) | `Ole00007/LexFlow-Chatbot` (pushed 2026-05-19) | **Railway** | `https://lexflow-chatbot-production.up.railway.app/` → **200**, `/health` **200**, `/chat` **405** (POST-only) | LIVE, healthy. Not yet wired to the new site (`chatbotUrl` path 404s) |
| **LexFlow-MVP (first CRM iteration)** | Flask + admin, Procfile + `railway.toml` | `~/Desktop/projects/services/LEGAL/LexFlow-MVP` (branch `main`, HEAD `f1ad2d3` 2026-09-02, dirty) | `Ole00007/LexFlow-MVP` | Railway service still exists | `https://lexflow-mvp-production.up.railway.app/` → **404** | Legacy/superseded service. Old docs naming it "the backend" are stale |
| **RLS hardening work** | Alembic migration + 18 cross-tenant tests | `~/Desktop/projects/services/LEGAL/lexflow-rls` (branch `feat/rls`) | not pushed | n/a | n/a | **Built, NOT merged.** 11 RLS tables + 2 uncovered gap tables; 5 Alembic risks documented (card `t_4637a500`) |
| **Saved-views worktree** | Flask work copy | `~/Desktop/projects/services/LEGAL/lexflow-savedviews` | not pushed | n/a | n/a | Working copy, no remote |

## B. AVIBE / infrastructure

| Asset | What it is | Deploy | Live URL | Status (2026-09-16) |
|---|---|---|---|---|
| **avibe-hindsight** | Long-term memory backend for the 24-profile Hermes roster (bank `avibe-hq`) | Railway | `https://avibe-hindsight-production.up.railway.app/health` → **200** | HEALTHY. LLM routed to OpenRouter, **free models only** (Ole decision 2026-08-30) |
| **Hermes roster** | 24 independent profiles (own config/keys/sessions/gateway), `operator-installer` orchestrates | local | n/a | Active. operator-installer model moved to OpenRouter `deepseek/deepseek-v4.1-flash` (resolved the Nous-auth blocker) |
| **Hermes Kanban boards** | Inter-profile work channel; `default` + new isolated `lexflow-learning` | local SQLite `~/.hermes/kanban.db` | n/a | Active, dispatcher running |
| **Obsidian vault** | Knowledge layer, PARA + `_Inbox`, `AGENT_RULES.md` v2.2 | local + GitHub private | `github.com/Ole00007/obsidian-vault` | git repo, linked graph 210/226 |
| **AVIBE agency assets** | Brand/site/proposal material | local | n/a | `~/Desktop/projects/services/AVIBE AGENCY` (site placeholder, style book, agentic-architecture-package-v2) |
| **lexflow_saas_factory** | SaaS-factory deck + plan (HTML/PPTX/XLSX) | local | n/a | `Lexflow Ecosystem & Saas Factory/` — source material for this index |

## C. Client & vertical sites

| Asset | Client | GitHub | Live URL | Status (2026-09-16) |
|---|---|---|---|---|
| **Avv-Pagliano site / CRM** | Avvocato Diego Pagliano (Genova) | `Ole00007/Avv-Pagliano` (pushed 2026-05-25) | `https://verdant-crumble-021449.netlify.app/` → **200** ("Avv. Diego Pagliano — Avvocato Civilista a Genova") | LIVE. Pagliano is also tenant `ws=pagliano` on the LexFlow CRM (200) and is the **canary** for the UX rollout order |
| **Romanelli-studio site** | Studio-Romanelli | `Ole00007/Romanelli-studio` (pushed 2026-08-31) | no URL recorded | Client site + `romanelli-studio SEO Audit LP` locally |
| **9 generated vertical sites** | demo/vertical templates from `gen_site.py` | not on GitHub | local only | `~/Obsidian/01-Projects/sites/`: bar-del-porto, beauty-studio, firenze-segreta, genova-segreta, liguria-viaggi, mare-fiori.it, massage-studio, nail-studio, parruchiere (+ `.json` configs, `sites-INDEX.md`) |
| **Alena-Krot** | SEO/AEO client (bilingual RU/IT) | not on GitHub | no URL recorded | `~/Desktop/projects/services/ALENA KROT/Alena Krot SEO` + vault `01-Projects/Alena-Krot-Med-Expert` |
| **Carrozzeria 2DI** | auto-body client | not on GitHub | no URL recorded | `~/Desktop/projects/services/2DI Catrozzeria` |
| **Commercialista-Client** | accounting client | not on GitHub | no URL recorded | vault `01-Projects/Commercialista-Client` |

---

## D. Live endpoint verification (all probed 2026-09-16 with `curl`)

| URL | Method | Code | Verdict |
|---|---|---|---|
| `https://web-production-031a6.up.railway.app/` | GET | 200 | Live CRM (title "aLEXy – Legal Intake & Status Suite") |
| `.../login` | GET | 200 | Login page |
| `.../login?ws=lexflow` | GET | 200 | **Correct CTA target** — workspace deep link |
| `.../login?ws=pagliano` | GET | 200 | Pagliano tenant |
| `.../admin/panel` | GET | 200 | Superadmin surface |
| `.../kanban` | GET | 200 | Board |
| `.../api/contacts` | GET | 200 | Returns `[]` for anonymous by design (not a leak) |
| `.../api/contacts` | POST | 401 | Auth required — this is why site intake is unwired |
| `.../api/chatbot` | GET | 404 | Route does not exist |
| `.../api/public/intake` | GET | 404 | **Contract-defined, not implemented** |
| `.../api/public/intake` | POST | 404 | Same |
| `.../api/health` | GET | 404 | Route does not exist (do not use as a healthcheck) |
| `.../robots.txt` | GET | 404 | Not served |
| `https://lexflow-chatbot-production.up.railway.app/` | GET | 200 | Chatbot service live |
| `.../health` | GET | 200 | Chatbot healthcheck |
| `.../chat` | GET | 405 | POST-only |
| `https://lexflow-mvp-production.up.railway.app/` | GET | 404 | Service answers, no root route (superseded service) |
| `https://avibe-hindsight-production.up.railway.app/health` | GET | 200 | Memory backend HEALTHY |
| `https://poetic-kleicha-28d058.netlify.app/` | GET | 200 | **Live legacy LexFlow LP** (Alessia widget) |
| `https://poetic-kleicha.netlify.app/` | GET | 404 | Stale URL in older docs (missing `-28d058`) |
| `https://lexflow-landing.netlify.app/` | GET | 404 | Stale URL in older docs |
| `https://lexflow-lp.netlify.app/` | GET | 404 | Never deployed |
| `https://lexflow.netlify.app/` | GET | **401** | Site **exists** behind Netlify password protection. Ownership/contents unverified |
| `https://verdant-crumble-021449.netlify.app/` | GET | 200 | Avv. Pagliano client site (listed as CORS origin in old CRM config) |
| `https://muzloto-apr-1f8f19.netlify.app/` | GET | 200 | "LexTaskFlow — Architecture Schema" — not a LexFlow product surface |
| `https://lexflow.pages.dev/` | GET | 200 | **NOT ours** — a South African legal-admin company. No LexFlow deployment on Cloudflare Pages |
| `https://alexy.it/` | GET | 200 | Resolves with an empty body; ownership unconfirmed — treat as unknown |

**Correct CTA deep link (verified by card `t_198870bd` on 2026-09-16):**
`/login?ws=lexflow&back=<landing>` — the legacy LP's 7 CTAs all use it; 0 bare-root, 0 `/admin`.

**Where does the web-site actually deploy? Answer: nowhere, yet.** The new multi-page site
has no git remote and no `netlify.toml` / `vercel.json` / `wrangler.toml`, so no host can be
building it. The only live LexFlow marketing surface today is the **legacy** Netlify LP at
`poetic-kleicha-28d058.netlify.app`. Deploy target is still Ole's open decision (Cloudflare
was his stated preference on 2026-09-13).

## E. GitHub repos (live, public API, 2026-09-16 — 9 total)

| Repo | Language | Last push | Note |
|---|---|---|---|
| `LexFlow-MVP` | Python | 2026-09-02 | First CRM iteration; superseded |
| `LexFlow-landing` | HTML | 2026-09-02 | Legacy LP → Netlify `poetic-kleicha-28d058` |
| `lexflow-crm` | Python | 2026-09-04 | **Canonical CRM repo** (the local `aLEXy/` folder tracks it, branch `lexflow_hermes_v1`) |
| `LexFlow-Chatbot` | Python | 2026-05-19 | Chatbot → Railway, live |
| `aLEXy` | Python | 2026-08-03 | Sister CRM product |
| `avibe-hindsight` | Python | 2026-08-30 | Memory backend |
| `Avv-Pagliano` | — | 2026-05-25 | Client site/CRM |
| `Romanelli-studio` | HTML | 2026-08-31 | Client site |
| `obsidian-vault` | HTML | 2026-08-30 | Private-ish knowledge repo (vault sync) |

Not listed = not enumerable without a token (private). `gh` CLI is **not authenticated** on
this machine and no `GH_TOKEN` is set, so private repos are invisible to this audit.

## F. Local repo map (`~/Desktop/projects/services/`)

```
LEGAL/
  LexFlow-MVP/            git → Ole00007/LexFlow-MVP, branch main, HEAD f1ad2d3, dirty
  aLEXy/                  git → Ole00007/lexflow-crm, branch lexflow_hermes_v1, HEAD 8ea18c2
  lexflow-rls/            RLS branch work copy (feat/rls) — not pushed
  lexflow-savedviews/     work copy — no remote
  LEXFLOW Production/
    LEXFLOW Web-Site/     new marketing site — NO git remote (HEAD 88f6cc9)
    lexflow-crm/          Flask app work copy (card t_16356a2c target)
    lexflow-calendar/     archive/work copy
    lexflow-attachments/  archive/work copy
    Elisa/                Elisa access plan (dev access)
    Lexflow Ecosystem & Saas Factory/   deck, plan, this index (v3 here)
    architect & plan_Perpl REASONING_Double check/  plans, decisions log
  Romanelli 4page site_with Avv Pics /, romanelli-studio SEO Audit LP/
  CRM refs/, LEGAL_CRM examples/, SEO/, Templates copy/
ALENA KROT/, 2DI Catrozzeria/, AVIBE AGENCY/, SALES & Marketing/, SEO/, R&D_Audit_PNL/
```

`~/Projects/` (separate root, already in use — this is where the frozen/moved repos live):

```
Projects/
  LEGAL_backup/           MIRROR of relocated LEGAL repos:
    LexFlow-landing/      git → Ole00007/LexFlow-landing, HEAD 47ed616, has netlify.toml
    LexFlow-Chatbot/      server.py + Procfile
    aLEXy/, Romanelli-studio/, pagliano_backup_readonly/, lexflow-landing-visual/
  avibe-hindsight/        git → Ole00007/avibe-hindsight, HEAD bfbe48e (free-only OpenRouter chain)
  avibe-flowershop/       local, no git
```

Note: `~/LexFlow-landing` and `~/LexFlow-Chatbot` (paths quoted in older docs) no longer exist —
they were relocated under `~/Projects/LEGAL_backup/`. Card `t_198870bd` re-found the landing repo
there on 2026-09-16.

**Repo-root caveat (unchanged from the 2026-09-16 decision note):** `~/Desktop` is TCC-protected
and agents hit intermittent `Operation not permitted`; the recommended root is
`/Users/olesiarasing/projects` (lowercase), with `~/Desktop/projects` frozen read-only legacy.
Awaiting Ole's go — nothing migrated.

## G. Obsidian vault status

- PARA + `_Inbox` structure, 01-Projects has 19 entries incl. LexFlow, aLEXy, AVibe-CRM, `sites`.
- Wikilink graph: **210/226 notes linked** (auto-linked 2026-08-26), per-leaf-folder hubs
  (`LexFlow-INDEX`, `aLEXy-INDEX`, …). Hub notes intentionally have no outgoing Links section.
- Vault is a git repo pushed to private `Ole00007/obsidian-vault` (secrets gitignored).
- **LexFlow folder hubs:** `01-Projects/LexFlow/LexFlow-INDEX.md`; legacy material still lives in
  `01-Projects/AVibe-CRM/LexFlow/` (older mirror) — do not confuse the two.
- Hindsight syncs the vault, so notes written here become long-term memory (`avibe-hq`).

## H. Gaps & blockers

| # | Gap | Owner | Impact |
|---|---|---|---|
| 1 | Web-site has no host, no remote, no domain | **Ole** (Cloudflare decision) | Site cannot deploy; 74 files hold `lexflow.example.com` |
| 2 | `POST /api/public/intake` not implemented; `POST /api/contacts` 401 | backend-dev / operator-installer | Website lead capture is dead-ended; intake falls back to WhatsApp |
| 3 | Site copy: `llms.txt` line 18 says calendar/cloud/notifications "NOT shipping", contradicting `faq_a15` | frontend-developer | Published factual contradiction |
| 4 | 27 webhook URLs null; `intakeEndpoint` null; WhatsApp digits unconfirmed | Ole + frontend-developer | Silent failures / wrong contact number |
| 5 | IT/RU article bodies pending | Ole | Localised articles stay English (pipeline requires registration in `templates/article_content.py`) |
| 6 | RLS built but unmerged; 2 tables uncovered (`contact_relationship`, `firm_team_member`) | backend-dev (card `t_4637a500`) | Multi-tenant safety not enforced at DB level |
| 7 | `lexflow.netlify.app` password-protected site ownership unknown | Ole | Possible orphaned deploy consuming the "lexflow" Netlify name |
| 8 | `GH_TOKEN`/`gh` not authenticated; no railway CLI binary; no netlify token | Ole | No agent can enumerate private repos or platform dashboards |
| 9 | Repo-root migration to `~/projects` unapproved | Ole | Agents keep hitting Desktop TCC walls |
| 10 | `verification-plan.md` figures (34% faster, 2.4× billable, 91% WAU) unverifiable from the CRM schema | Ole | Marketing claims need confirm-or-replace |

## I. What I could NOT verify (honesty section)

- **Railway dashboard / project list:** the `railway` CLI is installed but its binary is
  missing (`@railway/cli` install incomplete) and no project token is present. Status above
  comes from live HTTP probes of the service URLs, not the platform.
- **Netlify account site list:** no Netlify auth token on this machine (`~/.netlify` absent;
  CLI config holds only `cliId`/`userId`). So `lexflow.netlify.app` (401) cannot be attributed
  to Ole's account from here — log into Netlify and check whether that site is yours.
- **Private GitHub repos:** unauthenticated API returns public repos only.
- **Cloudflare account:** not checked (no credential); only public `pages.dev` hosts probed.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Agent-Surface-2026-09-15]]
- Related: [[LexFlow-Web-Site-Session-Recap-Batch2-2026-09-13]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-Public-Intake-Contract-2026-09-15]]
