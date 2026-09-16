# RLS Hardening — Audit Findings (t_4637a500)

**Date:** 2026-09-16  
**Task:** [t_4637a500](https://linear.app) — LexFlow CRM RLS hardening: confirm build status + close the ticket  
**Status:** Audit complete, delegation ticket drafted, awaiting Ole's go-ahead on filing

---

## RLS Build Status

**RLS IS BUILT** on `feat/rls` branch — **NOT MERGED** into main.

- Migration: `f3a4b5c6d7e8_rls.py` (11 tables)
- Tests: `tests/test_rls.py` (18 tests — 2 RLS-enabled, 11 read-blocked, 3 write-blocked, 2 intra-tenant)
- Depends on: `flask-rls` library + manual `NOBYPASSRLS` step
- Branch: `feat/rls` (git worktree at `~/Desktop/projects/services/LEGAL/lexflow-rls`)

Current isolation on main: app-level `workspace_filter()` on 8 tables only. No database-level enforcement.

---

## Tables Filtered by `workspace_filter()` (8)

1. `deadlines` — deadlines.py
2. `contacts` — contacts.py
3. `tasks` — tasks.py
4. `cases` — cases.py, roadmap.py
5. `activity_log` — activity.py
6. `notes` — notes.py
7. `attachments` — attachments.py
8. `calendar_events` — calendar.py

## Tables with `workspace_id` but NOT filtered

| Table | RLS covered? | Notes |
|-------|-------------|-------|
| `views` | ✅ TenantPolicy | Added by RLS migration |
| `events` | ✅ TenantPolicy | Added by RLS migration |
| `notifications` | ✅ ExpressionPolicy | NULL rows allowed |
| `contact_relationship` | ❌ GAP | Has workspace_id, not in migration |
| `firm_team_member` | ❌ GAP | Has workspace_id, not in migration |
| `user` | ❌ N/A | Single workspace per user |
| `workspace` | ❌ N/A | The hierarchy itself |

**Total data tables with workspace_id: 10**  
**Covered by workspace_filter(): 8**  
**Covered by RLS: 11 (8 + views + events + notifications)**  
**GAP: 2 tables — `contact_relationship`, `firm_team_member`**

---

## Alembic RLS Compatibility Risks

1. **Custom Alembic methods** — `op.enable_rls()`, `op.force_rls()`, `op.create_policy()` come from `flask_rls` and must be registered in `environment.py`. Risk: migration fails if operations not registered.
2. **Downgrade symmetry** — `op.no_force_rls()` is non-standard. Downgrade crashes if `flask_rls` missing.
3. **NOBYPASSRLS prerequisite** — Manual `ALTER ROLE ... NOBYPASSRLS` must run BEFORE migration. If app connects as table owner, RLS silently bypassed.
4. **Notifications ExpressionPolicy** — `workspace_id IS NULL` clause allows system notifications to be visible to all tenants. `user_to` should ideally be workspace-scoped too.
5. **`flask-rls` dependency** — Must be in `requirements.txt` before migration runs.

---

## Draft Delegation Ticket

Full ticket text at: `~/.hermes/kanban/workspaces/t_4637a500/findings_and_delegation_ticket.md`

**Scope:** Enable RLS on 11 tables + 2 gap tables. Merge gate: 18 tests pass on Postgres with NOBYPASSRLS.  
**Budget:** 1–2 days implementation + 0.5 days test suite  
**Out of scope:** schema-per-tenant, DB-per-customer, RBAC-within-tenant

---

## Links

- [[LexFlow-MVP]] — LexFlow multi-tenant CRM codebase
- [[Multi-Tenancy Plan]] — Phases 2-4 design document
- [[Safety Assessment]] — Safe vs unsafe actions matrix
- [[RLS Architecture Roadmap]] — Current architecture diagram and gap analysis
