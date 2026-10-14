---
title: LexFlow — Project Status
created: 2026-09-19
updated: 2026-10-14
tags: [lexflow, status, orchestration]
status: active
---

# LexFlow — Project Status

Live project-status note for the LexFlow CRM. Refreshed by the `operator-installer`
daily status cron (`lexflow-daily-status-crm`, 09:00). The **authority for task status
is `docs/LexFlow_Agentic_Roadmap.json`** in the CRM repo; this note is the human-readable
mirror and is never written back into that file.

## Snapshot — 2026-10-14

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

## What is open (by roadmap id)

- **Blocked on Ole:** T-002 cross-section reflection, T-010 Resend delivery, T-011 multi-tenant
  inventory, T-014 RLS merge (18-test Postgres gate + `NOBYPASSRLS`), T-015 uploads persistence,
  T-019 design/UX rollout (his localhost review; calendar/tasks contrast ~4.1:1 vs AA 4.5:1),
  T-020 i18n (NEXT WEEK).
- **Awaiting confirmation:** T-005 WhatsApp scoping, T-008 read-only app audit.
- **Local-verified:** T-019 (audit + UX package), plus one more per the recovered revision.
- **Dependency-gated:** T-003, T-004, T-006, T-012 (behind T-002), T-013, T-018 (behind T-009),
  **T-021 diagram/Gantt view (behind T-019)**.
- **Done/deployed:** T-001 intake manual name entry, T-007 Contacts two-model split,
  T-016 landing repoint.

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
  production root (same stale 16-node bytes).
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

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]
- Related: [[LexFlow-Audit-Checklist]]
- Related: [[2026-10-14]]
- Related: [[2026-10-12]]
- Related: [[2026-10-10]]
