---
title: LexFlow Harvey-like tools — brainstorm brief (for Perplexity Deep Research + partner lawyer's Claude Code)
date: 2026-10-26
author: backend-dev
status: DRAFT for brainstorming — nothing here is decided; plan goes to Kanban only after Ole decides
tags: [lexflow, brainstorm, harvey, contracts, roi-calculator, pitch, research-brief]
---

# LexFlow Harvey-like tools — brainstorm brief
No secrets, no client data in this file. Safe to paste into external tools.

## 1. Context (paste this first)
LexFlow = multi-tenant CRM for lawyers (Flask, one Railway service; first client: a civil lawyer in Genoa, Italy; UI English, client LPs Italian). Already built locally: matters/contacts/tasks/agenda, Kanban, Gantt, context graph, responsible people + agent-bus view, in-app assistant "Elisa" (bubble; asks before writing; summaries/drafts by a model, provider-agnostic). Goal: a Harvey-style layer for small/mid Italian firms, at a fraction of Harvey's price.
Reference pages: https://www.harvey.ai/roi-calculator/in-house · https://www.harvey.ai/solutions/in-house

## 2. Proposals (all of them, with estimates — estimates are scope comparisons, not measurements, USD)
| ID | Proposal | Time | Cost | Depends on |
|---|---|---|---|---|
| A | ROI calculator (LP + in-app): lawyers, annual cost, matters/month, LexFlow price → hours regained, EUR value, 3-yr ROI | ~0.5 d | $4–10 | pitch assumptions (hours saved/user/month) |
| B | Contract review MVP: clause extraction, risk flags vs a playbook, suggested redlines, citations to clause text, .docx export | 5–7 d | $50–100 | contract skill (Ole), Italian playbook |
| C | Drafting via Elisa from templates with approvals + versions | 2–3 d | $15–40 | B, contract skill |
| D | Vault: bulk-analyse many documents into a table | 3–4 d | $25–60 | pilot feedback |
| E | Intake + workflow routing on the existing graph/Kanban | ~2 d | $10–25 | — |
| F | Pitch pack: calculator link + 3-min demo script + pilot one-pager | wk 3 | small | A, B pilot |
| Out of scope for now | Word add-in (+5 d min), licensed legal-research DB, security certifications | — | — | decisions |
Core build A–D ≈ 2–3 weeks, ≈ $100–230. Run cost: 30-page contract review ≈ $0.15–0.40 premium model, cents on a flash-class model.
Hard constraints: features OFF by default; human approves every write and legal conclusion; every summary cites its source clause; GDPR/EU AI Act aware.

## 3. Pitch timing (proposal)
- Week 1: calculator as lead magnet for small Italian firms (disclaimer, no personal data stored).
- Weeks 3–4: live demo of contract review + drafting on a real contract; pilot lawyer in Genoa, then 3–5 firms.
- Weeks 6–8: case study with MEASURED hours saved → partners / bar associations / investors; re-base the calculator on measured numbers.

## 4. Harvey in-house — feature map to verify (what we think vs what research must confirm)
Harvey modules seen on their site: Assistant, Vault, Knowledge (research), Spaces, Contract Intelligence (playbook review, in Word), Intake, Agents/Workflows, Command Center analytics, Connector Library. Their ROI basis: ~25 h/user/month typical, 35–50+ h power users (their cited study) — treat as marketing until verified.

## 5. Questions for Perplexity Deep Research (copy each as a separate prompt)
1. Harvey ROI calculator methodology: formula, assumptions, which study, how credible; what a conservative, defensible hours-saved-per-lawyer figure is for small Italian firms. Cite sources.
2. Italian legal-tech competitors for contract review and legal AI (e.g. verify candidates such as Lexroom, DeJure, Leggi d'Italia, others): features, pricing, target size, weaknesses. Cite sources; mark anything unverified.
3. Italian-law data sources usable commercially or free for citations: Normattiva, EUR-Lex, Cassazione/ItalgiureWeb, Brocardi, others — licensing terms, APIs, reuse limits.
4. Regulation: Italian Bar (CNF) guidance on AI use by lawyers; EU AI Act risk class for legal-assistance tools; GDPR (DPIA, DPA, data location, sub-processors for model providers); professional secrecy implications of sending client documents to model APIs.
5. Contract-review quality: how to evaluate an AI contract reviewer (benchmarks such as CUAD/LegalBench, human-eval protocol), failure modes, safe UX (citations, confidence, "never auto-send").
6. Pricing: what do small European firms pay for legal-AI/CRM seats; a defensible LexFlow price band vs Harvey enterprise pricing.
7. Pitch: which channels reach Italian solo/small firms (bar associations, events, newsletters); cost of acquisition benchmarks.

## 6. Prompt for the partner lawyer's Claude Code (copy)
"Context: section 1 above. Task: (a) review proposals B and C as a practising lawyer — which clauses/risks matter most for Italian commercial, employment and NDA contracts, (b) draft an Italian playbook (clause → acceptable / fallback / red-flag wording) for 10 common contract types, (c) list what a lawyer must verify before trusting AI output, (d) mark anything that would breach professional duties. Output: markdown tables, Italian terms with English glosses, no invented case law — cite or say 'unverified'."

## 7. Decisions Ole must take after brainstorming
1. Go/no-go and date for A (calculator). 2. Which contract types in B first. 3. Italian-law data source. 4. Price band and pilot terms. 5. Then: Kanban cards (one per ID, right specialist, parents set) via operator-installer — not created yet.
Separate, not for external research: Railway/Hindsight cost decision (Admy's audit report is on his card), pending push/deploy retry.

## Links
- Parent: [[LexFlow-Platform-Plan-2026-10-24]]
- Related: [[LexFlow-Harvey-Like-Tools-Estimate-and-Pitch-2026-10-26]]
