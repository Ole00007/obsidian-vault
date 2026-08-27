---
name: agentic-orchestration-credits-mng
description: Design and operate low-cost, production-grade multimodal AI agent architectures using a no-code-glue stack (Hermes native orchestration with named agent roles, Obsidian memory, Airtable as client-facing hub, OpenRouter model routing, Composio tool connections, plus app-building tools Lovable/GitHub/Netlify/Hostinger). Use when the user asks to design agent architecture, manage AI credits/costs, set up cron-scheduled agents, coordinate agent swarms, plan build-test-deploy pipelines, or map business jobs (CRM, email digests, client response automation, marketing funnels, content cross-posting) to specific agents. Trigger phrases: "agentic architecture", "orchestration", "credit management", "Hermes agents", "agent swarm", "low cost AI stack", "build test deploy app with AI", "client automation".
license: MIT
metadata:
  space: Roles and skills
  domain: agentic-architecture
  stack: hermes, obsidian, airtable, openrouter, composio, lovable, github, netlify, hostinger
---

# Agentic Architecture: Orchestration & Credits Management

## When to Use This Skill

Use this skill whenever the user needs to:
- Design or refine a multi-agent AI architecture that must run at low cost and in production.
- Decide how to route tasks across AI models to minimize spend (credit management).
- Set up scheduled (cron) autonomous agent jobs.
- Coordinate multiple agents working on one shared mission (swarm), in parallel, with clear role ownership.
- Plan a build → test → deploy pipeline for an app using AI coding/UI tools.
- Map recurring business jobs (CRM, email digests, drafted-to-autonomous client replies, task management, marketing funnels, content creation and cross-channel posting) to specific agents and tools.
- Explain any of the above to a non-technical stakeholder or client using simple visuals and diagrams.

## Approved Stack

| Layer | Tool | Role |
|---|---|---|
| Orchestration (native) | Hermes Agent | Built-in agent flows, cron scheduler, and Agent Swarm — no separate workflow builder needed |
| Memory | Obsidian | Hermes' private notebook/vault — logs sessions, decisions, and lessons learned; NOT client-facing |
| Client-facing data hub | Airtable | CRM, task management, client zones, marketing data, forms, automations — where requests arrive and results land |
| Model routing / cost control | OpenRouter | Single API key, 500+ models, per-key credit limits with daily/weekly/monthly resets, ~5.5% fee, no markup |
| Tool connections | Composio | Secure auth + execution across Airtable and other apps; lets agents act, not just talk |
| App UI/full-stack builder | Lovable | AI-generated frontend + backend from plain-English specs, GitHub sync |
| Code versioning | GitHub | Stores and versions everything Lovable/Coder generates |
| Deployment | Netlify (primary) / Hostinger (domain/standard hosting) | Push-to-deploy previews and live sites; Hostinger for domains and simpler hosting needs |

Notion has been explicitly dropped from this stack — do not suggest it unless the user reintroduces it. "Orb" is a billing/monetization platform, not a hosting provider — do not confuse it with Netlify/Hostinger; only reintroduce Orb later if the user needs usage-based SaaS billing/metering.

Only introduce a separate visual workflow builder (e.g., Flowise) if the user explicitly needs a drag-and-drop canvas for non-Hermes team members. Default to Hermes-native orchestration first.

## Hermes Agent Roster (Named Roles)

Use this fixed roster and wake only the agent(s) needed per task — never run the full roster simultaneously, to keep cost low:

- **Installer** — sets up new tools, connectors, and permissions.
- **Orchestrator** — receives the mission, decides sequence, delegates in parallel to other agents.
- **Router** — picks the cheapest AI model capable of the task via OpenRouter.
- **Builder** — assembles workflows, drafts, and content.
- **Keeper** — writes/reads long-term memory into Obsidian; logs lessons learned each cycle.
- **Coder** — builds and updates apps via Lovable, commits to GitHub, coordinates deploys.
- **Ops** — monitors cron jobs, deployments, errors, and system health.
- **Personal Assistant** — handles email digests, drafted replies, reminders, light client support.

Recommended starting count: 3 active agents (Orchestrator, Router, Keeper) for a solo operator; expand to the full 8-role roster as app-building and client-response automation scale up. Never exceed the roster without a distinct, non-overlapping function for the new agent.

## Instructions

