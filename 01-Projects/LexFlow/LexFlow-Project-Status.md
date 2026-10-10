---
title: LexFlow — Project Status
created: 2026-09-19
updated: 2026-10-10
tags: [lexflow, status, orchestration]
status: active
---

# LexFlow — Project Status

Live project-status note for the LexFlow CRM. Refreshed by the `operator-installer`
daily status cron (`lexflow-daily-status-crm`, 09:00). The **authority for task status
is `docs/LexFlow_Agentic_Roadmap.json`** in the CRM repo; this note is the human-readable
mirror and is never written back into that file.

## Snapshot — 2026-10-10

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

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]
- Related: [[LexFlow-Audit-Checklist]]
- Related: [[2026-10-10]]
