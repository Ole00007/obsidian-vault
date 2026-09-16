---
title: Hermes 14-Day Installation Roadmap — agents, memory, skills, routing, tests (draft)
created: 2026-09-16
updated: 2026-09-16
tags: [hermes, roadmap, installation, orchestration, model-routing, decisions]
status: draft
source_task: t_62db7c26
author: memory-curator
confidence: mixed — every §0/§2.1/§4/§6 figure re-verified from disk 2026-09-16 17:21–17:33 CEST (revision r4); items still marked (unverified) need a live check
revision: r4 — 2026-09-16 17:33 CEST: round-3 review corrections — §0/§7 skill count range 59–117 / ~2,200 → **59–123 / 2,131**; §6.3 completed to all 13 aux routes (4 named-ID rows added: `triage_specifier`, `kanban_decomposer`, `profile_describer`, `curator`) and the inaccurate "not verifiable from config" parenthetical removed
---

# Hermes 14-Day Installation Roadmap (draft)

**Status: DRAFT / PROPOSAL.** Nothing in here has been executed. No profile was created,
merged, renamed or deleted; no connector was connected. Every profile-level change listed as
"propose" needs Ole's approval and is executed by `operator-installer`, not by this note's author.

Source of instructions: `~/Obsidian/03-Resources/Hermes-Setup-and-MCP/hermes_setup_brief.md`.
Recorded decision (Ole, 2026-09-16): stack = **Option 1.4 — Nous Plus primary + OpenRouter
overflow**; **LexFlow stays the top-priority workspace**.

## 0. What is already true today (evidence, 2026-09-16)

Read from the live machine, not from the brief — the brief assumes a greenfield install, the
reality is a running 22-profile estate.

**Re-verified 2026-09-16 17:21–17:25 CEST (r3).** Every row below was re-read from disk at that
timestamp. The estate is live and moves under the note: two profile defaults (`lexflow_dev_head_admin`,
`personal-assistant`) were repaired at 17:15 *during* the r2 review, which invalidated three rows
written at 17:10. Read a row as historical if it is older than the timestamp in it.

| Fact | Evidence |
|---|---|
| 22 profiles + the default instance | `ls ~/.hermes/profiles/` (was 23; `librarian` retired into `memory-curator` on 2026-09-16) |
| Model keys exist for 19/22 profiles | `OPENROUTER_API_KEY` present in 19 profile `.env` files (re-verified 2026-09-16 17:21); `chatbot_builder`, `email-digest-agent`, `tester` have none |
| Nous Portal auth is **stale** | weekly KPI cron on `operator-installer` last failed with `No access token found for Nous Portal login. Run 'hermes model' to re-authenticate.` — this breaks the "Nous primary" half of Option 1.4 |
| Cron plumbing is partly broken | `memory-curator` has **9** cron jobs; 8 carry `last_status: error` — 7 on the dead model `qwen/qwen3-4b:free`, 1 on `RuntimeError: Connection error.` (all `last_run_at` = 2026-09-15, i.e. *before* the 2026-09-16 model swap — the recorded errors are stale, not necessarily current; verified 2026-09-16 17:23). 2 `operator-installer` jobs error on a Hermes code bug (`ImportError: cannot import name '_FULL_ARGS_LOG_BOUND' from 'agent.message_sanitization'`) |
| Telegram **delivery** is failing from cron | `deliver: telegram:1372207688` → `httpx.ConnectError: [Errno 8] nodename nor servname provided` |
| Provider diversity is already real | read from `model.provider` (line 3) of each of the 21 `config.yaml` files: `openrouter` **11**, `google` **8**, `nous` **2**, `tester` unset (`tester` has no `config.yaml` at all) — re-verified 2026-09-16 17:21; the r2 figure (openrouter 10 / nous 3) was invalidated at 17:15 when `personal-assistant` moved `nous` → `openrouter`. Body-level `provider:` fields do not exist; the value lives under the top-level `model:` block. See §6 |
| Skills are duplicated 22× | **59–123** `SKILL.md` per profile (`operator-installer` has the most at 123; `email-digest-agent` and `tester` the fewest at 59), **2,131** skill copies in total (`find <profile> -name SKILL.md \| wc -l`, re-verified 2026-09-16 17:33) |
| 3 profiles have **no model key** (and therefore cannot call a model) | `chatbot_builder`, `email-digest-agent`, `tester`. Not identical cases: `chatbot_builder` has a configured default (`deepseek/deepseek-v4-pro`, openrouter), `memories/MEMORY.md` + `USER.md` and 1 session (2026-08-04) — its only blocker is the missing key; `email-digest-agent` has the model config (`anthropic/claude-haiku-4.5`) but an empty `memories/` and 0 sessions; `tester` has **no `config.yaml` at all** (only `profile.yaml`), an empty `memories/` and 0 sessions (verified 2026-09-16 17:24) |
| Dead `:free` IDs: **repaired on defaults, still on 3 aux routes** | At 17:10 `lexflow_dev_head_admin` default was `minimax/minimax-m3:free` and `personal-assistant` default was `tencent/hy3:free`. **Both were repaired at 17:15:20/21** — they now read `deepseek/deepseek-v4.1-flash` and `google/gemini-3.5-flash` respectively (re-verified 2026-09-16 17:21). No profile default points at a dead ID today. Residual exposure: `minimax/minimax-m3:free` is still set on 3 auxiliary routes (`web_extract`, `mcp`, `title_generation`) of `frontend-developer-lovable_react` — the only profile in the estate whose aux routes are pinned to a named ID; every other profile runs aux as `provider: auto` / `model: ''`. `qwen/qwen3-4b:free` and `tencent/hy3:free` now appear in **no** profile config — only in stale cron error logs. See §6.2 rule 3 and §6.3 |
| Repo-root rule exists, migration has **not** run | `~/projects/` holds only 3 repos (`avibe-hindsight`, `LEGAL_backup`, `avibe-flowershop`) — AGENT_RULES §8 staged migration is still pending |

