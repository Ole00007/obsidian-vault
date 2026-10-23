# LexFlow Stack Decision and Agent Continuity

## Immediate Decision

Do **not** let each agent choose Flask, Next.js, or a Node.js API case by case. Flexibility is safe only at service boundaries decided by architecture; it is unsafe when agents independently choose competing backends for the same feature.

The latest approved Master Plan explicitly says:

- Flask is the active backend for the current MVP sprint.
- The Node.js/TypeScript service under `apps/api` is paused.
- Lovable/React is the frontend and calls the Flask API.
- Node migration is evaluated only after the Flask CRM ships and is tested.
- Flask files must not be mixed into `apps/api`.

`CLAUDE.md` describes the long-term Next.js + Node.js/TypeScript monorepo, so it is a target architecture, not permission to build a duplicate API during this sprint. Before implementation resumes, a repo-and-deployment audit must confirm that the Master Plan still matches the real code and live Railway services.

## Technology Map

| Technology | What it is | Best LexFlow role | Compatible with | Duplication risk |
|---|---|---|---|---|
| Flask | A Python web framework for APIs and server-rendered pages | Current MVP API and existing Railway backend | React, Next.js, PostgreSQL, Python AI/document libraries | High if a Node API implements the same routes or writes the same domain data |
| Node.js | A JavaScript/TypeScript server runtime, not a UI framework | Possible future API/worker runtime | Next.js, React, PostgreSQL | High if it becomes a second general backend beside Flask |
| Next.js | A React framework for frontend pages plus optional server/API features; it normally runs on Node.js | Main CRM web frontend; optional thin browser-facing server layer | Flask API or Node API | High if Next API routes duplicate Flask business logic |
| React/Lovable | Browser user-interface layer | CRM screens and landing/app UI | Flask API or Node API | Low if it remains UI-only |
| PostgreSQL | Shared relational database | System of record | Flask or Node | Severe if two backends own migrations and business rules without one governance model |

## Compatibility Rule

**YES:** Next.js frontend → Flask API → PostgreSQL.

**YES:** Next.js frontend → Node.js API → PostgreSQL, after a controlled migration decision.

**DEPENDS:** Flask and Node can coexist only when each has a named, non-overlapping responsibility. Example: Flask remains the legacy CRM API while a separate Node worker handles one bounded integration through an approved interface.

**NO:** Agents freely implement the same contacts, cases, auth, migration, or payment feature in whichever backend they prefer.

## Recommended Path

### Now

1. Preserve the working Flask service; no rewrite.
2. Audit the repository, branches, Railway services, route map, migration heads, frontend calls, and live deployment commit SHAs.
3. Record one Architecture Decision Record (ADR): “Flask active for MVP sprint; Node API paused; Next/React may consume Flask API.”
4. Correct `CLAUDE.md` only after the audit and user approval so it distinguishes **current** and **target** architecture.

**ADR:** Architecture Decision Record, a short file recording one technical choice and why. Example: `docs/adr/0001-active-backend.md`.

### Next

Ship and stabilize the Flask CRM slice using the approved Plan and Flask Starter schema. Add no new Node domain API and do not move schema ownership.

### Later

After the MVP is stable, compare “keep Flask” with “migrate to Node” using measured criteria: delivery time, defects, agent reliability, operational cost, tests, and migration risk. If Node wins, migrate one bounded domain at a time using API compatibility tests; never run two uncontrolled migration systems against production.

## Updated Role Split

| Participant | Primary role | Continuity rule |
|---|---|---|
| User | Product owner and final approver | Approves architecture, production, deletion, protected areas, and final merge |
| Perplexity | Research, strategy, architecture options, specifications, acceptance criteria, independent review | Does not compete with Hermes execution |
| Hermes lead crew: Smooth, Admy, Ole00007 PA | Primary orchestrators with durable context; delegate to specialist Hermes agents | Own the canonical task, handoff, branch, evidence, and resumption state |
| Hermes specialist agents | Primary implementation, QA, deployment, and specialist work | Work under lead-agent scope and governance |
| VS Code harness agent | Support and operational fallback; also fast repo-local coding, setup, tests, review, and recovery | Takes over a blocked Hermes task from a written handoff, finishes it on the same approved branch/scope, then returns evidence for Hermes or user approval |
| Reviewer | Independent Перекрёстный тест | Must not be the same run that authored the change for critical work |

VS Code is not restricted to deployment. It must be capable of completing a Hermes task when Hermes fails after an update, reaches a service limit, crashes, or becomes unavailable. It may not silently redesign the task, create a parallel architecture, or merge to `main`.

## Prompt 1 — Stack Audit

Use first. It is read-only and makes no architecture changes.

