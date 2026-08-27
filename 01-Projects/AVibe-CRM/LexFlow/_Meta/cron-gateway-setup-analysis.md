# Cron Scheduler Setup: Standalone Daemon vs Gateway-Embedded

## Context

This document compares two approaches for running scheduled cron jobs in Hermes Agent, for use in:
- **Service offering documentation** (agency service description)
- **Customer Q&A** (what to recommend based on client needs)
- **Technical reference** (this analysis)

---

## Option 2: Standalone Cron Daemon (`hermes cron daemon`)

### What It Is

A single lightweight Python process that ticks once per minute, checks `next_run_at` for all scheduled jobs, fires due jobs, and sleeps. Can be run as a **macOS launchd agent** (auto-starts at login), a **systemd service** (Linux servers), or a simple background process.

### Resource Profile

| Metric | Value |
|--------|-------|
| RAM | ~50 MB |
| CPU | Near-zero between ticks |
| Dependencies | None (Hermes core only) |
| Persistence | launchd / systemd / nohup |

### Advantages

- **Dead simple** — one process, one thing to monitor
- **Minimal footprint** — your laptop or server won't notice it
- **No extra credentials** — no API keys, no platform configuration
- **Platform-agnostic** — works on macOS, Linux, Windows (WSL)
- **Launchd / systemd** — auto-starts on boot, restarts on crash
- **Silence is the feature** — for jobs whose output *is* the deliverable (files written, DB updated, data synced)

### Pitfalls

- **No push notifications** — you only know it ran by its effect (files appearing, API calls made)
- **Silent failures** — if the script errors, you discover it when you go looking for the result
- **Single point of failure tracking** — no built-in alerting

### Configuration

```bash
# Start in background (quick test)
hermes cron daemon &

# Install as macOS launchd agent
# Create ~/Library/LaunchAgents/com.hermes.cron.plist
# See reference below for plist template

# Install as systemd service (Linux)
# See reference below for systemd unit
```

**launchd plist template:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hermes.cron</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/ole/.hermes/hermes-agent/venv/bin/hermes</string>
        <string>--profile</string>
        <string>memory-curator</string>
        <string>cron</string>
        <string>daemon</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/ole/.hermes/logs/cron-daemon.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/ole/.hermes/logs/cron-daemon.log</string>
</dict>
</plist>
```

---

## Option 3: Gateway-Embedded Scheduler

### What It Is

The full Hermes gateway process — messaging platform adapters (Telegram, Discord, Slack, etc.) + kanban dispatcher + cron scheduler — running as one daemon. All three subsystems share the same process, configuration, and lifecycle.

### Resource Profile

| Metric | Value |
|--------|-------|
| RAM | ~200–400 MB |
| CPU | Low idle, spikes during platform reconnects |
| Dependencies | Full Hermes gateway stack |
| Persistence | launchd / systemd |

### Advantages

- **Cron results deliverable to Telegram, Discord, etc.** ("Stager ran ✅ — 3 files moved")
- **Central management** — one daemon does everything
- **Scalable infrastructure** — when you need more later (kanban boards, multi-platform messaging, event-driven triggers), it's already running
- **Health monitoring** — gateway logs, restart logic, crash recovery built in
- **Context sharing** — cron jobs can reference gateway-state (connected channels, active sessions)

### Pitfalls

- **Overkill for "run a Python script at 6 PM"** — you're loading all platform adapters you may not use
- **Requires API keys** for every connected platform (more secrets to manage)
- **More memory and network** — more things that can break
- **Dependency on platform availability** — if Telegram/Discord is down, the gateway may still run, but delivery degrades
- **Gateway config** is a learning curve if you only need cron

### Configuration

```bash
# Interactive setup (choose platforms)
hermes gateway setup

# Start foreground (for testing)
hermes gateway run

