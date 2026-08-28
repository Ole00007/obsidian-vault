# aLEXy — Deployment Status

**Date:** 2026-07-23  
**URL:** https://web-production-b2e68.up.railway.app  
**Login:** admin@alexy.test / Admin123!  
**GitHub:** [Ole00007/aLEXy](https://github.com/Ole00007/aLEXy)  
**Branch:** `main`

---

## Current State

The CRM app is deployed and fully operational. The kanban board, dashboard, and all API endpoints are live. Demo seed data is populated.

### Frontend Pages

| Route | Page | Description |
|-------|------|-------------|
| `/` | Dashboard | Live stats (contacts, cases, tasks, pending), recent activity, quick actions |
| `/kanban` | Kanban Board | 3-column task board with drag-and-drop, login form, add-task modal |
| — | Landing page | **Not yet integrated** — awaiting source file |

### API Endpoints (all verified ✅)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/health` | GET | No | Health check + DB status |
| `/api/auth/login` | POST | No | JWT login |
| `/api/auth/me` | GET | JWT | Current user |
| `/api/tasks/` | GET/POST | JWT | List / create tasks |
| `/api/tasks/<id>` | PATCH | JWT | Update task (drag-drop) |
| `/api/tasks/<id>/complete` | PATCH | JWT | Mark task completed |
| `/api/tasks/<id>` | DELETE | JWT | Delete task |
| `/api/tasks/export.csv` | GET | JWT | Export tasks CSV |
| `/api/tasks/import` | POST | JWT | Import tasks CSV |
| `/api/tasks/bulk-update` | PATCH | JWT | Bulk update tasks |
| `/api/tasks/bulk-complete` | POST | JWT | Bulk complete tasks |
| `/api/tasks/bulk-delete` | DELETE | JWT | Bulk delete tasks |
| `/api/cases` | GET/POST | JWT | List / create cases |
| `/api/cases/<id>` | GET/PUT/DELETE | JWT | Single case CRUD |
| `/api/contacts/` | GET/POST | No | List / create contacts |
| `/api/contacts/<id>` | DELETE | No | Soft-delete contact |
| `/api/calendar/events` | GET/POST | JWT | Calendar events |
| `/api/email/settings` | GET | JWT | Email SMTP config |
| `/api/email/send-test` | POST | JWT | Send test email |
| `/api/webhooks/subscriptions` | GET/POST | JWT | Webhook subscriptions |
| `/api/notifications/unread-count` | GET | JWT | Unread notification count |
| `/chatbot/health` | GET | No | Chatbot status |
| `/chatbot/chat` | POST | No | Chat with Alessia |

### Seed Data

| Entity | Count | Details |
|--------|-------|---------|
| Contacts | 12 | Sarah Mitchell, James Rodriguez, Emily Chen, Marcus Webb (×3 each due to re-seed) |
| Cases | 8 | Employment Dispute, Lease Review, Debt Collection, Family Trust (×2 each) |
| Tasks | 12 | Mixed across pending / in_progress / completed |

### Demo Data Distribution

**Pending (5):** Draft demand letter, Order valuation report, Draft trust deed (×2), Order valuation report  
**In Progress (2):** Review lease terms (×2)  
**Completed (5):** File court summons (×2), Review contract (×2), Draft demand letter

---

## Recent Fixes

| Date | Fix |
|------|-----|
| 2026-07-23 | Added `PATCH /api/tasks/<id>` route for kanban drag-and-drop |
| 2026-07-23 | Built dashboard page with live stats and recent activity |
| 2026-07-23 | Fixed `template_folder` to serve both dashboard and kanban templates |
| 2026-07-23 | Updated sidebar navigation to Dashboard + Kanban links |
| 2026-07-22 | Added root route `/` → kanban board (solved 404 on Railway) |
| 2026-07-22 | Fixed webhook 500 error (missing `requests` dependency) |
| 2026-07-22 | Deployed native chatbot, calendar, email, webhooks modules |

---

## Remaining

- [ ] Copy landing page source to `~/aLEXy/` and integrate as root route
- [ ] Clean up duplicate seed data
- [ ] Add public intake form
- [ ] Add client status page (`/status/<token>`)
- [ ] Configure SMTP credentials for live email

---

## Running Locally

```bash
cd ~/aLEXy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python wsgi.py
```

## Deploy

```bash
cd ~/aLEXy
git add -A
git commit -m "description"
git push
# Railway auto-deploys from main branch
```