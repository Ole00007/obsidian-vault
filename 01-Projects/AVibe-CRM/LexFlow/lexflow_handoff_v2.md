# LexFlow — Full Project Handoff Document v2
**Date:** June 21, 2026  
**Status:** Backend live. Frontend partially live. Reconnection in progress.

---

## Live URLs

| Component | URL | Status |
|---|---|---|
| Main backend (new) | https://lexflow-mvp-production.up.railway.app | Live |
| Admin panel (new) | https://lexflow-mvp-production.up.railway.app/admin | Live |
| Landing page (Netlify) | https://poetic-kleicha-28d058.netlify.app | Live |
| Old backend (pre-migration) | https://web-production-031a6.up.railway.app | Broken after migration |
| GitHub repo | https://github.com/Ole00007/lexflow-crm | Active |
| Lovable CRM sketch | https://lovable.dev/projects/544fbbf8-4475-4cb9-81e3-ab9d6651193b | Unconnected |

---

## Local Project Path
/Users/olesiarasing/Desktop/LexFlow/LexFlow Review Build

---

## Tech Stack (confirmed)

### Backend
| Tool | Version | Role |
|---|---|---|
| Python | 3.13.13 | Runtime |
| Flask | 2.3.3 | Web framework |
| Flask-JWT-Extended | 4.4.4 | Login tokens |
| Flask-SQLAlchemy | 3.1.1 | Database ORM layer |
| Flask-Migrate + Alembic | 4.1.0 / 1.18.4 | DB migrations (caused prior crash) |
| Flask-CORS | 6.0.2 | Allows Netlify frontend to call Railway API |
| Gunicorn | 21.2.0 | Production web server |
| Resend | 2.0.0 | Email sending |
| python-dotenv | 1.2.2 | Load environment variables |

### Database
| Tool | Role |
|---|---|
| PostgreSQL (Railway) | Main database |
| psycopg2-binary 2.9.12 | Python connector |
| SQLAlchemy 2.0.50 | ORM layer - sufficient for full CRM |

Is SQLAlchemy enough for a CRM?
YES - handles clients, cases, relationships, filters, status workflows
MISSING: Calendar needs FullCalendar.js (frontend) + events table (backend)
MISSING: File storage needs object storage (Railway volume or S3)

### Chatbot Backend
| Component | Tool | Status |
|---|---|---|
| Routing + guardrails | server.py on Railway | Active |
| AI model | Llama 3.3 70B Instruct :free via OpenRouter | Active |
| System prompt | LexFlow legal intake persona | Done |

Chatbot flow:
  User browser
    -> Netlify (Alessia chatbot bubble)
    -> Railway server.py (guardrails)
    -> OpenRouter / Llama 3.3 70B free
    <- Response back through same chain

### Frontend

| Layer | URL | Status | Notes |
|---|---|---|---|
| Landing page | poetic-kleicha-28d058.netlify.app | Live | Italian/English, full product pitch |
| Chatbot Alessia | Same Netlify LP | Live | Widget visible at bottom |
| Old full app | web-production-031a6.up.railway.app | Broken | Was login+dashboard+CRM. Broke at migration. |
| New admin panel | lexflow-mvp-production.up.railway.app/admin | Live | Flask-Admin basic panel |
| Lovable CRM upgrade | lovable.dev/projects/544fbbf8... | Unclear | Exists, not yet connected |
| Stylebook | Perplexity thread/Space | Locate | Exact file location unknown |

Features confirmed on landing page:
- Case & Matter Management
- Client Intake & CRM
- Document & File Management
- Legal Calendaring
- Client token-secured tracking pages (no login for clients)
- Practice area forms: Criminal, Civil, Labour, Family, Real Estate
- GDPR + ISO 27001:2022 + ISO/IEC 27701:2025 compliance

Roadmap (not yet built): Billing, Workflow Automation, Payments

