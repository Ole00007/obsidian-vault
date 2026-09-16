# Agent Roster Consolidation — proposal (2026-09-16)

**Status:** PROPOSAL — awaiting Ole's approval. Nothing merged or deleted yet.
**Author:** operator-installer
**Trigger:** three roster profiles cannot boot (no model keys) and/or have no track record.

## Measured findings (evidence, not assumption)

Roster: 23 profiles. Session counts read from each profile's `state.db`; model chains from `config.yaml`.

Three profiles are **unusable as configured**:

| Profile | Sessions | Last active | Skills (unique) | Problem |
|---|---|---|---|---|
| `chatbot_builder` | 1 (169 msgs) | 2026-08-04 | 92 (2 unique) | no API keys in `.env` → cannot start |
| `email-digest-agent` | 0 | — | 59 (0 unique) | no API keys → cannot start; **owns the only cron job in the workspace** |
| `tester` | 0 | — | 59 (0 unique) | no keys, no model, no memories — a shell |

Also found (independent of the three):
- `memory-curator`, `lexflow_dev_head_admin`, `personal-assistant` all ran on dead `:free` models (`minimax-m3:free`, `gemma-3-27b-it:free`, `qwen3-4b:free`, `tencent/hy3:free`). **memory-curator failed a delegated run today with HTTP 404 "No endpoints found"** — its weekly cron jobs (vault-logging enforcer, self-improvement report) are silently failing. Fixed today: memory-curator → `deepseek/deepseek-v4.1-flash` + live fallback `anthropic/claude-haiku-4.5` (verified working).
- The **only cron job in the workspace** is `email-digest-06am` (enabled, 06:00 Europe/Rome) on `email-digest-agent` — a profile that cannot boot and has never produced output (`cron/output/` empty). It needs `COMPOSIO_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_HOME_CHANNEL`; none are present in that profile, and `COMPOSIO_API_KEY` exists in **no** profile `.env`.

## Proposed merges (best role fit + proven experience)

| Orphan | Merge into | Why (fit + experience) | What moves across |
|---|---|---|---|
| `chatbot_builder` | `frontend-developer-lovable_react` | owns the LexFlow marketing site and the Elisa/Lexy widget surfaces; 23 sessions, active 2026-09-15 | 2 unique skills (`chatbot/chatbot-intake`, `software-development/chatbot-widget`) + its `USER.md` LexFlow-chatbot context |
| `email-digest-agent` | `personal-assistant` | its mission IS a 06:00 daily brief ("proactively surface what needs attention today"); 18 sessions | the `email-digest-06am` cron job + required env names; nothing else is unique |
| `tester` | `backend-dev` | LexFlow code fixes + Railway validation = backend-dev's domain; 32 sessions, active 2026-09-15; already my code-review partner | nothing unique; fold in its mission text minus the ungated `git push` clause |

Alternates, if Ole prefers:
- `chatbot_builder` → `backend-dev` (if the chatbot becomes a CRM/server-side service, e.g. wired to `POST /api/public/intake`).
- `email-digest-agent` → `telegram-utility-agent` (has `TELEGRAM_BOT_TOKEN` today → least setup work; 9 sessions, last 2026-07-27).
- `tester` → `lexflow_dev_head_admin` (77 sessions = most experience, but dormant since 2026-08-06 and also on a dead model).

## What "merge" means concretely

1. Copy the orphan's unique skills/memories into the target profile.
2. Fold the orphan's role text into the target's `SOUL.md` / `MEMORY.md`.
3. Re-point or delete the orphan's cron job so it runs under the target profile.
4. Retire the orphan profile (`hermes profile delete <name>`) — **irreversible, needs Ole's explicit go**.

## Open questions for Ole

1. Approve the three mappings, or swap any for an alternate above?
2. `tester`: keep a standing QA function, or let backend-dev absorb it with a QA checklist skill?
3. `email-digest-agent` cron: revive it at all? It needs a Composio key that exists nowhere on this machine — SMTP/Gmail alternative may be cheaper.

## Links
- Parent: [[AVibe-Agency-INDEX]]
- Related: [[05-Daily-INDEX]]