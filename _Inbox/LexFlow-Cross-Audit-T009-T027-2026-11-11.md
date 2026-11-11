---
title: LexFlow Cross-Audit — T-009 (be5ae63) + T-027 (848c2c3)
created: 2026-11-11
tags: [lexflow, cross-audit, backend, migrations, hindsight, operator-installer]
project: LexFlow
home: 01-Projects/LexFlow
status: active
---

# LexFlow Cross-Audit — T-009 (be5ae63) + T-027 (848c2c3)

Card: `t_15bf3380` · Auditor: `smoothy_op_dir` (operator-installer) · Date: 2026-11-11 09:43 CET
Repo: `/Users/olesiarasing/projects/lexflow/lexflow-crm-wt-merge` (branch `lexflow_hermes_v1`, HEAD `84af7fc` = `be5ae63` + one docs-only daily-status commit)
Scope: review only — **no push, no deploy, no external send.**

## Verdicts

| Commit | Task | Verdict | Column effect |
|---|---|---|---|
| `be5ae63` | T-009 scheduled_actions + worker poll + should_notify | **APPROVED** | none — stays `local_verified`, `deploy_status: local` |
| `848c2c3` | T-027 Hindsight memory nodes + digest merge | **APPROVED** | none — stays `local_verified`, `deploy_status: local` |

Cross-audit notes appended to both roadmap nodes and committed locally as `e94c396` (not pushed).

## T-009 — evidence

- `python3 -m pytest tests/test_scheduled_actions.py -v` → **4 passed**.
- `python3 -m pytest tests/test_agent.py -v` → **25 passed, 1 failed**; the failure (`test_elisa_chat_tasks_and_agenda`) was **reproduced at `07fe270`** in a detached worktree, so it is pre-existing and not attributable to T-009. The changed head assertion (`tests/test_agent.py:287` expects `l3a4b5c6d7e8`) passes.
- Alembic: single head `l3a4b5c6d7e8`; full chain base→head executed on a **fresh database** → `scheduled_actions` with 19 columns, 5 indexes, 3 FKs (contact/case `ON DELETE CASCADE`), `alembic_version = l3a4b5c6d7e8`; downgrade drops it cleanly.
- PostgreSQL DDL rendered offline (no PG server, docker daemon down → **dialect-rendered, not executed**): `SERIAL` PK, `VARCHAR(n)`, `TIMESTAMP WITHOUT TIME ZONE`, `DEFAULT CURRENT_TIMESTAMP`, `ON DELETE CASCADE`.
- `python -m crm.worker --once` → exit 0, claims due rows.

### Follow-ups (non-blocking for `local_verified`, required before T-004 sends anything)
1. **No production handler exists.** Nothing outside tests calls `register_handler`, and `crm/worker.py` imports no handler module → every due row lands `state=failed`, `last_error='no handler registered for kind=…'` (measured). The first real handler module must be imported by the worker before T-004.
2. **Tenant guard missing.** `crm/services/scheduled_actions.py` `enqueue()` does not assert `contact.workspace_id == workspace_id`; a cross-tenant mismatch is constructible (TENANT AUDIT rule).

## T-027 — evidence

- No conflict markers left in `crm/ static/ templates/ tests/ migrations/`.
- Flag default **OFF** verified in code: `crm/routes/context_memory.py:53` `_enabled()` is False unless `CONTEXT_MEMORY_ENABLED` is explicitly `1/true/yes/on`; `crm/__init__.py` registers the blueprint without setting any env var.
- `python3 tests/test_context_memory.py` → **ALL PASS** (flag-off 404, anon 401, admin 403, superadmin 200 `unconfigured`, scrub, cache, digest ≤ 8, upstream-down, existing pages).
- `python3 tests/test_context_notes.py` → **ALL PASS** (merge did not regress the notes path).

### Deploy gates (none is a code-correctness defect)
1. **DESIGN GATE** — `/graph` gains a "Memory digest" card (`templates/graph.html:46`) → Ole must eyeball the localhost preview before any deploy.
2. `HINDSIGHT_URL` + `HINDSIGHT_API_KEY` are Ole's Railway vars and remain unset.
3. **Perf** — `static/js/graph/graph_view.js:163-167`: `ingest()` (paint) runs *after* the memory fetch, so a superadmin graph paints only when Hindsight recall returns (`TIMEOUT_S=20`, ~7.5 s measured). Recommend painting first, merging memory after.

## New P1 found while auditing (PRE-EXISTING, not T-009/T-027)

The migration chain **cannot provision a fresh schema**: no migration creates `firm_team_members`, `google_calendar_tokens`, `contact_relationships`, and none adds `workspaces.code_prefix`, `contacts.lifecycle_stage/tags/updated_at`, `cases.case_no`. Three FKs in the rendered chain point at the never-created `firm_team_members`, so a fresh **PostgreSQL** `flask db upgrade` would fail at `h9c0d1e2f3a4` (SQLite tolerated it, which is why tests never caught it). Routed to `backend-dev` as card `t_fdbc90f7`; existing databases are unaffected (built by `db.create_all()`).

## Links

- Parent: [[LexFlow-Roadmap]]
- Related: [[LexFlow-Cross-Feature-Consistency-Audit]]
- Related: [[LexFlow-Deploy-Verification-2026-10-27]]
- Related: [[2026-11-11]]
