---
title: LexFlow T-021 — Diagram View Spec (frontend, 2026-10-26)
created: 2026-10-26
updated: 2026-10-26
tags: [lexflow, t-021, spec, diagram, obsidian-canvas, frontend]
status: spec
---

# LexFlow T-021 — Diagram View of Task/Case Execution (frontend)

Roadmap id: **T-021** · Kanban card `t_f0f709f5` · Parent: T-019 (`t_bc68191b`).
Branch: `feat/t021-diagrams` (worktree `~/projects/lexflow/lexflow-crm-wt-t021`, off `feat/ui-elisa-nav @ 831e838`).

## Direction (Ole + backend-dev, 2026-10-26)

- **Obsidian Canvas / graph style ONLY. NO n8n.** Read-only, frontend-only.
- **Responsible manager/lawyer VISIBLE on both diagrams** — small letters, one colour per role.
- Backend is DONE + local (commit `b2423c2`): `GET /api/roadmap/graph` task nodes carry
  `data.responsible = [{name, role, role_label, color, inferred}]`; `GET /api/gantt/tasks` has `task.team[]`.
- **Spec-first**: 1-page spec + 2 layout options here, show Ole local screenshots BEFORE finalising.
- Design gate: no deploy before Ole's localhost review. Local only, NO push.

## Goal

A diagram view on the roadmap/kanban panel showing **who has what** in task/case execution —
nodes and edges, Obsidian-graph/Canvas style, readable by a lawyer in ~5 seconds:
Matter → Contact(client) → Tasks (owner, due, status colour) → Documents → Deadlines/Hearings,
with **BLOCKED / overdue clearly marked**. Click a node = open the task/matter.

## What is already built (base)

- `/graph` (canvas, `GRAPH_VIEW_ENABLED` flag) — Obsidian-style force-directed graph, today-status
  halos (overdue/today/active), blocked dashed ring + 🔒, type chips, search, local/today modes.
- `/gantt` (canvas, `GANTT_VIEW_ENABLED`) — Frappe-style timeline, role-coloured team tags.
- Data: `GET /api/roadmap/graph`, `GET /api/gantt/tasks`, `GET /api/context/notes` (superadmin).

## T-021 frontend work (this card)

1. **Responsible-role labels on graph task nodes** — DONE + committed (`b41d90b`):
   - Each task node draws a small label per responsible person in the role colour (font ~10px,
     truncated to 22 chars), shown when zoomed (k>0.9) or node selected/hovered.
   - `inferred=true` renders softer (alpha 0.6) — derived from assignee/matter owner, not explicit team.
   - **Roles legend** added to the graph sidebar: Case owner (amber #F5B942), Docs supply (cyan #38D6D0),
     Legal assistant (violet #B78CFF), Lawyer review (rose #FF6F91), inferred (soft grey).
   - Verified: graph endpoint returns `responsible`; canvas renders violet label (549px sampled);
     roles legend present (5 items); JS lint OK; dark theme.
2. **Per-matter execution diagram** (the "Harvey-like" view) — the remaining piece, spec below.

## Two layout options (for Ole to choose)

### Option A — Canvas (free-form, grouped by stage)
- Infinite canvas, node cards, arrows, collapsible groups by stage (intake → in-progress → closed).
- Drag to reorder/re-stage; zoom/pan; click node → open detail.
- Best for: a lawyer scanning a single matter's full lifecycle at a glance.

### Option B — Graph (auto-layout, force-directed)
- The existing `/graph` style: force-directed nodes, filterable by assignee/status/urgency.
- Best for: the "who has what" overview across many matters; already 80% built.

**Recommendation:** ship **B** (reuse existing `/graph`, add responsible labels — done) as the default,
and offer **A** as a toggle for single-matter deep-dive. Both read-only, no new dependency.

## Open questions for Ole

- Canvas (A) vs graph (B) as default, or a toggle?
- Should the diagram replace the board or sit beside it as a second view?
- Node density limit (how many matters before it gets noisy)?

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]
- Related: [[LexFlow-Project-Status]]
- Related: [[LexFlow-Gantt-Plan-v4-2]]