# Install as background service (uses launchd/systemd internally)
hermes gateway install
hermes gateway start
hermes gateway restart
hermes gateway stop
hermes gateway status
```

---

## Side-by-Side Comparison

| Criterion | Standalone Daemon (Option 2) | Gateway (Option 3) |
|-----------|------------------------------|-------------------|
| **Setup complexity** | 1 command + optional plist | Gateway setup + platform config + tokens |
| **Resource usage** | ~50 MB RAM | ~200–400 MB RAM |
| **Push notifications** | ❌ None | ✅ Telegram/Discord/Slack/etc. |
| **Best for** | Script-only jobs, silent background work | Jobs needing alerts, human-in-loop approval |
| **Persistence** | launchd/systemd | launchd/systemd |
| **Multi-platform** | No | Yes |
| **Restart recovery** | Manual (unless launchd) | Automatic (gateway has crash recovery) |
| **Learning curve** | Minimal | Medium (gateway config, platform tokens) |

---

## Decision Guide for Customer Onboarding

### Recommend Standalone Daemon (Option 2) when:

- The cron job **writes to a file, DB, or API** — its output *is* the deliverable
- The client is a **knowledge worker, freelancer, small team** — no ops infrastructure
- Only **1–3 cron jobs**, all script-based with no need for human review
- The client's priority is **"set and forget"** — minimal fuss
- No messaging platforms needed (no Telegram/Discord/Slack)

**Typical use cases:** Downloads stager, daily backup, log rotator, data sync, site crawler, file organizer, cache warmer.

### Recommend Gateway (Option 3) when:

- The cron job **needs to notify a person** ("Daily digest ready ✅", "New lead captured 🚨")
- The client already runs **gateway-connected platforms** (Telegram bot for client communication)
- **Multiple cron jobs** with different delivery targets
- Jobs need **human approval before acting** (approvals mode)
- The client is a **team or agency** with shared access through Telegram/Discord

**Typical use cases:** Daily briefing delivered to Telegram, sales lead alerts, system health notifications, approval-required maintenance tasks, multi-step deployment pipelines.

---

## Recommended Default for Our Agency

### Internal operations (default: **Gateway — Option 3**)

Reason: Our agency runs multiple profiles, Telegram-based team communication, and several cron jobs daily. One gateway process with embedded scheduler centralizes everything. The extra memory is worth the delivery infrastructure.

### Client deployments (recommend per case)

- **Small business / solo founder:** Standalone daemon + periodic email digest
- **Agency / team (2–10 people):** Gateway with shared Telegram bot for alerts
- **Enterprise / high-compliance:** Gateway with Discord + email + approval mode

---

## Frequently Asked Questions

**Q: Will the cron daemon drain my laptop battery?**  
A: No. It sleeps 99.9% of the time — a single `time.sleep(60)` tick loop. Even the gateway only uses measurable resources when actively processing a message or running a cron job.

**Q: Can I run both?**  
A: Yes, but unnecessary. The gateway already includes the scheduler. Running both would duplicate the tick loop and could cause double-firing if both processes pick up the same job.

**Q: What happens if my computer is off when a job is scheduled?**  
A: Hermes has a catchup window (default: half the job period, clamped to 2min–2h). If the job was scheduled while you were offline, it fires within that window after startup.

**Q: Do cron jobs survive a Hermes update?**  
A: Yes. Cron jobs are stored in the profile's `cron/jobs.py` (SQLite-backed), not in Hermes source code. Updating Hermes does not touch them.

**Q: Can I run cron jobs in a different profile?**  
A: Yes. Each profile has its own cron DB. A gateway running under `profile-a` only fires `profile-a`'s jobs. To fire jobs in `profile-b`, run a separate gateway or daemon for that profile.

---

## Technical Details

### How the Tick Loop Works

```
Every 60 seconds:
  1. Acquire file lock (~/.hermes/cron/.tick.lock)
  2. Query DB: SELECT * FROM jobs WHERE next_run_at <= NOW() AND enabled=1
  3. For each due job:
     a. Spawn subprocess with job's profile, skills, script
     b. Run with 3-minute hard timeout
     c. Record last_run_at, last_status in DB
     d. Calculate next_run_at from schedule + repeat
     e. Deliver result if delivery target is set
  4. Release lock
```

### Delivery Flow

```
Cron job runs → produces output (agent message or script stdout)
  → Gateway checks job.deliver field
  → If "local": save to session DB, no push
  → If "platform:chat_id": format message → push via platform adapter
  → If "all": fan out to every connected platform
```

### Cron Delivery Targets

| Value | Behavior |
|-------|----------|
| (omit / auto) | Auto-delivers to the current chat and topic |
| `local` | Save only, no delivery |
| `origin` | Same as auto |
| `all` | Fan out to every connected platform |
| `telegram:-1001234567890:17585` | Specific chat + thread |
| `discord:#engineering` | Named channel |
| `sms:+15551234567` | SMS number |

---

*Last updated: August 23, 2026 · Prepared for LexFlow agency operations*
## Links
- Parent: [[_Meta-INDEX]]
