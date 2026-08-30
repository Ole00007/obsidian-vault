---
title: LexFlow — Multi-tenant test setup (Pagliano + Romanelli + Gmail login)
created: 2026-08-29
updated: 2026-08-29
tags: [lexflow, crm, multitenant, test, pagliano]
status: READY FOR TESTING ✅
---

# LexFlow — Multi-tenant test setup (Pagliano + Romanelli + Gmail login)

## Goal (Ole, 2026-08-29 night)
Verify the CRM is REALLY multi-tenant: entering from different landing pages / websites of different customers feeds each into its **own isolated workspace** in the shared Postgres. Test with: (a) own Gmail login, (b) Pagliano LP button, (c) Romanelli studio LP.

## What was wrong (root cause — wiring, not credentials)
- Pagliano LP on Netlify (`verdant-crumble-021449`) pointed to the **legacy** Railway app `web-production-ab54f.up.railway.app` (old LexFlow-MVP backend) for both the **Login button** and the **intake fetch**. That's why Ole could not log in.
- The correct multi-tenant CRM is `web-production-031a6.up.railway.app` (project `perceptive-achievement`, branch `lexflow_hermes_v1`) — 5 workspaces.
- Also: test user `olesya00007@gmail.com` did NOT exist on the CRM yet (401).

## Fixes applied (all deployed)
1. **Pagliano LP source** (`~/Desktop/projects/services/LEGAL/LexFlow-MVP/pagliano/`):
   - `index.html` + `templates/pagliano.html`: Login button → `web-production-031a6.up.railway.app/kanban`; intake fetch → `/api/intake/pagliano` (multi-tenant slug)
   - `static/chat-widget.js`: intake fetch → `/api/intake/pagliano` (payload matches CRM). NOTE: `/api/appointments` still points to ab54f (legacy) — CRM has no such endpoint yet; follow-up.
2. **Netlify**: deployed `pagliano/` dir to site `verdant-crumble-021449` (site b060d5c1...) — verified live: 031a6 present, ab54f gone.
3. **CRM seed** (`crm/__init__.py`): added `_ensure_test_users()` — idempotently creates `olesya00007@gmail.com` / `Test1` (superadmin) on every boot.
4. **CORS** (`crm/config.py`): default `CORS_ORIGINS` now includes Netlify LP origins (`verdant-crumble-021449`, `poetic-kleicha-28d058`) so LPs can POST intake cross-origin.

## Deployed
- `lexflow-crm` → commit `7f95396` → Railway `web-production-031a6` (deployment 3bfdd676), prod health `db:ok`.
- `LexFlow-MVP` → commit `66e57a9` (pagliano LP files only) → Netlify.

## Production E2E verification (2026-08-29 23:5x)
- Login as `olesya00007@gmail.com` / `Test1` → 200 (token issued) ✅
- POST `/api/intake/pagliano` → case id 5 → **workspace_id 9** ✅
- POST `/api/intake/romanelli-studio` → case id 6/7 → **workspace_id 10** ✅ (DIFFERENT from pagliano — isolation proven)
- Workspaces confirmed present in prod Postgres (pagliano, romanelli-studio, etc.)

## Romanelli LP
- Cloudflare Worker site (`romanelli-studio`, wrangler.toml) — SEO/portfolio page; its CRM button already points to `web-production-031a6.up.railway.app`. No intake form on that LP (it links into the CRM instead). Workspace `romanelli-studio` accepts intake via `/api/intake/romanelli-studio`.

## Test creds (prod)
- `olesya00007@gmail.com` / `Test1` (superadmin — sees all workspaces)
- Also `olesya00007@yahoo.com` / `Test12345!` (existing superadmin)

## Kanban verified live (2026-08-30, on our own tasks)
- **Bug fixed:** `GET /api/cases` ignored `?status=` param → every kanban column showed the same cards/counts. Now filters by status (commit 2ee8349).
- **Verified in prod:** INTAKE only has its own cards (11), REVIEW shows moved card, other columns correctly empty.
- **"+ Add Task" button works** (not a mockup): created a real case through the UI (INTAKE 11→12).
- **Column move works:** PUT /api/cases/<id> {status} (same call the drag-drop uses) moved a card INTAKE→REVIEW, counts updated.
- Board populated with our **own roadmap** as real cards (LexFlow Ops contact id 8): Surgical #1 & #4 (High, due 09-01), Multi-tenant tests (QA), appointments endpoint + kanban fix (Done).

## Open follow-ups
- [x] ~~Chat-widget `/api/appointments` still → legacy ab54f~~ — **BUILT** `/api/appointments` on CRM (2026-08-30): public endpoint, creates Contact+Case+CalendarEvent in pagliano workspace, logs activity, sends booking notifications. Chat-widget repointed → `web-production-031a6.up.railway.app/api/appointments` (commit f8d11db) + Netlify redeploy (e558028).
- [x] ~~Superadmin visibility~~ — fixed: read routes now use `workspace_filter()` so superadmin sees all workspaces (commit c36cae9). Verified: superadmin sees ws9+ws10; pagliano admin only ws2; romanelli only ws3.
- [ ] Main landing `poetic-kleicha-28d058.netlify.app` still points at ab54f (9 refs) — not part of this test; fix when the main landing is adopted.
- [ ] Test user is superadmin (sees all); to demo per-client isolation login as the workspace admin users (e.g. `pagliano@lexflow.test`) once seeded.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Surgical-Additions-2-3]]