```text
CONTEXT

LexFlow has conflicting architecture documents:
- The latest approved Master Plan says Flask is ACTIVE for the MVP sprint and Node apps/api is PAUSED.
- The Flask Starter contains the approved current/next relationship schema.
- CLAUDE.md describes a long-term Next.js + Node.js/TypeScript monorepo.
- Older handoffs and memories are evidence only, not authority.

Do not assume which stack is actually deployed. Verify the repository and live configuration. Do not edit, install, migrate, commit, push, or deploy.

TASK

Perform a read-only Architecture Truth Audit.

1. Identify the repository root, remotes, branches, current branch, status, and latest commit.
2. Inventory actual framework/runtime evidence:
   - Flask/Python entrypoints, requirements, routes, models, migrations, tests
   - Next.js/React files, package manifests, pages/routes, build config
   - Node.js/TypeScript API files, package manifests, routes, repositories, migrations, tests
3. Map each frontend to the API URL/routes it actually calls.
4. Inventory Railway/Netlify/Cloudflare configuration files and report which service each appears to deploy. Do not access or print secret values.
5. Compare repository evidence with:
   - LexTaskFlow_Master_Plan_v4_UPDATED.xlsx
   - LexFlow_Flask_Starter_UPDATED.md
   - CLAUDE.md
   - lexflow_handoff_v3.md
6. Determine whether Flask and Node currently duplicate any route, domain logic, schema model, migration ownership, auth, webhook, or background job.
7. Produce:
   - current-state architecture diagram in Mermaid
   - route/service ownership table
   - conflict table: document claim vs repository evidence vs deployment evidence
   - protected areas and risks
   - recommendation: keep Flask sprint, switch to Node now, or controlled coexistence
8. Do not make the final decision for me. Give a rule-based recommendation and the smallest safe next step.

SCHEMA GOVERNANCE
For fields and relationships, use only the latest approved Master Plan plus latest Flask Starter. If they conflict or omit a field, stop and flag it; do not invent it.

VERIFICATION
Run Перекрёстный тест by checking every architecture conclusion against at least two independent forms of evidence where available, such as source file + package manifest, or source file + deploy config.

DELIVERABLE
Save only the report as `docs/audits/architecture-truth-audit.md` if that path already fits repository conventions; otherwise propose the path and wait. No other changes.

End exactly:
Done | [audit completed]
Next | [one decision/action]
Risks | [remaining risks]
```

## Prompt 2 — Decision Recording

Use only after reviewing Prompt 1 and selecting the active architecture.

```text
CONTEXT

The user has reviewed `architecture-truth-audit.md` and selected this decision:

[PASTE THE USER'S DECISION HERE]

TASK

Prepare a surgical documentation-only patch that makes current and target architecture unambiguous.

1. Back up every file to be edited and verify backups.
2. Create one ADR recording:
   - current frontend
   - current backend and database owner
   - paused/deprecated components
   - permitted coexistence boundaries
   - migration trigger, if any
   - rollback/review date
3. Update CLAUDE.md with separate “Current Architecture” and “Target Architecture” sections.
4. Mark conflicting older handoff statements as superseded; do not delete history.
5. Do not change application code, schema, migrations, dependencies, deployment settings, auth, payments, or secrets.
6. Show the diff and run Перекрёстный тест against the approved Master Plan, Flask Starter, and audit.
7. Create one reversible documentation commit on an isolated branch. Do not push or merge until the user approves the diff.

END REPORT
List backups, files changed, commit, verification, conflicts still open, and rollback.

End exactly:
Done | [result]
Next | [one action]
Risks | [remaining risks or None]
```

## Prompt 3 — VS Code Takeover

Use when Hermes is unavailable and an in-progress task must continue.

```text
CONTEXT

Hermes is the primary orchestrator but is currently unavailable. You are the VS Code support/fallback agent. Continue the existing task; do not replace Hermes, redesign the architecture, or create a parallel workflow.

HANDOFF
Canonical task ID: [ID]
Requester: [user / Smooth / Admy / Ole00007 PA]
Repository and local path: [PATH]
Approved branch: [BRANCH]
Base commit: [SHA]
Last known good commit/checkpoint: [SHA]
Task and acceptance criteria: [PASTE]
Files already changed: [LIST]
Commands/tests already run: [LIST]
Current failure/blocker: [DETAIL]
Protected areas: [LIST]
User approvals already granted: [LIST]

TASK

1. Verify repository, remote, branch, HEAD, working tree, and handoff against local evidence.
2. If branch, SHA, scope, or uncommitted changes do not match, stop and ask the user; do not guess.
3. Read current repo instructions and the task handoff.
4. Continue from the smallest unfinished step on the same approved branch.
5. Reuse existing work; do not restart or rewrite unless evidence proves it is unusable.
6. Make small reversible edits, run targeted tests, then full relevant verification.
7. Run Перекрёстный тест independently.
8. Do not push, deploy, delete, migrate, touch production, or merge to main beyond permissions explicitly recorded in the handoff.
9. Return a resumption package for Hermes and the user: diff, files, commands, test evidence, commit SHA, open risks, rollback, and next approval gate.

End exactly:
Done | [completed result]
Next | [one approval or action]
Risks | [remaining risks or None]
```
