# LexFlow — Agent Context File

## Product

LexFlow is a privacy-first legal intake and workflow suite for small-to-mid-sized Italian law firms (avvocati). It is a vertical micro-SaaS — **not a chatbot only**. It covers: matter intake, CRM, task management, document collection, status notifications, and admin pipeline in one Flask application. It does not give legal advice or AI-generated legal conclusions.

**One-line purpose:** Clients submit legal matters privately, attach documents, and receive a personal tracking link. Workflow-only — intake to closure.

**Target market:** Small to mid-sized legal studios in Italy. Helps advocates manage their daily routine: client intake, case pipeline, document collection, task assignment, and client-facing status updates.

## Modules

| Module | Description |
|---|---|
| Intake | Matter submission form, document upload, unique tracking token per matter |
| Status Portal | Client-facing status page via tracking link |
| CRM | Case management dashboard (contacts, cases, pipeline, notes) |
| Task Manager | Action items per matter, assignable, with deadlines |
| Document Tracker | Required vs received docs, status per document |
| Notifications | Email via Resend when matter status changes |
| Admin | Internal Kanban-style matter pipeline for law firm |
| Chatbot (Alessia) | AI intake assistant via OpenRouter — collects intake data conversationally, routes to practice area, marks urgency. NOT a legal advisor. |
| LexBillFlow | Visual CRM & pipeline tracker — drag-and-drop pipeline, deal cards with metrics (to build) |

## Stack

- **Backend:** Python 3.11 / Flask 3.x / Flask-SQLAlchemy / Flask-Migrate / Alembic / Gunicorn
- **Database:** SQLite (local dev) / PostgreSQL via psycopg2-binary (Railway prod)
- **Email:** Resend API
- **Frontend (Flask):** Jinja2 / HTML5 / CSS3 / vanilla JS
- **Frontend (React):** TypeScript/React components generated in Lovable.dev (lovable.dev), GitHub-synced — used for CRM frontend and dashboard UI
- **API layer:** Node.js/Express TypeScript in `apps/api/src/` (index.ts, config.ts, db.ts, routes/)
- **Deploy:** Railway (backend, auto-deploy from GitHub main) / Netlify (landing + static)
- **AI/LLM:** OpenRouter API (Alessia chatbot, model: meta-llama/llama-3.3-70b-instruct)
- **Dev tools:** Lovable.dev (UI generation + GitHub sync), VS Code, Git CLI, ripgrep, SQLite3 CLI, pytest, curl, pipreqs

## Repositories

| Repo | URL | Status | Notes |
|---|---|---|---|
| LexFlow-MVP | github.com/Ole00007/LexFlow-MVP | Active — core app | Currently broken on Railway (see Known Issues) |
| LexFlow-Chatbot | github.com/Ole00007/LexFlow-Chatbot | Active — chatbot | Deploys fine; CORS set to Netlify frontend |
| LexFlow-landing | github.com/Ole00007/LexFlow-landing | Active — static landing | Netlify deploy |
| LexBillFlow | github.com/Ole00007/LexBillFlow | Empty — billing module | To be built; visual CRM + drag-and-drop pipeline |
| LexTaskFlow | Lovable.dev project | CRM React frontend | Not yet pushed to GitHub — connect Lovable → GitHub to sync |

## Key File Paths — LexFlow-MVP

```
app.py                         # Main Flask app, all intake/admin/status routes, SQLite helpers
Procfile                       # web: gunicorn app:app
requirements.txt               # All Python deps (NOTE: resend missing — see Known Issues)
.env.example                   # Env var template (never commit .env)
templates/admin.html           # Admin matter list view
templates/admin_matter.html    # Admin single matter detail + status update
templates/index.html           # Client intake form
templates/status.html          # Client-facing status portal
templates/base.html            # Base layout template
crm/__init__.py                # CRM Flask factory (create_app) — SEPARATE from app.py
crm/config.py                  # CRM config — reads DATABASE_URL
crm/extensions.py              # SQLAlchemy + Migrate instances
crm/models/contact.py          # Contact model (id, ownerid, fullname, email, phone, company, status, notes)
crm/models/case.py             # Case model (id, contactid, ownerid, title, casetype, status, priority, dates)
crm/routes/contacts.py         # Contacts blueprint
crm/routes/cases.py            # Cases blueprint
crm/routes/health.py           # Health check blueprint — GET /health
run_crm.py                     # CRM entry point — DO NOT mix with app.py
apps/api/src/index.ts          # TypeScript/Express API server
apps/api/src/config.ts         # API config
apps/api/src/db.ts             # DB connection
apps/api/src/routes/           # Express route files
data/app.db                    # SQLite DB — local only, NEVER commit
uploads/                       # Document uploads — NEVER commit
migrations/                    # Alembic migration files
Field-Decision-Reason_CRM table fields.csv   # Approved/rejected CRM contact fields
Field-Decision-Reason_cases table.csv        # Approved/rejected cases fields
```

## Key File Paths — LexFlow-Chatbot

