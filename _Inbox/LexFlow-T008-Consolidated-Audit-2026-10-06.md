# LexFlow T-008 — Consolidated Read-Only Audit + Improvement List

**Date:** 2026-10-06 | **Agent:** backend-dev | **Kanban:** t_6cf123af
**Scope:** Part A gap register + Part B proactive improvements. Local-only, NO deploy, NO push.

## Summary
Consolidated three 2026-09-16 audits (dead-button sweep, RLS, cross-feature) + a fresh proactive pass.

## Key NEW security findings (missed by prior audits)
1. **A1 — CRITICAL:** `POST /api/auth/seed` is UNPROTECTED + destructive: wipes all Users + Workspaces (`User.query.delete()`, `Workspace.query.delete()`) and reseeds 6 known-cred accounts incl. superadmin `Test12345!`. Gate behind auth or remove. Est 0.5-1h, P0.
2. **A2 — HIGH:** `_ensure_workspace_users()`/`_ensure_test_users()` re-seed hardcoded production creds on every boot until user changes password. Force password change on first login.
3. **A3 — HIGH:** `SECRET_KEY`/`JWT_SECRET_KEY` fall back to committed dev key if Railway env missing. Verify both set.

## Other audit results
- Dead-button: login 'Entra' 415 ALREADY FIXED locally (JSON fetch, fddbb7b).
- RLS: feat/rls not merged; workspace_filter on 8 tables; gap tables contact_relationship, firm_team_member (see T-014).
- Cross-feature: intake→no CalendarEvent; task→calendar disconnected; /tasks attachment 404.
- Correction: prior 'no workspace filtering in API routes' was vs broken prod — local cases/contacts/tasks/views DO call workspace_filter().
- Prod P0-PROD-DOWN = Railway outage, not code.

## Deliverable file
Register saved at kanban workspace: `lexflow-t008-gap-register.md`; conclusions recorded in repo `docs/LexFlow_Agentic_Roadmap.json` T-008 (commit 7e4343b, local, unpushed).

[[LexFlow-MVP]] — Project root
[[LexFlow-Agentic-Roadmap]] — Canonical tracker
