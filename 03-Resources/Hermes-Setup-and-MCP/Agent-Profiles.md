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
| [Agent 1] | default | General | Active | [Date] |
| [Agent 2] | specialty | Domain | Active | [Date] |

## Recent Updates

- **Jul 15, 2026:** Vault created for extended memory management
- Previous updates: See [[Knowledge/Skills-Log]]

---

See [[TOC]] for navigation.

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
