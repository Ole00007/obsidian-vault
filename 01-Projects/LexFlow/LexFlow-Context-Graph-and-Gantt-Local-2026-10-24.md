---
title: LexFlow — Context graph + Gantt local build
created: 2026-10-24
tags: [lexflow, gantt, graph, t-021, local]
status: local-only, awaiting Ole approval + cross-test
---

# LexFlow — Context graph (Obsidian-style, live) + Frappe Gantt

Repo `/Users/olesiarasing/projects/lexflow-crm`, branch `feat/t021-styled-demo` (isolated; nothing pushed, nothing deployed).

## Commits (local)
- `86cef9c` fix(gantt): `.gantt .grid-background` was `fill: var(--surface)` and is the LAST svg child → covered all bars. Now `fill: none` (as upstream).
- `4da5d22` feat(graph): `/graph` page — `templates/graph.html`, `static/js/graph/graph_view.js`, `static/css/graph/graph.css`, route `views.graph_view`, nav link, context vars `graph_enabled`/`gantt_enabled`.

## What the graph does
Live read-only canvas on `GET /api/roadmap/graph` (workspace-scoped JWT, same isolation as all `/api` routes): force layout, drag/pan/zoom, hover highlight, click → detail + connected list, dbl-click → local (2-hop) view, **Today** mode (overdue / due today / in progress / next 7 days get rings, rest dimmed, side list), search, type filters, 30 s auto-refresh. Flag `GRAPH_VIEW_ENABLED` (default off → 404). Regression: flag off → `/graph` 404, `/ /login /dashboard /kanban /contacts /calendar /tasks` 200, APIs 200, anon graph API 401.

## Not done / next
- Gantt dependency arrows (API returns `dependencies: ''`).
- Hindsight / vault notes as graph nodes (the "context window" idea) — not started.
- Cross-test by another agent, then Ole approval, then merge; Railway deploy needs merge check first.
- Pre-existing: `heal task dates` startup SQL is Postgres-only (warning on SQLite).

## Admy cross-test

Independent review by Admy (admy_ceo) of branch `integration/graph-gantt-local` (HEAD `901683a`) vs baseline `lexflow_hermes_v1` (`82d1f09`). Read-only; throwaway SQLite DBs under backend-dev scratch; no tracked repo files touched; no push/deploy; port 5057 untouched. Venv `gv/bin/python`.

### A. Test scripts (both ALL PASS)
- `tests/test_gantt_dependencies.py` → `RESULT: ALL PASS` (exit 0). Covers: endpoint 200, whitelisted keys, dedup, self-ref dropped, unicode-digit `²` no-500, undated excluded, anon 401, tenant-admin isolation.
- `tests/test_context_notes.py` → `RESULT: ALL PASS` (exit 0). Covers: flag-off 404, anon 401, non-superadmin 403, unconfigured vault 200 empty, symlink/big-file skip, no SECRET leak, frontmatter parse, excerpt ≤260, no body key, wikilink/mentions edges, regression pages 200.

### B. Flags-off parity vs baseline (PASS)
Ran a 38-route/API battery (pages + main APIs, anon + superadmin) on both branch and a `git worktree` checkout of `lexflow_hermes_v1`, all flags OFF. Status codes identical on every route. Only diffs = the NEW flag-gated endpoints themselves (baseline 404 → branch 401 anon / 200 superadmin for `/api/gantt/tasks`; `/api/context/notes` 404 superadmin flag-off). Nothing that must not change changed. Worktree removed after.

