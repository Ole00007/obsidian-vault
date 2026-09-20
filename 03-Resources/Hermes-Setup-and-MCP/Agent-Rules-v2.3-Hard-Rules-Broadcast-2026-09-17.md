---
title: Agent Rules v2.3 — Hard Rules Broadcast (single source of truth + reporting chain)
created: 2026-09-17
tags: [agent-rules, hermes, orchestration, cron, single-source-of-truth]
status: active
source: "Ole standing instruction 2026-09-17 (relayed via kanban t_228db57d, frontend-developer)"
project: "Hermes workspace"
---

# Agent Rules v2.3 — Hard Rules Broadcast (2026-09-17)

Ole set two new **permanent hard rules** for the whole agent roster, plus confirmed the daily
project-status mechanism. Operator-installer propagated them and fixed the cron that was supposed
to run the daily status. This note is the record of what changed and how it was verified.

## 1. The two new hard rules (now §9 in the rulebook)

1. **NO PARALLEL SOURCE OF TRUTH** — unless vitally necessary. When it genuinely is, the reason must
   be explained and flagged, and exactly one copy must be declared the authority (the other is
   *derived*, read-only).
2. **NO DUPLICATE REGISTRIES** — no second registry/config system for something that already has one.
   Extend the existing one.

Enforcement clause added with them: before creating any file/table/config/job, **search for the
existing one first**; found → update in place; fork → say so.

## 2. Reporting chain + daily status (now §10 in the rulebook)

- **operator-installer is the orchestrator.** Every agent working on the project reports to them and
  treats them as orchestrator. **Only Ole may overrule operator-installer.**
- If Ole gives an agent a direct instruction: the agent completes it, then reports to
  operator-installer noting it was done on Ole's direct request. operator-installer may reason and
  flag risks but does **not** overrule Ole's task.
- **operator-installer updates the LexFlow project status in the CRM (superadmin) DAILY** and
  **schedules unfinished tasks**.

## 3. Where the rules were written (one authority, then propagated)

| Target | What was done |
|---|---|
| `~/Obsidian/_Meta/AGENT_RULES.md` (symlink `~/Obsidian/AGENT_RULES.md`) | **The authority.** Added §9 + §10, bumped to **v2.3** |
| 23 × `~/.hermes/profiles/*/SOUL.md` | §9 + §10 appended |
| 1 × `~/.hermes/profiles/email-digest-agent/profile.yaml` | §9 + §10 appended to its `description` block |
| `~/.hermes/SOUL.md` (default instance) | §9 + §10 appended |

Verified: `grep -rl "## 9. Single Source of Truth" ~/.hermes/SOUL.md ~/.hermes/profiles/*/SOUL.md
~/.hermes/profiles/*/profile.yaml` → **24 files**.

## 4. Duplicates found and neutralised under the new rule

Two stale copies of the agent rules were sitting in the vault — a parallel source of truth:

- `03-Resources/Hermes-Setup-and-MCP/AGENT_RULES.md` — v2.0 (Aug 27)
- `03-Resources/Hermes-Setup-and-MCP/AGENT_RULES-v2.txt` — v2 draft (Aug 6)

Both were given a prominent **SUPERSEDED — DO NOT USE AS A RULE SOURCE** banner pointing at the
authority. Nothing was deleted (no-deletion rule); archive proposed to Ole.

## 5. Daily status cron — confirmed live (and repaired)

The job originally created for this existed in the **wrong profile**: frontend-developer's cron
store (`2573e20ab61f`). That profile **has no running gateway**, so the job could never fire — it was
registered but dead. It also duplicated the mechanism (a second registry of the same schedule).

- **Removed**: `2573e20ab61f` from `frontend-developer-lovable_react`.
- **Created** in the owning profile: `cda5f6d4a18a` — `lexflow-daily-status-crm`, `0 9 * * *`,
  deliver `telegram:1372207688`, toolsets terminal/file/search/kanban/skills. Next run
  **2026-09-18 09:00 CEST**.
- Scheduler verified: `hermes cron status` → gateway running (PID 12005, ticker heartbeat 11 s),
  8 active jobs.

## 6. Open warnings reported to Ole (not mine to fix silently)

- `lexflow-morning-plan` (dbe4783b4249) and `lexflow-morning-report` (f057d12934a7) last runs failed
  with `ImportError: _FULL_ARGS_LOG_BOUND` from `agent.message_sanitization` — re-checked at 12:00
  that symbol exists and imports cleanly, so this looks like a mid-update tree at 07:48/08:57 rather
  than a live bug. Re-check after the next fire.
- Telegram delivery failing from cron (`httpx.ConnectError: nodename nor servname provided`) on
  `lexflow-try-demo-daily-check`, `agent-roster-friday-kpi`, `lexflow-morning-report` — stale DNS in
  the long-running gateway process is the prime suspect; gateway restart recommended.
- `agent-roster-friday-kpi` also failed with `No access token found for Nous Portal login`.
- Only **two** profile gateways are running (`operator-installer`, `lexflow_dev_head_admin`); any
  cron job living in another profile can never fire.

## Links
- Parent: [[_Meta-INDEX]]
- Related: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[Agent-Profiles]]
- See also: [[LexFlow-INDEX]]
