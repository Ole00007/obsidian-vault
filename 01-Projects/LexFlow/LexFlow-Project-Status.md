---
title: LexFlow — Project Status
created: 2026-09-19
updated: 2026-11-04
tags: [lexflow, status, orchestration]
status: active
---

# LexFlow — Project Status

Live project-status note for the LexFlow CRM. Refreshed by the `operator-installer`
daily status cron (`lexflow-daily-status-crm`, 09:00). The **authority for task status
is `docs/LexFlow_Agentic_Roadmap.json`** in the CRM repo; this note is the human-readable
mirror and is never written back into that file.

## Snapshot — 2026-11-04

- **🔴 P0 REGRESSION — production is DOWN again (404, no service bound).**
  `https://web-production-031a6.up.railway.app` at 08:14 CET returns **404** on `/` (0.34s),
  `/login?ws=lexflow` and `/kanban`, with `server: railway-hikari` and
  `x-railway-fallback: true` — the Railway edge again has **no active service** on that domain.
  This is a regression: the 2026-11-03 run probed the same endpoints and got **200**. Same
  signature as the 2026-09-26 → 10-27 outage. Recorded in the tracker as
  **`P0-PROD-DOWN-REGRESSION-2026-11-04`** and as card **`t_9f758266`** (created `blocked` on
  purpose — it is an R3 human-ops gate, not agent work). **Only Ole can fix it** (Railway
  dashboard/service access; the CLI token 403s on Backboard GraphQL).
- **Repo paths (§8, they matter):** canonical clone
  **`/Users/olesiarasing/projects/lexflow/lexflow-crm`** — the real path is one level deeper
  than the cron prompt claims. Branch `lexflow_hermes_v1` lives in worktree
  **`…/lexflow-crm-wt-merge`** (the primary checkout sits on `integration/graph-gantt-local`
  with a stale 2026-10-27 tracker). Today's local commit **`155dd6d`**; branch is
  **14 commits ahead of `origin/lexflow_hermes_v1`** (`ddec0aa`) — **unpushed**, because a push
  there triggers a Railway deploy and needs Ole's explicit go.
- **Tracker stamped 2026-11-04** (`docs/LexFlow_Agentic_Roadmap.json`, authority unchanged).
  **7 nodes re-columned from card evidence, nothing guessed:**
  T-005, T-009, T-027 `backlog → local_verified` (cards done: WhatsApp scope decision delivered
  2026-10-06; delay engine built + independently reviewed but its 8 files were never committed;
  Hindsight memory nodes on `feat/t027-hindsight-memory` `afc4d8e`), T-013 / T-018 / T-020 /
  T-026 `backlog → blocked` (dispatcher auth crash loops, Ole's i18n window, merge-scope
  decision), and T-008 `done → local_verified` (an audit register has no deploy to cite, so
  `done` + `deploy_status: local` could never satisfy `report_rule`).
- **`[A]` gaps closed where evidence actually existed:** **T-001** → `commit_hash 309e33c` and
  **T-007** → `ef293ab`, both verified with `git merge-base --is-ancestor origin/lexflow_hermes_v1`,
  so the fix *is* inside the deployed branch. The node note carries the caveat that a deploy
  record resting on ancestry is **not** a live 200 — today prod is 404.
- **Validator: exit 1 — 14 → 4 violations.** No violation was papered over.
  - **`[A]` T-016** (landing repoint) — commit `da19b36` is not an object in this repo and the
    Netlify landing repo is gone from disk. Unverifiable, left empty rather than invented.
  - **`[B]` T-030 / T-031** — roadmap `deployed` (deploy `7354426195`, verified 2026-10-27) vs
    cards `t_7fc8830f` / `t_c0c2b530` still **blocked** awaiting Ole's visual approval. The
    **cards** are stale; a human must close or re-scope them. Not touched by this run.
  - **`[C]` two legacy tracker copies still on disk** under
    `~/Desktop/projects/Products & Services/LEGAL/LEXFLOW Production/` (2026-09-03 and
    2026-10-06). The 2026-10-12 note claiming they were "gone" was wrong. Deletion is an
    approval-gated action → reported, not removed.
