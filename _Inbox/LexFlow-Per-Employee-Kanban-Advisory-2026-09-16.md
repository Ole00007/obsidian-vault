---
title: Per-employee Kanban + status colours — advisory (Hermes board vs LexFlow CRM)
created: 2026-09-16
updated: 2026-09-16
tags: [lexflow, crm, kanban, advisory, rbac, statuses, design]
status: proposal — no code written, no design changed
confidence: high — every claim read from the repos/DBs at 2026-09-16 18:05–18:20 CEST
source: Ole question 2026-09-16 ("each employee can have their own Kanban" + Started→In Progress→Done with colours)
---

# Per-employee Kanban + status colours — advisory

## 0. The question

Ole: the `lexflow-learning` board exists **to test the CRM**, not for study. He wants
(1) **each employee with their own Kanban**, (2) a new project opening **without being confused with
the rest**, (3) status moved `Started → In Progress → Done` **with colours**, on **both** the main
Kanban and this one.

## 1. What each "Kanban" actually is today (verified, not remembered)

### 1.1 The Hermes board (`lexflow-learning`)

| Fact | Evidence |
|---|---|
| Isolation IS the design | one board = one SQLite DB + its own workspaces dir + its own dispatcher (`hermes kanban boards` → `default`, `lexflow-learning`) |
| Status vocabulary is **code-fixed**, 9 values | `hermes_cli/kanban_db.py:89` `VALID_STATUSES = {triage, todo, scheduled, ready, running, blocked, review, done, archived}` |
| Colours per status **already exist** | `plugins/kanban/dashboard/dist/style.css`: `triage #b47dd6`, `todo` muted, `ready #d4b348`, `running #3fb97d`, `blocked #d14a4a`, `review #48b0c4`, `done #4a8cd1`, `archived` border |
| Per-person = `assignee` field (a Hermes *profile* name) | `hermes kanban --board <b> list --assignee <profile>` |
| **No per-user login / no permissions** | board files are plain SQLite under `~/.hermes/kanban/` — anyone with the machine reads all boards |

**Consequence:** on the Hermes board you can *never* have columns literally named
"Started / In Progress / Done" — but the closest honest mapping is
`todo → Started`, `running → In Progress`, `done → Done`, and **the colours are already there**.

### 1.2 The LexFlow CRM Kanban (`templates/kanban.html` + `crm/models/case.py`)

| Fact | Evidence |
|---|---|
| 8 columns, **hardcoded in HTML** | `data-status="…"`: `Intake`, `Conflict Check`, `Review`, `In Progress`, `Waiting Docs`, `To Verify`, `Engaged`, `Closed` (`templates/kanban.html:678–720`) |
| Status is a free string on the row | `crm/models/case.py:13` `status = db.Column(db.String(50), default="Intake")` |
| **Assignment fields already exist** | `case.py:10 ownerid`, `case.py:17 assignedto`, `case.py:18 case_no` (e.g. `R-01`) |
| API filters by status only | `crm/routes/cases.py:28` `request.args.get('status')` — **no assignee/owner filter** |
| Priority is coloured, **status is not** | `kanban.html:375–378` `.badge-low/medium/high/urgent`; no `.status-*` colour rule exists |
| Per-user saved views **already built** | `crm/routes/saved_views.py` — `View` per `(created_by, workspace_id, object_type)` with `filters_json`, `sort_json`, `visible_columns_json`, `is_default`; API `/api/views` |
| A per-person board page **already exists** | `templates/staff_board.html:264` "each column = one staff member, cards = their matters (owner or assignee)" — but it is a *separate page*, not the Kanban |
| Staff directory ≠ login users | `crm/models/user.py` (login: `workspace_id`, `role`, default `"user"`); `crm/models/firm_team.py` `FirmTeamMember` (name, role, active) |

## 2. Reasoning

1. **"Don't confuse a new project with the rest" is board-level isolation** — that instinct is right,
   and the Hermes board proves the pattern cheaply. In the CRM the isolation unit is already
   `workspace_id`; a *new project* should be a new **case** (or a new board scope), **not** a new
   workspace. Creating a workspace per employee/project would shred the tenant model, the RBAC and
   the RLS work in flight.
2. **"Each employee has their own Kanban" = a scoped view over one shared board**, not a separate
   board per person. Two reasons: (a) a lawyer must be able to see the team's pipeline
   (`Unassigned`, hand-overs, cover during leave); (b) the assignment fields (`ownerid`,
   `assignedto`) and the per-user `saved_views` table already exist — the missing piece is only the
   **filter + a scope selector**, which is additive and migration-free.
3. **Statuses must become data, not HTML.** Right now renaming or recolouring a column is a template
   edit. A per-workspace `case_status` table (key, label EN/IT, colour, order, `is_terminal`) makes
   "Started → In Progress → Done **with colours**" a row edit. Seed it with today's 8 legal statuses
   so nothing changes visually on day one.
4. **Colours should match across both surfaces.** Use the palette the Hermes board already renders,
   so "amber = not started, green = in progress, blue = done, red = blocked/waiting" is one mental
   model in both places.

## 3. Recommendation

**Layer 1 — isolation (no code):** keep the Hermes `lexflow-learning` board as the *prototype/test
bench*. Map `todo / running / done` and use them with their existing colours to demo the flow to
yourself before any CRM work.

**Layer 2 — CRM, additive first (small, safe):**
- add `assignee` (and `unassigned`) filtering to `GET /api/cases` — fields already on the model;
- add a board **scope selector** (Mine / Team / Unassigned) that reuses `saved_views`
  (`is_default` per user already implemented) — no new tables;
- render columns + colours **from a config map** instead of the hardcoded 8 (behaviour-identical
  first pass).

**Layer 3 — statuses as data (the real feature):** per-workspace `case_status`
(`key, label_en, label_it, colour, sort_order, is_terminal`), admin-editable; board and case form
render from it; the string `Case.status` keeps its current values during the transition.

**Layer 4 — RBAC:** role `user` sees own board only; `admin`/`superadmin` sees all boards in the
workspace. Per the standing rule, whatever bug/behaviour is fixed for one tenant gets audited on the
others in the same pass.

### Suggested status → colour mapping (both surfaces)

| Stage | Hermes status | CRM column | Colour |
|---|---|---|---|
| Started | `todo` (or `ready`) | Intake / Conflict Check | amber `#d4b348` |
| In Progress | `running` | In Progress / Review / To Verify | green `#3fb97d` |
| Blocked / Waiting | `blocked` | Waiting Docs | red `#d14a4a` |
| Done | `done` | Engaged / Closed | blue `#4a8cd1` |

## 4. Gates before any code

- **Design gate:** colours + column changes are a UX change → no deploy until Ole reviews a
  localhost preview and tests it manually (`docs/UX-Fix-Plan-*.md`, then implement).
- **Mapping table first (standing rule):** status → destination → triggers (does moving to
  "In Progress" fire a notification? does "Closed" log an activity entry?) must be signed off
  **before** code — it was the open requirement on the earlier status-change ticket.
- Additive-only; no tenant/RLS/unmerged-branch merge without the 18-test gate.

## 5. Decisions needed from Ole

- **D1** — employee board = *scope over the shared board* (recommended) or a *separate board per person*?
- **D2** — keep the 8 legal statuses and only add labels/colours (recommended, zero migration), or
  collapse the pipeline to Started / In Progress / Done?
- **D3** — prototype on the Hermes board first (throwaway, today) or go straight to the CRM spec?

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-Workspace-UX-Overhaul]]
- Related: [[05-Daily/2026-09-16|Daily 2026-09-16]]
