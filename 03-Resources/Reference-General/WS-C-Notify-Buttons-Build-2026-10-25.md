# WS-C — Telegram + WhatsApp Notification Buttons (build log)

**Date:** 2026-10-25 · **Agent:** WS-C builder (for Ole) · **Branch:** `feat/notify-buttons` · **Commit:** `f6ee69a`
**Repo:** /Users/olesiarasing/projects/lexflow-crm-wt-notify (worktree)

## What was built
Deep-link-first Telegram/WhatsApp notification buttons for tasks (Gantt popup) and case/task pages,
behind feature flag `NOTIFY_BUTTONS_ENABLED` (default OFF).

- **Deep links (no token):** Telegram `t.me/<bot>?start=task<id>` + share link; WhatsApp `wa.me/<digits>?text=...`. Built server-side with strict sanitising (E.164 digits 7–15, control/newline stripping, length caps). No client PII in text — matter number + task title (+ due) only.
- **Real Telegram send:** Bot API `sendMessage` only, via a SEPARATE token (`LEXFLOW_TELEGRAM_BOT_TOKEN`), gated by a per-recipient consent record (`notify_consents`). No consent → 403; no token → 501; no chat id on file → 422. HTTP sender is injectable → tests never hit the network; token is never logged.
- **WhatsApp real send:** out of scope — stub raises `NotImplementedError` (Meta verification required).

## Endpoints (JWT, tenant-scoped via `workspace_filter`)
- `GET /api/notify/task/<id>/links`
- `POST /api/notify/task/<id>/send`
- `PUT /api/notify/consent`

## New files
`crm/models/notify_consent.py`, `crm/services/notify_links.py`, `crm/routes/notify.py`,
`static/js/notify/notify_buttons.js`, `static/css/notify/notify.css`,
`templates/partials/notify_buttons.html`, `tests/test_notify.py`.

## Tests
`49 passed, 0 failed — RESULT: ALL PASS` (link building, sanitising/injection, PII, tenant
isolation → 404, consent → 403, injected-sender payload + no token in logs, flag off → 404).

## Hand-off to backend-dev
Shared-file snippets (blueprint registration in `crm/__init__.py`, asset includes in Gantt
template) are in `scratch/handoff_C.md`. No `git push`, no deploy, no Postgres touched.

## Known gaps
Telegram `/start` chat-id capture flow not built (send needs a stored chat id); WhatsApp Cloud API
send pending Meta verification; recipients = firm team only (no `task_assignees` table on this branch).

## Links
- [[LexFlow-Platform-Plan-2026-10-24]]
- [[LexFlow CRM]]
