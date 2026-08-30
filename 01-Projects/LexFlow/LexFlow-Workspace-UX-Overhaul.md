---
title: LexFlow — Workspace UX overhaul + account roster (2026-08-30)
created: 2026-08-30
updated: 2026-08-30
tags: [lexflow, ux, credentials, superadmin, kanban, vault-sync]
status: DEPLOYED ✅
---

# LexFlow — Workspace UX overhaul + account roster (2026-08-30)

## What was built & deployed (commit `b1fae8c`, Railway auto-deploy, prod `db:ok`)

### 1. Full workspace account roster (idempotent, `_ensure_workspace_users`)
| Login | Password | Role | Workspace |
|---|---|---|---|
| superadmin@lexflow.it | lexflow0826 | superadmin | lexflow |
| olesya00007@yahoo.com | crm0826 | superadmin | lexflow |
| alegra_007@proton.me | avibe0826 | admin | avibeagency |
| ms.okuneva@internet.ru | pagliano0826 | admin | pagliano |
| olesya00007@google.com | Romanelli0826 | admin | romanelli-studio |
| ferro@lexflow.it | ferro0826 | admin | tommasoferro |

Rule: passwords are reset ONLY when still at a known default (never overwrite a user's changed creds). Prod verified: all 5 new logins 200; superadmin sees 6 workspaces; pagliano admin scoped to pagliano.

### 2. Change-credentials feature
- `POST /api/auth/change-credentials` — change password and/or email (requires current password).
- Sends email notifications to old + new address + password-changed notice.
- UI at `/settings` (Settings in nav).

### 3. Super Admin panel (superadmin only)
- `/admin/panel` page + `GET /api/admin/workspaces` (all ws + emails/roles, never hashes) + `POST /api/admin/reset-password` (emails the reset user).
- Non-superadmin redirected away / 403 — verified.

### 4. Shared nav + workspace badge (all base.html pages)
- Workspace badge (e.g. 🏢 Avvocato Pagliano) from user.workspace.name.
- Active-nav highlighting, Settings + Logout links, 🛡 Super Admin link (superadmin only), ← Return to main website (per-workspace site map).
- kanban.html got the same shared nav + ws chip + return-to-site; init now loads `/api/auth/me` so reloads show real user.

### 5. Kanban expanded to 8 statuses
`Intake → Conflict Check → Review → In Progress → Waiting Docs → To Verify → Engaged → Closed`
(existing cards keep old statuses; filter works per-column).

### 6. LP login → CRM root home
- Pagliano LP Login button → `/` (root). `/` redirects logged-in users to their workspace dashboard. Isolation: each client sees only their own sector; no cross-client data visible to non-superadmins.

## Repo ↔ Vault sync gap (FOUND + FIXED)
- Compared `~/Desktop/projects/services/LEGAL/lexflow-crm` (1,934 tracked files, ~26 docs) vs Obsidian `01-Projects/LexFlow/_from-repos/LexFlow-CRM/` (1 stale file) vs project folder.
- Root cause: `repo_sync.py` (memory-curator nightly) ROOTS did NOT include `lexflow-crm`.
- Fix: wired `~/Desktop/projects/services/LEGAL/lexflow-crm` → `01-Projects/LexFlow/_from-repos/LexFlow-CRM` (docs only, hash-compared, safe). Dry-run confirms NEW files detected.

## Open / next
- [ ] uploads/ persistence: on Railway, `web` service has NO persistent volume — uploads live on ephemeral disk, wiped on redeploy (DB rows persist, files don't). Fix options: Railway volume mounted at `uploads/` OR object storage (S3/R2). Awaiting Ole's approval (needs redeploy).
- [ ] Romanelli sub-workspaces (3 client sub-spaces inside romanelli-studio) — approach proposed in chat.
- [ ] Per-customer + per-client Hindsight memory banks (future).
- [ ] Sept 10: Surgical #1 (Person+Company split) + #4 (RBAC).

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-MultiTenant-Test-Setup]]