WARNING - Landing page still links to OLD backend URL:
  Currently points to: web-production-031a6.up.railway.app
  Must change to:       lexflow-mvp-production.up.railway.app

### Perplexity-Generated Artifacts to Locate
| Artifact | Created | Contents |
|---|---|---|
| LexFlow Stylebook | Perplexity thread (URL unknown) | Visual design system |
| LexFlow Chatbot frontend | Building Space | Chatbot design |
| lexflow_chatbot_summary.csv | May 18 sandbox | Chatbot architecture CSV |
| LexFlow_Bot_Complete_Briefing.xlsx | May 18 sandbox | 4-sheet Excel, full bot briefing |
| MP_LexFlow_FullStack_V4.md | Perplexity Space file | Master prompt V4 (3732 chars) |
| CLAUDE.md | GitHub repo root | Stack rules, folder structure |
| LexVik_Option1_vs_Option2.xlsx | May 22 sandbox | Decision matrix |

---

## What Was Fixed (June 19-20, 2026)

| # | Problem | Fix |
|---|---|---|
| 1 | Flask 3.0.3 broke flask-jwt-extended | Downgraded Flask to 2.3.3 |
| 2 | resend missing from requirements.txt | Added resend==2.0.0 |
| 3 | Duplicate load_demo() at lines 220+248 | Renamed second to load_demo_admin() |
| 4 | Railway watching wrong repo | Updated git remote to Ole00007/lexflow-crm |
| 5 | .venv pushed to Railway | Added .venv/ to .gitignore |

---

## Open Questions - Priority Order

PRIORITY 1 (RED) - Inspect what already exists (5 min)
  cd "/Users/olesiarasing/Desktop/LexFlow/LexFlow Review Build"
  grep -n "@app.route" app.py
  ls templates/
  ls static/

PRIORITY 2 (RED) - Fix landing page URL
  Surgical change in Netlify HTML: swap old Railway URL for new one.

PRIORITY 3 (RED) - Restore full app (login/dashboard/CRM)
  Was working before migration. Check if templates still exist. Patch routes only.

PRIORITY 4 (YELLOW) - Resolve Lovable -> Railway connection

  a) Connect Lovable to existing Netlify frontend:
     Option A: Export Lovable -> redeploy on Netlify (replace files)
     Option B: Lovable publishes separately, LP links to it
     Option C: Embed Lovable inside Netlify LP via iframe

  b) UI/UX that matches backend:
     Need API contract - which Flask route does each screen call?
     Minimum: login -> cases list -> case detail -> intake form -> client tracking

  c) App user -> Railway backend API:
     App user -> Lovable/Netlify -> Flask API (CORS: whitelist Netlify domain) -> PostgreSQL
     Flask-CORS already installed. Needs correct origin in config.

PRIORITY 5 (YELLOW) - Locate Stylebook + Chatbot artifacts
  Search Perplexity Spaces and download threads from May 2026.

PRIORITY 6 (GREEN) - Calendar feature (roadmap)
  Backend: SQLAlchemy events table (id, matter_id, date, type, description)
  Frontend: FullCalendar.js via CDN
  Build AFTER core reconnection is done.

---

## Recommended Path Forward

| Step | Action | Effort |
|---|---|---|
| 1 | Run inspect commands, map routes + templates | 5 min |
| 2 | Update Netlify LP URL old -> new Railway | 10 min |
| 3 | Restore login + dashboard if templates exist | 30-60 min |
| 4 | Clarify Lovable -> Railway connection plan | 30 min |
| 5 | Write API contract (3 routes) for Lovable screens | 1 hr |
| 6 | Calendar feature | After above |

---

KEY REMINDER:
  Backend is deployed and working.
  Landing page is live.
  Full app (login, CRM, dashboard) broke at migration - inspect before rebuilding.
  DO NOT rebuild from scratch.
  Strategy: Inspect -> patch -> reconnect -> only then extend.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Dev-Handoff]]
