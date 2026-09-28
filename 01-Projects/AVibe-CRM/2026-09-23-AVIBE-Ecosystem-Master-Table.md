---
title: AVIBE Ecosystem — Master Table
created: 2026-09-23
updated: 2026-09-23
tags: [avibe, lexflow, inventory, ecosystem, master-table]
status: DRAFT — pending Ole review
owner: memory-curator
---

# AVIBE Ecosystem — Master Table

> **Format decision (2026-09-23):** `AVIBE_Muzloto_Chatbot_Master_Index.xlsx` was **not found** anywhere
> in the vault or `~/Downloads`, and Google Drive is **not authorised** on this profile
> (`setup.py --check` → `NOT_AUTHENTICATED`). So this table is a **self-designed best fit** built only from
> sources verifiable locally right now: the Obsidian vault (file system truth), GitHub (`gh`, verified),
> and Railway (`railway`, verified). Drive-only assets are **not listed** — they need OAuth first (see §D).

**Columns:** name · type · location/link · status · last updated · owner

---

## A. Railway projects (verified via `railway list` / `railway api`)

| Name | Type | Location / link | Status | Last updated | Owner |
|---|---|---|---|---|---|
| graceful-presence | Railway project — avibe-hindsight + Postgres | https://railway.app/project/9b08be93-b288-4772-8ccc-29b724851bf0 | ✅ online — Hindsight memory bank `avibe-hq` | 2026-09-21 (audit) | operator-installer |
| perceptive-achievement | Railway project — web, LexFlow-Chatbot, Postgres | https://railway.app/project/1fe25c7a-6a68-4c21-b27f-50c3e69daaf3 | ✅ live — **LexFlow CRM production** (`web-production-031a6`, health 200) | 2026-09-21 (status run) | operator-installer |
| precious-rejoicing | Railway project — web, Postgres, function-bun | https://railway.app/project/9c6f87e9-2d41-438b-b92c-1f62120b4d6a | 💤 idle | 2026-07-21 | Ole (unassigned) |
| dependable-vitality | Railway project — outstanding-connection | https://railway.app/project/cea51701-d5dd-43ab-be30-7488bc2785db | 💤 idle | 2026-07-19 | Ole (unassigned) |
| flask-EMPTY-Postgres | Railway project — web, Postgres | https://railway.app/project/70cd9252-31f6-49f5-b86c-a3ac32469f57 | 💤 idle scaffold | 2026-08-03 | Ole (unassigned) |
| compassionate-trust | Railway project — web | https://railway.app/project/5fb4dd26-3a6b-4646-a8d8-65dddd85eb1f | 💤 idle | 2026-05-09 | Ole (unassigned) |

## B. GitHub repos (verified via `gh repo list Ole00007`)

| Name | Type | Location / link | Status | Last updated | Owner |
|---|---|---|---|---|---|
| obsidian-vault | **PUBLIC** repo — vault backup | https://github.com/Ole00007/obsidian-vault | ⛔ **visibility risk** (see §E) | 2026-09-22 | memory-curator |
| avibe-hindsight | Public — master-brain / memory stack | https://github.com/Ole00007/avibe-hindsight | ✅ active | 2026-09-17 | operator-installer |
| avibe-agency-mvp | Private — agency MVP | https://github.com/Ole00007/avibe-agency-mvp | ✅ active | 2026-09-19 | Ole |
| lextaskflow-e953c3e7 | Private | (private) | ⚠️ unclear — duplicate-ish of LexFlow? | 2026-09-17 | Ole |
| lexflow-crm | Public — CRM | https://github.com/Ole00007/lexflow-crm | ⚠️ stale (Jul 20) | 2026-07-20 | operator-installer |
| LexFlow-MVP | Public | https://github.com/Ole00007/LexFlow-MVP | ✅ active | 2026-09-02 | operator-installer |
| LexFlow-landing | Public — landing page | https://github.com/Ole00007/LexFlow-landing | ✅ active | 2026-09-02 | operator-installer |
| lexflow-website | Public — multipage | https://github.com/Ole00007/lexflow-website | ✅ active | 2026-09-17 | Ole |
| LexFlow-Chatbot | Public — empathic-secretary chatbot | https://github.com/Ole00007/LexFlow-Chatbot | ✅ active | 2026-07-20 | Ole |
| aLEXy | Public — vertical legal SaaS (v0 heritage) | https://github.com/Ole00007/aLEXy | 💤 Phase 4, deploy failed | 2026-08-03 | Ole |
| Avv-Pagliano | Public — client site | https://github.com/Ole00007/Avv-Pagliano | ✅ live | 2026-08-01 | agency |
| Romanelli-studio | Public — client site | https://github.com/Ole00007/Romanelli-studio | ✅ live | 2026-09-17 | agency |
| MTA-Group- | Public — client site | https://github.com/Ole00007/MTA-Group- | ✅ live | 2026-09-19 | agency |
| (client sites via gen_site.py) | Public — Alena-Krot, Studio-Romanelli, Carrozzeria-2DI, Commercialista, Genova Mediation | not enumerated here | ✅ live | — | agency |

