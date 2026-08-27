# LexFlow — Full Project Handoff Document v3
**Date:** June 21, 2026  
**Status:** Backend live. Frontend partially live. Reconnection in progress.  
**Build mode:** Hermes-first. Perplexity plans and prompts Hermes. Hermes builds. Human overrides only on failure or drift.

---

## Build Workflow (NEW — v3)

### Who does what

| Role | Responsibility |
|---|---|
| Perplexity (this Space) | Architecture decisions, planning, prompt authoring, review, QA specs |
| Hermes (AI building agent) | All file writes, code generation, commits, deployments |
| You (founder) | Final approval, business decisions, override when Hermes drifts or fails |

### How every task runs from now on

1. **Perplexity plans** — defines exactly what to build, why, acceptance criteria, and risks.
2. **Perplexity writes a Hermes prompt** — a precise, self-contained instruction block ready to paste into Hermes.
3. **You paste into Hermes** — no terminal commands for you unless overriding.
4. **Hermes builds and commits** — all file writes and git operations done by Hermes.
5. **Perplexity reviews output** — checks result against acceptance criteria.
6. **Override rule** — if Hermes produces bad output or drifts from the plan, Perplexity provides a corrective prompt or surgical fix instruction. You apply only if Hermes cannot self-correct.

### Hermes prompt format (standard template)

Every Hermes prompt Perplexity writes will follow this structure:

```
CONTEXT
[Project state, relevant files, stack facts]

TASK
[Exactly what to build — one atomic unit]

ACCEPTANCE CRITERIA
[What done looks like — testable conditions]

CONSTRAINTS
[Do not touch X. Do not rebuild Y. Surgical only.]

FILES TO EDIT / CREATE
[Exact paths]

VERIFICATION
[How to confirm it worked]
```

### Override conditions

Invoke manual override (you + Perplexity) only if:
- Hermes edits files outside the specified scope
- Hermes rebuilds something that should be patched
- Hermes breaks a working feature
- Hermes loops on the same error 3+ times without progress

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
```
User browser
  -> Netlify (Alessia chatbot bubble)
  -> Railway server.py (guardrails)
  -> OpenRouter / Llama 3.3 70B free
  <- Response back through same chain
```

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

⚠️ WARNING — Landing page still links to OLD backend URL:  
Currently points to: `web-production-031a6.up.railway.app`  
Must change to: `lexflow-mvp-production.up.railway.app`

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

**PRIORITY 1 (RED) — Inspect what already exists**  
Hermes task: read `app.py`, list all routes, list `templates/` and `static/` contents.  
Output needed: route map + template inventory before any fix begins.

**PRIORITY 2 (RED) — Fix landing page URL**  
Hermes task: surgical find/replace in Netlify HTML.  
Swap `web-production-031a6.up.railway.app` → `lexflow-mvp-production.up.railway.app`

**PRIORITY 3 (RED) — Restore full app (login/dashboard/CRM)**  
Was working before migration. Check if templates still exist. Patch routes only.  
DO NOT rebuild from scratch.

**PRIORITY 4 (YELLOW) — Resolve Lovable → Railway connection**

a) Connect Lovable to existing Netlify frontend:  
- Option A: Export Lovable → redeploy on Netlify (replace files)  
- Option B: Lovable publishes separately, LP links to it  
- Option C: Embed Lovable inside Netlify LP via iframe

b) UI/UX that matches backend:  
Need API contract — which Flask route does each screen call?  
Minimum: login → cases list → case detail → intake form → client tracking

c) App user → Railway backend API:  
App user → Lovable/Netlify → Flask API (CORS: whitelist Netlify domain) → PostgreSQL  
Flask-CORS already installed. Needs correct origin in config.

**PRIORITY 5 (YELLOW) — Locate Stylebook + Chatbot artifacts**  
Search Perplexity Spaces and download threads from May 2026.

**PRIORITY 6 (GREEN) — Calendar feature (roadmap)**  
Backend: SQLAlchemy events table (id, matter_id, date, type, description)  
Frontend: FullCalendar.js via CDN  
Build AFTER core reconnection is done.

---

## Recommended Path Forward

| Step | Action | Who builds | Effort |
|---|---|---|---|
| 1 | Inspect routes + templates | Hermes | 5 min |
| 2 | Update Netlify LP URL old → new Railway | Hermes | 10 min |
| 3 | Restore login + dashboard if templates exist | Hermes | 30-60 min |
| 4 | Clarify Lovable → Railway connection plan | Perplexity plans, Hermes builds | 30 min |
| 5 | Write API contract (3 routes) for Lovable screens | Perplexity drafts, Hermes implements | 1 hr |
| 6 | Calendar feature | Hermes | After above |

---

## KEY REMINDERS
- Backend is deployed and working.
- Landing page is live.
- Full app (login, CRM, dashboard) broke at migration — inspect before rebuilding.
- **DO NOT rebuild from scratch.**
- Strategy: Inspect → patch → reconnect → only then extend.
- **All build instructions go to Hermes first. Terminal is last resort.**

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Dev-Handoff]]