- **§10.3 scheduling:** **0 new cards for roadmap work** — every unfinished node already owned
  exactly one open card, so creating more would have been a duplicate registry (§9). The single
  new card is the prod regression escalation above.
- **Unchanged:** no CRM code commit since 2026-10-29, no deploy, no push, no code change of any
  kind today — this run touched exactly one tracker file plus the vault.

## Snapshot — 2026-11-03

- **🟢 Production is UP and stable.** `https://web-production-031a6.up.railway.app` at
  09:0x CET: `/` **200** (1.34s), `/health` **200** (0.23s), `/login?ws=lexflow` **200**
  (0.24s). No Railway-edge 404 fallback signature. Prod serves
  `origin/lexflow_hermes_v1` = **`ddec0aa`** (2026-10-27, superadmin-token opt-in), which
  contains **`396bea2`** — verified with `git merge-base --is-ancestor`, so the T-030 /
  T-031 "deployed" claims hold.
- **Repo paths (they matter, §8):** canonical clone **`/Users/olesiarasing/projects/lexflow/lexflow-crm`**
  (real path is one level deeper than the cron prompt says). Branch `lexflow_hermes_v1`
  lives in worktree **`…/lexflow-crm-wt-merge`**, local tip now **`e8c3cdb`** — three local
  commits today: validator fix `cbe9b29`, status stamp `0b34e13`, post-run note `e8c3cdb`;
  **11 commits ahead of `origin`** — all unpushed (a push triggers a Railway deploy → Ole's gate).
- **🔧 Split-brain in the tracker — RESOLVED today (§9).** Two divergent copies existed:
  the integration-branch copy (`last_updated 2026-10-27`, carrying T-029..T-031, the
  2026-10-26 decisions and the P0 RESOLVED stamp) and the `lexflow_hermes_v1` copy
  (`last_updated 2026-10-24`, **129 diff lines behind**). The deploy branch is what the
  CRM superadmin UI renders and what Railway ships, so **the integration content was
  landed onto `lexflow_hermes_v1`** — that checkout is now the authority. Direction is
  safe: the integration copy was a strict superset (additions + status only, no deletions).
- **🔧 Validator was BROKEN, now fixed.** `docs/tools/validate_roadmap.py` crashed with
  `sqlite3.OperationalError: unable to open database file` because it opened
  `~/.hermes/kanban.db` with a strict `mode=ro` URI on a **WAL-mode** board with no
  pre-existing `-shm`. Fixed with a fallback chain (ro → ro+immutable → rw; SELECTs only).
  The one-tracker guard also now ignores same-repo **git worktree** checkouts (git tracks
  those) while still failing on foreign copies.
- **New cards (§10.3):** roadmap tasks **T-022…T-029 had no Kanban card at all** — one card
  each created today. `T-022` `t_2fdf274d` · `T-023` `t_2f2479f8` · `T-024` `t_aa43a4c0`
  (blocked: needs Ole's Railway access) · `T-025` `t_fe4e8687` (parent-gated on T-022 / T-024 /
  T-029) · `T-026` `t_76894c79` (Ole's scope decision) · `T-027` `t_a4eb8bf2` ·
  `T-028` `t_f3890cf5` · `T-029` `t_8115f68b`. **No duplicate cards** — the existing push
  gate `t_8fe36335` and cross-test gate `t_e4706b73` were reused by reference.
  Within ~10 min the dispatcher claimed five of them (T-022 / T-023 / T-027 / T-028 / T-029 now
  `running`); T-024 sits `blocked` on Ole's Railway access, and T-025 / T-026 are parent-gated
  in `todo`.
- **Nothing else moved:** no CRM code commit since 2026-10-29, no deploy, no push, no task
  column change. Board: 80 cards (26 blocked, 48 done, 4 todo, 1 ready, 1 scheduled).
- **Validator result: exit 1 — 12 violations, 4 corrected today, 8 left open honestly.**
  - Fixed: `[D]` freshness (stamped 2026-11-03) and 8 × `[B] "unfinished task has no card"`.
  - **`[A] report_rule gaps (4, open):** T-001 / T-007 (done+deployed) and T-016 (deployed)
    carry no `prod_url`+`commit_hash`; T-008 (done+local) has no `local_preview_url`. No
    evidence anywhere — left empty rather than invented.
  - **`[B] card↔roadmap drift (7, open):** T-030 / T-031 = deployed on the roadmap and live
    on prod, but cards `t_7fc8830f` / `t_c0c2b530` are still **blocked** — the *cards* are
    stale, need their owners' close-out. T-005 / T-009 = roadmap backlog vs cards **done**
    (one of the two is wrong; no schema evidence proves T-009 shipped). T-013 / T-018 / T-020
    = deliberately blocked cards on backlog nodes (a validator mapping gap, not a data error).
  - **`[C] duplicate trackers (open):** two foreign copies under
    `~/Desktop/projects/Products & Services/LEGAL/LEXFLOW Production/` (14 KB @ 2026-09-03,
    33 KB @ 2026-10-06) — **still on disk**; the 2026-10-12 note claiming they were "gone"
    was wrong. Deletion gated on Ole.
- **⚠️ ~22 git worktrees** under `~/projects/lexflow/` each hold a copy of the tracker. They
  are derived-by-construction, but one of them *was* the stale parallel truth found today —
  worktree hygiene is a real risk here, not a theoretical one.

## Snapshot — 2026-10-14 (superseded; retained as history)

- **🔴 P0 STILL DOWN — production day 19.** `https://web-production-031a6.up.railway.app`
  returns **404** on `/` (0.27s), `/health` (0.25s), `/login?ws=lexflow` (1.67s) and
  `/api/health` (0.24s) at 09:00 CEST. Same Railway-edge fallback signature. Root cause is
  **outside the repo** — needs Ole's Railway account.
- **Repo/tracker:** `~/projects/lexflow-crm` @ `lexflow_hermes_v1`, HEAD **`82d1f09`**
  (`docs(roadmap): daily status 2026-10-14`), working tree has untracked `.DS_Store` +
  `Frappe-Gantt/`. **19 commits ahead of `origin`** — all docs/tracker/tooling, **unpushed**
  (a push here triggers a Railway deploy → Ole's gate). Tracker `last_updated: 2026-10-14`,
  21 nodes.
- **Nothing moved:** no CRM commit, no deploy, no push, no Kanban activity (`~/.hermes/kanban.db`
  mtime still 2026-10-10 22:23:25). All 21 nodes unchanged; **0 new cards** (every unfinished task
  still holds exactly one open card — no duplicate registry, §9/§10.3).
- **Validator first run:** `docs/tools/validate_roadmap.py` (added 2026-10-12) ran for the first
  time. Exits **1** with 8 violations — all pre-existing, none corrected (no evidence):
  - **[A] report_rule gaps (4):** T-001, T-007 done/deployed without prod_url+commit_hash;
    T-008 done/local without local_preview_url; T-016 deployed without prod_url+commit_hash.
  - **[B] card↔roadmap drift (3):** T-005 card=done vs roadmap=backlog; T-009 card=done vs
    roadmap=backlog; T-020 card=blocked vs roadmap=backlog.
  - **[C] multiple trackers (1):** 3 tracker files on disk — canonical + 2 stale copies under
    `~/Desktop/.../LEXFLOW Production/`. The 2026-10-12 "one tracker" claim missed them (that
    run's find did not search ~/Desktop). Deletion gated on Ole.
- **⚠️ P0 Kanban card (t_8cbc766e) is marked done but production is still 404.** The card was
  closed 2026-10-10 22:23 when a fix was briefly verified 200, but the platform reverted it.
  Card status does not reflect reality — flagged for Ole.
- **Status run health:** last successful run was 2026-10-12; no run on 2026-10-13 (provider
  failure). The job carries `model_snapshot=deepseek/deepseek-v4.1-flash` /
  `provider_snapshot=openrouter`, which overrides the profile `config.yaml` default.

## Snapshot — 2026-10-12 (superseded; retained as history)

- **🔴 P0 REOPENED — production went back down.** `https://web-production-031a6.up.railway.app`
  returns **404** on `/` (0.49s), `/health` (0.33s), `/login?ws=lexflow` (0.41s) and
  `/login?ws=romanelli-studio` (0.36s) at 12:41 CEST. **Day 17.** The 2026-10-10 fix was applied
  and verified **200**, then **removed again by the platform** — the same reversion behaviour
  observed that night. The 08:36 `lexflow-try-demo-daily-check` got `000` instead of 404, so the
  edge is **flapping between fast-404 and no-response**, not holding a steady state. Root cause is
  **outside the repo** — no code change fixes it; it needs Ole's Railway account.
- **The 2026-10-10 "P0 RESOLVED / LIVE again" claim below is SUPERSEDED** — it was true for a few
  hours that night, but it did not stick. Treat the section below as history, not current state.
- **Repo/tracker:** `~/projects/lexflow-crm` @ `lexflow_hermes_v1`, HEAD **`2189902`**
  (`docs(roadmap): daily status 2026-10-12`), working tree clean, **17 commits ahead of `origin`** —
  all docs/tracker, **unpushed** (a push here triggers a Railway deploy → Ole's gate).
  Tracker `last_updated: 2026-10-12`, 21 nodes.
- **⚠️ The status run itself was broken for 8 days.** Cron `cda5f6d4a18a` (`lexflow-daily-status-crm`)
  failed **2026-10-05 → 2026-10-12**: six runs with OpenRouter `HTTP 402 — requires more credits`
  (requesting up to 131072 tokens) and two with "Hermes can't reach the model provider". Today is the
  first run since 2026-10-10 that reached the provider. Cause is a **per-job model pin**
  (`model_snapshot=deepseek/deepseek-v4.1-flash`, `provider_snapshot=openrouter`) that overrides the
  profile default — see the model note below.
- **Nothing moved:** no CRM commit, no deploy, no push, no Kanban activity (`~/.hermes/kanban.db`
  mtime still 2026-10-10 22:23). All 21 nodes unchanged; **0 new cards** (every unfinished task still
  holds exactly one open card — no duplicate registry, §9/§10.3).
- **One clone, one tracker — VERIFIED holding.** Exactly one LexFlow clone and one
  `LexFlow_Agentic_Roadmap.json` on disk. The 2026-10-10 dedupe did not regress: no `~/lexflow-crm`,
  no second tracker. (A `find` may print the path under the casing `Projects` — `~/projects` and
  `~/Projects` are the same APFS directory, not two copies.)
- **PATH DRIFT resolved on disk, still open in the job text.** The §8 migration **has now run** for
  LexFlow: the canonical repo is `~/projects/lexflow-crm` and the legacy
  `~/Desktop/.../LEXFLOW Production/lexflow-crm` clone is **gone from disk** (so the 2026-10-10
  recovery source no longer exists — its objects are preserved here as remote `legacy-recovered`).
  The cron job's **prompt still points at the dead `~/Desktop/projects/services/LEGAL/...` path** —
  needs Ole's go to rewrite.

## Snapshot — 2026-10-10 (superseded; retained as history)

- **🟢 P0 RESOLVED — production is LIVE again after 15 days.** `https://web-production-031a6.up.railway.app`
  returns **200** on `/`, `/health` and `/login?ws={lexflow,romanelli-studio,orasing,pagliano}`; `/health`
  reports `{"database_url_set":true,"db":"ok","environment":"production","python":"3.11.8","status":"ok"}`;
  anonymous `/api/admin/users` correctly returns **401**. **Hindsight is also back**: `avibe-hindsight-production`
  `/health` 200, `/v1/default/banks` 401 (alive, auth intact) — vault notes reach long-term memory again (§V4).
  **Root cause (never the domain, never an app bug):** Railpack runs `mise` to install the interpreter pinned in
  `runtime.txt` (`python-3.11.8`); mise ≥ 2026.8.13 enforces GitHub artifact-attestation verification and that
  artifact publishes none → `mise install` aborts → build fails → no deployment → edge fallback 404.
  **Fix:** `MISE_PYTHON_GITHUB_ATTESTATIONS=false` set on service `web` (project `perceptive-achievement`,
  env `production`) + rebuild from source. **Second, separate fault:** `Postgres` had no running deployment
  (its `postgres-volume`, 117 MB, was intact) and the app 500'd on
  `could not translate host name "postgres.railway.internal"` until the DB was started with
  `railway service redeploy --from-source`. **No push was made.**
- **Canonical repo rebuilt at the §8 path.** **`~/projects/lexflow-crm`** on branch
  **`lexflow_hermes_v1`**, HEAD `c81372a` (16 commits ahead of `origin` — **unpushed**).
  Nothing was deleted anywhere.
- **The "unreachable" legacy clone was RECOVERED — the 2026-10-04/10-06 state is NOT lost.**
  `~/Desktop` refuses *directory listing* under TCC (`Operation not permitted`), but **direct
  reads of a known path and git plumbing still work**, and `mdfind` reads the Spotlight index
  without touching the filesystem ACL. That recovered
  `~/Desktop/projects/Products & Services/LEGAL/LEXFLOW Production/lexflow-crm`:
  **15 local-only commits** (incl. `ede8e13` 2026-10-04, `016568e` T-005 WhatsApp scoping,
  `7e4343b` T-008 consolidated audit, and daily status commits back to 2026-09-19) plus
  branches `feat/t021-diagram-gantt` `feat/rls` `feat/attachments` `feat/saved-views`
  `calendar-grid` `deploy/repoint-b`. **Fetched read-only into the canonical repo** as remote
  `legacy-recovered`; objects are now preserved in `~/projects/lexflow-crm`'s object store.
  Nothing was pushed and `origin` is untouched.
- **Canonical tracker = the recovered revision.** `docs/LexFlow_Agentic_Roadmap.json` now holds
  the 2026-10-06 revision — **21 task nodes** (10 backlog · 4 awaiting_confirmation · 3 done ·
  2 local_verified · 1 blocked · 1 deployed), md5 `60bbc9df97f7aaa5f62339db48efd692` — stamped
  `last_updated: 2026-10-10` and committed locally (`c81372a`). It **supersedes** the
  2026-09-03 / 19-node revision that was on `origin/lexflow_hermes_v1`. The pre-recovery
  commit is parked as tag `status-20261010-pre-recovery`.
- **Nothing moved 2026-10-07 → 2026-10-09:** no commits, no deploys, no pushes (the missing
  runs). Today: docs/status only. **No push** was made — a push to this branch triggers a
  Railway deploy and needs Ole's gate.
- **Kanban:** 53 cards, `~/.hermes/kanban.db` mtime 2026-10-06 13:05 — no new card activity.
  Every roadmap node already holds a card, so **0 new cards were created** (no duplicate registry).
- **Card ↔ roadmap mismatches left honest, not guessed:** T-009 (`t_7bdb5c53` done) and
  T-017 (`t_4af8abb6` done) vs roadmap `backlog`; T-013 / T-018 cards `ready` vs `backlog`;
  T-001/T-007 `deployed` without `prod_url`/`commit_hash` (the file's own `report_rule` gap).

## What is open (by roadmap id) — re-derived 2026-11-04

- **Blocked on Ole (decision/access):** T-002 cross-section reflection (his go before code),
  T-010 Resend delivery (verified domain or SMTP — client mail still 403 until then),
  T-011 multi-tenant inventory, T-014 RLS merge (18-test Postgres gate + `NOBYPASSRLS`),
  T-015 uploads persistence (final go for the volume redeploy), T-019 design/UX rollout
  (his localhost review; calendar/tasks contrast ~4.1:1 vs AA 4.5:1), T-020 i18n (window not
  open), **T-024 Railway `SECRET_KEY` / `JWT_SECRET_KEY` must be confirmed set before the next
  deploy** (card `t_aa43a4c0`), **T-026 keep-or-split the progress-visualiser** (card
  `t_76894c79`).
- **Deploy gate, ready once its parents close:** T-025 staging smoke test
  (`t_fe4e8687`, parent-gated on T-022 / T-024 / T-029).
- **Local-verified, waiting on the push gate:** T-017 seat limit, T-019 UX package, T-021
  context graph, **T-022 Gantt** (`t_2fdf274d`), **T-023 JWT-wipe fix** (`t_2f2479f8`).
- **Backlog / spec-first:** T-003, T-004, T-006, T-012 (behind T-002), T-013, T-018 (behind
  T-009), T-027 Hindsight nodes (`t_a4eb8bf2`), T-028 real roadmap dates (`t_f3890cf5`),
  T-029 notify_consents migration (`t_8115f68b`).
- **Done / deployed:** T-001 intake manual name entry, T-007 Contacts two-model split, T-008
  read-only audit, T-016 landing repoint, **T-030 Elisa launcher** and **T-031 blocked-state
  visual** (both live in deploy 7354426195 / commit `396bea2` — their *cards* are still
  blocked and need closing by their owners).

## Incoming task — Gantt master prompt (2026-10-10)

`~/Obsidian/Hermes_LexFlow_Gantt_Master_Prompt.Md` (v2026-10-07, byte-identical to the
`_Inbox` copy) asks for a narrowly scoped **read-only Frappe Gantt view** over existing
task/case records. **It is not a new task** — it maps onto roadmap node **T-021**
(card `t_f0f709f5`, already gated behind T-019). No duplicate card was created; the prompt was
attached to the existing card. Gate A (inspection + preflight) is done —
see `_Inbox/LexFlow-Gantt-GateA-Preflight-2026-10-10.md`.

- **News:** a Frappe Gantt prototype **already exists locally** on
  `legacy-recovered/feat/t021-diagram-gantt` (`87b847c`) — `docs/t021-demo/index.html` plus
  vendored `frappe-gantt.umd.js` / `.es.js` / `.css`. That is a demo under `docs/`, **not**
  production wiring, and the master prompt explicitly says the graph demo is a reference only.
- **Blocker:** T-021 sits behind T-019, which is blocked on Ole's localhost design review —
  so Gate B (implementation) cannot open yet.
- **Smallest owner decision:** which fields define each Gantt bar's start/end. No generic
  start/end pair exists — `Task` has `createdat`+`duedate`, `Case` has `openedat`+`duedate`,
  `Deadline` has `deadline_date` only, and only `CalendarEvent` has a true start+end.

## Parallel sources / duplicates (flagged, not touched)

- **Duplicate clone:** `~/lexflow-crm` — same remote (`Ole00007/lexflow-crm`) but on `main`
  (`06cef99`, 2026-07-20), no `docs/`; **not** the deploy source. Archive it — gated on Ole.
- **Legacy Desktop clone** — recovered, history now preserved in the canonical repo. The
  directory itself is TCC-listing-blocked; it is *not* a working location (§11) and should be
  archived only after Ole confirms nothing else lives there.
- **Stale roadmap copies (authority = the repo file, now the 21-node revision):**
  `01-Projects/LexFlow/_from-repos/LexFlow-CRM/docs/LexFlow_Agentic_Roadmap.json`
  (2026-09-03, 21 nodes, derived vault mirror), `~/Downloads/…` (2026-09-03, 16 nodes),
  `_Inbox/_Conflicts/…` (byte-identical to Downloads), and the copy at the legacy clone's
  production root (same stale 16-node bytes). The 16-node and 21-node JSON snapshots originally
  in `~/Obsidian/_Trash/2026-10-10-lexflow-dedupe/` were archived to `~/Obsidian/04-Archive/`
  on 2026-11-04 (Ole-approved).
- **`~/Projects/LEGAL_backup/Romanelli-studio/lexflow-crm` is a DIFFERENT repo** — its remote is
  `Ole00007/Romanelli-studio.git` (`5082d1b`), not `lexflow-crm`. It is a git work tree, not a
  LexFlow code authority. (An earlier note that it was a plain non-git snapshot was wrong —
  corrected 2026-10-10.)
- **Dead path in the cron prompt:** this job's own text still points the tracker at
  `~/Desktop/projects/services/LEGAL/...`; that was never the real location (the real legacy
  path was `.../Products & Services/LEGAL/...`). **Fix the cron prompt.**
- **Dedupe executed (2026-10-10, Ole-approved):** the stray home-root clone `~/lexflow-crm` and three
  stale tracker copies (Downloads, `_Inbox/_Conflicts`, vault `_from-repos`) were **archived, not deleted** —
  manifest at `~/projects/_archive/2026-10-10-lexflow-dedupe/README.md`, vault copies in
  `~/Obsidian/_Trash/2026-10-10-lexflow-dedupe/`. One clone, one tracker.
- **MCP rollout (2026-10-10, Ole-approved):** all 18 specialist profiles that carried a wild
  "everything enabled" template were aligned to the global config's approved state (12 enabled).
  **18 backups** at `…/config.yaml.bak-20261010-mcprollout`. One flagged side-effect: `brave-search`
  is now off everywhere — re-enable per profile if a search fallback is wanted.
- **New cards (2026-10-10):** `t_7048b1a6` Fronty progress-visualiser app (React, LexFlow data base,
  local URL deliverable, deployment gated); **T-019 unblocked** → `t_bc68191b` handed back to Fronty
  with a localhost-URL deliverable and the measured-contrast requirement.
- **Status file for Ole:** [[LexFlow-CRM-Where-We-Stand-2026-10-10]] — the single "where we stand" doc.
- **Owner-profile drift (§10.3):** the `lexflow-*` / `obsidian-*` cron jobs live in
  `smoothy_op_dir`'s cron store while §10.3 names `operator-installer` as owner.

## Model / cron health note (2026-10-12) — why the daily run kept falling over

- The TUI/chat header shows the **session's effective model**, not the file you edit. The daily job
  carries a **per-job pin**: `model_snapshot: deepseek/deepseek-v4.1-flash`,
  `provider_snapshot: openrouter`. That snapshot **overrides** the profile `config.yaml` default —
  so changing `config.yaml` alone does not change what this job (or an already-started session) runs on.
- **The chosen replacement is not a real model.** `meituan/longcat-2.5-preview:free` appears **0 times**
  in the Hermes model catalog (`https://hermes-agent.nousresearch.com/docs/api/model-catalog.json`,
  updated 2026-09-21), which ships exactly two providers — `openrouter` (64 models) and `nous` (47).
  No `meituan/*` and no `longcat` in either. It also mixes provider `nous` with an
  OpenRouter-style id (`meituan/…:free`) — a mismatch. `deepseek/deepseek-v4.1-flash` **is** in the
  catalog and is valid.
- **Action for Ole:** re-pin the job to a catalog model on a funded provider
  (`hermes config set` / the `hermes model` picker — never hand-edit `config.yaml`), and check the
  OpenRouter balance: the 402s are *credits*, not reachability. Nothing here is fixed from the repo side.

## 2026-11-03 — T-028 Gantt real dates (local only, not deployed)

`docs/LexFlow_Agentic_Roadmap.json` on `lexflow_hermes_v1` now carries evidence-based
`start_date`/`due_date` per task node instead of letting `/gantt` derive dates from the column:
10 of T-001..T-020 dated (git commit / Kanban card event / dated note as the source), 10 left
undated with a per-node `date_source` stating that no evidence exists, and a new top-level
`gantt_dates` block recording the policy + provenance. Stale past-due nodes re-baselined
(T-025, T-028, T-029 → 2026-11-03) or left as historical plan (T-026, card claimed live);
T-030/T-031 verified already correct (deployed 2026-10-27). Docs-only commit `1ed2b14`, NOT
pushed (push triggers a Railway deploy). Repo: `/Users/olesiarasing/projects/lexflow/lexflow-crm-wt-merge`.
Follow-up `t_6b05ac79`: the seeder still fabricates dates for undated nodes.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]
- Related: [[LexFlow-Audit-Checklist]]
- Related: [[LexFlow-Admy-Push-2026-10-27]]
- Related: [[2026-11-04]]
- Related: [[2026-11-03]]
- Related: [[2026-10-14]]
- Related: [[2026-10-12]]
- Related: [[2026-10-10]]