**Implication:** this is not a 14-day *install*, it is a 14-day **stabilise → standardise →
harden** programme. Installation-order items from the brief that are already done are marked ✅.

---

## 1. The 14-day plan

Owners: **OI** = `operator-installer` (does profile/config/infra work after approval),
**MC** = `memory-curator` (memory, vault, skills, logging), **Ole** = human decision,
**specialists** = the profile named in the row. Every day ends with a one-line entry in the
Daily Note (§V3 logging rule).

### Phase 0 — Stabilise plumbing (Day 1–2, Thu 17 – Fri 18 Sep)

| Day | Action | Owner | Done-criteria |
|---|---|---|---|
| 1 | Re-authenticate Nous Portal (`hermes model`); confirm the `nous` provider answers on one profile | Ole (interactive) + OI | one-shot `hermes chat -q "Reply OK." --provider nous -Q` returns OK |
| 1 | Fix the `_FULL_ARGS_LOG_BOUND` ImportError on the two `operator-installer` morning jobs | OI | `lexflow-morning-plan` and `lexflow-morning-report` exit `ok` on next fire |
| 1 | Fix Telegram delivery from cron (DNS/`send_path_degraded`) | OI | a test Telegram message from a cron job arrives |
| 2 | Verify the 9 `memory-curator` cron jobs recovered after the 2026-09-16 model swap (8 were `error` on their 2026-09-15 runs); pin a **live** model on each job (`model` field is currently `null` → it inherits the profile default, which is now live) | MC | every job shows `last_status: ok` after one cycle |
| 2 | Add a hard **model-existence pre-check** to the cron create path (rule from §8 of the obsidian skill: never configure an unverified model ID) | OI | a job pointed at a non-existent model is refused, not silently 404-ing nightly |

### Phase 1 — Identity, memory, skills (Day 3–5, Sat 19 – Mon 21 Sep)

| Day | Action | Owner | Done-criteria |
|---|---|---|---|
| 3 | Write the canonical **memory structure** (§5) and map every profile's `SOUL.md` / `memories/MEMORY.md` / `USER.md` onto it; no content invented, only placement rules | MC | structure note in vault + one pilot profile converted |
| 3 | Sweep the estate for the **dead/free model IDs** (`minimax/minimax-m3:free`, `tencent/hy3:free`, `qwen/qwen3-4b:free`) | MC proposes → OI executes | zero profile default is a `:free` model that does not resolve |
| 4 | Resolve the **3 unusable profiles** — approve or reject the existing consolidation proposal (merge into `frontend-developer-lovable_react`, `personal-assistant`, `backend-dev`) | Ole | decision recorded; nothing merged before the go |
| 4 | Consolidate the **initial skill set** (§7): 6 new skills, 4 mapped to existing ones; stop shipping ~100 unmodified skills into every profile | MC | skill inventory note + proposal |
| 5 | Hindsight: confirm bank `avibe-hq` on every profile that writes memory; re-run the read-auth probe | MC | probe output recorded; no bank-ID mismatch |

### Phase 2 — Connectors + routing (Day 6–9, Tue 22 – Fri 25 Sep)