## C. Vault assets (filesystem truth, `~/Obsidian`)

### C1. LexFlow — SaaS factory deck / strategy / pricing
| Name | Type | Location | Status | Last updated | Owner |
|---|---|---|---|---|---|
| lexflow_saas_factory.pptx | **SaaS factory deck** | `01-Projects/LexFlow/` | ✅ current | 2026-09 | Ole |
| lexflow_saas_factory.html | Deck (HTML) | `01-Projects/LexFlow/` | ✅ current | 2026-09 | Ole |
| lexflow_saas_factory_plan.xlsx | Deck plan | `01-Projects/LexFlow/` | ✅ current | 2026-09 | Ole |
| LexFlow_Ecosystem_Index_v3_2026-09-16.xlsx | Ecosystem index | `01-Projects/LexFlow/` | ✅ current | 2026-09-16 | memory-curator |
| LexFlow_Ecosystem_Index (1).xlsx | Ecosystem index — **duplicate twin** | `01-Projects/LexFlow/` | ⚠️ dedupe candidate | 2026-09-15 | memory-curator |
| LexFlow_Automation_MasterPlan.xlsx | Strategy / automation | `01-Projects/LexFlow/` | ✅ current | 2026-09-15 | Ole |
| ecosystem-index.md | Strategy index (markdown) | `01-Projects/LexFlow/` | ✅ current | 2026-09-19 | memory-curator |
| lexflow-pricing.html | **Price list** | `01-Projects/LexFlow/` | ✅ current | 2026-09-05 | Ole |
| LexFlow-Project-Status.md | Status mirror | `01-Projects/LexFlow/` | ✅ CURRENT | 2026-09-23 | operator-installer |
| LexFlow-INDEX.md | Folder hub | `01-Projects/LexFlow/` | ✅ | 2026-09-19 | memory-curator |
| LexFlow-Public-Intake-Contract-2026-09-15.md | Contract / legal | `01-Projects/LexFlow/` | ✅ | 2026-09-15 | Ole |
| LexFlow-Web-Site-SEO-AEO-GEO-Origin-Plan-2026-09-16.md | SEO/GEO strategy | `01-Projects/LexFlow/` | ✅ | 2026-09-16 | Ole |
| lexflow-agentic-v3.zip | Agentic pack (archive) | `01-Projects/LexFlow/` | ✅ | 2026-09-17 | Ole |
| LexFlow-Workspace-2026-08-31-Inventory.md | Workspace/tenant inventory | `01-Projects/LexFlow/` | ✅ CURRENT | 2026-09-03 | operator-installer |
| docs/LexFlow_Agentic_Roadmap.json | **Canonical roadmap tracker** | CRM repo | ✅ authority | 2026-09-21 | operator-installer |

### C2. AVIBE agency
| Name | Type | Location | Status | Last updated | Owner |
|---|---|---|---|---|---|
| agentic_architecture_deck.html | **Strategy deck** | `01-Projects/AVibe-Agency/` | ✅ | 2026-07-19 | Ole |
| agentic-architecture-package-v2/ | Architecture package (CSVs, diagrams) | `01-Projects/AVibe-Agency/` | ✅ | 2026-07-19 | Ole |
| AVibe_WebDev_Reference_2026.numbers | Reference | `AVIBE Agency Site/` | ✅ | 2026-06-17 | Ole |
| Advanced_Landing_Project_Plan.numbers | Project plan | `AVIBE Agency Site/` | ✅ | 2026-06-17 | Ole |
| offers_AVIBE_general.png | **Offer / price sheet (graphic)** | `03-Resources/Reference-General/` | ✅ | — | Ole |
| STYLE BOOK/ (logos) | Brand assets | `01-Projects/AVibe-Agency/` | ✅ | 2026-03-23 | Ole |
| Feature card *.png (3) | Marketing assets | `01-Projects/AVibe-Agency/` | ✅ | 2026-07-26 | Ole |
| avibe_agency_legal_site_package.zip | Client package | `01-Projects/AVibe-CRM/` | ✅ | 2026-09-17 | agency |
| avibe-preventivo-*.pdf (crm-officina v2–v5, mta-group) | **Price lists / quotes** | `01-Projects/AVibe-CRM/` | ✅ | 2026-09-20 | Ole |
| preventivo-mta-group-final-v2.html | Quote (HTML) | `01-Projects/AVibe-CRM/` | ✅ | 2026-09-19 | Ole |
| vertical_saas_pricing_benchmarks.xlsx | Pricing research | `03-Resources/Reference-General/` | ✅ | — | Ole |
| lovable-prompt-avibe-website-proposal.md | Website proposal | `01-Projects/AVibe-CRM/` | ✅ | 2026-08-27 | Ole |