1. **Clarify the job type first** — architecture design, cost/credit question, cron automation, swarm coordination, app build-test-deploy, or business-job mapping (CRM, email, marketing, content). Each has a distinct default pattern (see references/patterns.md).
2. **Map every request through the master flow**: Client Request → Airtable (hub) → Hermes Orchestrator → OpenRouter (model routing) → Composio (tool actions) → Result back to Airtable, with Obsidian as Hermes' private memory attached to the Orchestrator/Keeper, never client-facing.
3. **Apply cost discipline by default**:
   - Set OpenRouter per-key credit limits with automatic resets before deploying any agent.
   - Route high-volume/low-stakes steps (formatting, routing, memory sync, digests) to cheap/fast models; reserve frontier models (Claude, GPT) for final reasoning or code generation only.
   - Wake only the specific named agent(s) required for a task — idle agents should not consume cycles or tokens.
   - State a rough monthly cost range whenever presenting an architecture to a client (baseline ~$40-70/month for the core stack, excluding app-hosting-specific costs).
4. **For cron/scheduled jobs**: use Hermes' built-in cron scheduler (natural-language schedules, one-shot or recurring). Standard jobs: morning email digest, weekly CRM cleanup, scheduled content posting, nightly backup/health checks. Flow: Timer → Hermes wakes the right agent → job runs → result saved to Airtable → Keeper logs to Obsidian.
5. **For multi-agent (swarm) tasks**: use Hermes Agent Swarm with the Orchestrator at the center delegating in parallel to Router, Builder, Keeper, Coder, Ops, and Personal Assistant as needed — all reading/writing the same Obsidian memory vault to avoid duplicated context.
6. **For build-test-deploy app projects**: Idea/Spec → Orchestrator assigns → Coder uses Lovable to generate UI/backend → GitHub stores/versions code → Netlify deploys preview/live (Hostinger for domain/standard hosting) → Ops monitors and reports → Keeper logs lessons in Obsidian → loop back to Idea/Spec for next iteration.
7. **For business-job mapping**, use this default ownership table:

| Business job | Primary agent | Where it lives |
|---|---|---|
| CRM / customer management | Personal Assistant + Router | Airtable |
| Email digest | Personal Assistant | Airtable + delivered via email |
| Drafted client replies (early stage) | Personal Assistant | Draft in Airtable, human approves |
| Fully autonomous client replies (later stage) | Personal Assistant + Orchestrator | Airtable, with Ops monitoring |
| Task management w/ scoped access | Orchestrator | Airtable (per-agent/per-human project zones) |
| Marketing funnels | Builder | Airtable + Composio-connected marketing tools |
| App development & maintenance | Coder + Ops | Lovable, GitHub, Netlify/Hostinger |
| Content creation & cross-channel posting | Builder | Airtable, scheduled via cron |

8. **When explaining to a non-technical audience**: use a plain-language analogy (e.g., restaurant order → host → chef → pantry → notebook → plate), always pair diagrams with a simple cost line, and keep the first client-facing slide high-level before showing the full agent roster.
9. **When the stack grows further**: slot new tools into existing stages rather than creating new orchestration layers — keep exactly one orchestration brain (Hermes).

## Naming Convention

Name the overall architecture around the messenger/relay theme set by Hermes (e.g., "Relay", "Hermeticon"). Keep individual agent names functional and plain (as in the roster above) rather than creative, so logs and cost dashboards stay scannable during debugging.

## Diagram Set (for client decks)

Produce these four diagrams in this order when building a client-facing deck:
1. Master Architecture — Airtable hub, Hermes Orchestrator, OpenRouter, Composio, Obsidian memory, with a cost banner.
2. Cron Circle — Timer → Hermes wakes agent → job runs → Airtable result → Obsidian log, with example job chips.
3. App-Building Circle — Idea/Spec → Coder/Lovable → GitHub → Netlify/Hostinger → Ops → Obsidian, looping back.
4. Parallel Swarm Map — Orchestrator at center, all 7 other roles branching around it, one sentence per role.

See references/patterns.md for full visual-explanation templates, references/cost-table.csv for baseline cost breakdown, and references/obsidian-vs-airtable.csv for the hub-choice comparison.

## Examples

**Input:** "How do I keep AI costs down while running several agents?"
**Output:** Recommend OpenRouter per-key credit limits + model tiering (cheap models for routine steps, frontier models only for final output), waking only the needed named agent, with a cost table showing per-component monthly estimates.

**Input:** "Set up a daily report agent."
**Output:** Configure a Hermes cron job for the Personal Assistant (natural-language schedule, e.g. "every morning at 8am"), write results to Airtable, log to Obsidian via Keeper.

**Input:** "I need to build and ship an app feature."
**Output:** Orchestrator assigns Coder to build in Lovable, push to GitHub, deploy via Netlify, Ops monitors, Keeper logs lessons — loop until stable.

**Input:** "How should client email replies be automated?"
**Output:** Start with Personal Assistant drafting replies for human approval in Airtable; graduate to full autonomy only after Ops confirms error rate is low enough, per job-mapping table above.

## Links
- Parent: [[agentic-orchestration-credits-mng-skill-INDEX]]
