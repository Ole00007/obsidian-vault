---
title: LexFlow Gantt — Gate A Preflight Report (read-only Frappe Gantt view)
created: 2026-10-10
tags: [lexflow, t-021, gantt, gate-a, preflight, frappe-gantt]
status: preflight
---

# LexFlow — Gate A (inspection + preflight plan) — Frappe Gantt view

Governing doc: `Hermes_LexFlow_Gantt_Master_Prompt.Md` (owner). Scope of this gate:
**inspection only** — no code changes, no commits, no deploys, read-only inspection
of the canonical repo. Nothing here is implemented.

## 1. Baseline commit SHA and working-tree state

- Canonical repo: `/Users/olesiarasing/projects/lexflow-crm`
- Checked-out branch: **`lexflow_hermes_v1`** (tracking `origin/lexflow_hermes_v1`).
- **HEAD = `1ce1ca5`** — `docs(roadmap): daily status 2026-10-10`.
- Last **code** commit is **`8c17456`** (`repoint(marketing): CRM website/home links -> new LexFlow site`), which is HEAD~1. The task brief cited "HEAD 8c17456"; the real HEAD is one docs-only commit ahead (`1ce1ca5`). `8c17456` exists and is the code baseline.
- Working tree: **clean** — `git status --porcelain` returns 0 lines; no uncommitted or untracked owner changes to preserve.
- Recent history (`git log --oneline -5`): `1ce1ca5` → `8c17456` → `5182bf8` (SMTP fallback) → `0f0df5e` (admin workspace provisioning) → `3aaea16`.
- Local branch list shows **no `main`**. The master prompt's "baseline branch: main / never implement on main" cannot be honoured literally against this checkout — see §9.

## 2. App entry point, runtime command and port

- **Factory app**: `crm/__init__.py :: create_app()` (Flask app factory; registers all blueprints, security headers, schema-heal `before_request`).
- **Prod entry (Procfile)**: `web: python -m gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`.
- **`wsgi.py`** imports `crm.create_app()` and, run directly, binds `PORT` default **5000**.
- **`app.py`** also imports `crm.create_app()` (comment says "legacy intake app" but in this repo it points at the CRM factory), default port 5000. `Procfile.crm` alternative: `gunicorn "crm:create_app()" --bind 0.0.0.0:$PORT`.
- **Local command/port per `LOCAL_TESTING_GUIDE.md`**: `python run_crm.py` → `http://localhost:5001`. NOTE: **`run_crm.py` is not present** in the repo (only `run_crm.py.BACKUP-20260528-154815`, which binds `PORT` default 5000 + `debug=True`). See §9.
- **Port 8770 belongs to the demo reference**, not the Flask runtime (master prompt §First response). Confirmed not specified anywhere in the runtime files.
- Established runtime port = **`$PORT` env (Railway) / 5000 default**; local testing guide says 5001. Keep the established port; do not touch it.

## 3. Existing models, date fields, calendar/Kanban date sources, authorization pattern

### Models & date fields (`crm/models/`)
| Model | Table | Start-ish date | End-ish date | Other |
|---|---|---|---|---|
| `Task` (`task.py`) | `tasks` | `createdat` (DateTime, server default) | **`duedate`** (Date, nullable) | `status` (pending/in_progress/done), `priority`, `caseid`, `userid`, `workspace_id`, soft-delete |
| `Case` (`case.py`) | `cases` | **`openedat`** (Date, not null, default today) | **`duedate`** (Date, nullable) | `status`, `priority`, `casetype`, `case_no`/`display_id`, `assignedto`, `ownerid`, soft-delete |
| `Deadline` (`deadline.py`) | `deadlines` | — | **`deadline_date`** (Date, not null) | `deadline_type`, `status`, `priority`, soft-delete |
| `CalendarEvent` (`calendar_event.py`) | `calendar_events` | **`start_datetime`** (DateTime, not null) | **`end_datetime`** (DateTime, nullable) | `event_type`, `is_all_day`, legal fields (court/judge), soft-delete |

No generic `start_date`/`end_date` pair exists on Task/Case/Deadline; only CalendarEvent has a true start+end. Task/Case carry a single **due date** plus a creation/opening date.

