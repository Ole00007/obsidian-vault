# LexFlow — Master Context for Hermes Agent
> Version: Master Plan v4 Enhanced | Date: June 19, 2026 | Owner: Olesia Raising

---

## 1. PROJECT IDENTITY

**LexFlow** is a privacy-first legal SaaS for small-to-mid Italian law and audit firms.
Stack: Flask (REST API) + React (SPA) + PostgreSQL + Railway (deploy) + JWT auth.

**Live URLs:**
- Chatbot: https://lexflow-chatbot-production.up.railway.app/ ✅ LIVE
- MVP app: https://lexflow-mvp-production.up.railway.app/ ❌ BROKEN — fix first
- Web: https://lexflow-web-production.up.railway.app/ ❌ NOT RESPONDING

**Railway project:** https://railway.com/project/1fe25c7a-6a68-4c21-b27f-50c3e69daaf3

**Local working directory:** `~/Desktop/LexFlow/LexFlow Review Build`

---

## 2. WHAT IS ALREADY BUILT (DO NOT REBUILD)

### Backend — Flask REST API (`crm/`)
- App factory: `crm/__init__.py` — registers all blueprints
- Models: `contacts`, `cases`, `case_participants`, `contact_relationships`
- Models: `users` (JWT auth), `tasks` (CRUD)
- Routes: `/api/contacts`, `/api/cases`, `/api/tasks`, `/api/auth/login`, `/api/auth/me`
- Auth: Flask-JWT-Extended
- DB: PostgreSQL via Railway (`DATABASE_URL` in `.env`)
- Migrations: Flask-Migrate — `migrations/versions/` already initialised
- Committed: Phase 1 + Phase 2 done, pushed to git

### Chatbot
- Live at: https://lexflow-chatbot-production.up.railway.app/
- Routes: `/health`, `/chat`
- Status: healthy, do not touch

### DO NOT TOUCH
- `app.py` — live Railway intake app
- `migrations/` folder init — already done
- Chatbot service on Railway

---

## 3. WHAT IS BROKEN — FIX FIRST

### Railway Deploy Failure (lexflow-mvp)
Most likely causes in order:
1. App not binding to `$PORT` — fix: `app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))`
2. Wrong or missing `Procfile` — fix: `web: gunicorn "crm:create_app()" --bind 0.0.0.0:$PORT`
3. `gunicorn` missing from `requirements.txt` — add it
4. DB tables missing on Railway — run: `flask db upgrade` via Railway CLI

---

## 4. PHASE BUILD PLAN

### Phase 3 — Fix + Core Features (NEXT)
- [ ] Fix Railway deploy: Procfile + PORT + gunicorn
- [ ] Add FK: `tasks.caseid → cases.id`
- [ ] `crm/models/deadline.py` — deadlines linked to cases
- [ ] `crm/routes/deadlines.py` — CRUD `/api/deadlines`
- [ ] Verify `/api/cases` and `/api/contacts` full CRUD
- [ ] Register `deadlines_bp` in `crm/__init__.py`
- [ ] Run `flask db migrate` + `flask db upgrade`

### Phase 4 — Notifications + AI Assignment
- [ ] Email on case status change (SendGrid or SMTP)
- [ ] WhatsApp notification on intake + status change (Twilio)
- [ ] AI assigns intake request to lawyer (rule-based or LLM)
- [ ] Auto-email + WhatsApp to lawyer and client on new case

### Phase 5 — React Frontend
- [ ] Cases kanban dashboard
- [ ] Calendar view for deadlines
- [ ] Client portal — status page
- [ ] Lawyer + team dashboard

### Phase 6 — Compliance + Billing
- [ ] GDPR privacy-first: data minimisation, consent logging, right-to-erasure
- [ ] ISO 27001: audit trail on all CRM actions
- [ ] Invoice generation (Phase 3 of business plan)

---

## 5. DATA MODELS — APPROVED SCHEMA (DO NOT REDESIGN)

```
contacts         — all people AND legal entities (unified)
cases            — each case has contact_id (main client)
case_participants — secondary participants on a case
contact_relationships — person↔company, family, business role
users            — staff: lawyers, paralegals (email, password_hash, role)
tasks            — linked to cases + users (title, status, priority, duedate)
deadlines        — [TODO] linked to cases (date, type, description)
```

