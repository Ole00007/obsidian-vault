---
name: agentic-orchestration-credits-mng
description: Design and operate low-cost, production-grade multimodal AI agent architectures using a no-code-glue stack (Hermes native orchestration, Obsidian memory, OpenRouter model routing, Composio tool connections, Airtable data hub). Use when the user asks to design agent architecture, manage AI credits/costs, set up cron-scheduled agents, coordinate agent swarms, or plan build-test-deploy pipelines for AI-powered apps. Trigger phrases: "agentic architecture", "orchestration", "credit management", "Hermes agents", "agent swarm", "low cost AI stack", "build test deploy app with AI".
license: MIT
metadata:
  space: Roles and skills
  domain: agentic-architecture
  stack: hermes, obsidian, openrouter, composio, airtable
---

# Agentic Architecture: Orchestration & Credits Management

## When to Use This Skill

Use this skill whenever the user needs to:
- Design or refine a multi-agent AI architecture that must run at low cost and in production.
- Decide how to route tasks across AI models to minimize spend (credit management).
- Set up scheduled (cron) autonomous agent jobs.
- Coordinate multiple agents working on one shared mission (swarm).
- Plan a build → test → deploy pipeline for an app using AI coding agents.
- Explain any of the above to a non-technical stakeholder or client using simple visuals.

## Default Stack (No-Code-Glue Philosophy)

Prefer the leanest stack that avoids adding unnecessary orchestration layers:

| Layer | Default Tool | Role |
|---|---|---|
| Orchestration (native) | Hermes Agent | Built-in agent flows, cron scheduler, and Agent Swarm — no separate workflow builder needed |
| Memory | Obsidian (as Hermes' notebook) | Local-first Markdown vault; Hermes reads/writes notes here for persistent context across sessions |
| Model routing / cost control | OpenRouter | Single API key, 500+ models, per-key credit limits with daily/weekly/monthly resets, ~5.5% fee, no markup |
| Tool connections | Composio | Secure auth + execution across Airtable and other apps; lets agents act, not just talk |
| Data hub / human interface | Airtable | Where requests originate and results land; the client-facing "control panel" |

Only introduce a separate visual builder (e.g., Flowise) if the user explicitly needs a drag-and-drop canvas for non-Hermes team members, or needs RAG/chatflow patterns Hermes doesn't cover natively. Default to Hermes-native orchestration first — it removes one full layer of cost and complexity versus Flowise + Hermes combined.

Prioritize introducing new stack pieces (Claude Pro/Code, OpenClaw, Codex, Oracle, etc.) as they specialize a single stage (e.g., Coding agent, Data/Ops agent) rather than duplicating orchestration — keep exactly one orchestration brain (Hermes) even as the roster of specialist tools grows.

## Instructions

1. **Clarify the job type first** — architecture design, cost/credit question, cron automation, swarm coordination, or build-test-deploy pipeline. Each has a different default pattern (see references/patterns.md).
2. **Map the request to the 5-step flow**: Request (Airtable) → Orchestrator (Hermes) → Model routing (OpenRouter) → Tool action (Composio) → Result (Airtable), with Obsidian as the memory layer Hermes reads/writes at every step.
3. **Apply cost discipline by default**:
   - Set OpenRouter per-key credit limits with automatic resets before deploying any agent.
   - Route high-volume/low-stakes steps (formatting, routing, memory sync) to cheap/fast models; reserve frontier models (Claude, GPT) for final reasoning or code generation only.
   - Estimate and state a rough monthly cost range (hosting + pay-per-task fees) whenever presenting an architecture to a client.
4. **For cron/scheduled jobs**: use Hermes' built-in cron scheduler (natural-language schedules, one-shot or recurring, can attach specific skills per job). Do not introduce external cron tools unless Hermes cron cannot reach the required system.
5. **For multi-agent (swarm) tasks**: use Hermes Agent Swarm — assign clear roles (Planner, Builder, Reviewer, Reporter) around one shared mission and one shared Obsidian memory vault. Cap the roster at the smallest number of roles that removes ambiguity (typically 3-5); avoid adding agents without a distinct function.
6. **For build-test-deploy app projects**: pipeline as Idea/Spec → Build (Claude Code / Codex) → Test → Fix loop (auto-retest) → Deploy, supervised end-to-end by Hermes, with progress logged to Obsidian.
7. **When explaining to a non-technical audience**: use a plain-language analogy (e.g., restaurant order → host → chef → pantry → notebook → plate) and always pair any architecture diagram with a simple cost table or cost banner.
8. **When the stack grows** (Claude Pro/Code, OpenClaw, Codex, Oracle incoming): slot new tools into existing stages rather than creating new orchestration layers — e.g., Codex/Claude Code plug into the "Build" stage, Oracle plugs into the "Data/Ops" stage.

## Naming Convention

Name the overall architecture around the messenger/relay theme already set by Hermes (e.g., "Relay", "Hermeticon"). Keep individual agent names functional and plain (Planner, Builder, Reviewer, Reporter, Router) rather than creative — this keeps logs and cost dashboards scannable during debugging.

## Examples

**Input:** "How do I keep AI costs down while running several agents?"
**Output:** Recommend OpenRouter per-key credit limits + model tiering (cheap models for routine steps, frontier models only for final output), with a cost table showing per-component monthly estimates.

**Input:** "Set up a daily report agent."
**Output:** Configure a Hermes cron job (natural-language schedule, e.g. "every morning at 8am"), attach the relevant skill, and have it write results to Airtable, logging to Obsidian.

**Input:** "I need multiple agents to build and ship a feature."
**Output:** Propose a Hermes Agent Swarm with Planner/Builder/Reviewer/Reporter roles sharing one Obsidian memory vault, feeding into a build-test-deploy pipeline.

See references/patterns.md for full visual-explanation templates and references/cost-table.csv for the baseline cost breakdown.

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[industry-competitive-analyst-skill (2)]]
