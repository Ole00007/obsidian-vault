# Point 4 — Excel Deliverable Iteration: Legal & Local-Precision Financial Sheets (Extended)

## Direct Answer
The default competitive-analysis Excel workbook was iterated from a generic competitor comparison into a six-sheet template that forces two additions on every run: a dedicated Legal & Regulatory sheet, and a Financial sheet that never stops at a global figure — it must always resolve down to a cited, local/national market-volume number.

## The Six-Sheet Template (Recap)

| Sheet | Required Content |
|---|---|
| Overview | Scope statement, glossary, sheet index with hyperlinks |
| Competitors | Business model, pricing, data sources, strengths, weaknesses per competitor |
| **Legal & Regulatory** | Tier-1 binding rules, Tier-2 case law/practice notes, open legislative risks |
| **Financial & Market Sizing** | Global figure AND precise local market volume, cited separately, with growth rate |
| Strengths-Weaknesses | Conditional-formatting heatmap scorecard + comparison chart |
| Architecture (B2B) | Per-customer-segment workflow, moat levers, billing model |

## Extended Detail: Legal & Regulatory Sheet Design
This sheet should be structured as three stacked tables, not one flat list:
1. **Binding Requirements** — one row per obligation, columns: Requirement, Source (Tier-1 citation), Applies To (which part of the business), Compliance Status/Risk.
2. **Case Law & Practice Notes** — one row per relevant precedent or enforcement action, columns: Case/Decision, Source (Tier-2 citation), Practical Implication.
3. **Open Legislative Risk** — one row per pending or recently changed rule, columns: Change, Expected Timeline, Potential Business Impact.

Example row for an EU-scoped AI-adjacent product: Requirement = "High-risk AI system conformity assessment," Source = "Regulation (EU) 2024/1689, Art. 43," Applies To = "Any AI feature used in employment/credit-scoring decisions," Risk = "High — assessment must be completed before market placement"[web:135][web:139].

## Extended Detail: Financial & Market-Sizing Sheet Design
The key discipline is **never presenting a single blended number**. Structure as two parallel blocks:

**Block A — Global/Regional Context**
- Market size (value, unit, year), source, CAGR — from recognized global/regional market-research bodies.

**Block B — Local Market Volume (Mandatory, Country-Specific)**
- Market size for the exact scoped country/region, source, CAGR — sourced preferentially from:
  - **National statistical institutes** (e.g. ISTAT for Italy, Eurostat for EU aggregates) — ISTAT's ASIA business register and Eurostat's "Key figures on European business" provide granular, sector-level structural data down to enterprise counts, turnover, and employment by NACE code[web:150][web:152][web:155][web:162].
  - **National trade/industry associations** — e.g. Confindustria (Italy's main industrial confederation, ~150,000 member enterprises, 34% of GDP) and its sector-specific federations (e.g. Confindustria Nautica for marine/boating, Confindustria Assoimmobiliare for real estate) regularly publish sector-specific market volume and investment data that is far more precise than generic global reports[web:151][web:153][web:156][web:157][web:160].
  - **Sector-specific data platforms** — e.g. the Confindustria Research Center / Il Sole 24 Ore export-potential platform, covering ~5,000 product categories across 180+ countries, useful for import/export volume precision[web:163].

## Formula/Structure Note (Excel-Specific)
- Do not hardcode the local-market figure as static text — place it in a labeled input cell with a source citation in an adjacent comment/note cell, and reference it via formula in any downstream ratio or share-of-market calculation, so the sheet stays auditable and updatable.
- Add a "Data Confidence" column next to both Global and Local figures: High (official statistical institute), Medium (trade association estimate), Low (aggregator/market-research estimate) — this signals to the reader how much weight to place on each number.

## Escalation Note
If no local-precision figure can be sourced from a national statistical institute or trade association for the scoped niche, state this explicitly in the sheet rather than silently extrapolating a percentage share of the global figure — an unsupported extrapolation should never be presented with the same confidence level as a sourced number.

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[Sheets to an excel _1. Where with what and how we]]
