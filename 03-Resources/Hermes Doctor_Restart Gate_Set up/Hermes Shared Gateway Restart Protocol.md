---
title: Hermes Gateway — Consolidated Recovery and Setup Notes
created: 2026-11-07
updated: 2026-11-07
tags: [hermes, desktop, gateway, restart, recovery, troubleshoot]
status: active
---

# Hermes Gateway — Consolidated Recovery and Setup Notes

## Current setup and confirmed recovery

This Mac runs a shared Hermes host gateway under `launchd`, serving multiple
profiles. Hermes Desktop uses the local gateway; its backend profile is
`backend-dev`.

The command that restored the Desktop connection on 2026-11-07 was:

```bash
hermes --profile default gateway restart
```

After running it, the shared gateway took about six minutes to finish starting.
The profile-specific readiness check returned `ready`, the callback health check
returned HTTP 200, and Desktop logged `Hermes gateway is ready` followed by
`local: connection recovered`.

This was a confirmed successful recovery in this setup. Do not assume it is the
right restart command for every Hermes installation or profile topology.

## Recovery procedure for this Mac

1. In Hermes Desktop, open **Settings → Gateways → This window**, select
   **Local gateway**, and choose **Save and reconnect**.
2. If it remains disconnected, check for active work. A shared-host restart can
   interrupt live turns.
3. Run the host-level restart and let it finish normally:

   ```bash
   hermes --profile default gateway restart
   ```

4. Wait several minutes for all configured profiles and services to initialize.
   Do not issue repeated restarts just because Desktop's shorter timeout expires.
5. Verify the Desktop profile:

   ```bash
   hermes --profile backend-dev gateway ensure --json --timeout 90
   ```

   Continue when the result reports `"state": "ready"`. If the UI is still
   disconnected, inspect the current gateway status and recent Desktop/gateway
   logs, then retry **Save and reconnect**.

## Why these commands are not interchangeable

- `hermes --profile default gateway restart` is the host-level restart that
  recovered this shared-gateway setup.
- `hermes gateway restart` can restart only the currently selected profile
  through the host. In the 2026-11-07 recovery, it reported that
  `smoothy_op_dir` had restarted; it did not restart the shared host.
- `hermes gateway run` is for intentionally starting a foreground gateway. In
  this setup, it correctly declined to start a second gateway while the
  supervised host already owned the profiles.
- `hermes gateway ensure` is a readiness check for a profile; it is not itself
  a host restart.
- The `launchctl unload/load` instructions in an older incident report apply to
  that incident's profile-specific service and configuration changes. Do not
  copy those commands into this shared-host recovery without first verifying
  the current service configuration.

## Findings consolidated from related notes

| Note | What it documents | How it applies here |
|---|---|---|
| [[Hermes-Setup-and-MCP/Hermes-Gateway-Staleness-Root-Cause-2026-09-16]] | A long-running `operator-installer` gateway retained old imported code and stale DNS; restarting that specific profile fixed cron failures. | Demonstrates that a stale process can cause several apparently unrelated failures. Its `operator-installer` restart was for a different date and setup state, not the command to copy for this Desktop outage. |
| [[Hermes-Setup-and-MCP/hermes_incident_report]] | A July 2026 restart/cleanup incident involving an overly broad process kill, dashboard disruption, profile-scoped environment configuration, and a separate API-server failure. | Supports avoiding broad kills and separating dashboard, gateway, and profile configuration. Its profile-specific `launchctl` procedure is historical and not the current default. |
| [[Hermes-Setup-and-MCP/Agent-Rules-v2.3-Hard-Rules-Broadcast-2026-09-17]] | A Sep 2026 report that a long-running gateway was suspected of stale DNS and a restart was recommended. | Historical evidence for restarting a specific stale gateway; not a universal host-restart instruction. |
| [[Hermes-Setup-and-MCP/hermes-standing-rules]] | Project-specific advice to run `hermes gateway run` for the avibe-hindsight project. | Different project and operating mode. It conflicts with starting another foreground gateway here, where `launchd` already owns the shared host. |
| [[Hermes-Setup-and-MCP/2026-10-21-smoothy-op-dir-handover-and-open-blockers]] | An Oct 2026 operational handover covering Telegram delivery, MCP authorization, and profile-specific blockers; it reports the gateway healthy at that time. | Those platform/auth failures are separate from the Nov Desktop connection outage. A healthy gateway does not mean every integration is authenticated. |

## Safety and diagnosis

- Keep the installed `launchd` service as the single gateway owner. Do not start
  a second foreground gateway beside it.
- Never kill processes by a broad name or pattern. Inspect the exact PID and
  command first; the dashboard, gateway, and restart process are separate.
- Avoid force flags, `launchctl kickstart -k`, or manually killing the gateway
  as first-line recovery. Do not interrupt a normal startup.
- A `ready` profile, a running PID, and a connected Desktop are distinct
  signals. Check profile readiness and Desktop connection separately.
- When startup is slow, capture the time and inspect the newest relevant logs
  before taking further action. Do not expose `.env` contents, API keys, or bot
  tokens.
- Configuration edits to profile `.env` or `config.yaml` may require a service
  reload depending on how that installation loads its configuration. Diagnose
  and verify the actual service setup before choosing restart versus reload.

## Separate known issues

The Nov 7 review also found a duplicate Telegram bot credential between
`frontend-developer-lovable_react` and `smoothy_op_dir`, plus optional MCP
authorization/configuration warnings. These are separate from Desktop's local
gateway readiness. Do not change credentials as part of a gateway restart;
resolve the Telegram ownership question before editing either profile.
