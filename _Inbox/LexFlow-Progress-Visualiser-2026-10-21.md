---
title: Progress Visualiser — standalone React app (LexFlow data base)
created: 2026-10-21
tags: [lexflow, frontend, react, gantt, progress-visualiser, hermes-kanban]
card: t_7048b1a6
status: local-verified (committed, not pushed, not deployed)
---

# Progress Visualiser — standalone React app

Built the standalone **Progress Visualiser** (Kanban card `t_7048b1a6`) — a React + Vite app that
makes **any human's project progress visually obvious**, using the **LexFlow CRM roadmap as its data
base**, and renders how far the LexFlow Gantt work has actually progressed.

## What it is
- **React + Vite** SPA at `/Users/olesiarasing/projects/lexflow-crm/apps/progress-visualiser/`.
- Two views: **Pulse** (weighted-progress ring, stage bar, completed/in-flight/blocked counters,
  "done & shipped" highlight) and **Flow / Gantt** (kanban swimlane by stage + a completion-% Gantt).
- **Dateless by design** — the roadmap has no start/end dates, so the Gantt x-axis is **completion %**,
  not time. Nothing is invented. Backlog/blocked render as milestone diamonds; `depends_on` orders rows.
- A read-only task drawer (owner, priority, dependencies, blocks, notes). Dark/light toggle.
- **Project switcher** proves genericity: LexFlow roadmap ↔ a generic demo project ("Launch my blog").

## Data (single source of truth — AGENT_RULES §9)
- Authority = `lexflow-crm/docs/LexFlow_Agentic_Roadmap.json` (21 tasks, last_updated 2026-10-14).
- `scripts/sync-data.mjs` writes a **derived, labelled, read-only** snapshot (`_derived` block),
  regenerated on every predev/prebuild — never hand-edited, never written back.
- Optional live mode (`?crm=<url>`) probes `GET /api/gantt/tasks` and reports up/auth/down **honestly**.
  Production CRM is currently **404 (open_p0)**; the app does not depend on it to render.

## Separation from the in-CRM Gantt
This is the **standalone visualiser**. The **in-CRM Frappe Gantt** is roadmap **T-021** (card
`t_f0f709f5`), living on branch `feat/gantt-c` (`crm/routes/gantt.py`, `templates/gantt.html`,
`static/vendor/frappe-gantt/1.2.2`). Kept **linked, not duplicated**.

## Verification (measured)
- `npm run build` → clean (37 modules, 173 kB js / 57 kB gz). `npm run dev` and `npm run preview`
  both serve HTTP 200 on **http://localhost:5180/**.
- Rendered DOM (real browser): ring **41% weighted**, **4/21 completed**, **6 in-flight**, **1 blocked**
  — matches the roadmap exactly. Flow: **7 lanes, 21 Gantt rows (10 bars + 11 milestones)**, drawer opens.
- Contrast (dark theme): body text **16.31:1**, dim text **7.89:1** — both WCAG AAA.

## Git / deploy
- Repo `/Users/olesiarasing/projects/lexflow-crm`, branch **`feat/progress-visualiser`**
  (off `feat/gantt-c` 1e1a357), HEAD **62bf874**, 20 new files, additive only.
- **Not pushed, not deployed.** Cloudflare Workers (`wrangler.toml`) + Railway (`railway.json`)
  deploy plans prepared in `DEPLOY.md` — gated on Ole.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-CRM-Where-We-Stand-2026-10-10]]
- Related: [[LexFlow Frappe Gantt Hermes Plan v2]]
