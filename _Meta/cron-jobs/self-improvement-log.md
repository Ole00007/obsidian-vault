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

## Links
- Parent: [[cron-jobs-INDEX]]
