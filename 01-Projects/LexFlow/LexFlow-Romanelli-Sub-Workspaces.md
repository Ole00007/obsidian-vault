---
title: LexFlow — Romanelli sub-workspaces (2 for test) + uploads queue flag
created: 2026-08-30
updated: 2026-08-30
tags: [lexflow, sub-workspaces, multitenant, romanelli, uploads, queue]
status: DEPLOYED ✅
---

# LexFlow — Romanelli sub-workspaces (2 for test)

## What was built & deployed (commits `8084c8c` + fix `7e8e1d5`)
- **`workspaces.parent_workspace_id`** (self-FK, nullable) — additive; sub-workspaces are child spaces under a client workspace.
- Migration `e2f3a4b5c6d7` (batch mode, portable SQLite + Postgres).
- **`get_visible_workspace_ids()`** in `crm/workspace.py` — parent admin sees own + sub-workspaces; `workspace_filter` uses `.in_(ids)`; dashboard + kanban routes use visible ids.
- Seeded 2 sub-workspaces under `romanelli-studio` (3rd later):
  - `romanelli-cl1` — Romanelli Client 1 → `cl1@romanelli.test` / `cl10826`
  - `romanelli-cl2` — Romanelli Client 2 → `cl2@romanelli.test` / `cl20826`

## Critical prod fix learned
`db.create_all()` only creates **missing tables, not columns**. Prod Postgres predated the new column → boot 500. Fix: `_ensure_schema` now ALTERs `ADD COLUMN workspaces.parent_workspace_id` if missing, before seeding. Verified against a simulated old-schema DB.

## Verified (prod)
- Romanelli parent admin (`olesya00007@google.com`) → sees romanelli-studio + cl1 + cl2
- CL1 admin → only romanelli-cl1
- CL2 admin → only romanelli-cl2
- Superadmin → all

## Flagged on kanban (QUEUE — do not build)
- **uploads/ persistence**: on Railway the `web` service has no persistent volume → uploads on ephemeral disk, **wiped on every redeploy** (DB rows survive, files don't). Decision pending: **Option B** (object storage S3/R2) OR estimate **Hetzner migration**. Flagged as High/Infra case, status "Waiting Docs", due 2026-09-10. Not building until decided.

## Planning-only topics (no build yet)
1. Workers/agents inside Flask (Romanelli's control) — reasoning only.
2. Customer's Obsidian/Hindsight connect for doc context analysis.
3. Pre-trained context-analysis agent.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-MultiTenant-Test-Setup]], [[LexFlow-Workspace-UX-Overhaul]]
