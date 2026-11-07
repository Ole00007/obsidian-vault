# WORKFLOW SWARM — "Separazione Strategy Execution" (one swarm, parallel lanes)
**Owner/reporter:** admy_ceo · **Tracks run in parallel** · **Outcome:** the avvocato gets a ready
negotiation → mediation package, with a judicial fallback staged. (Swarm = multiple specialist agents
working different lanes against one Kanban board; each lane is a card assigned to its owner. Parallel
> sequential; no lane blocks another.)

---

## Orchestrator
**admy_ceo** — builds the 5 cards above, assigns owners, tracks completion on the Hermes Kanban,
collects outputs into one package, reports to Ole + the avvocato. Ole's rule: parallel work, no
permission gates beyond the approval gates (deploy / >$2 / publish).

---

## The swarm (parallel lanes)

| Lane | Owner (profile) | Deliverable | Card # | Depends on |
|---|---|---|---|---|
| **L1 — Evidence pack** | **backend-dev (Becky)** | Verified exhibits: exact screenshots of "I will not fight" + the amicable-line + ledger numbers; convert the 3 dossier mds for CRM if a real (non-scratch) DB is wanted | SEP-001 | — |
| **L2 — Mediation package** | **authored by admy_ceo, reviewed by avvocato** | Opening mediation letter (3-topic, same-day-answers, family-home tied to children) — using S1/S2/S5 | SEP-002 | L1 facts |
| **L3 — Ledger** | **operator-installer (smoothy)** | Loan/transfer ledger (6k + 5k Lessia + car insurance/rent offsets) as a clean spreadsheet | SEP-003 | — |
| **L4 — Counter-accusation memo** | **memory-curator (Memy)** | The calm, pre-emptive paragraph + the session evidence he never denied (fake IG accounts / reading messages) | SEP-004 | L1 |
| **L5 — Judicial fallback staged** | **backend-dev + avvocato** | Judicial separation template + cost-to-both estimate, ready to file if he stalls | SEP-005 | L1, L4 |

---

## Control flow (additive, non-blocking)
- **L1, L3 launch immediately** (no deps).
- **L2 waits on L1** facts only (not on L3/L4).
- **L4 reads L1** but can start drafting from the dossier itself when L1 is slow (soft dep).
- **L5 stages in parallel**, only *marked ready when needed* — never filed without the avvocato.
- **admy_ceo** merges L1→L5 into one package: `Separazione-Swarm-Package` in this folder, wikilinked.
- **Gate:** nothing is sent to Eugene or a court without Ole (client) + the avvocato signing off.

---

## Anti-temptation rules (Ole's)
- Only admy_ceo commits to the **delivery package** and the **roster notice**; no lane pushes externally.
- No lane deletes evidence (L1 is verbatim/verify; L4 is "acknowledge, don't suppress").
- Costs: L5 estimate is a doc, not a deploy. No >$2 ops without asking.
- Every lane reports completion **on its card** (the daily report reads the board).

---

## Elisa (in-CRM) hook
The same evidence already produced **Elisa's strategy draft** in Case L-01 (attachment id 7). If a
true **"strategy" draft kind** is wanted, lane L1 includes a tiny backend change to
`crm/agent/guard.py` (add `'strategy'` to the allowed kinds) so future Elisa drafts label themselves
strategy, not client_update — confirm with Becky.

## Links
- Parent: [[Separazione-Strategy-2026-11-07]]
- Related: [[Evidence-Dossier-Alessia-vs-Eugene-2026-11-05]]
