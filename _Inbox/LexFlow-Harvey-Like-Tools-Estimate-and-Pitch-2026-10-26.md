---
title: LexFlow Harvey-like tools — estimate, ROI calculator, pitch timing
date: 2026-10-26
author: backend-dev
status: proposal (awaiting Ole go on calculator)
tags: [lexflow, harvey, contracts, roi-calculator, estimate, pitch]
---

# LexFlow Harvey-like tools — estimate, ROI calculator, pitch timing

Reference: https://www.harvey.ai/roi-calculator/in-house · https://www.harvey.ai/solutions/in-house

## Harvey's calculator (what we copy, in LexFlow's own words)
- Inputs: number of legal employees, average annual compensation, currency.
- Outputs: ROI multiple (example 6x), 3-year table of hours regained and productivity value.
- Their basis: ~25–28 h saved per user per month (independent study they cite).
- LexFlow version: lawyers, annual cost, matters per month, LexFlow price → hours regained, EUR value, 3-year ROI. Public page on the LexFlow LP + in-app view.

## Estimate (comparison of scope, NOT measured; costs in USD, Nous credit balance not visible)
Assumes Ole gives me and Elisa the contract skill; cheaper agents do frontend/tests.

| Piece | Time | Cost |
|---|---|---|
| ROI calculator, Italian law-firm version | ~0.5 day | $4–10 |
| Contract review: clause extraction, risk flags vs playbook, suggested redlines, source-text citations, Word export | 5–7 working days | $50–100 |
| Drafting from templates (Elisa + Ole's skill), approvals, versions | 2–3 days | $15–40 |
| Vault: bulk-analyse many documents into a table | 3–4 days | $25–60 |
| Intake + workflow routing on existing graph/Kanban | ~2 days | $10–25 |

- Core build (calculator + contracts + drafting + Vault): ~2–3 weeks, ~$100–230.
- Excluded: Word add-in (+5 days at least), licensed legal-research database (Italian-law data source is a decision), security certifications (not build time).
- Running cost per use: 30-page contract review ≈ $0.15–0.40 on a premium model, a few cents on step-3.7-flash.
- Hard constraints: features OFF by default; human approves every write and every legal conclusion; summaries cite the clause they come from.

## When it makes sense to pitch (recommendation)
| When | What to pitch | To whom | Gate before it |
|---|---|---|---|
| Week 1 (right after calculator is live) | ROI calculator as a lead magnet, not the product | Italian solo/small firms via the LexFlow LP | Disclaimer "estimate, not legal/financial advice"; inputs sanity-checked; no personal data stored |
| Weeks 3–4 | Live demo: contract review + drafting on a REAL contract with an Italian playbook | Avv. Pagliano as pilot, then 3–5 firms in Genoa/Liguria | Current build deployed on Railway safely (Hindsight cost resolved), contract skill installed, GDPR/DPA text ready, writes approval-gated |
| Weeks 6–8 | Case study with measured hours saved from the pilot, then partners/investors | Bar associations, legal-ops partners, investors | At least one pilot with real numbers; ROI calculator re-based on measured hours (not Harvey's 25–28 h) |

Why not earlier: Harvey sells trust (citations, security certs). A pitch before the contract demo and a pilot reference is a promise; after it, it is evidence. The calculator is the exception because it needs no trust, only curiosity.

## Add to the project plan (proposed tasks — to be placed on the Kanban/roadmap by operator-installer, not a second tracker)
1. T-NEW-A ROI calculator (LP + in-app) — backend-dev builds, Fronty polishes, Admy gates. Day 1.
2. T-NEW-B Contract review MVP (clauses, playbook, redlines, citations, docx) — backend-dev; skill from Ole. Days 2–8.
3. T-NEW-C Drafting via Elisa with approvals — after B. Days 8–11.
4. T-NEW-D Vault bulk analysis — optional, after pilot feedback.
5. T-NEW-E Pitch pack: calculator link + 3-minute demo script + pilot one-pager — Week 3.
Dependencies: Railway/Hindsight cost decision (Ole), contract skill (Ole), Italian-law data source decision.

## Links
- Parent: [[LexFlow-Platform-Plan-2026-10-24]]
- Related: [[LexFlow-Reusable-Build-Protocol-2026-10-25]]
