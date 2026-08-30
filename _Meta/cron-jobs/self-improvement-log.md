# Self-Improvement Log — memory-curator

> Running record for Part F of the unified memory-management directive.
> Nightly `nightly-self-improvement-log` job appends daily observations here.
> Sunday `weekly-self-improvement-report` job reads this to produce the weekly cumulative report.

Created: 2026-08-26

### 2026-08-26 — Decision: Hindsight read-auth deferred (runbook ready)
- Live probe: `/v1/default/banks` + `/v1/default/banks/avibe-hq/stats` return **HTTP 200 without auth** (bank metadata + graph stats exposed; note content NOT exposed; writes already key-protected).
- Ole chose **option 2 (defer)** + **option 3 (runbook)** — operator-installer busy with urgent job.
- Runbook: `~/Obsidian/_Inbox/Hindsight-Read-Auth-Runbook.md` (mechanism, verify steps, client-side key placement, safety, decision log).
- Reminder: cron `hindsight-read-auth-reminder` (Mon 10:00 → Telegram) flags when to do option 1 at scale.
- Other fixes same day: wrong-bank bug fixed (operator-installer `hindsight/config.json` → `avibe-hq`); AGENT_RULES §3.1 schedule updated (18:00 → 05:00/05:15/06:00 chain).

### 2026-08-27 — 2nd PC setup + Hindsight-for-LexFlow decisions
- **2nd PC provisioning scheduled:** calendar event "2nd PC Setup plus Hindsight Test" (Home cal, Thu Sep 3 10:00-11:30) + cron `second-pc-setup-reminder` (Thu 09:00 → TG). Runbook: `~/Obsidian/_Inbox/2nd-PC-Bootstrap-Runbook.md`.
- **Calendar access:** YES via macOS AppleScript (Home/Work/etc.). Note: inline heredoc AppleScript with `&` triggers the shell backgrounding guard — write to a .applescript file and `osascript` it; `date "Thursday…"` strings are locale-fragile, use `current date` + day offsets. EventKit XPC error on some calendars — use "Home".
- **Hindsight for LexFlow (backend-dev, 2026-08-27):** use SEPARATE Hindsight service + HTTP API, NOT clone/embed. LexFlow needs its own bank. **Per-client banks confirmed correct** — backend-dev endorses (b): one bank per law firm (e.g. lexflow-clientA-hq), same single deployment, distinct bank_id per client. Rationale: hard data isolation at retrieval layer, GDPR right-to-be-forgotten = atomic `DROP bank_id=firmX`, banks are cheap namespaces (not clusters), trivial query routing (bank_id from session), per-bank auth. Ole's instinct validated.
- **Vault-logging enforcement + scaling thresholds** added (see crons).

### 2026-08-28 — Hindsight READ-AUTH ENABLED ✅ (was deferred since 08-26)
- **Fix applied via Railway CLI** (CLI was already authenticated as ole00007 — no token needed from Ole).
- Added 2 variables to service `avibe-hindsight` (project graceful-presence, ID 9b08be93-b288-4772-8ccc-29b724851bf0):
  - `HINDSIGHT_API_TENANT_EXTENSION=hindsight_api.extensions.builtin.tenant:ApiKeyTenantExtension`
  - `HINDSIGHT_API_TENANT_API_KEY` = same 64-char value as `HINDSIGHT_API_KEY` (so all existing clients already have the right key — no client-side change needed).
- Source of truth: Hindsight code `hindsight-api-slim/hindsight_api/extensions/builtin/tenant.py` — `DefaultTenantExtension` = NO auth by default; `ApiKeyTenantExtension` validates `Authorization: Bearer` against `HINDSIGHT_API_TENANT_API_KEY`.
- Env change auto-triggered redeploy (~5 min, large image). Verified:
  - `/health` → 200 (stays open for Railway probes) ✓
  - `/v1/default/banks` no-key → **401** ✓ (was 200)
  - `/v1/default/banks/avibe-hq/stats` no-key → **401** ✓ (was 200)
  - `/v1/default/banks` with key → **200** ✓
  - `/v1/default/banks` wrong key → **401** ✓
