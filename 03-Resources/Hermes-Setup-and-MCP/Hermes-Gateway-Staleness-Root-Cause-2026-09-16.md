---
title: Hermes gateway staleness — single root cause of the Sep-16 cron failures
created: 2026-09-16
updated: 2026-09-16
tags: [hermes, cron, gateway, troubleshoot, operator-installer, evening]
status: verified
author: operator-installer
---

# Stale gateway = one root cause behind four "separate" failures

## Symptom set (as reported on the board)

`hermes cron doctor` listed four independent-looking failures:

| Job | Reported error |
|---|---|
| `lexflow-morning-plan` | `ImportError: cannot import name '_FULL_ARGS_LOG_BOUND' from 'agent.message_sanitization'` |
| `lexflow-morning-report` | same `ImportError` |
| `lexflow-try-demo-daily-check` | script exit 1 — `health=000`, `/login?ws=lexflow=000`, kanban checks 000 |
| all Telegram-delivering jobs | `httpx.ConnectError: [Errno 8] nodename nor servname provided` |

## Root cause (verified, not assumed)

**One stale process.** The whole estate's cron ticker runs *in-process* inside the
`operator-installer` gateway (`PID 12005`, started **Sun 2026-09-13 14:01**). The
`lexflow_dev_head_admin` gateway (`PID 12004`) is the only other gateway alive; every other
profile has no gateway.

Two consequences of a 3-day-old process:

1. **Old code in memory.** The `hermes-agent` working tree was updated by a `git pull` on
   **2026-09-15 11:42** (file mtime + `__pycache__` timestamps agree). That pull brought the
   commit that defines `_FULL_ARGS_LOG_BOUND` in `agent/message_sanitization.py:132`. Agent-mode
   cron jobs are executed inside the gateway process, whose in-memory module objects predate the
   pull, so a lazy `from agent.message_sanitization import _FULL_ARGS_LOG_BOUND` raises
   `ImportError` — even though the on-disk file defines it.
2. **Rotten resolver.** The same process can no longer resolve `api.telegram.org` (all external
   calls return `000`), while a **fresh** shell resolves it fine.

## Evidence

| Check | Result |
|---|---|
| `./venv/bin/python -c "from agent.message_sanitization import _FULL_ARGS_LOG_BOUND"` (fresh process) | `import OK 100000` |
| `git log -S_FULL_ARGS_LOG_BOUND` on `message_sanitization.py` | introduced by `1a02e8a793`, landed in the tree on the 09-15 pull |
| `dig +short api.telegram.org` + `curl https://api.telegram.org/` (fresh shell) | `149.154.166.110`, HTTP 302 |
| `curl -o /dev/null -w %{http_code} .../health` (fresh shell) | `health=200`, `login=200` |
| `bash scripts/lexflow-try-demo-check.sh` (fresh shell) | exit 0, no FAILURES block |
| Same checks inside the gateway (cron run 08:37) | `000` / DNS error / `ImportError` |

The script that "failed" the demo check is fine — it was executed by the stale parent, which is
why every one of its probes returned `000`.

## Fix

Restart that one gateway (`hermes gateway restart` on the `operator-installer` profile). It
re-execs a fresh process: current code on disk + a fresh resolver. No config change is needed, and
none of the four errors is a config error.

**Sequencing constraint:** the gateway is also the Kanban dispatcher, and it is the parent of
in-flight worker processes (e.g. the `t_62db7c26` review run, PID 30829, own PGID). Restart while
a worker is mid-run and that run is abandoned / at risk of a duplicate dispatch. Restart between
cards.

## Applied in the same pass (independent of the restart)

Two profile defaults were pointed at dead `:free` model IDs. Both were reproduced as HTTP 404
live, then replaced with smoke-tested models and re-verified by booting each profile once:

| Profile | Was | Now | Evidence |
|---|---|---|---|
| `lexflow_dev_head_admin` | `minimax/minimax-m3:free` | `deepseek/deepseek-v4.1-flash` (openrouter) | old ID → 404 "unavailable for free"; new ID → `OK` |
| `personal-assistant` | `tencent/hy3:free` (provider `nous`) | `google/gemini-3.5-flash` (provider switched to `openrouter`) | old ID → 404 "free period ended"; new ID → `OK` |

`personal-assistant` was doubly broken: its provider was `nous`, whose Portal auth is stale.

## Still open (needs Ole, not an agent)

- **Nous Portal re-authentication** — interactive (`hermes model`). Until then the `nous` provider
  (and therefore the "Nous primary" half of stack decision 1.4) does not answer, which also breaks
  the weekly `agent-roster-friday-kpi` job.
- Gateway restart scheduling — see above.
- `GITHUB_PERSONAL_ACCESS_TOKEN` and `COMPOSIO_API_KEY` are set in no profile, so the `github` MCP
  server and the `email-digest-06am` job remain inert.

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[Hermes-14-Day-Installation-Roadmap-2026-09-16]]
- Related: [[hermes-standing-rules]]
- Related: [[2026-09-16]]
