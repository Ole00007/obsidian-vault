# LexFlow CRM — Cross-Feature Consistency Audit

**Date:** 2026-09-16
**Task:** t_4f1a9c3c
**Status:** COMPLETE
**Prod URL:** https://web-production-031a6.up.railway.app

## Executive Summary

Audited LexFlow CRM for cross-feature consistency per Ole's standing requirement:
every intake or task must show up in Contacts, Calendar, and Dashboard for the owning workspace.

**Overall result: 4 issues found, 0 deploy-ready fixes.** No changes pushed to prod.

## Issues Found

### 1. File Upload on /tasks → 404 (not 500)

The production app has **no file upload endpoint** for tasks. `POST /api/tasks/import` returns 404 on production, while the local dev copy has the route (returns 400 without file). The `/tasks` SPA page has a file-attach button that sends to a non-existent endpoint.

**Root cause:** The `routes/tasks.py` `import_tasks_csv()` route exists locally but was never deployed to production. The file upload flow only exists on the legacy `/submit` endpoint.

**Fix:** Add `POST /api/tasks/<int:task_id>/attach` endpoint with file validation.

### 2. Intake Does NOT Create Calendar Events

The `/api/intake` endpoint creates only `Contact` and `Case` records. There is no code path from intake → `Event` creation. Appointments create Events via a separate `POST /api/appointments` endpoint.

**Verdict: FAIL**

### 3. Tasks → Calendar Disconnected

The `Task` model has an `eventid` FK to `Event`, but no API route creates Events from Tasks. There's no calendar page that shows tasks.

**Verdict: FAIL**

### 4. No Workspace Filtering

None of the API routes filter by workspace (`ws=lexflow` or `ws=pagliano`). The models have no workspace column:
- Contact: `source` field (not ws)
- Case: `ownerid` (user FK)
- Task: `userid`, `assigned_to` (user FK)
- Event: no workspace field

The frontend JS expects `/api/workspace` to return workspace data, but the server-side data layer has no workspace model or filtering.

**Verdict: FAIL**

## Per-Workspace Status Matrix

| Feature | lexflow | pagliano |
|---|---|---|
| Intake → Contact | PASS | PASS |
| Intake → Case | PASS | PASS |
| Case → Dashboard/Kanban | PASS | PARTIAL (no ws filtering) |
| Tasks visible on Dashboard | PARTIAL | PARTIAL |
| Tasks → Calendar | FAIL | FAIL |
| File attach on /tasks | FAIL | FAIL |
| Workspace filtering | FAIL | FAIL |

## Fix Plan

1. **Priority 1:** Add `POST /api/tasks/<id>/attach` endpoint to `crm/routes/tasks.py`
2. **Priority 2:** Add `Workspace` model + `workspace_slug` FK to all data models
3. **Priority 3:** Add Task→Event creation route
4. **Priority 4:** Add `GET /api/kanban/tasks` endpoint for dashboard

## Technical Notes

Production is running an older build than local code. Several routes exist on prod (`/api/workspace`) that are not in the current local codebase. Routes that work locally (`/api/intake`) return 404 on prod. This needs a code sync before deploying fixes.

## Links
- Parent: [[LexFlow]]
- Related: [[LexFlow-Deployment-Status]]