- **Note:** the auth is a SINGLE shared key (ApiKeyTenantExtension) — this closes the public-read hole. It does NOT give per-client bank isolation (that's the future `lexflow-hq` / per-client-bank work). Revisit when scaling.
- Railway CLI notes: `railway link -p graceful-presence --environment production`, then `railway service avibe-hindsight`, then `railway variables set NAME=val`, `railway redeploy`. Env-var changes auto-trigger deploy.

## Log Entries

### 2026-08-26 — Baseline (wikilinks initiative)
Vault retro-fitted into a connected graph: 210/226 notes linked (was 8/177), 409 edges.
- Total notes: 323
- Unlinked (0 links): 30 — ALL are hub/INDEX/README notes (intended: they receive backlinks)
- Distinct unresolved [[targets]]: 28 (40 refs) — mostly template placeholders (TOC, Agent-Name, Relevant-Workflow) + a few genuinely-missing notes (Composio-Integration, Email-Digest-Pipeline)
- Future weekly reports trend these numbers against this baseline.
- **Daily note:** `05-Daily/2026-08-26.md` does not exist — no staging log for today. Latest daily notes on disk: 2026-08-25, 08-24, 08-23, 08-20, 08-13.
- **(a) Conflicts flagged today:** 0 (no stager run detected).
- **(b) Identical dupes skipped:** 0 recorded.
- **(c) _Conflicts backlog size now:** N/A — `~/Obsidian/_Inbox/_Conflicts/` does not exist yet. No prior count to compare.
- **(d) Recurring pattern observed:** Yes — even without a stager run, `_Inbox/` already holds several parenthetical version-suffix collisions that would be conflict candidates:
  - `nous_models_purpose_first.xlsx` + `nous_models_purpose_first (1).xlsx`
  - `md.md` + `md (1).md`
  - `industry-competitive-analyst-skill.md` + ` (1)` + ` (2)`
  - `med_expert_editorial_plan_attached (1).md` (no base file present)
  - `image (2).jpg` (no base file present)
  Pattern: browser re-download `" (n)"` suffix. Also note serial-part families (`ica-v3-1..5`, `industry-competitive-analyst-v3-part1..3`) which are legitimate multi-part sets and must NOT be treated as dupes.
- **(e) False-positive suspicion:** `md (1).md` / `md.md` — generic base name, likely two unrelated pastes rather than a true duplicate. Also flagged: any `-part1/2/3` or `v3-N` family should be excluded from suffix-based dedup heuristics.
- **Note:** first nightly entry; baseline established.

### 2026-08-27 — Nightly log (downloads stager run)
- **Daily note:** `05-Daily/2026-08-27.md` present — downloads_stager.py executed (real, 24h window): 0 newly staged, 2 verified identical, 1 conflict quarantined, 1 system file excluded.
- **(a) Conflicts flagged today:** 1 — `md (1).md`. Vault copy (md5 6352b3f7) preserved; divergent Downloads copy (md5 771f3de3) quarantined to `_Inbox/_Conflicts/md (1).md` for review.
- **(b) Identical dupes skipped:** 2 — `olesia_state_overview.xlsx` (md5 477fd5d1, verified identical) + `hermes_tracking_plan (1).xlsx` (md5 e5c7d691, verified identical). Both correctly skipped (not staged).
- **(c) _Conflicts backlog size now:** 1 (`md (1).md`). Previous count: N/A (`~/Obsidian/_Inbox/_Conflicts/` did not exist on 2026-08-26). Net change: dir created, +1 conflict quarantined.
- **(d) Recurring pattern observed:** Yes — browser re-download ` (n)` version-suffix collisions continue. Today's instances: `hermes_tracking_plan (1).xlsx` (verified-identical, skipped) and `md (1).md` (divergent, quarantined). Same ` (1)` signature seen in the 2026-08-26 baseline (`nous_models_purpose_first (1).xlsx`, `md (1).md`, `industry-competitive-analyst-skill (1)`). Serial-part families (`v3-N`, `-part1..3`) remain legitimately distinct — still excluded from suffix dedup.
- **(e) False-positive suspicion:** None of today's flags look like false positives. `md (1).md` was the 2026-08-26 false-positive suspect (generic name, "two unrelated pastes"), but the stager proved it IS a genuine conflict — divergent checksums (771f3de3 ≠ 6352b3f7), correctly quarantined, not a false positive. `hermes_tracking_plan (1).xlsx` carries the conflict-looking ` (1)` suffix but was verified identical (md5 e5c7d691) and correctly skipped — benign re-download, not a flag error.
- **Note:** first real conflict actually quarantined into `_Conflicts/`; backlog now non-empty. The 2026-08-26 suspicion on `md (1).md` is resolved as a true positive.

### 2026-08-28 — Nightly log (downloads stager run)
- **Daily note:** `05-Daily/2026-08-28.md` present — downloads_stager.py executed (real, 24h window): 0 newly staged, 0 verified identical, 0 new conflicts, 1 system file (`.DS_Store`) excluded. No Downloads files fell inside the 24h recency window (3 most-recent items are already in `_Inbox` and just outside the cutoff).
- **(a) Conflicts flagged today:** 0 — stager ran but raised no new conflicts. (Stale conflict from 2026-08-27 remains unresolved — see note below.)
- **(b) Identical dupes skipped:** 0 recorded today.
- **(c) _Conflicts backlog size now:** 1 (`md (1).md`). Previous count (2026-08-27): 1. Net change: 0 — backlog unchanged; the single quarantined conflict has persisted un-reviewed for a 2nd consecutive day.
- **(d) Recurring pattern observed:** Yes — the browser re-download ` (n)` version-suffix collision family persists. The 3 most-recent Downloads items sit just outside the 24h cutoff and are already in `_Inbox`: `hermes_tracking_plan (1).xlsx` (verified-identical re-download, skipped 2026-08-27) and `md (1).md` (divergent conflict, still quarantined). Same ` (1)` signature as the 2026-08-26/27 baselines. Serial-part families (`v3-N`, `-part1..3`) remain legitimately distinct — excluded from suffix dedup.
- **(e) False-positive suspicion:** None new. `md (1).md` remains a confirmed TRUE conflict (divergent md5 771f3de3 ≠ 6352b3f7) — was the 2026-08-26 false-positive suspect, confirmed true positive 2026-08-27, and still unresolved as of today. No new flag today to suspect.
- **Note:** 2nd consecutive day with no new conflicts and one unresolved stale conflict. `_Inbox` backlog now 237 files (growing, not being triaged out into `01-Projects`/`03-Resources`). Recommended: human review of `md (1).md` (keep vault / accept Downloads / merge) + periodic `_Inbox` triage pass (see `downloads_cleanup.py`).

### 2026-08-29 — Nightly log (NO stager run detected)
- **Daily note:** `05-Daily/2026-08-29.md` does NOT exist — no downloads_stager.py run captured for today (no [STAGED]/[CONFLICT]/dedup lines to read).
- **(a) Conflicts flagged today:** 0 (no stager run detected).
- **(b) Identical dupes skipped:** 0 recorded.
- **(c) _Conflicts backlog size now:** 0. Previous count (2026-08-28): 1. **Net change: -1** — the single long-lived `md (1).md` conflict (quarantined 2026-08-27, unresolved 2026-08-27 and 2026-08-28) is GONE. Global vault search for `md (1)` returns 0 hits, so it was **deleted/removed wholesale, not merged or relocated** into the vault. Backlog now empty.
- **(d) Recurring pattern observed:** No new instance today (no stager run). The browser re-download ` (n)` version-suffix collision family remains the dominant recurring signature historically (seen 2026-08-26/27/28: `nous_models_purpose_first (1).xlsx`, `md (1).md`, `industry-competitive-analyst-skill (1)`, `hermes_tracking_plan (1).xlsx`, `image (2).jpg`). Serial-part families (`v3-N`, `-part1..3`) remain legitimately distinct and excluded from suffix dedup.
- **(e) False-positive suspicion:** None new. **Flag for Ole:** the previously-confirmed TRUE conflict `md (1).md` (divergent md5 771f3de3 ≠ 6352b3f7) vanished from `_Conflicts/` with no merge record anywhere in the vault — its removal looks like a hard delete rather than an intentional resolution. Confirm intent (was the divergence reviewed and the right copy kept?) before assuming it was correctly cleared.
- **Note:** 1st day of empty `_Conflicts/` backlog since the directory was created (2026-08-27). Stale-conflict watch: resolved. Outstanding: `_Inbox` triage (237 files) and the recurring ` (n)` re-download pattern prevention still unaddressed.

## Links
- Parent: [[cron-jobs-INDEX]]

## WEEKLY ENFORCEMENT — 2026-08-30 (vault-logging, §V3/V4)
- Profiles checked: **23** (all profiles under ~/.hermes/profiles/)
- Left a vault trace this week: **23 / 23** ✓
- Non-compliant (active but zero vault trace): **none**
- Session-active this week: 18 profiles; idle: chatbot_builder, content-creator, sales-crm, seo-aeo-expert, telegram-utility-agent
- Thin-trace watchlist (1–3 notes touched in 7d, mostly cron one-liners): chatbot_builder (1), chatseo-agent (2), crm-outreach-agent (2), gsc-agent (2), seo-cron-agent (2), seo-swarm-agent (2), telegram-utility-agent (2), email-digest-agent (3), frontend-developer-lovable_react (3)
- Daily-note gaps (last 7d): **2026-08-26 missing**; 08-27/08-28/08-30 are thin (18–22 lines)
- Action: remind thin-trace cron agents to append a one-line Daily Note entry per run per §V3.

## WEEKLY REPORT — 2026-08-30 (Part F synthesis)
- Window: 2026-08-26 → 2026-08-30 (first full week of the wikilinks initiative + vault-logging enforcement).
- **(1) FALSE-POSITIVE RATE**
  - Nightly `downloads_stager.py`: **0%** false positives. Only 1 conflict ever quarantined (`md (1).md`) — confirmed TRUE (divergent md5 771f3de3 ≠ 6352b3f7). ` (1)`-suffixed identical re-downloads correctly skipped (benign).
  - `sunday-organize-inbox` (18:15 today): dumped **45 files** into `_Conflicts/`. ≥12 are serial-part families (ica-v3-1..5, industry-competitive-analyst-v3-part1..3, Point1-5) — LEGITIMATELY DISTINCT per AGENT_RULES §3/§7 and must NOT be quarantined → **~27% false-positive rate** on this batch. 3 are confirmed TRUE divergent duplicates (`Deep_Research_Report… (1)`, `Point6… (1)`, `industry-competitive-analyst-skill (2)` — all md5-DIFFER from base). ~30 others pending manual review.
- **(2) RECURRING PATTERNS** — browser re-download ` (n)` suffix collisions remain the dominant weekly signature. Serial-part families (v3-N / partN / PointN) repeatedly mis-flagged as would-be dupes. **Proposed rule refinement → see (6).**
- **(3) BACKLOG TREND** — `_Conflicts/` size: 08-26 N/A → 08-27:1 → 08-28:1 → 08-29:0 → **08-30:45**. Net week-over-week 0 → 45 (spike from today's organize-inbox run). The long-lived `md (1).md` was hard-deleted 08-29 with no merge/relocate record (flagged for Ole's confirmation 08-29).
- **(4) WIKILINKS HEALTH** (regression vs 2026-08-26 baseline): Notes 323→339 (+16). Zero-link 30→56 (+26); of the 56, **6 are genuine orphan CONTENT notes** (flagged: `Untitled.md`, `Hermes doctor 29 08 2026.md`, `2026-08-29.md`, `Hindsight-Read-Auth-Runbook.md`, `2nd-PC-Bootstrap-Runbook.md`, `LexFlow-CRM-Architecture.md`). Unresolved distinct targets 28→41 (+13); 59 refs (baseline 40). New unresolved dominated by template placeholders (`[[TOC]]`, `[[Agent-Name]]`, `[[<sibling note>]]`) + still-missing `Composio-Integration`, `Email-Digest-Pipeline`, `avibe-hindsight`, `LexFlow`.
- **(5) VAULT-LOGGING COMPLIANCE** (weekly enforcer 18:12): **23/23 profiles left a vault trace ✓, 0 non-compliant.** Idle (no trace expected): chatbot_builder, content-creator, sales-crm, seo-aeo-expert, telegram-utility-agent. Thin-trace watchlist (1–3 notes/7d): chatbot_builder(1), chatseo-agent(2), crm-outreach-agent(2), gsc-agent(2), seo-cron-agent(2), seo-swarm-agent(2), telegram-utility-agent(2), email-digest-agent(3), frontend-developer-lovable_react(3). Daily-note gaps: **2026-08-26 MISSING**; 08-27/08-28/08-30 thin (18–22 lines).
- **(6) PROPOSED ADJUSTMENT (awaiting Ole's decision):** Harden `sunday-organize-inbox.py` + `downloads_stager.py` conflict detection with an explicit **serial-part EXCLUDE rule** — filenames matching `(?:v\d+-\d+|-part\d+|part\d+|point\d+-|_v\d+)` skip quarantine and are treated as distinct notes (optionally grouped under a hub). This would have prevented the ≥12 false-positive quarantines in today's 45-file `_Conflicts/` backlog.

### 2026-08-30 — Nightly log (NO stager run; large `_Conflicts` spike from organize-inbox)
- **Daily note:** `05-Daily/2026-08-30.md` present but contains **no [STAGED] / [CONFLICT] / dedup lines** — `downloads_stager.py` did NOT run (or logged nothing). Note content is the 07:30 lexflow morning briefing + the 12:5x Hindsight free-only fallback fix.
- **(a) Conflicts flagged today:** 0 from the nightly stager. However **45 files** now sit in `_Inbox/_Conflicts/` following today's 18:15 `sunday-organize-inbox` run (that job, not the stager, produced them).
- **(b) Identical dupes skipped:** 0 recorded (no stager run → no md5 verify pass logged).
- **(c) _Conflicts backlog size now:** **45**. Previous count (2026-08-29): 0. **Net change: +45** — largest single-day spike since the directory was created (2026-08-27). Trend: N/A → 1 → 1 → 0 → **45**.
- **(d) Recurring pattern observed:** Yes, two distinct families in today's 45:
  1. Browser re-download ` (n)` suffix — `Deep_Research_Report_Car_Industry_Skill_Session (1).md`, `Point6_Skill_MCP_Marketplaces_Extended (1).md`, `industry-competitive-analyst-skill (2).md`. Same dominant weekly signature as 08-26/27/28.
  2. **Serial-part families mis-quarantined** — `ica-v3-1..5`, `industry-competitive-analyst-v3-part1..3`, `Point1..Point6`, `dev_landing_page_RU/EN` (language pair). These are legitimately DISTINCT notes, not duplicates.
  3. Generic/low-signal base names also quarantined: `md.md`, `INDEX.md`, plus several prompt-fragment titles ("1. Make a step by step instruction…", "find in this thread existing vertical legal saas a…") which are truncated-prompt filenames, another recurring source of collisions.
- **(e) False-positive suspicion:** **HIGH — ≥12 of 45 (~27%)**. All `v3-N` / `-partN` / `PointN` members and the RU/EN language pair look like true false positives (distinct content, suffix-only similarity). `INDEX.md` is especially concerning — quarantining a hub note breaks wikilink graph parents (§V2). Confirmed TRUE conflicts among the 45: the 3 md5-divergent ` (n)` items listed in (d).1. Remaining ~30 pending manual review.
- **Note:** the nightly stager produced a clean record for the 3rd time in 5 days, but `sunday-organize-inbox` is now the main source of noise. The serial-part EXCLUDE rule proposed in the 2026-08-30 weekly report §(6) remains the single highest-value fix; recommend also excluding `INDEX.md`/hub notes from quarantine unconditionally.

## Links
- Parent: [[_Meta/cron-jobs/INDEX]]
- Related: [[_Meta/AGENT_RULES]]
