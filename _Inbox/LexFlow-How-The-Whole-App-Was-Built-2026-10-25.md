---
title: How the whole LexFlow was built (July–October 2026) — evidence-based reconstruction
date: 2026-10-25
sources: git history of lexflow-crm (166 commits, 2026-07-15 → 2026-10-25), repo inventory, docs/*, agent memory (Hindsight bank avibe-hq). Items marked (memory) come from recorded session history, not from the repo; items marked (unverified) were not re-checked today.
---

# 1. What LexFlow is
A multi-tenant legal CRM + intake system for small law firms (first client: Avv. Diego Pagliano, Genoa; second tenant studio: Romanelli; marketing sites for LexFlow, aLEXy, AVIBE). One Flask application serves every tenant; each landing page posts into the CRM with a different `source`/workspace.

# 2. Stack (verified from the repo)
| Layer | What |
|---|---|
| App | Flask 2.3.3 app-factory (`crm/__init__.py: create_app()`), blueprints per domain, Jinja templates + vanilla JS (no SPA); `wsgi.py` entry |
| Data | SQLAlchemy 2.0 + Flask-Migrate/Alembic (14 revisions, single head) ; SQLite locally, PostgreSQL on Railway |
| Auth | Flask-JWT-Extended (24 h tokens, identity = user id), Flask-Limiter, Flask-CORS |
| Mail | Resend |
| Run | gunicorn (`Procfile: python -m gunicorn wsgi:app --workers 2 --timeout 120`), Railway |
| Size | ~8.3 k lines of Python in `crm/`, 19 models, ~25 route modules, 21 templates, 28 pytest tests + plain-script tests |
| Front doors | Static landing pages (Netlify / Cloudflare Pages) + an intake chat widget "Elisa" |

# 3. The architectural decisions that shaped everything
1. **Multi-tenancy as a query filter, not separate apps.** Every table carries `workspace_id`; `workspace_filter()` and `get_visible_workspace_ids()` are the single choke point (superadmin → all, firm admin → firm + client sub-workspaces via `parent_workspace_id`, anyone else → own). Every new feature since has been tested against that rule.
2. **Additive evolution.** New columns are nullable and applied twice-safely: Alembic migration *and* an idempotent `_ensure_schema` ALTER guarded by an inspector check, so an old production DB heals on first request.
3. **One canonical roadmap.** `docs/LexFlow_Agentic_Roadmap.json` is the single source of truth for project status; the Gantt, the graph and the Kanban roadmap are derived views (`seed_gantt_data.py` upserts from it).
4. **Feature flags default OFF** (`GANTT_VIEW_ENABLED`, `GRAPH_VIEW_ENABLED`, `CONTEXT_NOTES_ENABLED`, `CALENDAR_DEADLINES_ENABLED`, `NOTIFY_BUTTONS_ENABLED`) so unfinished work can ship dark.
5. **Two contact models**: internal firm Team (`FirmTeamMember`) vs client-facing Contacts (memory); clients of a firm see only their parent firm's team, read-only.
6. **Everything built by agents obeys one workflow** (see [[LexFlow-Reusable-Build-Protocol-2026-10-25]]): isolated worktree → cross-test by a different agent → orchestrator gate → merge locally → separate, human-approved deploy gate.

# 4. Timeline (git + memory)
- **Jul 15–22 — MVP backbone.** Flask API (`crm/`), contacts/cases/tasks, task priority/assignment/duration, CSV import/export, calendar + Google Calendar sync code (mock mode), `wsgi.py`/Procfile so Railway serves the modular API. *Lesson:* Railway served the old `app.py` because there was no entry point → 404s.
- **Aug 26–30 — hardening + multi-tenant.** Seed passwords moved to env (no hard-coded credentials), pbkdf2 hashing (scrypt missing on macOS), schema refresh in a `before_request`, `@jwt_required` gaps closed, Romanelli sub-workspaces, per-workspace login page. **Build 2 (Aug 29)**: Saved Views + Attachments built in parallel by two subagents on isolated worktrees, merged, deployed (memory). Timeline/activity auto-logging for tasks, deadlines, calendar.
- **Sep 1–17 — client model, notifications, sites.** Calendar pull/push, email notifications on event creation, firm-team directory and client-facing contact lifecycle (T-007, 41/41 cross-audit checks, memory), WhatsApp intake guard, UX audit + contrast fixes (T-019), landing pages (Netlify, then Cloudflare Pages deployment of the marketing site on Sep 17).
- **Sep 26 → Oct 14 — production outage period (recorded in the roadmap as P0-PROD-DOWN):** Railway returned "Application not found"; no code fix possible, blocked on access. Work continued locally.
- **Oct 14 — Gantt gate (P0–P4).** Plan v4: inventory, architecture decision (keep the Flask monolith; do NOT start the half-built Next.js monorepo), bar semantics, task `startdate`, per-user authorisation rule. Decision records in `docs/gantt_*.md`.
- **Oct 24 — Gantt + context graph.** Fixed the opaque grid rect that hid every bar; dependency arrows (`tasks.depends_on`); live Obsidian-style graph `/graph` (cases, tasks, contacts, staff, vault notes as nodes); overdue-task crash fix; JWT-wipe fix; roadmap T-022…T-028.
- **Oct 24–25 — Wave 1** (this log: [[LexFlow-Wave1-Build-Log-Technical-2026-10-25]]): team roles + vault docs + lawyer flags, deadlines in the calendar, Telegram/WhatsApp buttons; first multi-agent wave with an orchestrator (Admy), an ops agent (Smoothy) and independent cross-tests.

# 5. What is deployed vs local (as of 2026-10-25)
- Local only (this work): Gantt/graph/team/deadlines/notify, merged in the local `lexflow_hermes_v1` (nothing pushed). Production state on Railway was down at the last roadmap check (Oct 14) — (unverified today).
- Open gates before any deploy: SECRET_KEY + JWT_SECRET_KEY must exist in Railway (no fallback in config), run migrations on staging, enable flags one at a time.

# 6. Recurring failure modes (so they are not repeated)
| Failure | Root cause | Standing fix |
|---|---|---|
| Production 404 | deploy had no WSGI entry for the new app | `wsgi.py` + explicit start command, checked in a smoke test |
| "Empty pages" after login | client code deleted the stored token on any network error | only delete on 401/403 |
| Hidden Gantt bars | opaque SVG background drawn last | `fill:none` |
| Whole chart blank on one overdue task | library rejects two-class `custom_class` | pass one token, re-apply the rest |
| Feature visible through UI but 500s | frontend sends datetimes, backend parsed dates | test with the *real page's* request format |
| Agent run silently empty | provider credits exhausted / profile without key | health-check every agent profile before dispatch |
| Port/server chaos | ad-hoc servers from scratch dirs | one canonical boot command + fixed ports |

## Links
- Parent: [[LexFlow-Platform-Plan-2026-10-24]]
- Related: [[LexFlow-Reusable-Build-Protocol-2026-10-25]], [[LexFlow-Wave1-Build-Log-Technical-2026-10-25]]
