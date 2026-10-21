# Prompt — Choose Admy or Smothy as LexFlow CRM Project Owner

Paste this entire prompt into Hermes before Gantt M0.

---

## Context

LexFlow CRM needs one accountable AI Project Owner/orchestrator. The only candidates are **Admy** and **Smothy**.

Do not choose from reputation, model name or the current role labels. Choose from verifiable project evidence: completed work, retained context, tools, judgment, reliability and ability to coordinate the whole LexFlow CRM build.

This is an inspection and recommendation task only. Do not change application code, branches, migrations, configuration or deployment state.

## Goal

Determine:

1. Which candidate has completed and correctly understood more relevant LexFlow CRM work.
2. Which candidate is more aware of current architecture, schema governance, protected areas, deployment rules, open risks and decisions.
3. Which candidate has the skills and available tools to orchestrate the entire project safely.
4. Which candidate should be Project Owner and which should be Deputy/independent reviewer.

## Evidence to inspect

Inspect all locally available evidence for both candidates:

- Agent/session history and handoffs.
- Prompts received and outputs produced.
- Reports, plans, screenshots and test evidence.
- Commits or patches attributable to each candidate.
- Files reviewed or created.
- Issues found before they caused rework.
- Gate decisions, stop decisions and rollback planning.
- Tool access and demonstrated tool use.
- Accuracy of claims compared with repository state.
- Understanding of latest Master Plan, latest Starter, `CLAUDE.md`, deployment flow and protected files.
- Context continuity across sessions.
- Cost awareness and model-routing discipline.
- Ability to coordinate other agents without writing or approving everything personally.

Search for both names and variants:

```text
Admy
admy
Smothy
Smoothy
smothy
smoothy
```

Do not count duplicated text, copied plans, unsupported self-claims or quantity without quality as completed work.

## Mandatory candidate interview

If both agents can be queried, give each the same questions independently. Require file paths, commit SHAs or report names as evidence.

1. What is the current active LexFlow CRM architecture, and what conflict still requires resolution?
2. What are the schema sources of truth and which sources are archived/reference-only?
3. What protected areas require a stop or owner approval?
4. What work have you personally completed or reviewed for LexFlow CRM?
5. Which current risks could expose client data or break production?
6. How do staging and production deployment differ?
7. What is `D_READY`, when must it be checked, and what happens when it becomes true?
8. Which tools can you actually use for repository inspection, tests, browser checks, deployment evidence, cost tracking and project documentation?
9. Give one example where you stopped unsafe work or corrected drift.
10. Describe how you would coordinate Backend, Fronty, Tester and the Deputy without approving your own work.

If an agent cannot be queried, score only verified artifacts and clearly state the limitation.

## Scoring matrix

Score every category from 0 to its maximum. Give evidence for every score.

| Category | Maximum | What earns points |
|---|---:|---|
| Verified relevant work completed | 20 | Correct deliverables, reviews, tests or decisions supported by artifacts |
| Current project/context awareness | 20 | Correct architecture, schema, deployment, branch and open-risk understanding |
| Orchestration ability | 15 | Work breakdown, ownership, dependencies, gates, drift control and handoffs |
| Tools and execution visibility | 15 | Demonstrated repository, test, browser, report, cost and deployment-evidence tools |
| Security and risk judgment | 10 | Authorization, leakage, secret, migration, backup and rollback discipline |
| Reliability and evidence quality | 10 | Claims match files/logs; reproducible evidence; no invented completion |
| Communication to a non-technical owner | 5 | Clear decisions, concise reports and one concrete next step |
| Cost and launch discipline | 5 | Nous Portal routing, budget stops, low rework and launch-speed awareness |
| **Total** | **100** | |

Apply penalties after the base score:

| Failure | Penalty |
|---|---:|
| Invented or unverifiable completed work | -15 each |
| Missed critical client-data or production risk | -15 each |
| Edited a protected area without approval | -20 each |
| Approved own implementation without independent review | -10 each |
| Ignored latest approved Plan/Starter | -15 |
| Caused avoidable broad rewrite instead of a surgical change | -10 |

## Eligibility rule

A candidate is eligible only if:

- Final score is at least 70/100.
- Security and risk judgment is at least 7/10.
- Current project/context awareness is at least 14/20.
- No unresolved protected-area violation exists.

If only one candidate is eligible, select that candidate.

If both are eligible, select the higher score.

If scores differ by 5 points or less, use these tie-breakers in order:

1. Higher current project/context awareness.
2. Higher orchestration ability.
3. Higher security and risk judgment.
4. Better verified tool coverage.
5. Fewer unsupported claims or drift incidents.

If neither is eligible, do not invent a winner. Report the exact gaps and propose the smallest qualification task for each; Admy remains temporary gate coordinator only until one passes.

## Separation of duties

The winner becomes **LexFlow CRM Project Owner/orchestrator**.

The other becomes **Deputy Owner and independent reviewer**.

The Owner:

- Maintains decisions, state, gates, risks, budget and next actions.
- Assigns implementation work to specialists.
- Checks `D_READY` at C M6 and later relevant release events.
- Reports to Olesia and starts D0 when all D conditions are true.
- Stops destructive, unauthorized, unverified or over-budget work.
- Cannot be the sole approver of work they authored.

The Deputy:

- Challenges the Owner’s assumptions.
- Re-runs critical tests.
- Reviews security, accessibility, leakage and regression evidence according to strengths.
- Takes temporary ownership if the Owner is unavailable or conflicted.

## Required output

Create `reports/LexFlow_Project_Owner_Audit_<YYYY-MM-DD>.md` with:

### Evidence inventory

```text
candidate | artifact/path/commit | work claimed | work verified | quality | relevance
```

### Scorecard

```text
category | Admy score | Admy evidence | Smothy score | Smothy evidence
```

### Tool matrix

```text
tool/capability | Admy verified access/use | Smothy verified access/use | project need | gap
```

### Awareness test

```text
question | Admy answer accuracy | Smothy answer accuracy | source used
```

### Decision

Use exactly:

```text
PROJECT OWNER: <Admy or Smothy or NO ELIGIBLE CANDIDATE>
DEPUTY: <other candidate or pending>
OWNER SCORE: <number>/100
DEPUTY SCORE: <number>/100
CONFIDENCE: high / medium / low
DECISIVE EVIDENCE: <3–5 evidence-backed points>
KNOWN GAPS: <remaining limitations>
FIRST OWNER ACTION: <one small reversible action>
```

### D responsibility acknowledgement

The selected Owner must state:

```text
I accept responsibility for checking D_READY at C M6, at each later release affecting client authentication/portal/authorization/visibility, and once per active build cycle while D is blocked. When D_READY becomes true, I will report the evidence to Olesia and start D0 in the same working session. I will not merge or deploy D without Olesia’s explicit D4 command.
```

## Stop conditions

Stop and report instead of selecting if:

- Candidate evidence has been deleted or is inaccessible.
- Agent identity cannot be reliably connected to artifacts.
- Repository state contradicts both candidates.
- A protected-area violation is unresolved.
- Scoring evidence is too incomplete for a defensible decision.

## Final action

Commit only the audit report if the working tree and project rules allow documentation commits. Do not commit application changes. Provide one verification command and the exact safe `git add`, `git commit` and branch push commands for the report. Then stop for Olesia’s acceptance of the owner selection.
