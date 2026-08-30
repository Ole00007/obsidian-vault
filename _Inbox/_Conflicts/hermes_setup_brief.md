# Hermes / Claude / OpenRouter decision and installer brief

## Objective
Design a low-friction, cost-aware stack for LexFlow building first, while also supporting SEO/AEO client work, CRM and outreach automation, Telegram bot responses, and broader personal/professional workflows.

## Verified market facts
- Nous Portal Plus is a $20/month subscription tier with access to 300+ models, bundled tool usage, and about $22 in monthly credits.[cite:4]
- Nous public docs point users to a pricing/info page and indicate pricing details are available there.[cite:2]
- OpenRouter states that credit purchases carry a 5.5% fee with a $0.80 minimum, while inference pricing follows provider token pricing without markup.[cite:29]
- Public reporting on Claude Pro in 2026 is inconsistent: some sources state Claude Code is included in Pro at $20/month,[cite:17][cite:19] while other sources report temporary removal or changing eligibility in April 2026.[cite:18][cite:25]

## Recommendation
The default recommendation for a founder building LexFlow is a hybrid setup: start with Nous Plus as the primary agent workspace, then add OpenRouter top-ups only if credits become the bottleneck. This keeps orchestration, hosted tools, and multi-model experimentation in one place, while preserving a cheap overflow path for heavier coding or automation bursts.[cite:4][cite:29]

Claude Pro at $20/month is attractive only if the main daily workflow is centered on Claude chat and coding UX rather than Hermes-native orchestration. Because public 2026 reporting on Claude Code entitlement is inconsistent, any Claude-first decision should be validated directly in Anthropic pricing UI before purchase.[cite:17][cite:18][cite:19][cite:25]

## Option analysis

### 1.1 Nous Plus only
Best for a single-vendor setup with the fewest moving parts. The main strengths are broad model access, bundled tools, and low setup friction for agent workflows.[cite:4]

Weakness: monthly credits are likely sufficient for prototyping, orchestration experiments, and light production trials, but not for sustained heavy coding, scraping, or multi-agent automation at scale. Budget guardrails and workload separation remain necessary.

### 1.2 Claude subscription plus Hermes free
Best for users who primarily want Claude quality and a polished conversational UX. It is weaker as a complete multi-agent business operations stack unless additional API services, memory layers, and connectors are added.[cite:17][cite:19]

Weakness: the exact 2026 scope of Claude Code on the $20 plan is unclear from public sources, so this path carries avoidable plan-risk unless verified in-product.[cite:18][cite:25]

### 1.3 Hermes/OpenRouter top-up only
Best for maximum cost efficiency and model freedom. This route works well when tasks are explicitly routed: cheap models for classification, extraction, drafts, and routine CRM messaging; premium models only for difficult legal/product reasoning or complex code edits.[cite:22][cite:29]

Weakness: this is less seamless operationally because spend, routing, retries, and tool/provider behavior need active management.

### 1.4 Nous Plus plus OpenRouter overflow
This is the strongest balanced architecture. Nous handles the primary operator experience and hosted tools; OpenRouter handles burst capacity and model-specific routing when economics or availability favor another provider.[cite:4][cite:29]

This setup fits a founder with multiple concurrent workflows because it reduces vendor lock-in while avoiding a fragmented day-one stack.

### 1.5 Claude Pro plus OpenRouter, Hermes paid later
This is sensible only if coding and chat quality matter more in the first 1-2 months than agent orchestration, memory, skills, or Telegram/CRM automation. It can evolve into a stronger stack later, but it delays the architecture you ultimately described.

## Answer to the Railway question
A 20/month Nous Plus subscription should be enough to prototype orchestration, tool chains, and product logic without needing major Railway spend immediately, because model access and hosted tools are bundled into the platform subscription and credits.[cite:4] However, Railway still bills infrastructure for deployed apps, databases, background jobs, and traffic, so LexFlow staging or production workloads will not be covered by Nous alone.

A practical expectation is: minimal Railway spend is realistic for local development plus light staging, but not for sustained hosted environments with database, worker, and preview deployments. The AI subscription reduces separate AI tooling costs; it does not replace application hosting.

## Cancellation / termination
The public sources reviewed establish monthly pricing and credit structure for Nous and OpenRouter, but they do not fully verify cancellation terms from official billing policy pages in this research set.[cite:2][cite:4][cite:29] The safe working assumption for monthly subscriptions is that they can usually be stopped before the next billing cycle, but this should be verified inside each platform billing UI before subscribing.

For OpenRouter, the model is prepaid credits rather than a classic seat subscription, and public material emphasizes credit purchases and fees rather than lock-in term commitments.[cite:29] That generally means spend can be paused by not topping up, subject to any separate account or service terms.

## Multi-agent workflow architecture

