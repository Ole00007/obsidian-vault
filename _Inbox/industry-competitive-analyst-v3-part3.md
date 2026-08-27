---
name: industry-competitive-analyst-v3-part3
description: "Part 3 of 3 - Default Excel output structure and escalation rules for the industry-competitive-analyst v3 skill."
---
# Industry-Competitive Analyst v3 - Part 3: Default Output & Escalation

## Default Deliverable: Multi-Sheet Excel Workbook
Unless the user requests a different format, produce an Excel workbook with one sheet per analytical dimension. Follow standard spreadsheet-engineering practice: Overview sheet first with a sheet index and internal hyperlinks, formal Excel Tables (not manual ranges), frozen header rows, conditional-formatting heatmaps for scorecards, and native charts - never hardcode calculated values, use formulas.

| Sheet | Required content |
|---|---|
| Overview | Scope statement (from Part 1, Step 0), glossary of any jargon used, sheet index with hyperlinks |
| Competitors | Per-competitor: business model, pricing, data sources, strengths, weaknesses |
| Legal & Regulatory | Tier-1 binding rules (per Part 2), Tier-2 case law/practice notes, open legislative risks |
| Financial & Market Sizing | Global figure AND local/national market volume for the scoped geography, cited separately, with growth rate and source |
| Strengths-Weaknesses | Comparative scorecard with conditional-formatting heatmap and a comparison chart |
| Architecture (if B2B) | Per-customer-segment workflow, moat levers, billing model |

## Other Output Formats (on request)
- CSV exports for agentic/pipeline reuse
- Markdown reports for copy-paste into other agents or docs
- HTML pitch decks / one-pagers for partners, collaborators, investors
- Simple websites/dashboards for ongoing competitor tracking

## Escalation Rule
If a requested analysis needs a capability not available in the current session (e.g. live scraping of a paywalled site, proprietary financial data, a paid legal database subscription, or industry-specific regulatory databases), say so explicitly and recommend one of:
(a) a specific tool/data source the user should add,
(b) switching to a different Space/workspace better suited to the task,
(c) switching to a different model/mode better fit for the task (e.g. a coding-capable mode for scraping scripts).

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[industry-competitive-analyst-skill (2)]]
