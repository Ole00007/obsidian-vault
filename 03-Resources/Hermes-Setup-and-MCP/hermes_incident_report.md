# Hermes Agent Incident Report — Dashboard/Gateway Crash from VS Code Process Kill

## Date
2026-07-19

## Summary
While using VS Code (Claude Haiku) to clean up a stuck `hermes gateway restart` process,
the cleanup command killed more than intended — it took down the dashboard process and
the gateway's api_server connection along with it. This cascaded into a multi-hour recovery
effort involving stuck session locks, MCP server bloat, credit exhaustion, and a missing
profile-scoped environment variable.

## Root Cause Chain

1. **Trigger**: A `hermes gateway restart` command hung (PID 82326), holding a lock on
   `state.db`, which blocked `session.resume` for the LexFlow session.
2. **Overly broad kill**: VS Code's cleanup correctly killed PID 82326 (stuck restart) but
   also killed PID 30528 (`hermes dashboard`), which was a *healthy, unrelated* process
   holding harmless read locks — it did not need to die.
3. **Cascading effect**: With the dashboard process gone, `127.0.0.1:9119` became
   unreachable (`ERR_CONNECTION_REFUSED`), forcing a rebuild of the web UI on next launch
   (`vite build`, ~1.9MB bundle, one-time ~1-2 min delay).
4. **Separate, unrelated failure**: The gateway's `api_server` platform independently kept
   refusing to start with `API_SERVER_KEY is required`, even after the key was confirmed
   present in `~/.hermes/.env`. Root cause: launchd sets `HERMES_HOME` to the
   **profile-scoped** directory, so the gateway reads
   `~/.hermes/profiles/lexflow_dev_head_admin/.env`, not the global `~/.hermes/.env`. The
   key existed globally but was missing in the profile-scoped file.
5. **Compounding factor**: A mid-session profile rename
   (`lexflow_dev_project-owner` → `lexflow_dev_head_admin`) earlier in the day caused the
   dashboard's cached profile selector to point at a stale/nonexistent profile slug,
   independently causing "Chat unavailable" and empty Sessions views — unrelated to the
   process-kill incident, but compounding the confusion during debugging.

## Why This Was Hard to Diagnose Fast

- Multiple unrelated failures overlapped in time (profile rename UI bug, stuck lock,
  MCP server bloat, credit exhaustion, missing profile-scoped env var) — each needed to be
  isolated and fixed independently, but symptoms looked similar ("nothing responds").
- `hermes gateway status` and `hermes mcp list` reflect **cached/in-memory state**, not
  always the live file state — edits to `config.yaml` or `.env` don't take effect until a
  **full launchd unload/reload**, not just `hermes gateway restart`.
- Errors were split across two log files (`gateway.log` for info, `gateway.error.log` for
  errors) plus terminal stdout — easy to miss the actual blocking error if only checking one.

## Recommendations to Prevent Recurrence

1. **Never let an AI coding assistant (Copilot/Claude in VS Code) run broad process kills
   without listing every PID and its command line first.** Require explicit confirmation
   per-PID, not a batch kill — dashboard and gateway restart processes can look similar in
   `ps aux` output but serve very different roles.
2. **Never rename an active Hermes profile mid-session.** Finish or explicitly close out a
   session before renaming; the CLI-side data survives fine, but the dashboard's cached
   profile selector does not auto-refresh.
3. **After any manual edit to `config.yaml` or `.env` (global or profile-scoped), always do
   a full stop/start cycle, not just `restart`:**
   ```
   launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist
   launchctl load ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist
   ```
4. **Remember Hermes profiles are fully isolated** — env vars, MCP config, and secrets set
   globally in `~/.hermes/.env` do NOT propagate to `~/.hermes/profiles/<name>/.env`. Any
   key needed by a specific profile's gateway must be set in that profile's own `.env`.
5. **Keep dashboard and gateway as separate mental processes** — `hermes dashboard` serves
   the web UI only; `hermes gateway run` handles api_server, MCPs, and cron. Restarting one
   does not restart the other.

## Fastest Debug Sequence (Use This First, Every Time)