### Roles
- **Founder Operator Agent**: central triage, routing, and daily command interface for tasks across LexFlow, SEO, outreach, and personal operations.
- **LexFlow Builder Agent**: product planning, code generation, architecture notes, documentation, test planning, and deployment checklists.
- **SEO/AEO Agent**: content briefs, schema opportunities, FAQ mining, landing page variants, entity mapping, and reporting.
- **CRM & Outreach Agent**: lead qualification, email drafts, sequence maintenance, CRM updates, meeting prep, and follow-up summaries.
- **Telegram Utility Agent**: handles simple requests, reminders, quick lookup, status checks, and forwarding tasks to specialist agents.
- **Memory Curator Agent**: updates durable project notes, customer context, reusable prompts, and operating preferences.

### Orchestration principles
- Keep one command agent at the top; avoid every agent calling every other agent.
- Separate "fast/cheap" and "deep/expensive" model routes.
- Use a memory write policy: only durable facts, decisions, credentials references, and repeatable workflows should be persisted.
- Use connector isolation: CRM, email, Telegram, docs, GitHub, and deployment credentials should be scoped per agent role where possible.

### Suggested routing
- Cheap models: classification, extraction, tags, short drafts, lead enrichment, SEO clustering.
- Mid-tier models: feature specs, PR reviews, campaign drafts, workflow design, customer messaging.
- Best models: legal logic, architecture trade-offs, critical code refactors, investor-facing writing.

## Installation plan
1. Create the primary Hermes workspace dedicated to LexFlow.
2. Create separate agent profiles for LexFlow, SEO/AEO, CRM/Outreach, Telegram Utility, and Memory Curator.
3. Connect core tools first: GitHub, browser/web tools, docs/drive, email, Telegram, CRM, and deployment targets.
4. Establish memory files and skill files before broad automation.
5. Configure model routing rules, cost ceilings, and failover providers.
6. Test with three end-to-end workflows: LexFlow feature ticket, SEO page brief, and Telegram inbound request.
7. Only then add autonomous schedules and background jobs.

## Files to prepare

### profile.md
Purpose: stable operator identity and constraints.

Suggested contents:
- owner name and role
- businesses/projects: LexFlow; client SEO/AEO; outreach/CRM; life admin
- tone and defaults
- budget rules
- approved tools/connectors
- escalation rules
- security boundaries

### memory.md
Purpose: durable facts and decisions only.

Suggested sections:
- projects and repositories
- environments and deployment URLs
- client identities and constraints
- lead stages and CRM taxonomy
- writing preferences
- recurring operating procedures
- do-not-forget items

### soul.md
Purpose: long-horizon behavior and decision style.

Suggested sections:
- mission hierarchy: build LexFlow first, protect focus, preserve optionality, minimize recurring spend
- non-negotiables: privacy, billing awareness, concise execution, no silent tool changes
- behavioral style: proactive, structured, founder-friendly, cost-aware
- failure mode handling: ask before destructive actions; fall back to cheaper model if premium route stalls

### skills
Suggested initial skills:
- repo-planning
- feature-spec-writer
- bug-triage
- deployment-checklist
- legal-tech-domain-notes
- seo-aeo-briefing
- crm-outreach-sequencing
- telegram-short-reply
- memory-curation
- cost-guardrails

## Prompt 1: Installer agent system prompt
```text
You are the Hermes Installer and Orchestration Setup Agent for a founder building LexFlow and running parallel SEO/AEO, CRM, outreach, Telegram utility, and daily operations workflows.

Primary objective: set up a low-friction, cost-aware multi-agent environment in Hermes with clean memory, role separation, connector hygiene, and explicit model-routing rules.

Constraints:
- Optimize for 20/month baseline spend, with optional overflow through pay-as-you-go credits.
- Keep LexFlow as the highest-priority workspace.
- Minimize setup friction and recurring paid tools.
- Default to cloud-hosted models and tools; do not require high local RAM.
- Never store secrets in memory files; only store secret references.
- Before any destructive or billing-affecting action, request confirmation.

Required outputs:
- workspace map
- agent list with responsibilities
- connector checklist
- memory structure
- skill list
- model routing policy
- test plan for three end-to-end workflows

Success criteria:
- Founder can start daily work from one primary control agent.
- Specialist agents are isolated but coordinated.
- Budget guardrails and fallback behavior are documented.
- Telegram utility path is defined.
```

## Prompt 2: Installer execution prompt
```text
Set up a Hermes-first multi-agent architecture for the following use case:
- Primary product: LexFlow legal-tech SaaS
- Additional workflows: SEO/AEO for client websites, CRM and email automation, sales outreach, social media support, daily personal/professional operations, Telegram bot responses

Tasks:
1. Create the agent architecture.
2. Define profile.md, memory.md, soul.md structures.
3. Propose the minimum viable connector set.
4. Define model-routing rules for cheap / standard / premium tasks.
5. Produce a 14-day installation roadmap.
6. Produce a testing checklist for LexFlow, SEO, CRM, and Telegram workflows.
7. Flag all areas where human confirmation is required.

Design goals:
- fastest path to useful daily operation
- minimal recurring cost
- low maintenance burden
- scalable to multiple projects and clients
- clear separation between memory, prompts, and skills
```

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[Claude_Hermes_Setup_Guide]]