```
server.py          # Flask app, OpenRouter integration, Alessia system prompt, CORS
Procfile           # web: gunicorn server:app --bind 0.0.0.0:$PORT
requirements.txt   # flask, flask-cors, requests, gunicorn, python-dotenv
chatbot UI/        # Frontend files (connected to Netlify)
.env.example       # Env var template
```

## Procfile Rules

- LexFlow-MVP: `web: gunicorn app:app`
- LexFlow-Chatbot: `web: gunicorn server:app --bind 0.0.0.0:$PORT`
- Missing Procfile = silent Railway deploy failure. Always verify before push.

## Environment Variables (never commit to GitHub)

**LexFlow-MVP:** RESEND_API_KEY, ADMIN_EMAIL, EMAIL_FROM, EMAIL_FROM_NAME, RAILWAY_PUBLIC_DOMAIN, WEBHOOK_SECRET
**LexFlow-Chatbot:** OPENROUTER_API_KEY, OPENROUTER_MODEL, SITE_URL, SITE_NAME
**CRM (run_crm.py):** DATABASE_URL (PostgreSQL connection string)

## Architecture Warning — Two Apps in One Repo

LexFlow-MVP contains **two separate Flask apps** that must NOT be mixed:

| App | Entry | DB | Note |
|---|---|---|---|
| `app.py` | `gunicorn app:app` | SQLite | Intake, admin, status portal |
| `crm/__init__.py` | `gunicorn run_crm:app` | PostgreSQL | CRM API (blueprints) |

`run_crm.py` explicitly states: **DO NOT use app.py for CRM work.**
The Procfile currently points to `app.py` only. CRM runs as a separate process or must be integrated via conditional blueprint registration.

## Known Issues — Current Railway Outage (as of 2026-06-18)

**app.py has 3 bugs preventing Railway boot:**

1. `load_demo` route defined **twice** → Flask AssertionError on startup
2. `resend` package missing from `requirements.txt` → ImportError on startup
3. `# PASTE CRM BLOCK HERE` comment + duplicate `if __name__ == "__main__"` block → unfinished edit committed to main

**Fix:** Add `resend==2.4.0` to requirements.txt, remove duplicate route and duplicate `__main__` block, remove placeholder comment, push to main.

## Approved CRM Schema (from field decision CSVs)

**contacts table:** id, ownerid, fullname, email, phone, company, status, notes, entitytype, isactive, relationshipcapturestatus, createdat, updatedat
**cases table:** id, contactid, ownerid, title, casetype, status, priority, openedat, duedate, assignedto, createdat, updatedat
**case_participants:** id, caseid, contactid, roleincase, isprimary, side, representationstatus, notes, createdat, updatedat

## Matter Status Flow

New intake → Conflict check → Lawyer review → Waiting client docs → Quoted → Engaged → Closed

## Lovable.dev Integration

- Platform: **lovable.dev** (not lovable.ai)
- Generates React/TypeScript frontend components and full UI screens
- Syncs directly to GitHub via built-in GitHub integration
- Used for: CRM frontend, dashboards, LexBillFlow UI
- LexTaskFlow Lovable project not yet pushed to GitHub — go to Lovable → project → Settings → GitHub → connect repo to sync
- Standalone React apps deploy to Netlify; components integrated into Flask via static build or API layer

## Agent Roster (Hermes)

| Agent | Role |
|---|---|
| Atlas | Orchestrator / Chief of Staff — decomposes tasks, delegates |
| Research Scout | Research, web search, source validation |
| Content Operator | Writing, briefs, client-facing copy |
| Build Architect | Coding, file diffs, repo tasks, deploys — primary agent for this repo |
| QA Auditor | Review, testing, error catching |
| Automation Steward | n8n workflows, crons, integrations |
| Perplexity | Research & planning lead — architecture decisions, ready-to-paste prompts |
| LexFlow Code Reviewer | Sub-agent of Build Architect — audits existing code, maps what is complete vs missing |
| Deploy Guard | Sub-agent of QA Auditor — checks Railway deploy status, runs smoke tests |

## Tracking Protocol

After every completed step:
- **Notion:** Concise 3–5 line protocol entry (what was done, result, next step). For collaborators and first test customers.
- **Hermes Kanban:** Update task card In Progress → Done. For: owner (Olesia), QA/Test Manager agent, Supervisor (signs off before sending to test customer).

## Coding Conventions

- Python: PEP8, type hints where practical
- Flask: blueprints per module (crm, intake, admin, docs)
- SQL: SQLAlchemy ORM preferred; raw sqlite3 for legacy helpers in app.py
- Migrations: always Alembic, never alter DB directly in prod
- Templates: Jinja2; Italian for client-facing strings, English for admin UI and all code
- JS: vanilla ES6+; React/TypeScript only for Lovable-generated components
- Commits: `[module] short description — what changed`

## Deploy Rules

1. Test locally: `gunicorn app:app --bind 0.0.0.0:5000`
2. Run tests if present: `pytest`
3. Push to main → Railway auto-deploys
4. Check Railway deploy logs after every push
5. Never push .env, data/app.db, uploads/, .venv/

## Deadline: 23 June 2026

## Links
- Parent: [[LexFlow_Hermes_Kit_v2-INDEX]]
- Related: [[SKILL_lexflow-deploy]]
