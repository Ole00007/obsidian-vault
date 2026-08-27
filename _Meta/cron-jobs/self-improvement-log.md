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


## Links
- Parent: [[cron-jobs-INDEX]]
