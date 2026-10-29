---
title: Eliza in-app agent (LexFlow) — build note 2026-10-25
status: local, awaiting Ole review; NOT pushed
---
# Eliza — in-app assistant (floating bubble)

Branch `feat/wave2-agent`, worktree `/Users/olesiarasing/projects/lexflow-crm-wt-agent`, 6 local commits on top of `lexflow_hermes_v1` 682e1a5. Flag `AGENT_ENABLED` (default off → routes 404, no HTML).

- Purpose: helps the logged-in user with matters, documents, **tasks and agenda** — no lead capture (that is the website bot).
- UI: bottom-right bubble, `templates/_eliza_bubble.html`, `static/js/eliza/eliza.js`, `static/css/eliza/eliza.css` (textContent only, history in sessionStorage).
- API: `POST /api/agent/chat`, `POST /api/agent/chat/actions/<id>/approve|reject`.
- Tools: read (matters, tasks, calendar, gantt, docs) + approval-gated writes (create_task, create_calendar_event, update_task_status, flag_lawyer, draft_notification). Audit table `agent_audit`.
- Offline rule brain (EN+IT) by default; LLM brain via server env `LEXFLOW_AGENT_LLM_URL` only (client header ignored on chat — SSRF).
- Known side effect: calendar event with a matter notifies the client by email (existing behaviour); the approval card warns.
- Tests: `python3 -m pytest tests -q` → 33 passed (28 base + 5 agent).
- Fixed along the way: untracked spike was unregistered, seed script syntax error, tool results >4KB were truncated BEFORE filtering (list_matters returned empty on real data), test DB leakage into other suites.

## Links
- Parent: [[LexFlow-Reusable-Build-Protocol-2026-10-25]]
- Related: [[LexFlow-Wave1-Build-Log-Technical-2026-10-25]]
