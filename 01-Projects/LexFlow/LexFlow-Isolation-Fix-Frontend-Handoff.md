---
title: LexFlow — Workspace isolation fix + frontend upgrade handoff (2026-08-30)
created: 2026-08-30
updated: 2026-08-30
tags: [lexflow, security, isolation, frontend, handoff]
status: PARTIAL ✅/🔄
---

# LexFlow — Workspace isolation fix + frontend upgrade handoff

## ✅ CRITICAL: Workspace isolation — it IS working (accounts verified separate)
Prod verification (2026-08-30):
- `olesya00007@yahoo.com` → **superadmin**, workspace `lexflow` (id 7)
- `olesya00007@google.com` → **admin**, workspace `romanelli-studio` (id 10)

**Separate Postgres NOT needed.** Two issues caused the "see superadmin" symptom:

1. **Security bug FIXED** (commit `9af8cdc`): `get_visible_workspace_ids()` returned `None` for unauthenticated requests → dashboard treated it as "superadmin sees all" → anonymous page loads rendered EVERY workspace's data. Now returns `[]` (see nothing) for unknown/anon; only a genuine superadmin gets `None` (all). Dashboard passes `current_user` explicitly.
2. **Stale-token trap:** the browser still held the superadmin JWT (from earlier testing) in localStorage, so kanban auto-authenticated as superadmin. Fix on user side: **Log out** (clears localStorage) then log in as Romanelli `olesya00007@google.com` / `Romanelli0826`.

## ✅ /admin/panel "Missing Authorization Header" FIXED (commit `44c692f`)
Route was `@jwt_required()` (header auth) but JWT lives in localStorage. Now `@jwt_required(optional=True)` + client-side verification via `GET /api/admin/workspaces`; redirects non-superadmins home. Deployed.

## 🔄 Frontend upgrade — handed to existing `frontend-developer-lovable_react` profile
- Brief written: `references/lexflow-crm-frontend-brief.md` (base = aLexy LP coruscating-pegasus, style = romanelli-studio.olesya00007.workers.dev, full endpoint map, all templates listed).
- Profile SOUL.md + MEMORY.md re-pointed to LexFlow CRM upgrade.
- **Calendar** flagged as weak spot → build a proper month grid.
- frontend agent edits templates locally on `lexflow_hermes_v1`; operator-installer verifies + deploys.

## Deploys this session
`9af8cdc` (isolation), `44c692f` (admin panel) — Railway `d6232b83` Online, db:ok.

## Open
- [ ] frontend upgrade completion → verify in local server → deploy
- [ ] uploads/ persistence decision (B / Hetzner) — kanban Waiting Docs
- [ ] Sept 10-11: planning topics + Surgical #1/#4

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Workspace-UX-Overhaul]], [[LexFlow-Romanelli-Sub-Workspaces]]
