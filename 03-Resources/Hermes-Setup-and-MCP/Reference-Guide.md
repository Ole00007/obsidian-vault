# Reference Guide

## Overview

Quick reference materials, templates, external links, API documentation snippets, and reusable resources for common tasks.

## Quick Links

### Hermes Agent Documentation
- [Hermes Docs](https://hermes-agent.nousresearch.com/docs) — Official documentation
- [[Skills]] — Skill directory and usage
- [[Workflows/Obsidian-Config]] — Vault setup & integration

### External Services
- **Composio:** API Key: `ak_bKwRsbuMfghQTNqf39Em` (Active)
- **GitHub:** OAuth tokens — stored securely
- **Gmail:** Service account — stored securely
- **Notion:** API integration — see deployment logs

### Important Configs
- **Vault Path:** `~/Obsidian/_Hermes`
- **Env Var:** `OBSIDIAN_VAULT_PATH=/Users/olesiarasing/Obsidian/_Hermes`
- **Profile Location:** `~/.hermes/profiles/operator-installer/`
- **Memory Location:** `~/.hermes/profiles/operator-installer/memories/`

## Template: Setup Guide

```markdown
# [Service/Tool] Setup Guide

## Prerequisites
- [Requirement 1]
- [Requirement 2]

## Installation
1. Install package: [command]
2. Configure: [steps]
3. Verify: [verification command]

## Configuration
- Set env vars
- Update config files
- Authenticate

## Verification
Run: [command]
Expected output: [output]

## Troubleshooting
- **Issue:** Symptom → Fix
- **Issue:** Symptom → Fix
```

## Tier-1 OAuth Services (Composio)

14 verified services ready for integration:
1. Gmail
2. Google Drive
3. Google Calendar
4. Notion
5. GitHub
6. AWS
7. Asana
8. Figma
9. Linear
10. Stripe
11. Airtable
12. Atlassian
13. Canva
14. PayPal

See [[Workflows/Composio-Integration]] for integration playbook.

## Reference Documents

| Document | Link | Purpose |
|----------|------|---------|
| Composio Tier-1 Checklist | [[Reference/Tier1-Services]] | OAuth service audit |
| Email Digest Recipe | [[Reference/Email-Digest-Recipe]] | Production email setup |
| Agent Roster | [[Agents/Agent-Profiles]] | Agent directory |

---

See [[TOC]] for navigation.

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
