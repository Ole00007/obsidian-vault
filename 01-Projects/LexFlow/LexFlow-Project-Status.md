---
title: LexFlow — Project Status
created: 2026-09-19
updated: 2026-09-21
tags: [lexflow, status, orchestration]
status: active
---

# LexFlow — Project Status

Live project-status note for the LexFlow CRM. Refreshed by the `operator-installer`
daily status cron (`lexflow-daily-status-crm`, 09:00). The **authority for task status
is `docs/LexFlow_Agentic_Roadmap.json`** in the CRM repo; this note is the human-readable
mirror and is never written back into that file.

## Snapshot — 2026-09-21

- **Canonical tracker:** `~/Desktop/projects/services/LEGAL/LEXFLOW Production/lexflow-crm/docs/LexFlow_Agentic_Roadmap.json` — `last_updated` now `2026-09-21`.
- **Product/health:** `https://web-production-031a6.up.railway.app/health` = 200 (`db: ok`, `environment: production`).
- **Repo:** branch `lexflow_hermes_v1`, local commit `404247e` (docs-only, **unpushed** — a push triggers a Railway deploy and is gated on Ole). Previous commit `d8c9fde` (2026-09-20), last code commit `6ef25da` (2026-09-17). Remote branch still at `8c17456`.
- **Moved today:** nothing (Monday, first run of the week). No CRM commit, no deploy, no push, no Kanban card activity (`kanban.db` untouched since 2026-09-19 19:45). All task columns carried over unchanged from the 2026-09-20 run.
- **Kanban:** 51 cards on the board; all 18 unfinished roadmap tasks still hold exactly one open card → 0 new cards created on 2026-09-21.
- **§8 Repo Root Rule:** the CRM repo still sits under the legacy `~/Desktop/projects/...` path. Migration is staged and Ole-approved but not yet run for LEGAL; `~/projects/lexflow-crm` does not exist.

## What is open (by roadmap id)

- **Blocked on Ole:** T-002 cross-section reflection (explicit go before code), T-010 Resend delivery finish (verified domain or SMTP fallback), T-011 full multi-tenant inventory, T-014 RLS merge (18-test Postgres gate + `ALTER ROLE ... NOBYPASSRLS` on the Railway role, and a filing decision), T-015 uploads persistence (Railway volume, needs a redeploy), T-019 design/UX rollout (his localhost review; calendar/tasks contrast still ~4.1:1 vs WCAG AA 4.5:1), T-020 i18n (scheduled NEXT WEEK).
- **In progress:** T-008 read-only app audit (three audits delivered 2026-09-16: dead-button sweep, RLS audit, cross-feature consistency).
- **Ready/queued:** T-005 WhatsApp scoping, T-009 `scheduled_actions` delay engine, T-017 `SEAT_LIMIT_DEFAULT`.
- **Dependency-gated:** T-003, T-004, T-006, T-012 (all behind T-002), T-013, T-018 (behind T-009), T-021 (behind T-019).
- **Done/deployed:** T-001 intake manual name entry, T-007 Contacts two-model split, T-016 landing repoint.

Known product gaps recorded 2026-09-16: `/tasks` attachment endpoint 404, intake creates no Calendar event, task→calendar disconnected, no workspace filtering in API routes, and RLS not merged (app-level filter only).

## Kanban mapping (created 2026-09-19)

- T-002 `t_a5f4dd68` · T-003 `t_a7e05e2c` · T-004 `t_34e5415d` · T-005 `t_cba427b1` · T-006 `t_ba95cc42` · T-008 `t_6cf123af` · T-009 `t_7bdb5c53` · T-010 `t_da4552e5` · T-011 `t_226f9045` · T-012 `t_b8dfc0cc` · T-013 `t_5cf7a308` · T-014 `t_594fcced` · T-015 `t_f0a8b939` · T-017 `t_4af8abb6` · T-018 `t_f48b0a11` · T-019 `t_bc68191b` · T-020 `t_a4e0ad76` · T-021 `t_f0f709f5`

## Parallel sources / duplicates (flagged, not touched)

- **Data-quality gap (new 2026-09-21):** T-001 and T-007 are `column: done` with `deploy_status: deployed` but carry no `prod_url`/`commit_hash`, which the roadmap file's own `report_rule` requires; T-016 names commit `da19b36` in notes but has no `prod_url`. Left unfilled rather than guessed — needs an evidence pass.
- `_from-repos/LexFlow-CRM/docs/LexFlow_Agentic_Roadmap.json` — byte-identical copy of the live tracker; it is a derived mirror and must be labelled derived or removed. Authority: the live repo file.
- `01-Projects/AVibe-CRM/LexFlow/PROJECT_STATUS.md`, `.../DEPLOYMENT_STATUS.md`, `01-Projects/aLEXy/_from-repos/PROJECT_STATUS.md` — stale July-2026 LexFlow status notes in other folders. Proposed: archive, single authority is the roadmap JSON + this note.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-Web-Site-Scope-2026-09-17]]
- Related: [[LexFlow-Audit-Checklist]]