### Calendar date source
`crm/routes/calendar.py` — CalendarEvent CRUD; date filtering on `start_datetime`
(`date_from`/`date_to`), sorted by `start_datetime`. Service layer: `crm/services/calendar.py`,
plus read-only Google sync in `crm/google_cal_sync.py` (superadmin-triggered).

### Kanban date source
- Server page: `crm/routes/views.py :: kanban()` groups **Cases** by the fixed status list
  `['Intake','Conflict Check','Review','In Progress','Waiting Docs','To Verify','Engaged','Closed']`.
- Template: `templates/kanban.html` renders cards from **`/api/cases/?status=…`** (per-column fetch);
  the due chip uses **`c.duedate`** (`isOverdue(dateStr)` compares to today). Cards can be dragged
  between columns → `PUT /api/cases/<id>` `{status}` (write path).
- Tasks page `templates/tasks.html` lists via **`/api/tasks/`**, shows `t.duedate`, and can
  optionally mirror a task onto the calendar ("Also add to calendar (uses due date)" →
  creates a CalendarEvent at 09:00 on the due date; see `tasks.py::create_task`).

### Authorization pattern (server-side, mandatory)
- `crm/workspace.py` is the single tenant-scope authority:
  - `get_current_workspace_id()` → the JWT user's `workspace_id`.
  - `get_visible_workspace_ids()` → `None` for superadmin (see all); `[own] + active children` for
    a parent admin; `[]` for anonymous/unknown (see NOTHING — never `None`).
  - `workspace_filter(query, model)` → applies `model.workspace_id.in_(visible_ids)`; superadmin bypasses.
- API blueprints apply it via a local `_filtered_query()`:
  `crm/routes/tasks.py`, `crm/routes/calendar.py`, `crm/routes/cases.py` (all use
  `workspace_filter(...)`), with `@jwt_required()` (tasks/calendar) or `@jwt_required(optional=True)` (cases/views).
- Every API route enforces scope **server-side** — the pattern a Gantt adapter must reuse.
  Tenant isolation is workspace-based (`workspaces` + `parent_workspace_id` sub-workspaces,
  `crm/models/workspace.py`). No per-record ACL beyond workspace membership + `role` (superadmin/admin/staff/user).

## 4. Existing Gantt library / assets

- **None.** Case-insensitive search for `gantt`, `frappe`, `dhtmlx`, `vis-timeline`, `vis.js`,
  `fullcalendar` across all `.py/.html/.js/.css/.json/.txt` (excluding `apps/api/node_modules`)
  returns **zero** matches. No vendored JS libs in `static/` (`static/` holds only favicons, a
  Pagliano landing page, `chat-widget.js`, and two standalone mockup HTMLs).
- There is **no JS build step / bundler** for the Flask app (no `package.json` at repo root; `apps/api`
  is a separate unused TS experiment). Front-end is server-rendered Jinja + inline vanilla JS.
- Conclusion: shipping Frappe Gantt will be a **new, self-hosted asset** — nothing to duplicate.

## 5. Proposed Frappe Gantt version, compatibility basis, loading strategy, license

- **Upstream metadata (inspected):** repo `github.com/frappe/gantt`; `package.json` on `master`
  = **version `1.2.2`**, `"license": "MIT"`, ES/UMD build outputs `dist/frappe-gantt.umd.js`,
  `dist/frappe-gantt.es.js`, `dist/frappe-gantt.css` (exports map). npm registry `dist-tags`
  **`latest = 1.2.2`**; the latest GitHub *release tag* is **`v1.0.3`** (published 2025-02-03).
- **Proposed pin:** **`frappe-gantt@1.2.2`** (npm `latest`), self-hosted. Document the exact
  version + its sha256 in the change ledger. (If the owner prefers a tagged release artifact,
  `v1.0.3` is the newest GitHub release — flag as the one alternative to confirm.)
- **Compatibility basis:** the v1.x UMD bundle is a standalone `FrakeGantt`/`Gantt` constructor
  consuming a plain array of `{id,name,start,end,progress,dependencies,custom_class}` — no framework,
  no bundler; a `<script src="…umd.js">` + `<link …css>` is enough. That matches this repo's
  no-build Jinja + vanilla-JS front end. Data lives in Python dicts already serialized by
  `to_dict()`; the UMD build needs plain JSON, so a thin adapter is required.
