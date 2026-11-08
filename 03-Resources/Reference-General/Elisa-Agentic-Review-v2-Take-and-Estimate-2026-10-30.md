---
home: 01-Projects/LexFlow/Elisa-CRM/
type: review-take
date: 2026-10-30
author: backend-dev (Backy)
source: 01-Projects/LexFlow/Elisa agentic market and control-layer review v2.zip
---
# Elisa agentic review v2 - Backy's take + Phase 0 estimate

**Verdict:** agree with the pack's conditional go: one workflow first (W01 intake -> draft -> review -> approved delivery, plus W02 CNF disclosure). Do NOT build a universal harness, accounting or enterprise tracks now.

## Fit with Elisa-CRM today (from code I wrote, not from the pack)
- Already true: writes only propose, human confirm card, caller's JWT (server-side authz), tool guard, no delete tool, LLM URL from server env only, features default OFF.
- Missing vs pack: approval bound to payload hash + expiry + idempotency; evidence/audit record; CNF disclosure lifecycle; citations; execution_unknown (no external sends exist yet); tenant tests beyond SQL rows.
- Rule (AGENT_RULES s9): extend the existing confirm path, do not stand up a second control plane.

## Phase 0 estimate (rough, agent time; humans are the long pole)
| Task | Owner | Est. |
|---|---|---|
| T01 read-only discovery | Backy | 0.5 d |
| T04 tenant/store isolation tests | Backy | 1-2 d |
| T05 action+policy contract (delta on existing) | Backy | 1 d |
| T06/T07 approval hash/expiry/replay + executor | Backy | 3-4 d |
| T08 review inbox mocks | Fronty | 2-3 d |
| T10 CNF lifecycle | Backy+Fronty | 2-3 d (+ counsel) |
| T11 one workflow end-to-end (synthetic) | Backy | 3 d |
| T12 adversarial suite | Backy | 2 d |
| T09 outbox/reconcile | Backy | 2-3 d, only when real sends exist |
Total to P2 about 3-4 weeks agent time, API spend roughly tens of USD with fresh sessions. Not included: counsel fees, T02 buyer, T14 paid pilot (3 paying firms) - agents cannot speed these up.

## Questions: who resolves what
- Olesia + Backy now: Q01-Q05, Q09, Q10 (scope, exclusions, claims).
- Backy by evidence (T01): Q11-Q22 - answers must be file paths + tests, not verbal.
- Counsel: Q23-Q28. Customers: Q07, Q29-Q34.
- Decision log = one note in 01-Projects/LexFlow/Elisa-CRM/ (single registry); tasks stay on the Kanban board.

## Caveats
Pack reviewed documents, not our code; LangGraph/OpenContracts/Graph items do not apply to the current Flask Elisa. Nothing here is implemented or legally reviewed.

## Links
- Parent: [[Elisa-CRM]]
- Related: [[Elisa-CRM-Status-and-Architecture-2026-10-29]], [[Elisa-Improvement-Plan-2026-10-27]]
