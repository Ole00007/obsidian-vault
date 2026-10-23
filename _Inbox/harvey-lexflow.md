# Harvey → LexFlow: Clean-Room Legal Agent Plan

## Executive View

Harvey is a proprietary legal AI platform, not a customer relationship management (CRM) system and not an open-source product that LexFlow can clone. The useful approach is a **clean-room functional reimplementation**: study public behavior and published architecture patterns, then build LexFlow-owned workflows, data structures, evaluations, and user experience without copying hidden code, protected content, branding, or confidential materials.

**Clean-room implementation:** rebuilding public capabilities from independent requirements and lawful open-source components. Example: implement cited document review from a written specification, not from Harvey source code.

## What Harvey Provides

| Layer | Publicly described capability | LexFlow interpretation |
|---|---|---|
| Assistant | Research, drafting, analysis and document-grounded answers | Matter-aware legal assistant with jurisdiction and source controls |
| Vault | Large document collections, search, review tables and cited reports | Case document workspace connected to LexFlow matters |
| Workflow Agents | Repeatable multi-step legal work using firm knowledge and playbooks | Hermes legal specialists launched from a case/task |
| Knowledge | Trusted external and firm-specific sources | Approved source registry with citation provenance |
| Shared Spaces | Governed collaboration around data, artifacts and tools | Client/counsel workspace with matter permissions and audit trail |
| Plan and review | Preview scope, approve plan, review outputs and citations | Human approval gates before legal work is finalized or sent |
| Command/analytics layer | Track agent adoption and outcomes | Run history, quality score, cost, latency, reviewer decision and failure reasons |

## What “Harness” Means

A harness is the operational system around a model: instructions, tools, source access, playbooks, examples, state, permissions, stop conditions, validation hooks, evaluation rubrics and human approval gates.

Harvey's public Legal Agent Benchmark (LAB) uses:

1. A partner-style instruction.
2. A synthetic client matter with source documents.
3. A required legal work product.
4. An expert-written rubric.
5. A sandboxed execution run.
6. Evaluation, written feedback and comparison reports.

The public Harvey repository is a benchmark and execution harness, not the Harvey commercial application or CRM source code.

## Relevant Links

### Harvey Official

- Website: https://www.harvey.ai/
- Agents: https://www.harvey.ai/platform/agents
- Vault: https://www.harvey.ai/platform/vault
- Getting started/product map: https://help.harvey.ai/articles/getting-started-with-harvey
- Vault developer API: https://developers.harvey.ai/guides/vault
- Official on-demand demo — litigation and transactional teams: https://www.harvey.ai/resources/webinars/live-demo-harvey-for-litigation-and-transactional-teams-oct2026
- Official on-demand demo — law firms: https://www.harvey.ai/resources/webinars/from-ai-adoption-to-ai-impact-live-demo-of-harvey-for-law-firms
- Harness/Spectre architecture article: https://www.harvey.ai/blog/building-spectre-internal-collaborative-cloud-agent-platform
- Legal Agent Benchmark announcement: https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark

### Video

- Harvey YouTube channel: https://www.youtube.com/@harvey-ai
- Official platform overview: https://www.youtube.com/watch?v=ydIT4EdLK54
- “How Harvey Works”: https://www.youtube.com/watch?v=92_ipeEdpU0
- Product briefing and feature demonstration: https://www.youtube.com/watch?v=LyIRPOqMWEM
- Agentic tax-analysis demonstration: https://www.youtube.com/watch?v=5P-6uvM6o5o
- Shared Vault tutorial: https://www.youtube.com/watch?v=KuZktjh6iAA
- Reliability/evaluation discussion: https://www.youtube.com/watch?v=kuXtW03cZEA

### GitHub and Benchmark

- Harvey GitHub organization: https://github.com/harveyai
- Harvey LAB repository: https://github.com/harveyai/harvey-labs
- LAB tutorial: https://github.com/harveyai/harvey-labs/blob/main/docs/tutorial.md
- LAB architecture: https://github.com/harveyai/harvey-labs/blob/main/docs/architecture.md

### Open Components to Evaluate

- OpenContracts repository: https://github.com/Open-Source-Legal/OpenContracts
- OpenContracts documentation: https://open-source-legal.github.io/OpenContracts/
- Open Source Legal organization: https://github.com/Open-Source-Legal
- LangGraph/LangChain open-source agent stack: https://www.langchain.com/oss-overview
- Example LangGraph legal reviewer: https://github.com/younisalazzeh/Legal_Document_Reviewer_Using_LangGraph-
- Example local contract pipeline: https://github.com/shaficse/langgraph-ollama-contract-review

## Best Open-Source Starting Point

OpenContracts is the strongest candidate for an evaluation spike, not an automatic dependency. It is self-hosted and MIT-licensed, and publicly describes document collections, PDF/DOCX ingestion, annotations, citations, structured extraction, AI agents, APIs, and an MCP server. Those features overlap with the document intelligence layer needed for a Harvey-like legal vertical.

