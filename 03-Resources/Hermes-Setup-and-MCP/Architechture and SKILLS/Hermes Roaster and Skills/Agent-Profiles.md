# Agent Profiles

## Overview

Central registry for all Hermes Agent profiles. Document capabilities, configuration, deployment status, and recent learnings for each agent.

## Agent Profile Template

```
---
Name: [Agent Name]
Profile: [Profile Path/ID]
Status: Active | Standby | Archived
Role(s): [e.g., ML Ops, Email, Content]
Created: [Date]
---

### Capabilities
- Skill 1: [[Skills/Skill-Name]]
- Skill 2: [[Skills/Skill-Name]]
- Integration: [External service]

### Configuration
- **Model:** [AI Model Used]
- **Tools:** [List of tools]
- **Env Vars:** [Key configs]
- **Cron Jobs:** [[Workflows/Cron-References]]

### Deployment
- **Location:** [Where deployed]
- **Credentials:** [Secure: Store separately]
- **Last Updated:** [Date]

### Notes
- [Key learning 1]
- [Key learning 2]

### Related
[[Projects/Relevant-Project]]
[[Workflows/Orchestration-Note]]
```

## Agent Roster

| Agent | Profile | Role | Status | Last Update |
|-------|---------|------|--------|-------------|
| tester | `tester` | QA & Regression Specialist — LexFlow gate (verdicts, pytest, browser E2E, tenant isolation) | Active | 2026-11-06 |
| [Agent 1] | default | General | Active | [Date] |
| [Agent 2] | specialty | Domain | Active | [Date] |

## Configured Profiles

### tester — QA & Regression Specialist (2026-11-06)
- **Profile dir:** `~/.hermes/profiles/tester` · config `config.yaml` (created 2026-11-06; the profile previously had `profile.yaml` only and could not boot)
- **Model:** `anthropic/claude-sonnet-5.5` (provider `nous`, `agent.reasoning_effort: high`, `agent.max_turns: 200`, `terminal.timeout: 300`)
- **Tools verified live:** `terminal`, `browser_exec`, `execute_code`, `read_file`, `web_search`
- **Skill:** `devops/qa-regression-playbook` — evidence-first gate procedure for LexFlow
- **Memory:** `memories/MEMORY.md` — verified baseline, working interpreter, tenant matrix, flag list, hard gates
- **Mission:** certify or refuse a build with a `VERDICT` block (PASS / PASS WITH GAPS / FAIL / BLOCKED), severity-ranked findings, absolute repo path + branch + HEAD SHA. Verifier, never shipper: no push, no deploy, no production mutation.
- **Standing gate:** staging smoke card T-025 (`t_fe4e8687`) · Reports to orchestrator `smoothy_op_dir`
- **Induction run 2026-11-06:** `python3 -m pytest tests/ -q --ignore=…` → 23 passed in 18.46s; both script-mode smokes `RESULT: ALL PASS`; surfaced two P3s (pytest discovery defect from module-level `sys.exit()`, and the Postgres-only `EXTRACT(YEAR FROM duedate)` heal SQL at `crm/__init__.py:461` failing harmlessly on SQLite).

## Recent Updates

- **Nov 6, 2026:** `tester` profile configured as the roster's QA gate (config.yaml + SOUL + MEMORY + qa-regression-playbook skill), induction run verified.
- **Jul 15, 2026:** Vault created for extended memory management
- Previous updates: See [[Knowledge/Skills-Log]]

---

See [[TOC]] for navigation.

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