### C3. Hindsight / memory stack
| Name | Type | Location | Status | Last updated | Owner |
|---|---|---|---|---|---|
| avibe_hindsight_setup_guides.xlsx | **Setup guides** (device + per-client) | `01-Projects/AVibe-CRM/` | ✅ | 2026-08-15 | memory-curator |
| hermes_rules_avibe_hindsight.md | Runtime rules | `01-Projects/AVibe-CRM/` | ✅ | 2026-08-30 | operator-installer |
| AGENTS.md (avibe-hindsight) | Authoritative runtime doc | repo + `_from-repos/` | ✅ | 2026-09-17 | operator-installer |
| Hindsight-Read-Auth-Runbook.md | Runbook | `03-Resources/Hermes-Setup-and-MCP/` | ⚠️ `status: pending` is **stale** | 2026-09-21 | memory-curator |
| 2026-09-21-avibe-hindsight-network-egress-audit.md | Audit (egress/networking/cost) | `_Inbox/` | ✅ | 2026-09-21 | memory-curator |

### C4. Hermes setup / ops
| Name | Type | Location | Status | Last updated | Owner |
|---|---|---|---|---|---|
| Obsidian_Hermes_Vault_Strategy_AllSheets.md | **Strategy doc** | `03-Resources/Hermes-Setup-and-MCP/` | ✅ | — | Ole |
| Obsidian_Hermes_Vault_Strategy_AllSheets (1).md | Duplicate twin | same | ⚠️ dedupe candidate | — | memory-curator |
| hermes-chatbot-builder.md | **Chatbot index / builder** | `03-Resources/Hermes-Setup-and-MCP/` | ✅ | — | Ole |
| hermes-chatbot-builder (1).md | Duplicate twin | same | ⚠️ dedupe candidate | — | memory-curator |
| hermes-multi-agent-ops-plan.xlsx | Ops plan | `03-Resources/Hermes-Setup-and-MCP/` | ✅ | — | operator-installer |
| hermes_tracking_plan (1).xlsx | Tracking plan | `03-Resources/Hermes-Setup-and-MCP/` | ✅ | — | operator-installer |
| Copyrighter_Skills_IT_EN_RU.xlsx | Skills matrix | `03-Resources/Hermes-Setup-and-MCP/` | ✅ | — | Ole |
| Model-Priceinoutper1M-Tier-Bestfitinyourroster.csv | Model price list | `03-Resources/AI-Models-and-Prompts/` | ✅ | — | Ole |
| Hermes swarm *.png (3) | Org charts | `_Trash/` + `_Inbox/` | ⚠️ **trash-only risk** | — | memory-curator |

### C5. Widget patches / client web work
| Name | Type | Location | Status | Last updated | Owner |
|---|---|---|---|---|---|
| Romanelli worker patches | Widget / site patch (Cloudflare Worker v c15cde68) | repo `Ole00007/Romanelli-studio` | ✅ live | 2026-09-17 | agency |
| Alena-Krot / Studio-Romanelli / Carrozzeria-2DI / Commercialista / Genova Mediation | Client sites (gen_site.py) | repos + `01-Projects/<Client>/` | ✅ live | — | agency |
| LexFlow-Web-Site-* (Build / Scope / Enrichment / CRM-Repoint) | Web build patches | `01-Projects/LexFlow/` | ✅ | 2026-09-18 | Ole |
| Area-LocalLexFlowpage-NetlifyLP-WhatHermesshoulddo.csv | Netlify LP patch task | `01-Projects/LexFlow/` | ✅ | 2026-09-16 | Ole |

---

## D. Not covered — blockers

| Gap | Why | Unblock |
|---|---|---|
| **Google Drive assets** | Drive not authorised on this profile: no `google_token.json`, no `google_client_secret.json`, no `gws` | One-time OAuth (Ole): Google Cloud OAuth client → `setup.py --client-secret` → `--auth-url` → `--auth-code` |
| `AVIBE_Muzloto_Chatbot_Master_Index.xlsx` | Not present in vault or `~/Downloads` | Locate it (Drive, once authorised) — then merge its rows into §C |
| Drive-only items named in the request (strategy docs, chatbot indexes, price lists, setup guides, widget patches, SaaS factory deck) | Same OAuth blocker | Same |

## E. Findings raised by building this table

1. **`obsidian-vault` is PUBLIC** (`isPrivate: false`, verified via `gh`). The vault holds client PII (addresses, phone numbers, test credentials, workspace IDs). This is the highest-severity item here — flip to private or purge the sensitive notes from history.
2. **Duplicate twins in permanent folders** (`LexFlow_Ecosystem_Index (1).xlsx`, `Obsidian_Hermes_Vault_Strategy_AllSheets (1).md`, `hermes-chatbot-builder (1).md`) — the stager/`_Conflicts` sweep only guards `_Inbox`, so twins inside `01-Projects`/`03-Resources` are never caught.
3. **Hermes swarm org-chart PNGs survive only in `_Trash/`** — `_Trash` is pruned after 30 days, so these are on a deletion timer.
4. **`lextaskflow-e953c3e7` (private repo)** overlaps the LexFlow name family with no description — needs identification or archiving.

## Links
- Parent: [[AVibe-CRM-INDEX]]
- Related: [[01-Projects/LexFlow/LexFlow-INDEX|LexFlow-INDEX]]
- Related: [[AVibe-Agency-INDEX]]
- Related: [[2026-09-21-avibe-hindsight-network-egress-audit]]
- Related: [[LexFlow-Workspace-2026-08-31-Inventory]]