### C. Tenant isolation (PASS)
Romanelli-style parent admin (romanelli-studio) + client sub-workspace admin (romanelli-cl1, parent_workspace_id) + superadmin, 4 workspaces:
- Gantt: parent admin sees own+cl1 only (not lexflow/pagliano); cl1 admin sees only cl1; cl1 task's dependency on a hidden romanelli task is DROPPED (no leak); parent admin keeps it (visible). Superadmin sees all 4.
- Graph: parent admin sees only own+cl1 data nodes; cl1 admin only cl1; superadmin all 4. (Staff node for the shared owner carries the owner's home workspace_id — legitimate, pre-existing, not a data leak.)
- Context notes: parent & cl1 admins → 403; superadmin → 200.
- Superadmin scope: superadmin sees ALL workspaces' tasks in `/api/gantt/tasks` and `/api/roadmap/graph`. This MATCHES the CRM's existing design — `workspace_filter`/`get_visible_workspace_ids` return unfiltered for superadmin on every `/api` route (dashboard, /api/tasks, /api/cases, etc.). The "ws7 lexflow for writes" note refers to where superadmin WRITES (default workspace for new records), not what it reads. Consistent; no change needed.

### D. Production risk (Postgres)
- Migration `g8b9c0d1e2f3` additive nullable `depends_on VARCHAR(255)`, `batch_alter_table` (Postgres-safe). Alembic chain single head `g8b9c0d1e2f3` (verified via ScriptDirectory). `_ensure_schema` ALTER is additive + existence-checked + try/except. Safe.
- Procfile / wsgi.py UNCHANGED. requirements-dev.txt is a NEW dev-only file (pytest). 
- **MAJOR (outside described change set):** `crm/config.py` now reads `SECRET_KEY`/`JWT_SECRET_KEY` via `os.environ[...]` with NO fallback → app CRASHES on import (KeyError) if either env var is unset. Verified. This is a security improvement (removes hardcoded dev secrets) but a boot risk: Railway MUST have both set before this branch deploys.
- Pre-existing (not this branch): `heal task dates` startup SQL uses Postgres-only `EXTRACT` → warning on SQLite (non-fatal, try/except).

### E. Roadmap source of truth (PASS)
`docs/LexFlow_Agentic_Roadmap.json` remains canonical. `seed_gantt_data.py` is a one-way seed (reads roadmap → DB tasks/cases, maps depends_on); graph/Gantt read the DB, not a parallel tracker. `apps/progress-visualiser/src/data/lexflow-roadmap.generated.json` is a properly-labelled DERIVED read-only copy (regenerated by sync-data.mjs, never written back) — §9.3 compliant. No parallel tracker created.

### F. Verdict
**GO for LOCAL merge into `lexflow_hermes_v1`** (all tests pass; flags-off parity; tenant isolation; single-head migration; roadmap SSOT intact). Conditions for a later Railway deploy gate: (1) confirm `SECRET_KEY` + `JWT_SECRET_KEY` are set in Railway (config.py no-fallback boot risk); (2) run `alembic upgrade head` on staging first (single head g8b9c0d1e2f3); (3) smoke-test `/graph`, `/gantt`, `/api/gantt/tasks`, `/api/context/notes` on staging with flags ON; (4) verify seed endpoint now requires superadmin JWT (auth.py change) and that no seed passwords are missing in prod env.

### Defects
- **MAJOR** — `crm/config.py:29-30` SECRET_KEY/JWT_SECRET_KEY no-fallback → boot crash if unset (deploy-gate condition; not a local-merge blocker).
- **MINOR** — branch bundles far more than the described 4-item change set (whole `apps/progress-visualiser` React app, auth.py seed-endpoint hardening, tasks.py startdate, startdate migration f7a8b9c0d1e2, docs/scripts/tests). Confirm Ole wants all of it in the local merge, or split.
- **MINOR** — tracked `crm_local.db` / `data/app.db` show as deleted in the working tree (pre-existing, not from this review); repo hygiene — these DB files shouldn't be tracked.
- **MINOR** — Gantt/graph reflect DB task state seeded from the roadmap; if the roadmap JSON is updated, the Gantt won't reflect it until reseeded (one-way seed, not a live sync).

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]

## Update 2026-10-24 late — project view
- Roadmap JSON (canonical) gained T-022..T-028; Gantt + graph now show the LexFlow project itself (28 roadmap tasks, 15 dependency arrows). Demo law-firm matters were soft-deleted from the local DB only.
- Local one-click sign-in: http://127.0.0.1:5057/dev/enter?to=/gantt (and ?to=/graph) — lives in the scratch launcher, not in the repo.
- Fixes: Gantt crash on overdue tasks; Kanban wiping JWT (T-023).
