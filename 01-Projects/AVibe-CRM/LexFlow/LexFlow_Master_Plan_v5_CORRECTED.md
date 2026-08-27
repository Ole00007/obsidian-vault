# LexTaskFlow / LexFlow Master Plan v5 (CORRECTED)
### Supersedes: LexTaskFlow_Master_Plan_v4_UPDATED.xlsx
### Correction date: July 20, 2026

---

## 1. What Changed From v4 → v5

| Item | v4 (old) | v5 (corrected) | Why |
|---|---|---|---|
| Route naming | Mixed Italian (`/api/attivita`, `/api/registro`) referenced in some prompts | English only: `/api/tasks`, `/api/activities`, `/api/contacts`, `/api/cases` | Matches v4's own override decision (English routes, Italian UI labels only) AND matches what is actually live on Railway |
| Phase 4 endpoints | Not present in v4 | Added: `/admin/status`, `/admin/health`, `/admin/load-demo`, Event model + CRUD, Event-Task linking, Chatbot webhook handlers | Confirmed in-progress via RAILWAY_FIX_CHECKLIST.md, July 20 2026 |
| WSGI entry point | Not documented | `wsgi.py` created, `Procfile` updated to `gunicorn wsgi:app` | Fixed live 502 deploy issue, commit `bf5fe4b`, branch `lexflow_hermes_v1` |
| Frontend integration source | Not present | `lextaskflow-e953c3e7` (Lovable/React export) approved as style+structure reference for Kanban/task UI, Supabase hooks to be stripped and replaced with Flask fetch calls | Session decision, July 20 2026 |
| Repo scope for "Project A" | Ambiguous | Explicit: `LexFlow-MVP`, `LexFlow-landing`, `LexFlow-Chatbot` — ship today, no renaming | Founder clarification |
| ContaFlow (accountancy version) | Not distinguished from Project A | Explicitly parked as "Project B" — reuse via cloning missing features from ContaFlow into LexFlow-MVP later, not rebuilding from scratch | Founder decision |
| Deploy safety rule | Not documented | One push at a time; wait for Railway Deployments tab to show green before next push | Added after Hermes flagged build-queue confusion risk |

---

## 2. Confirmed LIVE Endpoints (Railway, July 20 2026)

| Endpoint | Status | Auth |
|---|---|---|
| GET /health | ✅ Live — returns `{"status":"ok","db":"ok"}` | None |
| GET /api/contacts | ✅ Live | None (per checklist) |
| GET /api/cases | ✅ Live | None (per checklist) |
| /admin/status | ✅ Live (auth required) | X-Admin-Token |

## 3. Endpoints To Confirm / Add (Corrected English Names)

| Endpoint | Method | Purpose | Notes |
|---|---|---|---|
| /api/tasks | GET, POST | Task list/create | Was wrongly mapped to `/api/attivita` in earlier prompts — corrected |
| /api/tasks/:id | PUT, DELETE | Update/delete task | — |
| /api/activities | GET, POST | Activity log | Was wrongly mapped to `/api/registro` — corrected |
| /api/cases/:id/stage | PATCH | Stage change, auto-writes activity row | Core audit trail feature per original v4 design |
| /auth/login | POST | Hardcoded admin auth (Phase 1) | Not yet confirmed live — verify before building on top of it |

## 4. Database Schema (Unchanged From v4 — Confirmed Live)

Live Railway Postgres tables confirmed July 20 2026:
`alembic_version, attivita, cases, clienti, contacts, pratiche, registro, tasks, users`

Note: both old Italian tables (`attivita`, `clienti`, `pratiche`, `registro`) and new English tables (`tasks`, `contacts`, `cases`) currently coexist in the live database. This is a known transitional state from the v4 migration — do not delete either set without explicit verification of which one the live API code actually reads from.

## 5. Repo Map (Corrected, July 20 2026)

| Repo | Role | Status |
|---|---|---|
| LexFlow-MVP | Core backend + app (Flask, Railway) | Live, ship today, Project A |
| LexFlow-landing | Static landing page (Netlify) | Live, Project A, do not touch during this work |
| LexFlow-Chatbot | Alessia chatbot backend | Live, Project A, do not touch during this work |
| lextaskflow-e953c3e7 | Lovable/React Kanban export | Reference only for now — style/structure source, Supabase hooks to be stripped, fetch-to-Flask rewire approved, can go to production once complete |
| lexflow-crm | Original CRM backend repo (pre-rename discussions) | To become "ContaFlow" — Project B, parked |
| LexBillFlow | Visual pipeline/deal tracker (Lovable template) | Reference only, not active |

## 6. Supabase Status (Confirmed)

No Supabase project, package, or environment variable exists in LexFlow-MVP, on Railway, or locally, confirmed via live Postgres table inspection July 20 2026. Supabase hooks exist ONLY inside the disconnected `lextaskflow-e953c3e7` frontend code and must be stripped, not reconnected, during integration.

## 7. Deploy Safety Rule (New in v5)

Push one commit at a time. After each push, confirm Railway's Deployments tab shows a fully green/healthy status before making the next push. Do not queue multiple pushes in quick succession — this caused build-queue confusion previously (see RAILWAY_FIX_CHECKLIST.md).

## 8. Open Action Items

1. Confirm whether live API code reads from Italian tables (`attivita`, `clienti`) or English tables (`tasks`, `contacts`) — resolve before adding new endpoints.
2. Verify `/auth/login` is actually live before building dependent features.
3. Complete Phase 4 backend work (Event model, webhooks, admin endpoints) before final production merge of reworked lextaskflow-e953c3e7 frontend.
4. Wire lextaskflow-e953c3e7 to LexFlow-MVP in an isolated branch NOW (parallel work), merge to production only after Phase 4 is confirmed stable — not fully deferred, not immediately risky.
5. When ContaFlow (Project B) resumes: identify and clone missing features into LexFlow-MVP structure rather than rebuilding from scratch.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Dev-Handoff]]
