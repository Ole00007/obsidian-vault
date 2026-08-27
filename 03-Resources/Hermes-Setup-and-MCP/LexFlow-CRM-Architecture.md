# LexFlow CRM — Architecture Overview

> **Version:** 1.0 (Aug 2026)  
> **Workspace:** `~/Desktop/LexFlow/lexflow-crm-build/`  
> **Branch:** `lexflow_hermes_v1`  
> **Local:** `http://localhost:5002`  
> **XLSX:** `03-Resources/Hermes-Setup-and-MCP/LexFlow_Architecture.xlsx`

## Stack

| Layer | Tech |
|-------|------|
| Backend | Flask 2.3 + SQLAlchemy 2.0 |
| Frontend | Jinja2 templates, Vanilla JS |
| Database | SQLite (local) / PostgreSQL (Railway) |
| Auth | JWT (24h, Flask-JWT-Extended) |
| Migrations | Alembic (5 migration levels) |
| Email | Resend API (free: 100/day) |
| WhatsApp | UltraMsg API (free: 100/day) |

## Project Structure

```
lexflow-crm-build/
├── crm/                    # Main application
│   ├── __init__.py         # App factory, registers all blueprints
│   ├── config.py           # Configuration (DB, JWT, CORS)
│   ├── extensions.py       # SQLAlchemy, Migrate, JWT, CORS, Limiter
│   ├── workspace.py        # Multi-tenant middleware (workspace filtering)
│   ├── activity_logger.py  # Auto-timeline logging helper
│   ├── notification_service.py  # Email (Resend) + WA (UltraMsg)
│   ├── validators.py       # Input validation functions
│   ├── models/             # 9 SQLAlchemy models
│   ├── routes/             # 12 API + view blueprints
│   └── clients/            # External integrations (chatbot)
├── migrations/             # 5 Alembic migrations
├── templates/              # 8 Jinja2 templates
├── static/                 # Static assets (dashboard HTML)
├── wsgi.py                 # Entry point for Railway/gunicorn
├── Procfile.crm            # Gunicorn config
└── requirements.txt        # Dependencies
```

## Multi-Tenant Workspaces

| # | Slug | Name | Login |
|---|------|------|-------|
| 1 | `avibeagency` | AVIBE Agency | avibe@lexflow.test / Avibe@12345 |
| 2 | `pagliano` | Avvocato Pagliano | pagliano@lexflow.test / Pag@12345 |
| 3 | `romanelli-studio` | Studio Romanelli | romanelli@lexflow.test / Rom@12345 |
| 4 | `romanelli-audit` | Romanelli Audit | audit@lexflow.test / Audit@12345 |
| 5 | `tommasoferro` | Avv. Tommaso Ferro | ferro@lexflow.test / Ferro@12345 |
| — | — | **Superadmin** | olesya00007a@yahoo.com / Test12345! |

Each workspace user sees ONLY their own data. Superadmin sees all.

## Frontend Pages

| Route | Page | Type | Auth |
|-------|------|------|------|
| `/` | Intake form | Public | No |
| `/dashboard` | Stats + activity | Internal | Optional |
| `/kanban` | Case pipeline board | Internal | Optional |
| `/calendar` | Hearing/deadline calendar | Internal | Optional |
| `/book` | Booking form | Public | No |
| `/admin` | Case list | Internal | Optional |
| `/admin/matter/:id` | Case detail + timeline | Internal | Optional |
| `/status/:token` | Client tracking | Public | No |

## API Endpoints (42 routes)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/login` | No | Login → JWT |
| GET | `/api/auth/me` | JWT | Current user |
| GET | `/api/contacts` | No | List contacts |
| GET | `/api/contacts/:id` | No | Get contact |
| POST | `/api/contacts` | JWT | Create contact |
| PUT | `/api/contacts/:id` | JWT | Update contact |
| DELETE | `/api/contacts/:id` | JWT | Soft-delete |
| GET | `/api/cases` | No | List cases |
| GET | `/api/cases/:id` | No | Get case |
| POST | `/api/cases` | JWT | Create case |
| PUT | `/api/cases/:id` | JWT | Update case |
| DELETE | `/api/cases/:id` | JWT | Soft-delete |
| GET | `/api/tasks` | JWT | List tasks |
| GET | `/api/tasks/:id` | JWT | Get task |
| POST | `/api/tasks` | JWT | Create task |
| PUT/PATCH | `/api/tasks/:id` | JWT | Update task |
| DELETE | `/api/tasks/:id` | JWT | Delete task |
| GET | `/api/calendar` | JWT | List events |
| GET | `/api/calendar/:id` | JWT | Get event |
| POST | `/api/calendar` | JWT | Create event |
| PUT | `/api/calendar/:id` | JWT | Update event |
| DELETE | `/api/calendar/:id` | JWT | Soft-delete |
| GET | `/api/notes` | JWT | List notes |
| POST | `/api/notes` | JWT | Create note |
| PUT | `/api/notes/:id` | JWT | Update note |
| DELETE | `/api/notes/:id` | JWT | Delete note |
| GET | `/api/activity` | No | Timeline |
| GET/POST/PUT/DELETE | `/api/deadlines` | JWT | Deadline CRUD |
| GET | `/api/admin/health` | No | Admin health |
| GET | `/api/admin/stats` | JWT | System stats |
| GET | `/api/admin/users` | JWT | List users |
| PUT | `/api/admin/users/:id/role` | JWT | Update role |
| DELETE | `/api/admin/users/:id` | JWT | Delete user |
| POST | `/api/webhooks/chatbot/message` | No | Chatbot webhook |

## Database Models (9 tables)

```
Workspaces ──┬── Users ── (workspace_id)
             ├── Contacts
             ├── Cases ───┬── Tasks
             │             ├── Deadlines
             │             └── CalendarEvents
             ├── Notes (polymorphic: case/contact/task)
             ├── ActivityLog (auto-logged timeline)
             ├── Events (chatbot/webhooks)
             └── ContactRelationships
```

## Security

- JWT with 24h expiry, workspace_id embedded
- Input validation on all write endpoints
- Rate limiting: 10/min auth, 60/min read, 30/min write
- Security headers: HSTS, CSP, X-Frame-Options, X-Content-Type-Options
- Soft delete on all tables (never lose data)
- CORS whitelist for frontend domain
- Multi-tenant: every query auto-filtered by workspace_id

## Notification Flow

```
Client fills booking form
  → CalendarEvent created in DB
  → Email via Resend to client (confirmation)
  → Email via Resend to workspace owner (notification)
  → WhatsApp via UltraMsg to client (if phone provided)
  → WhatsApp via UltraMsg to owner (if ULTRAMSG env set)
```

All notifications gracefully skip if API keys not set.

## Deployment (Railway)

Required env vars:

```
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=...
RESEND_API_KEY=...
EMAIL_FROM=onboarding@resend.dev
ADMIN_EMAIL=...
ULTRAMSG_INSTANCE_ID=...  (optional)
ULTRAMSG_TOKEN=...         (optional)
ADMIN_PHONE=...            (optional, for WhatsApp)
```

## Agentic Roster

This note is indexed by Hindsight (`avibe-hq` bank) and Hermes session search. Any Hermes agent working on LexFlow can reference this architecture by searching for "LexFlow CRM Architecture" or by loading this file from the Obsidian vault.