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
