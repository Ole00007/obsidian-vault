---
type: build-log
project: LexFlow
feature: WS-K Matter-stage checklist
agent: crm-outreach-agent
status: done-local
date: 2026-10-25
---

# LexFlow Wave 2 — WS-K Matter-stage Checklist (Build Log)

THE KEY FEATURE: for every matter the system knows the current stage, the next
missing document/action, who owns it, when it is due — and exposes it as an agent
API (`/api/checklist/next-actions`).

## Outcome
- Branch `feat/wave2-checklist`, commit `224c4e2` (NOT pushed, no deploy).
- 9 new files (model, routes, templates service, page, JS, CSS, seed, migration, tests).
- Tests: `python tests/test_checklist.py` → **RESULT: ALL PASS** (68 checks);
  `pytest tests/test_checklist.py -q` → 1 passed.
- Migration `j1e2f3a4b5c6` (down_revision `i0d1e2f3a4b5`); upgrades clean on empty SQLite; single head on branch.

## What it does
- Stage templates are DATA (no table): `family_separation_it` (separazione, IT civil, 8 stages)
  and `generic_civil`, both headed "DRAFT — to be validated by a qualified lawyer".
- `MatterChecklistItem` tenant-scoped (workspace_id NOT NULL), statuses
  todo/in_progress/done/blocked/not_applicable, kinds document/action/deadline, optional
  owner_role (reuses Gantt TASK_ROLES), due_date, vault_ref, task_id link.
- API: templates / init (admin, idempotent 409, force wipe+reinit) / get (stages+current_stage+
  progress+next_missing) / patch (role-gated: status=any, owner+due=admin, vault_ref=superadmin) /
  materialize (→ Gantt Task, idempotent) / next-actions (agent feed, due asc nulls last, no PII).
- Behind `MATTER_CHECKLIST_ENABLED` (default OFF → 404 for ALL routes, pre-auth; query param can't force on).
- Reuses Gantt `_safe_ref` vault validation and `flag-lawyer` endpoint (imported, not copied).
- Dark-theme page `/cases/<id>/checklist`: stepper, progress ring, status toggles, role chips, materialize,
  flag-lawyer; no libraries, textContent-escaped.

## Hand-off
Report + shared-file snippets for backend-dev:
`/Users/olesiarasing/.hermes/profiles/backend-dev/cache/scratch/handoff_WS-K.md`
(shared edits: register blueprint + `checklist_enabled` context flag in crm/__init__.py,
export model in crm/models/__init__.py, Checklist link in templates/admin_matter.html).

## Links
- Parent: [[LexFlow-Platform-Plan-2026-10-24]]
- Related: [[LexFlow-Product-Research-KeyFeature-Lexroom-Agent-2026-10-24]]
- Related: [[LexFlow-Wave1-Build-Log-Technical-2026-10-25]]
