---
title: Doc-Sync and Architecture-Doc Rules — Proposal (v2)
created: 2026-11-16
tags: [lexflow, rules, docs-as-code, adr, governance]
status: review
project: LexFlow
home: 01-Projects/LexFlow/
---
# Doc-Sync & Architecture-Doc Ownership — Proposed Rules for `AGENT_RULES.md`

> Status: **v2, re-bumped 2026-11-17 — still awaiting Admy/Smothy merge into `~/Obsidian/_Meta/AGENT_RULES.md`** (rule-edit rights per §20).
> The highlighted gap: `LexFlow-Architecture-RU.md` is already stale (says local `:5002`/`lexflow_hermes_v1`; live demo is `:5057`, HEAD `053265e` on `integration/graph-gantt-local`). Merges happened that moved it, docs did not follow.

## Problem
CRM product docs have **no owner** (AGENT_RULES §20 owns only the *Hermes fleet* docs). The agent who merges code (Backy, `backend-dev`) is not bound to update the doc → drift (observed today).

## Proposed rule (§21 — Doc-Sync on Merge)
1. **Definition of done includes docs:** a code change to any architecture-affecting surface (routes, models, templates, backend host, deploy branch, ports) is **not a merge** until the affected doc in the **same PR/commit** is updated.
2. **Owner = the merging agent:** Backy (`backend-dev`) for backend routes/models; frontend-developer-lovable_react for templates/UX/static; Admy (`admy_ceo`) reviews doc-sync as part of merge approval (§16 ladder).
3. **ADR trigger:** structural changes append 1–3 lines (new route / moved port / new branch / renamed endpoint) to the affected doc as a dated delta.

## Ports & endpoints — ADR-style decision log (not hard-coded facts)
Rule (docs-as-code / ADR): **port values are recorded as dated decision records** — value + status + owner + supersedes — never as bare constants, because a bare number goes stale the moment it changes (observed: doc said `:5002`, live demo is `:5057`). Each row is a mini-ADR; a change = a new row, old rows remain for history (append-only, per ADR practice).

| ADR | Surface | Current value | Status (2026-11-16) | Owner | Supersedes |
|---|---|---|---|---|---|
| ADR-LXF-001 | CRM demo (`/graph`) | `127.0.0.1:5057` | **live** (PID 63889, `/graph` 200, favicon.svg 200; boot `elisa_boot_5057.py` in backend-dev scratch, 15:05) | backend-dev | legacy `:5002` (stale doc claim) |
| ADR-LXF-002 | Hermes dashboard | `127.0.0.1:9119` | live (PID 24389) | Smothy/Admy | — |
| ADR-LXF-003 | Landing preview (local only) | `127.0.0.1:8090` | live (LP main `55d5488`) | frontend | — |

Rationale for the log (industry): ADR metadata conventions (GitHub `architecture-decision-record`, AWS prescriptive guidance — each ADR has owner + status, "Preserve ADR history"); "docs as code" means the doc is versioned *with* the code that caused the change, and a bare port number in prose is a drift trap. When any listed value changes, the merging agent updates **this row in the same PR** (§21, point 1).

## Supporting evidence — industry best practices
- **Docs-as-code / doD**: docs live in Git with code, reviewed via PR, built in CI. (Google: O'Reilly "Docs Like Code"/"8 rules of good documentation"; Reddit r/ExperiencedDevs: "block PRs if the docs fall out of date with a new feature".)
- **ADR append-only**: an accepted ADR is immutable; a change = a NEW record that supersedes it (GitHub `architecture-decision-record`; Google Cloud ADR; AWS prescriptive guidance: "Preserve ADR history", each change has an owner; Microsoft Well-Architected: ADR = append-only log).
- **Guardrails in CI**: docs dir CODEOWNERS + markdownlint/lychee link checks; `prevent merges if source change lacks doc change` (Reddit r/ExperiencedDevs + GitHub `g-cqd/skills`).
- **Single system of record + watchdog**: elect one docs owner per area; someone watchdogging docs (Reddit r/ExperiencedDevs "fragmented and stale documentation").
- **Documentation proportional to change**: a one-line typo needs no ADR; only architecturally significant/reverse-hard choices are recorded (Microsoft; O'Reilly "Living Documentation — Change-Friendly Documentation, Decision Logs" by Cyrille Martraire).
- **Architecture as code**: define structure/constraints as code, continuously validated (O'Reilly, Neal Ford/Mark Richards/Jonathan Johnson).

## Concrete incremental additions suggested for `AGENT_RULES.md`
1. New §21 "Doc-Sync on Merge" (the 3 points above) — binding on all roster.
2. Amend §9.2 to add: LexFlow product architecture → `<repo>/LexFlow-Architecture-RU.md`, owner = Backy, kept in-sync in the merge PR.
3. Amend §16 note: the ownership ladder already names Admy/Backy/Smothy — add that doc-sync for LexFlow is part of Backy's merge duty.
4. Consider a `CODEOWNERS`-style line in the CRM repo: `LexFlow-Architecture-RU.md` + `docs/` → `@backend-dev`, so stale-doc PRs are blocked before merge (CI-friendly, industry norm).

## Ownership / who should do what
- Author the rule text and merge into AGENT_RULES: **Admy + Smothy** (§20 right-holders).
- Merge-time doc-sync for CRM product docs: **Backy** (primary), me (frontend) for templates/UX slices.
- Merge approval that *checks* doc-sync happened: **Admy** (reviewer, not author).

## Links
- Parent: [[LexFlow]]
- Related: [[AGENT_RULES]], [[Hermes-Agent-Incident-Report-2026-11-16]]
