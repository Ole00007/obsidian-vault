# LexFlow — Deploy Verification 2026-10-27

## Status: LexFlow LIVE, but 14 commits NOT deployed

Ole reported LexFlow is live but not all changes are deployed. Verified via git + live probes.

## Deployed (origin/lexflow_hermes_v1 = 19b5401, deployed 2026-10-25)
- `/tasks` 200, `/api/context/notes` 401 (exists, auth-gated)

## NOT deployed (live probes 2026-10-27)
- `/gantt` 404
- `/api/roadmap` 404
- `/api/roadmap/bus` 404 ← agent-bus feature NOT live

## Root cause
Local `lexflow_hermes_v1` is **14 commits ahead of origin**, never pushed. Contains: Elisa rename/portrait, clickable dashboard cards, "← Main site", model-written summaries (opt-in OFF), responsible+agent-bus on graph/gantt/kanban (+GET /api/roadmap/bus), Kanban A–E blocked style, mobile overflow fixes, test fix.

## Gate
- Gate card `t_8fe36335` (push+deploy, Ole's go 2026-10-26) is **BLOCKED**.
- `feat/ui-elisa-nav` already merged into `lexflow_hermes_v1` (tip 396bea2).
- Deploy lock held by admy_ceo.

## Action taken
- Wrote message to backend-dev: `~/.hermes/profiles/backend-dev/cache/scratch/admy_contact_backend_20261027.md`
- Created kanban card `t_contact_bk_1027` (backend-dev, todo) to confirm push+deploy gate ready.

## Links
- [[LexFlow-Project-Status]]
- [[2026-10-27]]