- **Loading strategy:** **self-hosted, pinned, no bare-CDN-latest.** Copy the pinned
  `dist/frappe-gantt.umd.js` + `dist/frappe-gantt.css` into `static/vendor/frappe-gantt/1.2.2/`
  and reference them with `url_for('static', …)`. This satisfies the repo's CSP
  (`default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; connect-src 'self' https:`)
  — a bare CDN `<script>` from a third-party origin would be blocked by `script-src 'self'` anyway.
- **License obligation:** Frappe Gantt is **MIT** → ship its `LICENSE`/copyright notice alongside the
  vendored files (`static/vendor/frappe-gantt/1.2.2/LICENSE`) and cite it in the review doc. No copyleft.

## 6. Proposed branch, file-level scope, API contract, rollback

**Feature branch (off `lexflow_hermes_v1`):** `feat/t021-gantt-readonly`
(optional secondary worktrees for parallel backend/frontend: `feat/t021-gantt-api`, `feat/t021-gantt-view`).

**File-level scope (additive only):**
- `crm/routes/gantt.py` — **new** read-only adapter blueprint (`/api/gantt`), reusing `workspace_filter`.
- `crm/routes/views.py` — one new page route `GET /gantt` rendering the view (mirrors `tasks()`/`kanban()`).
- `crm/__init__.py` — one import + one `register_blueprint` (additive; ~2 lines).
- `templates/gantt.html` — **new** page: `<script>`/`<link>` to the vendored asset, fetch `/api/gantt`
  with the localStorage JWT, render `new Gantt('#gantt', tasks, {read_only:true, …})`.
- `templates/base.html` — one `<li><a class="nav-link" href="{{ url_for('views.gantt') }}">Gantt</a></li>` nav entry.
- `static/vendor/frappe-gantt/1.2.2/` — vendored `frappe-gantt.umd.js`, `frappe-gantt.css`, `LICENSE`.
- (Optional) `tests/test_gantt.py` — workspace-scoping + empty/malformed-date tests.

**API contract sketch (read-only):**
```
GET /api/gantt            @jwt_required()
  → 200 {
      "tasks": [
        {"id": <str, e.g. "task-12"|"case-6"|"deadline-3">,
         "name": "<escaped title (case display_id + title)>",
         "start": "YYYY-MM-DD",            # source field depending on chosen mapping (§8)
         "end":   "YYYY-MM-DD",
         "progress": <0-100 from status>,
         "dependencies": "<comma-ids or ''>",   # only if a real dependency field exists
         "custom_class": "unscheduled|case|task|deadline"}
      ],
      "unscheduled": [ {"id":..., "name":..., "reason":"no due date"} ]
    }
  # scoped via workspace_filter(Task|Case|Deadline, …); NO POST/PUT/DELETE.
```
- **Read-only enforced**: `read_only:true` + disable drag/resize persistence; no write endpoint added.
- Date validation mirrors `tasks.py::_safe_date` (strict `YYYY-MM-DD`, year 1900–2100) so malformed
  values cannot corrupt output.
- **Dependencies**: only emit if a real field backs them. Task/Case/Deadline have **no dependency
  column** today → either omit `dependencies`, or make the smallest **additive** proposal for owner
  approval (per master prompt §Scope 3). Do NOT invent them.

**Rollback plan:** revert the feature branch. Because the change is additive and isolated —
one new blueprint, one new view route function, one new template, one nav `<li>`, one vendored
folder — rollback = `git revert` the merge commit (or drop the branch); **no DB migration, no schema
change, no dependency change**, so no data-risk rollback step. Deleting `templates/gantt.html`,
`crm/routes/gantt.py`, the two `__init__.py` lines, the nav line and `static/vendor/frappe-gantt/`
returns the app to baseline byte-for-byte (minus vendored assets).

## 7. Time and token/cost estimate (labelled; unknowns flagged)

**Time (developer-hours, rough — NOT a guarantee):**
- Inspection / Gate A evidence-gathering: **0.5–1 h** (this report).
- Backend adapter (`crm/routes/gantt.py` + blueprint registration + scoping + date-safety): **1–1.5 h**.
- Frontend (`templates/gantt.html` + vendored asset + nav entry + read-only wiring + light/dark respect): **2–3 h**.
- Testing (unit + manual: scoping, empty/malformed dates, read-only, mobile/keyboard, CSP load): **1.5–2 h**.
- **Total ≈ 5–7.5 h.** Uncertainty: medium (±30%); the biggest unknown is the date-mapping/product
  decision in §8 and whether dependencies require an approved additive field.

