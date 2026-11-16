---
tags: [hermes-infra, gateway, troubleshooting, incident, runbook]
project: Hermes
home: 03-Resources/Hermes-Setup-and-MCP
---

# Hermes Fleet Stability Repair — 2026-11-16

Consolidated fix for the "constant self-repair, no real work" spiral. Four distinct root causes
were found and closed in one pass. Everything below was verified live, not assumed.

## 1. Leaked `HERMES_HOME` breaks every cross-profile call (the big one)

**Symptom:** `launch_credentials_unavailable (the frozen config credentials belong to another home)`
in the UI, and in Kanban workers:
`profile_parked (session authority database does not belong to the reserved profile …)`.

**Cause:** when `HERMES_HOME` is exported pointing at one profile dir
(e.g. `.../profiles/smoothy_op_dir`) and a command then targets a *different* profile, the child
can resolve the wrong session store / credential home. A running chat also freezes the
credentials+home it launched with, so replacing `config.yaml` under it invalidates that snapshot.

**Verified:** `hermes -p crm-outreach-agent chat -q …` failed with the parked error; the identical
call with `env -u HERMES_HOME` succeeded immediately.

**Fix:** wrapper `~/.hermes/bin/hx` — `hx <profile> <hermes args>` unsets `HERMES_HOME` then execs
`hermes -p <profile>`. Verified: `hx testy_tester --version` → exit 0.
**Rule:** never edit a profile's `config.yaml`/`.env` while a chat is open on it; never rely on an
exported `HERMES_HOME` for a cross-profile command.

## 2. Duplicate keys in `.env` (latent key flipping)

Root `.env` carried **two different `API_SERVER_KEY` values** (22-char `lex…` and 64-char `19d…`,
last wins) plus `HERMES_MAX_TOKENS` three times. Same duplicate in `admy_ceo` and `cron-sentinel`.

**Fix:** deduped keeping the last (effective) value, first-appearance order preserved, key set and
values asserted unchanged. Backups: `.env.bak-dedupe-20261116T180258`. Effective key is the 64-char one.

## 3. Kanban cards assigned to profiles that no longer exist

14 of 32 open cards pointed at dead profile names, so they could never dispatch:
`backend-dev`→`backy` (8), `memory-curator`→`memy` (3), `operator-installer`→`smoothy_op_dir` (2),
`frontend-developer-lovable_react`→`fronty` (1). Board now: smoothy_op_dir 13, backy 8, admy_ceo 4,
memy 4, crm-outreach-agent 2, fronty 1. Backup: `kanban.db.bak-reassign-20261116T180826`.

Fallback routing also re-aligned: `memy` had an `openrouter/anthropic/claude-haiku-4.5` fallback —
set to `[]` so the fleet rule holds (nous primary, **no** OpenRouter fallback until a spend cap exists).

## 4. Stale `operator-installer` paths in my own scripts

`profiles/smoothy_op_dir/scripts/obsidian-dedup-check.sh` and `obsidian-staging.sh` still wrote
logs to `profiles/operator-installer/logs/` (orphan dir). Repointed to `smoothy_op_dir`. Backups
kept as `*.bak-pathfix-*`.

## Verified state at end of pass

- Root + all 23 registered profiles: `model.provider: nous`, `fallback_providers: []`
  (memy included). Live inference confirmed on root, fronty, backy, admy_ceo, memy, crm-outreach-agent.
- `hermes gateway list` → every profile served by the one multiplexed host gateway (PID 67628,
  launchd `ai.hermes.gateway`), nothing parked.
- `hermes auth status nous` → logged in (root and profile homes).
- Dashboard restarted on current build, `127.0.0.1:9119` → HTTP 200.
- `hermes-agent` source HEAD `3b42157858`; no source file newer than the gateway process start →
  **no code skew** (the earlier "stale gateway" suspicion was wrong; the stale process was the dashboard).

## Open item (one manual command, outside the gateway)

`launchctl bootstrap` is blocked from inside a Hermes session by design. To make the dashboard
survive logout/crash, run **in a plain Terminal.app**, not in Hermes:

```
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.dashboard.plist
```

The plist `ai.hermes.dashboard` is already written and `plutil -lint` clean (KeepAlive on
non-zero exit, logs to `~/.hermes/logs/dashboard.launchd.*`). The gateway itself is already a
launchd service, so it already survives reboots.

## Links
- Parent: [[Hermes-Setup-and-MCP]]
- Related: [[2026-11-16]]
- Related: [[hermes_incident_report]]
