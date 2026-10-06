---
title: LexFlow T-021 — Diagram View Spec (Obsidian Canvas style)
created: 2026-10-06
updated: 2026-10-06
tags: [lexflow, t-021, spec, diagram, obsidian-canvas]
status: spec
---

# LexFlow T-021 — Diagram View of Task/Case Execution

Roadmap id: **T-021** · Kanban card `t_f0f709f5` · Parent: T-019 (`t_bc68191b`).

## Direction (Ole, 2026-10-06)

- **Obsidian Canvas / graph style ONLY. NO n8n for now** — explicit steering, recorded on the card.
- **Spec-first**, then local implementation on Pagliano, then replicate.
- Design gate applies: no deploy before Ole's localhost review. Local only, NO push.

## Goal

A diagram view on the roadmap/kanban panel showing **who has what** in task/case
execution — nodes and edges, Obsidian-graph/Canvas style, instead of (or alongside)
the flat list/board.

## Reference look

- **Obsidian Canvas** (infinite canvas, node cards, arrows, groups) — the primary model.
- **Obsidian graph view** (force-directed nodes) — secondary, for the "who has what" overview.
- Advanced Canvas plugin (developer-mike/obsidian-advanced-canvas) for node shapes,
  collapsible groups, presentations — as a feature reference, not a dependency.

## Scope (spec)

1. **Node types** — what appears on the canvas:
   - Case / practice (the unit of work)
   - Task / sub-task
   - Person (assignee: lawyer, assistant, client)
   - Stage / status (intake → in-progress → closed)
   - Milestone / deadline
2. **Edges** — what connects nodes:
   - case → task (parent/child)
   - task → assignee (who)
   - case → stage (status)
   - task → task (dependency / next-step)
3. **Layouts**:
   - Canvas (free-form, draggable, grouped by stage)
   - Graph (auto-layout, force-directed, filterable by assignee/status)
4. **Interactions**:
   - Click node → open case/task detail
   - Drag to reorder / re-stage
   - Filter by assignee, status, urgency
   - Zoom / pan
5. **Data source** — the existing roadmap/kanban data (same store as the board),
   no new backend; pure frontend rendering of the same nodes.
6. **Tech** — vanilla JS / lightweight canvas lib (e.g. a small graph renderer),
   consistent with the existing single-file / no-build approach. No n8n.

## Open questions for Ole

- Canvas vs graph as the default view (or toggle)?
- Should the diagram replace the board or sit beside it as a second view?
- Node density limits (how many cases before it gets noisy)?

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Project-Status]]
- Related: [[LexFlow-Per-Employee-Kanban-Advisory-2026-09-16]]
