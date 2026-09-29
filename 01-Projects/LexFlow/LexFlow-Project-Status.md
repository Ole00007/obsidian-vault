---
title: LexFlow — Project Status
created: 2026-09-19
updated: 2026-09-29
tags: [lexflow, status, orchestration]
status: active
---

# LexFlow — Project Status

Live project-status note for the LexFlow CRM. Refreshed by the `operator-installer`
daily status cron (`lexflow-daily-status-crm`, 09:00). The **authority for task status
is `docs/LexFlow_Agentic_Roadmap.json`** in the CRM repo; this note is the human-readable
mirror and is never written back into that file.

## Snapshot — 2026-09-29

- **🔴 P0 (day 4) — PRODUCTION IS STILL DOWN.** `https://web-production-031a6.up.railway.app/` returns **404 `{"status":"error","code":404,"message":"Application not found"}`** (`server: railway-hikari`, `x-railway-fallback: true`, `request_id: WaDnnWF9RAe0xwmQLPU1MQ`) — probes at 09:00 CEST 2026-09-29: `/` 404, `/health` 404, `/login` 404, `/api/health` **404**, all fast (0.31–0.42 s). It returned **200 on 2026-09-25**, so this is a genuine regression, and the Railway edge has **no service bound to that domain** — an app-layer outage invisible to the repo. **New detail:** the fourth probe is now a fast 404 rather than 2026-09-28's 12 s timeout. Independently corroborated at 08:47 CEST by the `lexflow-try-demo-daily-check` cron (exit 1: `health=000`, `/login?ws=lexflow=000`, `/login?ws=romanelli-studio=000`, anon `/api/admin/users=000` instead of 401, landing login refs=0, kanban siteMap missing lexflow). First reported 2026-09-26 07:41 CEST in [[2026-09-26]]. **Unblocking needs Ole's Railway prod access**: the CLI token gets 403 from Backboard GraphQL, so operator-installer can neither inspect nor restart the service. Card `t_8cbc766e`.
- **🔴 Related P0 — the Hindsight memory layer is DOWN with the identical signature.** `https://avibe-hindsight-production.up.railway.app` → **404** on `/` (verified 09:00 CEST 2026-09-29). Same Railway-edge 404 as the CRM ⇒ one edge/config action, not two independent app bugs. This breaks §V4: vault notes are not reaching long-term memory (the vault auto-push is also stalled, see [[2026-09-27]]).
- **🔴 Security P0 — the vault repo is still PUBLIC.** `Ole00007/obsidian-vault` (`isPrivate: false`, reported by memory-curator 2026-09-28 23:03), so its vault commit `42b8352` stayed local and local `main` is 3 commits ahead of `origin/main`. Pushing would publish client PII from `_Inbox/`/`_Trash`. **Action for Ole: flip the repo to private**, then the nightly vault push can resume.
- **Canonical tracker:** `~/Desktop/projects/services/LEGAL/LEXFLOW Production/lexflow-crm/docs/LexFlow_Agentic_Roadmap.json` — `last_updated` now `2026-09-29` (commit `b6b3f28`, path-limited local commit, **unpushed**).
- **Repo:** branch `lexflow_hermes_v1`, local HEAD `b6b3f28` (2026-09-29 docs-status commit, **unpushed**; local is **12 commits ahead** of `origin/lexflow_hermes_v1` = `8c17456`). Previous `8e7843a` (2026-09-28). Last real code commit remains `6ef25da` (2026-09-17).
- **Moved today:** nothing — no CRM commit, no deploy, no push, no movement on any roadmap task. All 21 task nodes carried over with unchanged columns (11 `backlog`, 1 `in_progress`, 1 `blocked`, 4 `awaiting_confirmation`, 1 `local_verified`, 2 `done`, 1 `deployed`). New facts: the outage entered its fourth day with all four probes now returning fast 404s instead of a timeout, Hindsight is still 404ing with the same edge signature, the vault repo is still public, and one non-status cron job failed (`f057d12934a7` `lexflow-morning-report`, 08:47, provider-layer `RuntimeError`).
- **⚠ Status-day health.** This job's own **2026-09-28 run completed and delivered** (09:00:14 → 09:06:41), so no new gap. Missed status days earlier this period: **2026-09-22** and **2026-09-24** (`RuntimeError: Hermes can't reach the model provider`), **2026-09-26** (`TimeoutError: idle for 929s`, limit 600 s). Evidence: `~/.hermes/profiles/smoothy_op_dir/cron/executions.db` (job `cda5f6d4a18a`). Today `dbe4783b4249` (`lexflow-morning-plan`) completed 07:32:10 → 07:48:38.
- **Kanban:** **52 cards — unchanged**, `~/.hermes/kanban.db` mtime still **2026-09-27 09:36** (no activity today). The only card created since 2026-09-19 remains `t_8cbc766e` (P0 prod down, blocked) — it maps to `open_p0`, not to a task node, and is the only prod-down card. All 18 unfinished roadmap tasks still hold exactly one open card → **0 new cards created on 2026-09-29**.
- **Working tree:** only an unstaged `.gitignore` edit and a modified `crm_local.db`. The large staged `.venv/**` / `uploads/**` deletions recorded on 2026-09-27 are **no longer staged**. The status run stages only its own tracker path; a blanket `git commit -a` must still be avoided without a deliberate decision.
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
- P0 prod-down `t_8cbc766e` (maps to `open_p0`, not to a task node)

## Parallel sources / duplicates (flagged, not touched)

- **Data-quality gap (new 2026-09-21):** T-001 and T-007 are `column: done` with `deploy_status: deployed` but carry no `prod_url`/`commit_hash`, which the roadmap file's own `report_rule` requires; T-016 names commit `da19b36` in notes but has no `prod_url`. Left unfilled rather than guessed — needs an evidence pass.
- **Owner-profile drift (§10.3, flagged 2026-09-27, still unfixed):** the `lexflow-*` / `obsidian-*` cron jobs live in `smoothy_op_dir`'s cron store while §10.3 names `operator-installer` as owner, and `operator-installer` has **no `jobs.json` (0 jobs)**. Needs Ole's decision before any job is re-homed.
- `_from-repos/LexFlow-CRM/docs/LexFlow_Agentic_Roadmap.json` — **derived** vault mirror, **STILL STALE** (`last_updated: 2026-09-03` vs authority 2026-09-28; file mtime 2026-09-04 12:44). Must be labelled `derived` or regenerated by `repo_sync`; never written back. Authority: the live repo file.
- `01-Projects/AVibe-CRM/LexFlow/PROJECT_STATUS.md`, `.../DEPLOYMENT_STATUS.md`, `01-Projects/aLEXy/_from-repos/PROJECT_STATUS.md` — stale July-2026 LexFlow status notes in other folders. Proposed: archive; single authority is the roadmap JSON + this note.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-Web-Site-Scope-2026-09-17]]
- Related: [[2026-09-29]]
- Related: [[2026-09-28]]
- Related: [[LexFlow-Audit-Checklist]]
