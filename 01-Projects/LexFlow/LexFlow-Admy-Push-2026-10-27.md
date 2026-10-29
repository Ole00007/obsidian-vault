# LexFlow — Admy Push + Deploy 2026-10-27

## Result: DEPLOYED ✅
Pushed `lexflow_hermes_v1` 19b5401..396bea2 (14 commits) → deploy 7354426195 success → prod /health 200.

## What went live
Elisa rename/portrait, clickable dashboard cards, "← Main site", model-written summaries (opt-in OFF), responsible+agent-bus on graph/gantt/kanban (+GET /api/roadmap/bus), Kanban A–E blocked style, mobile overflow fixes, test fix.

## Audits (all PASS)
- A: prod-style boot (fallback + with keys) all 5 endpoints 200
- B: tenant isolation — anon 401 on /api/roadmap/bus + /api/roadmap/graph; agent names gated to superadmin/lexflow
- C: push integrity (origin 19b5401 ancestor) + 45 tests passed

## Smoke
/login 200, / 200, /api/cases/ 200, /gantt 404, /graph 404, /agent 404 (flags OFF), /api/roadmap/bus anon 401 (route now live). Rollback NOT used.

## Links
- [[LexFlow-Project-Status]]
- [[2026-10-27]]