| Day | Action | Owner | Done-criteria |
|---|---|---|---|
| 6 | Connect the **minimum viable connector set** (§4): GitHub token, Railway CLI, Netlify, Obsidian/filesystem, Telegram | OI | each connector proven by one read-only call |
| 6 | Disable or quarantine the **enabled-but-inert MCP servers** (Linear, Stripe, Supabase, Postgres, Kubernetes, Figma…) | OI | agent boot is faster and the tool list stops advertising tools that cannot work |
| 7 | Apply the **model routing policy** (§6) to all 22 profiles + the auxiliary routes | OI (after Ole's approval of the table) | `config.yaml` diff per profile; a `hermes chat -q` smoke test per tier |
| 8 | Cost instrumentation: per-profile / per-task-type spend capture, >50 % spike alert | OI | one week of baseline numbers in the vault |
| 8 | Telegram utility path: confirm which profile owns the bot, `TELEGRAM_HOME_CHANNEL`, `TELEGRAM_ALLOWED_USERS` | OI | inbound message answered by `telegram-utility-agent` |
| 9 | Repo-root migration, batch 1 (LEGAL, git-checked before/after, symlink grace week) | OI + Ole per batch | `git status`/`git log` clean before and after; symlink live |

### Phase 3 — End-to-end tests + guardrails (Day 10–12, Sat 26 – Mon 28 Sep)

| Day | Action | Owner | Done-criteria |
|---|---|---|---|
| 10 | **E2E test 1 — LexFlow feature ticket** (§8.1) | backend-dev + OI | ticket → local commit → documented deploy gate; evidence attached |
| 11 | **E2E test 2 — SEO page brief** (§8.2) | seo-aeo-expert → MC | brief note in the vault with ≥2 wikilinks + Daily Note line |
| 11 | **E2E test 3 — Telegram inbound** (§8.3) | telegram-utility-agent | message in → task routed → answered in < 2 min |
| 12 | Budget guardrails + fallback drill (§9): kill the primary provider on one profile, prove the fallback answers | OI | documented drill result incl. the failure mode observed |

### Phase 4 — Autonomy + review (Day 13–14, Tue 29 – Wed 30 Sep)

| Day | Action | Owner | Done-criteria |
|---|---|---|---|
| 13 | Only now enable **new** schedules/background jobs (brief step 7); cap them to cheap tiers | OI | job list + model per job documented |
| 14 | Retro: what broke, what the estate learned; update this roadmap + AGENT_RULES if needed; hand the first weekly review to the existing Sunday report chain | MC | retro note + updated roadmap |

---

## 2. Agent list + responsibilities

### 2.1 Target shape (proposal — 6 brief roles → 22 existing profiles)

The brief asks for 6 roles. The estate already has specialists per role; **no new profile is
proposed**. What is proposed is *closure* (retire/merge the 3 bookable-nowhere profiles) and
*routing* (one command agent at the top).

| Brief role | Fulfilled by (today) | Notes |
|---|---|---|
| Founder Operator Agent (central triage) | `operator-installer` | already orchestrates; owns Boards, dispatch, deploys after approval |
| LexFlow Builder Agent | `backend-dev`, `frontend-developer-lovable_react`, `lexflow_dev_head_admin`, `tester` (pending) | `lexflow_dev_head_admin` is the estate's 3rd most-used profile (78 sessions, last 2026-09-16 17:15 — re-verified 17:21, so **not dormant**); its dead default was repaired at 17:15 → `deepseek/deepseek-v4.1-flash`. `tester` has no `config.yaml` and no key (see §0) |
| SEO/AEO Agent | `seo-aeo-expert`, `seo-swarm-agent`, `seo-cron-agent`, `chatseo-agent`, `gsc-agent`, `ads-expert`, `content-creator`, `marketing-analyst`, `agency-growth` | 9 profiles for one brief role — the strongest over-provisioning candidate for a later consolidation card |
| CRM & Outreach Agent | `crm-outreach-agent`, `customer-rel-manager`, `sales-crm` | 3 profiles, overlapping scopes; `crm-outreach-agent` is on the premium route (`anthropic/claude-opus-4.8` via nous) |
| Telegram Utility Agent | `telegram-utility-agent` | has `TELEGRAM_BOT_TOKEN`; delivery path is currently broken (§0) |
| Memory Curator Agent | `memory-curator` | absorbed `librarian` on 2026-09-16; also owns vault cron suite |

Profiles with no usable route today: `chatbot_builder` (missing key only — it has a model, memories
and 1 session), `email-digest-agent` (missing key; empty memories, 0 sessions), `tester` (no key,
**no `config.yaml`**, empty memories, 0 sessions). Merge proposal already exists — see
[[Agent-Roster-Consolidation-Proposal-2026-09-16]]. **Ole approval required; nothing has moved.**

### 2.2 Orchestration principles (adopt)

1. **One command agent at the top** — `operator-installer` receives work, decomposes, and
   assigns; specialists never call each other directly.
2. **Workers are dispatched, not chatted to** — cross-agent handoffs go through the Kanban board
   (`kanban_create` with an explicit assignee), not through prose.
3. **Every worker card carries its own context** — a worker cannot see its siblings.
4. **Fast/cheap and deep/expensive routes are separate** (§6).
5. **Connector isolation** — CRM, email, Telegram, GitHub and deploy credentials are scoped per
   role, never shared estate-wide.
6. **A card that needs review goes to review, never to the implementer's own verdict.**

---

## 3. Workspace map

| Layer | Path / system | Status |
|---|---|---|
| Code (source of truth for code) | `/Users/olesiarasing/projects/<repo>` (AGENT_RULES §8) | migration staged, not run; legacy `~/Desktop/projects` frozen read-only |
| Knowledge | `~/Obsidian/` (git → `Ole00007/obsidian-vault`) | live, _Inbox-first for new notes |
| Long-term memory | Hindsight bank `avibe-hq` on Railway | live, health-checked; read-auth still open |
| Orchestration | Kanban board `~/.hermes/kanban.db` (+ the isolated `lexflow-learning` board) | live |
| Runtime | 22 profiles under `~/.hermes/profiles/`, gateway + cron | live, partly broken (§0) |

---

## 4. Connector checklist

### 4.1 Already connected

- `OPENROUTER_API_KEY` — 19/22 profiles (`chatbot_builder`, `email-digest-agent`, `tester` have none).
- `TAVILY_API_KEY` + `FIRECRAWL_API_KEY` — web search / extract on most growth + utility profiles.
- `NOTION_API_KEY` — **5** profiles (`memory-curator`, `chatseo-agent`, `gsc-agent`, `seo-swarm-agent`, `agency-growth`; re-verified 2026-09-16 17:22 — the r2 text said 6 and listed 5; the list was right and the count was wrong. `operator-installer` has **no** Notion entry).
- `TELEGRAM_BOT_TOKEN` — `memory-curator`, `operator-installer`, `telegram-utility-agent`.
- `API_SERVER_KEY` — `operator-installer`, `lexflow_dev_head_admin`.
- Browser/web tooling, terminal, filesystem — everywhere (bundled).
- GitHub — via `ssh`/`gh` on the CLI, **not** via the `github` MCP server (its required
  `GITHUB_PERSONAL_ACCESS_TOKEN` env var is unset in every profile).

### 4.2 Minimum viable set to add (brief step 3)

| Connector | Why | Status |
|---|---|---|
| GitHub (token **or** keep gh CLI as the single path — pick one) | PRs, issues, reviews for LexFlow | partially there; MCP server inert |
| Railway CLI / API | LexFlow prod + staging deploys and env reads | manual today |
| Netlify | landing deploys (`poetic-kleicha-28d058`) | manual today |
| Telegram delivery (fix, don't add) | the bot exists but cron delivery errors | **broken** |
| Obsidian vault (filesystem, read/write) | every knowledge-producing task (§V3) | working via direct file tools |
| Airtable **or** Notion (pick one as the CRM-adjacent store) | agency client tracking | Notion keys exist on **5** profiles (re-verified 2026-09-16 17:22); Airtable MCP enabled but keyless |
| Email (SMTP / Resend) | client outreach + the `email-digest-06am` job | **absent** — `COMPOSIO_API_KEY` exists in no profile; `email-digest-06am` has never produced output |

### 4.3 Kill or quarantine (enabled, keyless, never used)

`linear`, `stripe`, `supabase`, `postgres`, `kubernetes`, `neon`, `asana`, `atlassian`, `cloudflare`,
`blender`, `canva`, `davinci-resolve`, `figma` (needs the desktop app on `127.0.0.1:3845`),
`dune`, `etherscan`, `paypal`, `higgsfield`, `thirdweb`, `the-graph`, `solana-agent-kit`,
`tradingview`, `ccxt`, `coingecko`, `aws`, `docker-hub`, `meigen-ai-design`, `brave-search`
(Tavily/Firecrawl already cover search). Each one is boot-time cost and a tool the model can
hallucinate into calling. Proposal: enable only what has credentials **and** a named owner.

---

## 5. Memory structure

The brief's three files map onto Hermes's four actual layers. Do not create parallel `profile.md`
/ `memory.md` / `soul.md` files inside the vault — that would duplicate what already exists and
drift from the runtime.

| Brief file | Hermes implementation | Content rule |
|---|---|---|
| `profile.md` — stable operator identity | `profile.yaml` (`description`) + `SOUL.md` | owner, businesses, tone, budget rules, approved tools, escalation, security boundaries. Hard rules live here (they reach the system prompt). |
| `memory.md` — durable facts only | `memories/MEMORY.md` (2,200-char budget) + `USER.md` (1,375) | projects+repos, environments+deploy URLs, client identities, lead stages/CRM taxonomy, writing preferences, recurring procedures, do-not-forget. **Never** instructions-to-self — write declarative facts. |
| `soul.md` — long-horizon behaviour | `SOUL.md` (already exists per profile) | mission hierarchy (LexFlow first → protect focus → preserve optionality → minimise recurring spend), non-negotiables, behavioural style, failure-mode handling. |

Additional layers that the brief does not model but the estate depends on:

- **Vault (Obsidian) = knowledge.** Every knowledge-producing task writes a note; `_Inbox/` first,
  never straight into `01-Projects/`, `02-Areas`, `03-Resources` (AGENT_RULES §V3 + vault boundary).
- **Hindsight `avibe-hq` = long-term memory**, built by syncing the vault. The vault note is the
  source; Hindsight is the searchable index. Do **not** duplicate content between them.
- **Secrets are never stored** — memory files hold secret *references* only (standing rule 7/8).
- Character budgets are hard: when memory is full, consolidate stale entries in one batch instead
  of silently dropping the new fact.

---

## 6. Model routing policy (cheap / standard / premium)

Models below are **the IDs actually configured today** (re-read from `config.yaml` on 2026-09-16
17:21 CEST).
Anything marked ⚠ is unverified or known-bad and must be smoke-tested before it is set anywhere.

### 6.1 Tiers

| Tier | Purpose | Candidate models | Evidence |
|---|---|---|---|
| **Cheap** | classification, extraction, tags, short drafts, title/approval/MCP routing, SEO clustering, lead enrichment | `deepseek/deepseek-v4-flash`, `qwen/qwen3.6-35b-a3b`, `deepseek/deepseek-v4.1-flash` | deployed defaults: `backend-dev` (qwen3.6-35b), `sales-crm` (v4-flash), `memory-curator`, `operator-installer`, `lexflow_dev_head_admin` (v4.1-flash) |
| **Standard** | feature specs, PR reviews, campaign drafts, workflow design, customer messaging, most agent defaults | `google/gemini-3.5-flash`, `deepseek/deepseek-v4-flash-0731`, `anthropic/claude-haiku-4.5` | `google/gemini-3.5-flash` is the **default on 11 profiles** — 8 with `provider: google` (`ads-expert`, `chatseo-agent`, `content-creator`, `customer-rel-manager`, `gsc-agent`, `marketing-analyst`, `seo-cron-agent`, `seo-swarm-agent`) plus `agency-growth`, `seo-aeo-expert` and `personal-assistant`, which run the same ID **over `openrouter`**; provider count (8) ≠ model count (11). Plus `frontend-developer-lovable_react` (`deepseek/deepseek-v4-flash-0731`), `telegram-utility-agent` + `email-digest-agent` (`anthropic/claude-haiku-4.5`) — re-verified 2026-09-16 17:21 |
| **Premium** | legal logic, architecture trade-offs, critical refactors, investor-facing writing | `anthropic/claude-opus-4.8` (nous), `deepseek/deepseek-v4-pro` | `crm-outreach-agent` (nous/opus), `chatbot_builder` (deepseek-v4-pro — configured but the profile has no key, so it cannot call anything today) |

### 6.2 Rules

1. **Default every profile to Cheap or Standard.** Premium is opt-in per task, never a profile default.
2. **Scheduled/background jobs run Cheap only.** A cron that burns premium tokens silently is the
   single biggest cost leak in this estate.
3. **Verify before configuring.** No model ID goes into a config without a live one-shot test —
   the estate carries three IDs proven dead in this estate (`minimax/minimax-m3:free`,
   `tencent/hy3:free`, `qwen/qwen3-4b:free`): they fail with HTTP 404 and took the whole
   `memory-curator` cron suite down for days. **State as of 2026-09-16 17:21:** the two that sat on
   *primary profile defaults* (`lexflow_dev_head_admin` = minimax-m3:free, `personal-assistant` =
   tencent/hy3:free) were repaired at 17:15 and **no profile default points at a dead ID any more**;
   `tencent/hy3:free` and `qwen/qwen3-4b:free` are gone from every config (the latter survives only
   in stale cron error logs); `minimax/minimax-m3:free` is still pinned on 3 aux routes
   (`web_extract`, `mcp`, `title_generation`) of `frontend-developer-lovable_react` — see §0 and §6.3.
4. **`:free` models are for non-critical auxiliary routes only**, and never as the sole option on a
   job that must report. They 404 under load — that is a capacity signal, not a config error.
5. **Free fallback chain** (Hindsight LLM, standing rule 2):
   `nvidia/nemotron-3-ultra-550b-a55b:free` → `nvidia/nemotron-3.5-lightning:free` →
   `nvidia/nemotron-3-super-120b-a12b:free` → `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`.
6. **Every profile gets a working fallback producer.** Today only `memory-curator` declares a
   non-empty one (`openrouter / anthropic/claude-haiku-4.5`); the other 20 profiles with a
   `config.yaml` carry `fallback_providers: []` (re-verified 2026-09-16 17:22).

### 6.3 Auxiliary routes (proposal — needs Ole's approval)

Aux routes are **per profile**, not estate-wide. Re-verified 2026-09-16 17:21: exactly **one**
profile pins named aux models — `frontend-developer-lovable_react` (11 named IDs); the other 20
`config.yaml` files run aux as `provider: auto` / `model: ''`, and `tester` has no `config.yaml`.
The "Current" column below is therefore *that* profile's configuration, which is also the only place
a dead ID survives in any config:

| Route | Current (`frontend-developer-lovable_react`) | Proposed |
|---|---|---|
| Vision | `nvidia/nemotron-3-super-120b-a12b:free` | `gemini-3-flash-preview`-class multimodal (cheaper, faster) |
| Web extract | `minimax/minimax-m3:free` ⚠ **dead ID** | auto / cheap-and-fast |
| Compression | `nvidia/nemotron-3-super-120b-a12b:free` | auto — compression needs speed, not size |
| Approval (classifier) | `nvidia/nemotron-3-super-120b-a12b:free` | cheap classifier |
| MCP tool routing | `minimax/minimax-m3:free` ⚠ **dead ID** | keep the *shape*, replace the dead ID |
| Title generation | `minimax/minimax-m3:free` ⚠ **dead ID** | keep the *shape*, replace the dead ID |
| Curator / skills hub (`skills_hub`) | `nvidia/nemotron-3-super-120b-a12b:free` | fine if it resolves; else auto |
| Triage specifier (`triage_specifier`) | `nvidia/nemotron-3-super-120b-a12b:free` | auto / cheap classifier |
| Kanban decomposer (`kanban_decomposer`) | `nvidia/nemotron-3-super-120b-a12b:free` | keep the shape; decomposition needs reasoning — Standard-tier candidate |
| Profile describer (`profile_describer`) | `nvidia/nemotron-3-ultra-550b-a55b:free` | auto — short descriptive text |
| Curator (`curator`) | `nvidia/nemotron-3.5-lightning:free` | keep the shape; replace if it 404s |

All **13** aux routes of that profile are accounted for above: **11 named IDs** + 2 `auto` (`tts_audio_tags`, `monitor`).
Every other profile's aux routes are `provider: auto` / `model: ''`, so there is nothing to tabulate for them.

Caveat: items 3 and 4 above still apply — a free ID that 404s is worse than a paid ID that costs
fractions of a cent. Ole's standing directive is free-only for the **Hindsight LLM**; agent
auxiliary routes are open for a costed decision.

---

## 7. Skill list

Initial set from the brief, mapped to what already exists so we do not create a fourth copy of a
skill that is already shipped to 22 profiles.

| Brief skill | Status | Action |
|---|---|---|
| `seo-aeo-briefing` | ✅ exists (`seo/seo-aeo-briefing`) | reuse |
| `memory-curation` | ✅ covered by `obsidian` + `wikilinks` + `hermes-hindsight-memory` | reuse, do not duplicate |
| `bug-triage` | ~ covered by `systematic-debugging`, `github-issues` | map, add a LexFlow-specific pitfall section |
| `repo-planning` | ~ covered by `plan` + `spike` | map |
| `deployment-checklist` | 🆕 | create (Railway + Netlify + the git-push gate) |
| `feature-spec-writer` | 🆕 | create (LexFlow ticket shape used on the board today) |
| `legal-tech-domain-notes` | 🆕 | create (per-client constraints, P.IVA/legal-page gates) |
| `crm-outreach-sequencing` | 🆕 | create (drip phases, suppression rules from `Delegation_Tracking.csv`) |
| `telegram-short-reply` | 🆕 | create (concise-reply style + routing rules) |
| `cost-guardrails` | 🆕 | create (tier routing, verify-before-configure, spike alerts) |

Also required by standing rules and **already shipped estate-wide** (do not re-create):
`obsidian`, `wikilinks`, `hermes-agent`, `kanban-worker`, `kanban-orchestrator`, `sdlc-review`.

**Structural note:** **2,131** `SKILL.md` copies exist across the estate (**59–123** per profile: `operator-installer` 123, `memory-curator` 108, `lexflow_dev_head_admin` and `personal-assistant` 103, down to `email-digest-agent` and `tester` at 59 — re-verified 2026-09-16 17:33). Skills
are auto-discovered from `HERMES_HOME/skills`, so the per-profile copies exist for *isolation*, not
necessity. A later consolidation card should decide which skills are global versus role-scoped,
because a wrong update to one copy silently diverges from the other 21.

---

## 8. Test plan — three end-to-end workflows

Each test produces **evidence** (a file path, a URL, or a command output) — a self-reported "it
worked" is not a pass.

### 8.1 LexFlow feature ticket

1. Operator creates a Kanban card with a real scope (e.g. "contact model field X").
2. `backend-dev` (or `frontend-developer-lovable_react`) is dispatched with a worktree workspace.
3. Work lands as a **local commit** (no push to a deploy-triggering branch without Ole's go).
4. A reviewer task checks the diff independently.
5. Deploy gate: Ole's explicit approval, then prod health check.
- **Pass:** card reaches `done` with `changed_files`, test counts, commit SHA in the handoff;
  `/health` returns 200 after deploy; no unapproved push.
- **Evidence:** card id + commit SHA + curl output.

### 8.2 SEO page brief

1. `seo-aeo-expert` receives a client + page target (start with a real client, e.g. Romanelli).
2. Brief is written as a **vault note in `_Inbox/`** with frontmatter, `## Links` with ≥2 wikilinks.
3. Daily Note gets a one-line entry (§V3).
4. Hindsight picks it up on the next sync.
- **Pass:** note exists at a stated absolute path, links resolve, Daily Note line present.
- **Evidence:** absolute path + the Daily Note line.

### 8.3 Telegram inbound

1. Message the bot from Ole's account.
2. `telegram-utility-agent` classifies it, answers simple requests directly, and forwards anything
   heavier to the right specialist as a Kanban card.
3. The reply arrives in Telegram within 2 minutes.
- **Pass:** round-trip works *from the gateway*, not just from a one-shot CLI run — cron delivery
  currently fails with a DNS/connect error, so the delivery path is the thing under test.
- **Evidence:** the message id/time and the card created for the forwarded part.

---

## 9. Budget guardrails + fallback behaviour

**Baseline:** Nous Plus ≈ $20/mo (bundled tools + roughly $22 of credits). OpenRouter is prepaid
overflow: 5.5 % fee on credit purchase with a $0.80 minimum, provider token pricing, no markup.
**Railway is separate** and is not covered by the AI subscription — app hosting, DB, workers and
traffic bill independently. Claude Pro is **not** being taken (unverifiable 2026 Claude Code
entitlement).

Guardrails (proposals):

1. **Tier discipline** — Cheap = default, Standard = normal work, Premium = explicit exception.
2. **No premium model on any scheduled job.** Enforced by a config lint at Phase 2 Day 7.
3. **Spike alert** — a >50 % week-over-week cost change is flagged out-of-band immediately, never
   batched into the next scheduled report (existing standing directive).
4. **Per-profile and per-task-type spend tracking**, with a monthly cap per profile; on breach the
   profile drops one tier rather than stopping work silently.
5. **No model ID without a live smoke test** (§6.2 rule 3).
6. **Cache is not a guardrail** but is free money: OpenRouter response caching is already on
   (`openrouter.response_cache: true`, 300 s TTL).
7. **Cron cadence hygiene** — **9** jobs on `memory-curator` alone (8 currently erroring — see §0); every new job needs a named owner and a Cheap-tier pin.

Fallback behaviour (proposal):

- Primary provider failure → next `fallback_providers` entry; **every profile must declare at
  least one** (today only `memory-curator` does).
- All providers down → the task **blocks with a reason**, it never silently completes or invents a
  result.
- A `:free` route that 404s is treated as *transient capacity*, retried on the chain, then reported —
  not re-pinned to the same dead ID.
- **Failure-mode rule from the brief:** if the premium route stalls, fall back to a cheaper model and
  say so in the output rather than stalling the whole task.

---

## 10. Human-confirmation list (things an agent must NOT do alone)

1. **Nous Portal re-authentication** — interactive login, Ole only.
2. **Approving the 3 profile merges / retirements** — irreversible profile deletion
   (`chatbot_builder`, `email-digest-agent`, `tester`).
3. **Any new paid spend** — OpenRouter top-up, tier upgrade, new connector with a subscription.
4. **Deploy-triggering `git push`** — always Ole's go, per the git-push gate.
5. **Railway environment / provider config changes** — tier-2: propose, then wait.
6. **Repo-root migration batches** — moving repos is only "safe" once `git status` + `git log` are
   clean before *and* after; go per batch.
7. **Legal/entity content on LexFlow pages** — blocked on the P.IVA; no agent edits
   `privacy.html` / `cookie-policy.html` until real legal values exist.
8. **Client data, pricing, LexFlow/aLEXy direction** — tier-3: surface, never autonomous.
9. **Disabling or deleting a cron job that currently reports to Telegram** — that is a loss of
   visibility, not cleanup.
10. **Changing AGENT_RULES hard rules** — version bump + estate-wide SOUL propagation via
    `operator-installer`, with Ole's approval.

---

## 11. Proposed final home for this note

Draft lives in `_Inbox/` per AGENT_RULES. Proposed filing, on Ole's approval:

- **Primary:** `03-Resources/Hermes-Setup-and-MCP/Hermes-14-Day-Installation-Roadmap-2026-09-16.md`
  — it is estate-wide setup knowledge, not LexFlow product work, and it belongs beside
  [[hermes_setup_brief]], [[Reference-Guide]] and [[Agent-Profiles]] whose hub it feeds.
- **Mirror/decision record:** the LexFlow-specific decisions (stack 1.4, roster change, repo-root
  rule) already live in [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]; the roadmap should
  link to it rather than duplicate it.
- **Do not** put it in `01-Projects/LexFlow/` — the roadmap covers SEO, CRM and Telegram workflows
  too, and LexFlow-first is a *priority order*, not the whole scope.

---

## 12. Re-verification kit (run this before filing)

Every §0 / §4 / §6 number above came from one of these read-only commands (`cd ~/.hermes/profiles`,
macOS, 2026-09-16 17:21):

    ls -d */ | wc -l                                                                        # 22
    for d in */; do grep -q '^OPENROUTER_API_KEY=' "$d/.env" && echo "$d"; done | wc -l      # 19
    for d in */; do grep -m1 '^  provider:' "$d/config.yaml"; done | sort | uniq -c          # openrouter 11 / google 8 / nous 2
    for d in */; do grep -m1 '^  default:'  "$d/config.yaml"; done | sort | uniq -c          # gemini-3.5-flash 11
    grep -l '^NOTION_API_KEY=' */.env | wc -l                                                # 5
    grep -rn 'minimax/minimax-m3:free\|qwen/qwen3-4b:free\|tencent/hy3:free' */config.yaml    # 3 hits, frontend profile only
    sqlite3 -readonly lexflow_dev_head_admin/state.db 'select count(*) from sessions;'        # 78
    for d in */; do find "$d" -name SKILL.md | wc -l; done | sort -n | sed -n '1p;$p'         # 59 .. 123
    find . -name SKILL.md | wc -l                                                             # 2131
    sed -n '/^auxiliary:/,/^display:/p' frontend-developer-lovable_react/config.yaml           # 13 routes, 11 named

Two traps that caused the r2 → r3 corrections — worth repeating:

- **`provider:` is nested** at line 3 under the top-level `model:` block. A body-level
  `grep '^provider:'` returns nothing, which *looks* like "provider unset" but is a grep artefact.
- **Provider count ≠ model count.** `google/gemini-3.5-flash` is the default on 11 profiles, but only
  8 of them run `provider: google`; the other 3 reach the same ID through `openrouter`.

**r4 correction log (2026-09-16 17:33 CEST, round-3 review):** §0/§7 skill-count range "59–117 per profile, ~2,200 total" → **59–123 per profile / 2,131 total** (`find <profile> -name SKILL.md`; 117 only appears if the six nested `mlops/<group>/<name>/SKILL.md` dirs are excluded — an unstated method); §6.3 completed to **all 13** aux routes of `frontend-developer-lovable_react` (**11 named IDs** + 2 `auto`), adding `triage_specifier`, `kanban_decomposer`, `profile_describer` and `curator`, and the inaccurate "(Rows not listed here were not verifiable from config…)" clause was removed. Nothing else changed; the two r4 items were the only outstanding findings.

**r3 correction log (2026-09-16 17:25 CEST):** memory-curator cron suite 6 → **9** jobs (8 erroring);
provider split openrouter 10 / nous 3 → **openrouter 11 / nous 2**; Notion keys 6 → **5** profiles;
`google/gemini-3.5-flash` "default on 8 profiles" → **11 profiles** (8 google-provider + 3 via
openrouter); dead-ID row rewritten (both defaults repaired 17:15, `minimax-m3:free` still on 3 aux
routes); §2.1 `lexflow_dev_head_admin` no longer described as dormant (78 sessions, last 17:15);
`chatbot_builder` no longer described as having "no model, no memories"; §0 rows date-stamped.

**Known link ambiguity (not fixed here):** `hermes_setup_brief.md` exists **twice** in the vault —
`03-Resources/Hermes-Setup-and-MCP/hermes_setup_brief.md` (the cited source) and
`_Inbox/_Conflicts/hermes_setup_brief.md` (different size). `[[hermes_setup_brief]]` therefore
resolves by shortest-path to the `_Inbox/_Conflicts/` copy. That is a taxonomy/curation job for
`memory-curator`, not a defect of this note.

---

## Links

- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[hermes_setup_brief]]
- Related: [[Agent-Roster-Consolidation-Proposal-2026-09-16]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[Agent-Profiles]]
- Related: [[hermes-standing-rules]]
- Related: [[2026-09-16]]
