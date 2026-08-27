---
name: hermes-chatbot-builder
description: >
  Build, integrate, manage, and control AI chatbots using Hermes Agent as the
  core orchestrator. Covers profile/SOUL/memory config, chatbot platform selection,
  OpenRouter model assignment, webhook→LLM→response flows, multi-agent team
  orchestration, cron/swarm scheduling, and LLMOps monitoring. OpenRouter only.
  Trigger phrases: "set up chatbot", "configure Hermes", "orchestrate agents",
  "deploy bot", "manage agent team", "LLMOps", "webhook flow".
license: MIT
metadata:
  version: "1.1"
  updated: "2026-07"
  context: Hermes Agent v0.8+ · OpenRouter only · hotel/hospitality chatbots
---

# Hermes Chatbot Builder

## When to Use This Skill

- Creating/configuring Hermes profiles, SOUL.md, MEMORY.md, USER.md
- Selecting chatbot platforms (Voiceflow, Botpress, Typebot, n8n, GHL)
- Building webhook → LLM → response flows (Hermes-native, no Make.com)
- Designing multi-agent team with cost-optimised OpenRouter model assignments
- Scheduling cron jobs or swarm triggers
- LLMOps: monitoring, evaluating, improving running bots

---

## Instructions

### PHASE 0 — Orchestrator Bootstrap Prompt

Paste into a fresh Hermes session to self-configure the whole team:
```
You are the Hermes Orchestrator for a hotel chatbot system.
Set up 4 profiles (orchestrator, researcher, writer, cron-reporter),
assign each its approved OpenRouter model from PHASE 2, wire Telegram
gateway for orchestrator, then create the 5 core skills from PHASE 4.
Work sequentially, confirm each step. Never use unapproved models.
Start: hermes profile create researcher
```

### PHASE 1 — Create Profiles & Identities

```bash
hermes profile create orchestrator
hermes profile create researcher
hermes profile create writer
hermes profile create cron-reporter
```

**SOUL.md per profile (keep each ≤300 chars):**

`orchestrator`: Route every request to the right sub-agent. Delegate:
research→researcher, drafting→writer, reports→cron-reporter. Never answer
guest questions directly. Escalate to human on: anger, payment, booking
conflict. Language: IT/EN. Tone: warm, professional, concise.

`researcher`: Retrieve and summarise info from hotel CMS, web, PMS API.
Return structured JSON to orchestrator. Never write final guest replies.

`writer`: Receive researcher JSON. Craft final guest reply ≤120 words, IT/EN,
warm concierge tone. Never search web. Never call APIs.

`cron-reporter`: Run daily/weekly LLMOps analytics. Post digest to home
channel. Token cost, escalation rate, top missed intents. Be terse.

**MEMORY.md** (≤2200 chars): Hotel name/address, PMS API endpoint, CRM
webhook URL, check-in 14:00 / check-out 11:00, escalation Telegram handle.

### PHASE 2 — Assign OpenRouter Models

```bash
echo "OPENROUTER_API_KEY=sk-or-..." >> ~/.hermes/.env
orchestrator  config set model anthropic/claude-haiku-3-5
researcher    config set model deepseek/deepseek-v4-flash
writer        config set model google/gemini-flash-2-5
cron-reporter config set model meta-llama/llama-3.3-70b-instruct:free
```

**Approved model stack (OpenRouter only):**
| Role | Model slug | $/M in | $/M out |
|---|---|---|---|
| Orchestrator | `anthropic/claude-haiku-3-5` | $0.25 | $1.25 |
| Researcher | `deepseek/deepseek-v4-flash` | $0.03 | $0.29 |
| Writer | `google/gemini-flash-2-5` | $0.10 | $0.40 |
| Cron/Reports | `meta-llama/llama-3.3-70b-instruct:free` | $0 | $0 |
| QA on-flag only | `anthropic/claude-sonnet-4` | $3.00 | $15.00 |
| Fallback | `openrouter/auto` | varies | varies |

**config.yaml snippet** (same pattern for all profiles, change `default`):
```yaml
model:
  provider: openrouter
  default: anthropic/claude-haiku-3-5
  base_url: https://openrouter.ai/api/v1
agent:
  max_turns: 40
  reasoning_effort: low
approvals:
  mode: smart
auxiliary:
  compression:
    provider: openrouter
    model: google/gemini-flash-2-5
  title_generation:
    provider: openrouter
    model: meta-llama/llama-3.3-70b-instruct:free
  approval:
    provider: openrouter
    model: anthropic/claude-haiku-3-5
delegation:
  provider: openrouter
  model: deepseek/deepseek-v4-flash
  max_iterations: 30
fallback_providers:
  - provider: openrouter
    model: google/gemini-flash-2-5
  - provider: openrouter
    model: meta-llama/llama-3.3-70b-instruct:free
```

### PHASE 3 — Wire Orchestrator as Entry Point

**Telegram** (each profile = its own BotFather token):
```bash
orchestrator gateway setup   # select Telegram → paste token + numeric user ID
# adds to .env: TELEGRAM_BOT_TOKEN + TELEGRAM_ALLOWED_USERS
orchestrator gateway start
```

**Webhook** (for Voiceflow / Typebot / GHL widget):
```bash
orchestrator gateway setup   # select Webhooks → set HMAC secret
```
Flow: `POST /webhook` → HMAC validate → orchestrator parses intent →
`delegate_task` to sub-agent → JSON response back to platform.

Security rules (never skip):
- Always set `TELEGRAM_ALLOWED_USERS` — no open access
- Use `terminal.backend: docker` for gateway-facing profiles
- Set `approval_required: true` in skill frontmatter for booking/payment actions

### PHASE 4 — Core Skills Library

```bash
orchestrator skills create hotel-concierge   # FAQ, amenities, escalation
orchestrator skills create booking-flow      # dates/pax, PMS API, confirm/cancel
orchestrator skills create lead-capture      # name/email → CRM webhook
orchestrator skills create sentiment-guard   # anger detection → auto-escalate
orchestrator skills create llmops-reporter   # cost, error rate, missed intents
```
Set `approval_required: true` in booking-flow and lead-capture frontmatter.
Review auto-drafted skills: `orchestrator skills list --pending`
Promote: `orchestrator skills approve <name>`

### PHASE 5 — Cron & Swarm

```yaml
# ~/.hermes/profiles/cron-reporter/crons/daily-digest.yaml
schedule: "0 8 * * *"
task: "Run llmops-reporter. Post digest to Telegram home channel."
model: meta-llama/llama-3.3-70b-instruct:free

# Peak swarm — fork sessions for check-in rush
schedule: "0 14 * * *"
task: "Fork 3 orchestrator sessions for parallel guest handling."
```
Merge MEMORY.md nightly at 23:00. Verify: `orchestrator cron list`

### PHASE 6 — LLMOps Control

Weekly targets: <$0.01/session · escalation rate <15% · free-model use >40%

| Frequency | Action |
|---|---|
| Daily | `hermes status` — error logs + cost |
| Weekly | Top missed intents → new skills; promote GEPA variants |
| Monthly | Skill audit; prune unused; update SOUL.md |
| Quarterly | Model cost/quality re-benchmark on OpenRouter |

Hot-swap mid-session: `/model deepseek/deepseek-v4-flash --global`
Trigger QA: tag session `#audit` → fires claude/sonnet-4 review
Disable skill: `orchestrator skills disable <name>`

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[hermes-chatbot-builder]]