**Field list source:** Master Plan v4 — `~/Desktop/LexFlow/LexFlow_Master_Workflow_and_Prompts.md`
This is the single source of truth. Any conflict → Master Plan v4 wins.

---

## 6. UI/UX UPGRADE TARGETS

- Add pagination to all list endpoints: `?page=1&per_page=20`
- Add filtering: `/api/cases?status=open&lawyer_id=3`
- Add sorting: `?sort=created_at&order=desc`
- Add full-text search on contacts: `/api/contacts?q=mario`
- Add soft delete (is_deleted flag) — never hard delete CRM data (GDPR)
- Add `updated_at` trigger on all tables
- Add request logging middleware (ISO audit trail)
- Rate limiting on auth endpoints (Flask-Limiter)
- Input validation with Marshmallow or Pydantic
- Error responses: always `{"error": "...", "code": "...", "field": "..."}` format

---

## 7. RULES HERMES MUST FOLLOW

| Rule | Action |
|------|--------|
| DO NOT touch `app.py` | Live Railway intake — breaking it stops production |
| DO NOT run `flask db init` | `migrations/` already initialised |
| DO NOT modify existing migration files | Create new ones only |
| Backup before migrate | `cp -r crm/ backups/crm_backup_$(date +%Y%m%d_%H%M)` |
| One command at a time | No chaining in terminal — paste-safe |
| Label every command | 🍎 MacBook Terminal OR 🖥️ VS Code Terminal |
| One file at a time | Complete file content, no partial edits |
| Single source of truth | Master Plan v4 wins on any conflict |

---

## 8. QUICK START COMMANDS

```bash
# 🍎 MacBook Terminal — activate environment
cd ~/Desktop/LexFlow/LexFlow\ Review\ Build
source .venv/bin/activate

# 🍎 MacBook Terminal — run CRM locally
FLASK_APP=crm flask run --port 5001

# 🍎 MacBook Terminal — create new migration
FLASK_APP=crm flask db migrate -m "description"

# 🍎 MacBook Terminal — apply migration
FLASK_APP=crm flask db upgrade

# 🍎 MacBook Terminal — check DB tables
psql $DATABASE_URL -c "\dt"

# 🍎 MacBook Terminal — commit after each phase
git add crm/ requirements.txt migrations/
git commit -m "Phase X complete: description"
```

---

## 9. DETECTED ISSUES & UPDATES

### Current state updates
- `gunicorn` is missing from `requirements.txt` and must be added for Railway deploy.
- Root `Procfile` points to `app:app` and must remain untouched for intake service.
- CRM should be deployed via `crm:create_app()` in Railway config.
- `cases` table is missing from current database schema.
- Migration chain ends at `7a8b9c0d1e2f` and requires a new migration chained from that hash.
- `tasks.caseid` currently lacks a valid FK because `cases` does not exist.
- `cases.assignedto` should be linked to `users.id` via FK.
- `RESEND_API_KEY` is not wired in `crm/`; no current CRM email crash risk.
- Soft delete is not implemented yet and should be started now, not delayed to Phase 6.

### Recommended immediate changes
- Add `gunicorn` to `requirements.txt`.
- Create `crm` deployment entry separately in Railway if needed.
- Add `cases` schema migration ASAP.
- Add `is_deleted` / `deleted_at` columns to CRM tables in Phase 3.
- Add `deadlines` model, routes, and migration after schema fix.

---

## 10. METRICS & SUCCESS CRITERIA

**Phase 3 complete when:**
- CRM runs from `crm:create_app()` on Railway or local dev
- `cases`, `tasks`, `users`, `contacts`, and `deadlines` tables are present
- All list endpoints support pagination, filtering, sorting
- No hard deletes exist in CRM routes
- `app.py` remains untouched and intake service still works

---

## 11. FILE LOCATION

Saved at:
`/Users/olesiarasing/Desktop/LexFlow/LexFlow Review Build/LexFlow_Hermes_Context.md`