```bash
# 1. Confirm what's actually running
ps aux | grep hermes

# 2. Check gateway service state (launchd)
hermes gateway status --profile <profile>

# 3. Check both logs — error log first
tail -n 50 ~/.hermes/profiles/<profile>/logs/gateway.error.log
tail -n 30 ~/.hermes/profiles/<profile>/logs/gateway.log

# 4. Confirm env vars are in the PROFILE-scoped file, not just global
cat ~/.hermes/profiles/<profile>/.env | grep API_SERVER_KEY
cat ~/.hermes/.env | grep API_SERVER_KEY

# 5. If anything was edited (config.yaml or .env), always full-cycle restart:
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist
launchctl load ~/Library/LaunchAgents/ai.hermes.gateway-<profile>.plist

# 6. Re-verify
sleep 5 && tail -n 10 ~/.hermes/profiles/<profile>/logs/gateway.log
```

## Open Item (Not Yet Resolved as of This Report)

Dashboard "Resuming LexFlow Phase 3" summarize action still returns nothing after the
api_server fix was applied. Next diagnostic step: confirm the dashboard's browser session
is pointed at the correct, currently-running gateway instance (check for a second stale
dashboard process on a different port, or a browser-cached WebSocket connection to a dead
gateway PID).

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[Hermes-Setup-and-MCP-INDEX]]

---

# 2026-11-16 — Hermes fleet "No model providers are set up yet" (dashboard, all agents)

## Owners
Admy + Smothy (settings owners per `~/Obsidian/_Meta/AGENT_RULES.md` §20). This entry written by frontend-developer on Ole's request; config changes executed by smokey_op_dir.

## Symptoms
- Web dashboard (`http://127.0.0.1:9119`) chat showed: *"No model providers are set up yet. Add an API key under Keys or sign in to a provider under Models."* for every agent — even on a fresh chat (personal-assistant, others).
- Screenshot supplied by Ole 2026-11-16, 10:36.

## Root Cause (two defects)
1. **Stale dashboard process (the proximate cause):** PID 87942 had been running ~21h on pre-update code (`2bd378ed1b`) while the checkout on disk was `3b42157858`. `GET /api/model/options` (the exact call behind the model picker) returned `HTTP 503 {detail:"Restart required: …risk a stale-module crash"}` → picker refused → zero providers → empty-state message. An isolated control home proved that a keyless `openrouter` provider alone still returns catalog rows (unconfigured providers are appended), so the missing key was NOT the single cause.
2. **Config pointing at credential-less providers:** root `~/.hermes/config.yaml` had `model.provider: openrouter` but `~/.hermes/.env` has NO `OPENROUTER_API_KEY`; 10 profiles pointed at `google`/`openrouter` (keys absent on this host).

## Fix applied (smokey_op_dir, verified real output)
- Root + **22/22 profiles → `model.provider: nous`** (Nous Portal shared token is the credential that actually exists). Default models preserved, all validated against live Nous catalog. `agency-growth`'s dead model (`poolside/laguna-s-2.1:free`) fixed → `deepseek/deepseek-v4-flash`.
- Restarted dashboard on current code → PID 24389, port 9119, open-profile `smoothy_op_dir`.
- Verified: live API `/api/model/options` now returns `nous … usable=3 models=131` (root/seo-aeo-expert/smoothy_op_dir/sales-crm, 129–157 models each, no 503) + real inference smoke tests returned `NOUS_OK` / `LIVE_OK_*`.
- Cron drift: `agent-roster-friday-kpi` pointed at a deleted path (`operator-installer/scripts/…`), fixed to `smoothy_op_dir/scripts/…`, backup kept.
- No token copied anywhere, `~/.hermes/.env` untouched (mtime Aug 29), nothing deployed/pushed.

## 4 "orphan" profile dirs — NOT a bug
- `memory-curator` → pre-rename home of **`memy`** (renamed 2026-11-06). `operator-installer` → pre-rename home of **`smoothy_op_dir`**. `lexflow-crm-elisa` / `lexflow-intake-elisa` = dead empty shells (no logs, Oct 29).
- Recommendation (followed): do **not** `hermes profile create` these — duplicate identities + known "assignee memory-curator cannot be dispatched" failure. Their 9 cron jobs live in registered stores (`memy` ×2, `smoothy_op_dir` ×7) and are active.

## Open items (await Ole)
- R1: host gateway PID 67628 also on pre-update code (up 21h+); works (new sessions read config fresh) but should restart at the next maintenance window — restarting drops live sessions across all profiles. **Decision: restart at maintenance window (Ole 2026-11-16).**
- R2: add an OpenRouter API key (or hide the row) — **Decision: add key before/right after R1.**
