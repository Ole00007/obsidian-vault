---
title: Hermes Cron Delivery Recovery — smoothy_op_dir (2026-11-06)
created: 2026-11-06
tags: [hermes, cron, infra, telegram, lexflow, incident]
project: infra
home: 03-Resources/
status: active
---

# Hermes Cron Delivery Recovery — smoothy_op_dir (2026-11-06)

Follow-up to card `t_8b6c6ca9` ("P1: all smoothy_op_dir cron deliveries dead 12 runs — Telegram
target has no bot token"). The P1 itself was closed on **2026-10-29**; this note records the
2026-11-06 re-verification plus the two defects that were still open in the same sweep.

## 1. P1 delivery death — verified closed, not assumed

| Claim (2026-10-29) | Verification (2026-11-06 21:58 CET) |
|---|---|
| `TELEGRAM_BOT_TOKEN` missing for the profile | present in `/Users/olesiarasing/.hermes/profiles/smoothy_op_dir/.env` (`grep -c '^TELEGRAM_BOT_TOKEN=.'` → 1) |
| gateway had no credentials | wired at `config.yaml:638` → `token: ${TELEGRAM_BOT_TOKEN}` |
| token valid | `GET api.telegram.org/bot<token>/getMe` → `ok:true`, bot `hermes_h3iqg5wnrw7ianba_bot` (id 8719769559) |
| jobs frozen until Monday | resumed Mon 2026-11-02 07:30 by one-shot job `2da4d7374e6e` (`cron-resume-monday.sh`, `repeat:1` → self-deleted, `state: completed`) |
| deliveries working | today's jobs ran **and delivered** — `cda5f6d4a18a` 09:06, `f057d12934a7` 09:15, `dbe4783b4249` 07:50, `6567cab17494` 09:09, `20b25bd341d5` 00:07: all `last_status: ok`, `last_delivery_error: null` |

Consequence resolved: the §10.3 daily LexFlow CRM status job **ran on 2026-11-06** (roadmap
`last_updated` = 2026-11-06, local commit `9af129c`, later `55b644b` — **not pushed**).

## 2. `bbde6d0665f4` (lexflow-try-demo-daily-check) — script hardened

Retry+backoff already existed from 2026-10-29 (3 attempts, 0/10/30 s). It was not enough: the
2026-11-06 09:01 run returned `000` on every probe while an unrelated DNS failure also killed the
three agent jobs at 08:58–09:01, so a host-level network blip was reported as a product
regression and burned 3 `failure_streak`.

Changed in `/Users/olesiarasing/.hermes/profiles/smoothy_op_dir/scripts/lexflow-try-demo-check.sh`:

- backoff widened to 4 attempts, `0/15/45/90 s`;
- **network-layer classifier**: if every CRM probe returns `000` AND a control URL
  (`api.telegram.org`) also returns `000`, the run prints a `WARN: NETWORK/DNS outage on this
  host`, appends a ledger line to `logs/lexflow-try-demo-check.log`, and exits **0** — a blip can
  no longer fake a regression;
- when at least one probe DOES get an HTTP status, the run still fails loudly (prod unreachable
  while the internet works is a real outage);
- **explicit prod-down signature**: `x-railway-fallback: true` / `railway-hikari` headers on
  `/health` add `PROD DOWN: Railway edge 404 'Application not found' — service/deployment missing
  on railway, not an app bug` to the failure list;
- probe URL/retry/backoff/log are env-overridable (`BASE_CRM`, `BASE_LP`, `CTRL_URL`,
  `PROBE_RETRIES`, `PROBE_BACKOFF`, `LEXFLOW_CHECK_LOG`) so the failure modes can be tested
  without editing the script; every exit path now writes the ledger.

Tests actually run (2026-11-06, real output, not narrated):
- all hosts invalid → `WARN NETWORK/DNS outage`, **exit 0**, ledger line written;
- CRM invalid + control OK → **exit 1** (correct: prod unreachable, network fine);
- live prod → **exit 1** with the six failures including the `PROD DOWN` line, 5.3 s runtime.

## 3. Stale frozen repo paths in cron prompts (AGENT_RULES §8)

- `dbe4783b4249` (lexflow-morning-plan): `~/Desktop/projects/services/LEGAL/lexflow-crm` →
  `~/projects/lexflow/lexflow-crm`.
- `f057d12934a7` (lexflow-morning-report): `/Users/olesiarasing/Desktop/projects/services/LEGAL/lexflow-crm`
  → `/Users/olesiarasing/projects/lexflow/lexflow-crm`.
- `cda5f6d4a18a` (lexflow-daily-status-crm): already corrected earlier the same evening (its old
  prompt pointed at `~/projects/lexflow-crm`, which is **not a git repo**; the real clone is
  `/Users/olesiarasing/projects/lexflow/lexflow-crm`, with `lexflow_hermes_v1` checked out in the
  `lexflow-crm-wt-merge` worktree).
- After the edits `grep -c 'Desktop/projects' cron/jobs.json` → **0**.

## 4. Still open (not this card's work)

- **P0 prod down**: `web-production-031a6.up.railway.app` returns Railway edge `404 Application
  not found` on `/`, `/health`, `/login?ws=lexflow` — day 3 of `P0-PROD-DOWN-REGRESSION-2026-11-04`,
  tracked as card `t_9f758266`, blocked on Ole's Railway access.
- **`59200151b7cc` (hindsight-weekly-sync)**: `failure_streak: 4`, last failure 2026-11-02
  `blocked_config: provider credential missing — No access token found for Nous Portal login`.
  `auth.json` was refreshed 2026-11-02 11:45 and agent cron runs succeed since, so the failure is
  stale; it should clear on the next run (Sun 2026-11-08 08:00) — if it does not, the Nous token
  refresh is not reaching this profile.
- **`hermes cron doctor` late-fire warnings** (5–52 min late): the ticker is healthy (`Ticker
  heartbeat: 37s ago`, and `cda5f6d4a18a` fired 3.3 s late today), so lateness tracks machine
  sleep/idle, not a scheduler defect.
- **`cda5f6d4a18a` interrupted at 11-05 09:06** (`waiting for model response, 561.7 s`) — model
  latency, not cron config; it succeeded the next day.

## Commands worth re-running next time

```bash
hermes cron status          # ticker alive? lateness?
hermes cron doctor          # per-job failures + delivery errors
hermes cron runs <job_id>   # durable run history with error text
hermes cron incidents       # grouped incidents; `incidents ack <id>` closes one
hermes cron edit <id> --prompt "$(cat /tmp/prompt.txt)"   # prompt fix (global --accept-hooks if hooks exist)
grep -c 'Desktop/projects' ~/.hermes/profiles/smoothy_op_dir/cron/jobs.json   # §8 regression guard
```

Files touched: `~/.hermes/profiles/smoothy_op_dir/scripts/lexflow-try-demo-check.sh`,
`~/.hermes/profiles/smoothy_op_dir/cron/jobs.json` (via `hermes cron edit`, jobs `dbe4783b4249`,
`f057d12934a7`), `~/.hermes/profiles/smoothy_op_dir/logs/lexflow-try-demo-check.log` (new ledger).
No secret value is recorded anywhere in this note — only key names and config line references.

## Links
- Parent: [[03-Resources]]
- Related: [[LexFlow-Project-Status]]
- Related: [[AGENT_RULES]]