**Token / cost:** Exact token count and unit price for this workflow are **NOT VERIFIED** — I will not
fabricate prices. Known: this Gate-A inspection ran on model **`deepseek/deepseek-v4.1-flash`**
via provider **`nous`** (from the runtime environment). Cost rates, credits and any per-token pricing for
that model/provider are **unknown to me** and are not asserted. Any budget figure must come from the
owner's actual Nous Portal billing.

## 8. The single smallest missing decision needing the owner

**Which fields define each Gantt bar's start and end.** The models give no generic start/end pair:
Task has only `duedate` (+`createdat`), Case has `openedat`+`duedate`, Deadline has only
`deadline_date`, CalendarEvent has `start/end`. The smallest consequential decision the owner must
make: **what is a Gantt bar here** — e.g. (a) Case bars = `openedat → duedate`, Tasks = milestone at
`duedate`; or (b) Tasks = `createdat → duedate`; or (c) CalendarEvents only. This cannot be resolved
from repository evidence alone (it is product intent) and it determines the API adapter contract.

Secondary procedural note: the standing rule that **nothing design/UX deploys before the owner's
localhost review**, and T-021 sitting behind **T-019 (design/UX)** which is still gated, means the
owner also needs to confirm that opening **Gate B** for this read-only view is permitted now (see §9).

## 9. Things in the master prompt I could NOT verify against the repository → NOT VERIFIED

- **Demo at `http://localhost:8770`** — no listener (`curl` → connection failed; HTTP 000), and no demo
  directory found on disk. Its "21 tasks / 3 done / 5 agents" and synthetic 2026-10-04 dates are
  **NOT VERIFIED**. (They are demo-only anyway and must never enter live dates.)
- **Roadmap JSON expectations** — `docs/LexFlow_Agentic_Roadmap.json` **exists** but contains
  **19 tasks (`T-001…T-019`), not 21**, and **no `T-021`**. Its `agents` key is a registry **object**
  (`operator_installer`, `backend_dev`, `frontend_dev`, `lexflow_head_admin`, …), not "5 agents".
  → "21 tasks / 3 done / 5 agents" is **NOT VERIFIED** against this repo.
- **`docs/LexFlow_Agentic_Roadmap.json` as T-021's source** — T-021 is **not present** in it. The
  roadmap `status_run` (2026-10-10) itself says "no new commits on lexflow_hermes_v1 beyond 8c17456".
- **Kanban card `t_f0f709f5` and parent `t_bc68191b`** — **not found** anywhere in the repo files
  (no kanban.db tracked; ID appears only in the vault spec note). **NOT VERIFIED** from the repo.
- **`.env.example`** (listed in the master prompt) — **does not exist** in the repo root. No `.env*`
  file is present. `.env`, api-keys CSVs and any secrets were intentionally NOT opened/quoted.
- **Repo URL / branch** — master prompt says `github.com/Ole00007/lexflow-crm`, baseline branch `main`.
  Local checkout is `lexflow_hermes_v1`; **no `main` branch** exists locally, and I did not fetch the
  remote. **NOT VERIFIED.**
- **"Exact library version" previously chosen by the owner** — the master prompt notes it was not
  available to its editor; it is **NOT VERIFIED**. Pin proposed in §5 is mine, on inspected upstream metadata.
- **Smothy / Admy reviewer profiles & tools** — not inspected (out of Gate-A scope); their independent
  cross-test capability is **NOT VERIFIED** and no review is claimed.
- **`run_crm.py`** — referenced by `LOCAL_TESTING_GUIDE.md` (`python run_crm.py` → :5001) but **absent**
  from the repo (only a `.BACKUP` variants at :5000). Local port command is therefore **NOT VERIFIED**
  as a runnable entry today.
- **`requirements.txt`** lists no frontend tooling; there is no bundler — stated from evidence, but a
  hidden build step elsewhere (outside the repo) is **NOT VERIFIED**.

## Links

- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]
- Related: [[LexFlow-Project-Status]]
