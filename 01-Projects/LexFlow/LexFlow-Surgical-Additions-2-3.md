---
title: LexFlow — Surgical Additions #2 & #3 (parallel build)
created: 2026-08-29
updated: 2026-08-29
tags: [lexflow, crm, build, twenty-clone]
status: DEPLOYED ✅ (2026-08-29)
---

# LexFlow — Surgical Additions #2 & #3 (parallel build)

## Context
LexFlow CRM (branch `lexflow_hermes_v1`) is the single system of record. The Aug-16 Twenty CRM comparison produced a 6-item clone proposal; items already adopted: polymorphic notes, kanban, calendar, email. Local run: `~/Desktop/projects/services/LEGAL/lexflow-crm` (port 5003). Live: https://web-production-031a6.up.railway.app (Railway project `perceptive-achievement`).

## Diagnosis — intake upload button was a MOCKUP (not a Postgres issue)
- `templates/index.html` form: `enctype="multipart/form-data"` + `documents` file input ✅
- `crm/routes/views.py` `submit()` read only `request.form` fields — never touched `request.files` ❌
- Railway Postgres healthy (`/health` → `db: ok`)
- **Fix = surgical item #3 (Attachments)** — Attachment model + upload handling + wire into `/submit`.

## Decision — parallel subagents with git-worktree isolation
Chose `delegate_task` (2 leaf subagents, deleg_0a577b19) over starting `backend-dev` / `lexflow_dev_head_admin` profiles because: speed, context isolation, stopped gateways, and git-worktree safety. Two worktrees on isolated branches:
- `feat/saved-views` → `~/Desktop/projects/services/LEGAL/lexflow-savedviews`
- `feat/attachments` → `~/Desktop/projects/services/LEGAL/lexflow-attachments`
- Migration head both extended: `bf5e6a7b8c9d`

## Built & MERGED ✅ (commit f9804ea on lexflow_hermes_v1)
| # | Feature | Legal term | Files | Migration |
|---|---|---|---|---|
| 2 | Saved Views | Viste salvate per fascicolo/cliente | `crm/models/view.py`, `crm/routes/saved_views.py` | `a1f2e3d4c5b6` |
| 3 | Attachments (+ intake upload fix) | Allegati / fascicolo documentale | `crm/models/attachment.py`, `crm/routes/attachments.py`, `crm/routes/views.py` | `c1d2e3f4a5b6` |

Both subagents fully tested their endpoints locally (201/200/404/401/413/400 verified).

## Extra fixes made during merge (real bugs)
1. **SECRET_KEY missing in `crm/config.py`** → `flash()`/session cookies made `/submit` return 500. Added `SECRET_KEY` (env override, safe default). This was the true reason the intake form broke end-to-end.
2. **Hardcoded Mac upload path** in `submit()` → made portable: now resolves `uploads/` from repo root (works on Railway).
3. **Merge conflicts** in `crm/__init__.py` + `crm/models/__init__.py` — resolved (both View + Attachment registered; 15 blueprints total).

## All buttons must be REAL, not mockups (Ole requirement)
- [x] Intake document upload button → wired to `/submit` file handling (was mockup)
- [x] Saved Views endpoints → real CRUD
- [x] Attachments endpoints → real upload/download/delete
- [ ] Full button sweep across all frontend templates pending (kanban, calendar, tasks, contacts, admin) — verify no other dead buttons

## Status
- [x] Diagnosis confirmed
- [x] Worktrees created
- [x] Both subagents dispatched (deleg_0a577b19) + built
- [x] Merged into lexflow_hermes_v1 (f9804ea)
- [x] SECRET_KEY + upload path fixes
- [x] Local test of merged code: **17/17 PASS** (fresh DB + prod-sim old-schema)
- [x] Pushed to GitHub (approved) — Railway auto-deploys on push to `lexflow_hermes_v1`
- [x] DEPLOYED to Railway (deployment 744dbb0d) — prod health `db: ok`
- [x] Prod verified: `/api/views` → 200 [], `/api/attachments` → 200 [], intake `/` → 200

## Additional real bugs fixed during build 2 (found via local + prod testing)
1. **SECRET_KEY missing** in `crm/config.py` → intake `/submit` 500 on `flash()`. Added.
2. **Hardcoded Mac upload path** in `submit()` → made repo-root portable.
3. **Idempotent seed**: migration seeds workspace slug `lexflow`, `_seed_default_users()` tried to insert a duplicate → UNIQUE constraint on fresh DB. Fixed to reuse.
4. **pbkdf2:sha256 hashing**: macOS system Python has no `hashlib.scrypt` → login 500 locally. Pin to pbkdf2 (works everywhere; existing scrypt hashes still verify).
5. **`db.create_all()` auto-migration** on app boot so new tables appear in already-deployed prod DBs (prod uses create_all, not alembic).
6. **Postgres-portable `is_default` server_default**: `db.func.false()` renders `DEFAULT false()` (invalid PG DDL, 500 on Railway); switched to `sa.text("'0'")`. This was caught by the real Railway deploy — local SQLite tolerated the bad SQL.
7. **Intake upload path** aligned to repo-root `uploads/` (matches attachments download route).

## Telegram reporting
- Target: `telegram:1372207688` (IG @Alessia_code)
- Report sent 2026-08-29: build 2 deployed, buttons now real.

## Cron jobs (created 2026-08-29, deliver to Telegram)
- **`lexflow-nightly-watchdog`** (23:59 daily) — script-based (`lexflow-nightly-watchdog.sh`, no_agent): if new commits pushed to `lexflow_hermes_v1` → reports them; if nothing changed → runs deployed health test (health/intake/api probes) and reports all-fine or needs-attention.
- **`lexflow-morning-plan`** (07:30 daily) — LLM agent: reads git log + prod health + Obsidian notes, then sends "Plan for today" (LexFlow building next steps, SEO/AEO clients, feedback, roster-agent suggestions). 10-15 bullets, ends with single most important task.

## Item #5 TimelineActivity auto-logging — COMPLETE (2026-08-29)
- Added `log_activity` to **tasks.py** (created/updated/deleted), **deadlines.py** (deadline_added/updated/deleted linked to case)
- **calendar.py**: real actor from JWT (was hardcoded 1) + event_created/updated/deleted logging
- Local 12/12 tests pass → pushed (5f35a49) → Railway auto-deployed (03c76257) → prod `db:ok`, `/api/intake/pagliano` responds (workspace exists), `/pagliano` 200

## Pagliano LP reconnect — COMPLETE (2026-08-29)
- `pagliano.html` fetch pointed at **legacy** `web-production-ab54f.up.railway.app/api/intake` → changed to relative `/api/intake/pagliano` (LexFlow CRM, workspace slug `pagliano` exists in prod)
- Login link → `/dashboard` (was ab54f root)
- No ab54f references remain in templates

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[Hermes_Prompt_Compare_Clone_Twenty_v1]]