Do **not** merge OpenContracts directly into LexFlow. First evaluate it as a separate, disposable service using synthetic documents. Its Python/Celery/GraphQL/React architecture may add considerable operational weight and may overlap with LexFlow's planned document, permission, repository, and worker layers.

## Major Milestones

### Milestone 0 — Define One Legal Job

Choose one narrow, monetizable and reviewable workflow, for example:

- Intake-to-case summary with missing-information flags.
- Contract clause extraction against an approved playbook.
- Matter chronology from uploaded documents.

Define jurisdiction, users, source types, output, prohibited behavior, escalation points and expert rubric. Do not start with a general “AI lawyer.”

### Milestone 1 — Clean-Room Architecture Spike

Compare three options with synthetic documents only:

1. Build a thin LexFlow-native document retrieval/evaluation layer.
2. Integrate OpenContracts as a separate bounded document-intelligence service.
3. Use selected OpenContracts components/patterns without adopting the full platform.

Measure setup effort, security boundary, citation quality, document parsing, permissions, API fit, hosting cost, maintenance and license obligations. No production integration yet.

### Milestone 2 — Legal Hermes Vertical

Create one lead Legal Hermes agent and bounded specialists. The browser must call the LexFlow Railway API; it must never call the model provider directly. A run should be attached to a LexFlow case and include:

- approved case documents and legal sources
- plan preview and user approval
- matter-scoped tools and credentials
- citations to source passages
- structured deliverable
- uncertainty and escalation flags
- immutable run/audit record
- lawyer review before external use

Do not give agents unrestricted database access. LexFlow repositories/API boundaries remain the only path to system-of-record data.

### Milestone 3 — Eval Harness

Adapt Harvey LAB's public pattern for LexFlow:

- task instruction
- synthetic matter pack
- expected deliverable
- expert rubric
- isolated run
- evaluator and written feedback
- human review and disagreement tracking
- regression report across model/harness versions

Start with 5–10 synthetic tasks for one workflow. A passing automated grade never replaces lawyer approval.

### Milestone 4 — CRM Integration Pilot

Expose the workflow inside one case screen behind a feature flag. Store run metadata, citations, artifact versions, reviewer decision, latency and cost. Use staging, synthetic matters and role-based permissions first. Production requires privacy/security review, retention rules, incident logging and a rollback path.

## Architecture Guardrails

- Do not market the result as Harvey or copy Harvey branding, hidden prompts, proprietary workflows or UI assets.
- Do not scrape gated content or attempt to obtain private source code.
- Use synthetic or expressly authorized documents during development.
- Keep each matter isolated; apply least-privilege access.
- Require citations and distinguish retrieved facts from model analysis.
- Require human approval for legal conclusions, filing, sending, deletion and CRM record mutation.
- Version prompts, tools, rubrics and model configuration so every result is reproducible.
- Treat evaluation data separately from production client data.
- Add one workflow at a time; do not build the full Harvey surface before product validation.

## First Hermes Research Prompt

Use this for a research/architecture spike only. No integration or code changes yet.

```text
CONTEXT

We want a clean-room, Harvey-like legal agent vertical for LexFlow CRM. Harvey is proprietary; its public harvey-labs repository is an evaluation benchmark/harness, not application source. We must not copy branding, hidden prompts, proprietary content, or gated behavior.

LexFlow's current stack and schema must be verified from active repo instructions plus the latest approved Master Plan and Flask Starter. Do not invent schema or choose Flask/Node independently.

TASK

Produce a build-vs-integrate technical spike for one candidate workflow:
[INSERT ONE WORKFLOW]

Research and compare:
1. A thin LexFlow-native implementation.
2. OpenContracts as a separate bounded service.
3. Selective reuse of lawful OpenContracts patterns/components.
4. Harvey LAB as evaluation methodology only.

For each option assess:
- exact features reusable
- architecture and runtime
- API/MCP boundaries
- document formats and citation provenance
- permissions and matter isolation
- license and commercial-use implications
- deployment services and estimated operational weight
- overlap with LexFlow
- security/privacy risks
- expected implementation stages
- rollback and exit cost

CONSTRAINTS
- Research and documentation only; no clone, install, edits, dependency changes, schema work, deployment, or secrets.
- Use official repositories/docs as primary sources.
- Do not use production/client documents.
- Treat browser-to-provider calls as prohibited; all agent calls must go through the LexFlow backend.
- All system-of-record database access must follow the approved LexFlow backend/repository boundary.
- If current stack documents conflict, report the conflict and stop before proposing integration paths that depend on it.

DELIVERABLE
Create `docs/research/harvey-like-legal-agent-spike.md` only if that path matches repo conventions; otherwise propose a path first.
Include:
- recommendation with rule
- system diagram
- data flow and trust boundaries
- milestone plan: Now / Next / Later
- 5–10 synthetic evaluation tasks and draft rubric categories
- open decisions requiring the user or a lawyer
- explicit “do not build yet” list
- sources with direct links

VERIFICATION
Run Перекрёстный тест: have an independent reviewer challenge the recommendation for licensing, security, stack overlap, hallucination risk, and unnecessary complexity.

End exactly:
Done | [research completed]
Next | [one approval/action]
Risks | [remaining risks]
```
