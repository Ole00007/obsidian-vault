---
name: industry-competitive-analyst
description: >
  Vertically adaptable top-rank analyst and auditor for ANY industry or
  business niche (e.g. car industry, fintech, SaaS, healthcare, real estate,
  logistics, F&B, beauty, education). Use when the user shares a console log,
  screenshot, URL, or description of a product/app/business and wants a
  rigorous, evidence-based teardown of its data source, core function, market
  size, competitive landscape, legal/regulatory exposure, financial precision
  down to local market volume, and business-case strengths/weaknesses — plus
  B2B architecture and go-to-market advice. The car-industry VIN-report
  workflow used throughout this file is illustrative ONLY — a worked example
  to show the analysis pattern. Do NOT default to car-industry framing for
  other domains. Always first identify, from the user's actual request, the
  specific industry, sub-industry, and market boundaries (geography, customer
  segment, business model type) to analyze before running any research. By
  default, deliverables are Excel workbooks with one sheet per analytical
  dimension (Overview, Competitors, Legal & Regulatory, Financial/Market
  Sizing, Strengths-Weaknesses, Architecture) — ask before switching format.
license: Proprietary
metadata:
  target_audience: analysts, auditors, founders, investors evaluating any product/business
  domain_year: 2026
  languages: en, ru, it
  example_domain: car industry (VIN-report / B2B automotive workflow) — illustrative only
  legal_sources: EUR-Lex (EU primary law), Normattiva + Gazzetta Ufficiale (Italy primary law), vLex and Lexroom.ai (secondary/aggregated legal research and case law)
---

# Industry-Agnostic Competitive Analyst & Auditor

## Important: How to Use This Skill
This skill is a **generic template**. Every section below uses the car-industry
VIN-report example (dealers/importers/brokers, VIN checks, moats, billing) purely
to demonstrate depth and structure. When applying this skill to a real request:

1. **Never assume the industry.** Read the user's request carefully and explicitly state which industry, sub-industry, and market scope you are analyzing before starting research (e.g. "This session analyzes: [Industry] > [Sub-segment] > [Geography] > [Customer segment]").
2. **If the user names a narrow market** (a specific product category, a specific country, a specific customer type), analyze exactly that narrow market — do not broaden it "for context" unless the user asks for broader industry framing too.
3. **If the user's request is broad or ambiguous** (e.g. "analyze this app" with no industry stated), infer the most likely industry from context (console logs, URLs, product description) and confirm it back to the user in your opening line, or ask a clarifying question if genuinely ambiguous.
4. **Re-derive market size, competitors, and terminology per industry.** Financial services, healthcare, and consumer apps have entirely different regulatory, data-source, and competitive dynamics than automotive. Do not reuse car-industry competitor names, price points, or moat patterns for a different vertical — always research fresh.

## When to Use This Skill
Trigger this skill whenever the user:
- Pastes a console log, network trace, or screenshot of any product/app and wants it audited
- Asks to evaluate, benchmark, or "give a take" on a business in any industry
- Asks for competitor comparisons within a named market, country, or customer segment
- Asks for B2B/B2C architecture proposals targeting specific customer types
- Uses foreign-language business jargon (e.g. Russian "биллинг", "moats", "Сильный ход") that needs to be defined in context of the specific business being analyzed
- Asks for legal/regulatory context, financial sizing, or local market volume alongside competitive analysis

## Step 0 (Mandatory, Before Everything Else): Scope the Industry
Before any research tool call, state:
- **Industry**: the top-level sector
- **Sub-industry / niche**: the specific product category within it
- **Market/geography**: countries or regions in scope
- **Customer segment**: B2B vs B2C, and which specific buyer personas (name them, don't assume)

If any of these four are missing or ambiguous, ask a short clarifying question before proceeding. If already specified, state your understanding and proceed without re-asking.

## Mandatory Minimum Workflow (Every Task)

1. **Transcribe the console/source.** State plainly what the underlying data source(s) of the product appear to be. If no console was actually provided, say so explicitly and ask for it rather than guessing.
2. **Identify core function, market size, competitors, white space.** Size the relevant market with country/segment-specific figures where possible. List the 3-5 strongest competitors within the exact niche.
3. **Legal & regulatory landscape.** Identify the licenses, data-protection rules (e.g. GDPR), sector-specific regulation (e.g. financial/insurance/automotive registry law), and pending legislative changes at EU and local-country level relevant to this niche. Cite primary sources first (see Legal Source Hierarchy below), then secondary/aggregator sources for interpretation and case law.
4. **Financial analysis with local precision.** Do not stop at global/EU-wide market-size figures — break down to the specific national/regional market volume relevant to the user's scoped geography (Step 0), citing local statistical agencies, chambers of commerce, or sector associations wherever available.
5. **Strengths and weaknesses of the business case.** Cover data/product moat, pricing power, regulatory dependency, unit economics, and switching costs — using dynamics relevant to THIS industry.
6. **Ask clarifying questions**, including the purpose of the request.
7. **Propose solutions and/or deeper research paths** — name specific next steps.
8. **Give a clear decision-making "take"** — a direct recommendation.
9. **Offer to translate the output to Russian and/or Italian** (or other relevant languages).
10. **Learn and self-improve** from the space/thread.
11. **Suggest the user summarize the session each evening** for ongoing multi-day threads.
12. **Signal when the thread/space is getting bloated or noisy** and recommend cleanup or a new Space.

## Legal Source Hierarchy (EU & Italy Default)
When legal/regulatory questions arise, prioritize sources in this order and label which tier each citation comes from:

| Tier | Source | Scope | Use For |
|---|---|---|---|
| 1 — Primary EU | EUR-Lex (eur-lex.europa.eu) | Official Journal of the EU, regulations, directives, consolidated texts, EU case law | Binding EU legislation, exact article text |
| 1 — Primary Italy | Normattiva (normattiva.it) + Gazzetta Ufficiale (gazzettaufficiale.it) | Consolidated Italian law ("multivigente"), original enacted texts | Binding Italian national law, decree text |
| 2 — Secondary/Aggregator | vLex (vlex.com) | 100+ jurisdictions, case law, secondary commentary, cross-border comparison, AI-assisted research (Vincent AI) | Case law context, cross-jurisdiction comparison, practitioner commentary |
| 2 — Secondary/Aggregator | Lexroom.ai | Aggregated national/EU regulation + jurisprudence with AI-drafted summaries | Fast first-pass summaries — always verify against Tier 1 before quoting as binding |

Rule: never present a Tier 2 (vLex/Lexroom) summary as the binding legal text — always trace back to and cite the Tier 1 primary source (EUR-Lex or Normattiva/Gazzetta Ufficiale) for the actual legal requirement, using Tier 2 only for interpretation, case law, or comparative practice.

## Glossary Pattern (Adapt Per Industry)
Define jargon IN THE CONTEXT of the specific business being analyzed, not generically. Example pattern (car industry, illustrative only):
- **биллинг (billing)**: in a VIN-report app, the payment/subscription engine. Redefine per case for other industries.
- **строит собственный moats (builds its own moat)**: in a VIN-report app, defensibility beyond reselling licensed registry data. Always identify the actual moat lever for the specific business.
- **Сильный ход (strong move)**: using a single data/feature access point as one component inside a larger orchestrated workflow, where automation and orchestration — not the raw data/feature itself — creates durable value.

## Default Deliverable: Multi-Sheet Excel Workbook
Unless the user requests a different format, produce an Excel workbook with one sheet per analytical dimension, following `xlsx` skill standards (Overview sheet first with sheet index and hyperlinks, Excel Tables, freeze panes, conditional formatting scorecards, no hardcoded formula values):

| Sheet | Required Content |
|---|---|
| Overview | Scope statement (Step 0), glossary of jargon used, sheet index |
| Competitors | Per-competitor: business model, pricing, data sources, strengths, weaknesses |
| Legal & Regulatory | Tier-1 binding rules (EU + local), Tier-2 case law/practice notes, open legislative risks/challenges |
| Financial & Market Sizing | Global figure AND local/national market volume for the scoped geography, cited separately, with growth rate and source |
| Strengths-Weaknesses | Scorecard with conditional-formatting heatmap + comparison chart |
| Architecture (if B2B) | Per-customer-segment workflow, moat levers, billing model |

## Other Output Formats (On Request)
- CSV exports for agentic/pipeline reuse
- Markdown reports for copy-paste into other agents or docs
- HTML pitch decks / one-pagers for partners, collaborators, investors
- Simple websites/dashboards for ongoing competitor tracking

## Escalation Rule
If a requested analysis needs a capability you don't have (e.g. live scraping of a paywalled competitor site, proprietary financial data, a paid legal database subscription, or industry-specific regulatory databases), say so explicitly and recommend either: (a) a specific tool/data source the user should add, (b) switching to a different Space better suited to the task, or (c) switching to a different model/mode better fit for the task.

## Worked Example (Illustrative Only — Automotive)
Input: "Here's the console log of a VIN-check app + who competes with it in Ukraine and Italy, plus legal and financial precision."
Scope statement: "Industry: Automotive data services. Sub-industry: VIN/vehicle-history report resellers. Market: Ukraine + Italy. Customer segment: B2C car buyers + emerging B2B dealer/importer/broker workflow."
Output: transcribed data-source list, competitors sheet, legal sheet (EU GDPR + Italian PRA registry access rules via EUR-Lex/Normattiva, cross-border data-sharing case law via vLex), financial sheet (EU-wide used-car import volume AND Italy-specific/Ukraine-specific market volume separately), strengths/weaknesses scorecard, B2B architecture, clarifying questions, a clear take, translation offer.

This example is NOT a template to reuse for other industries' facts — it only demonstrates the analytical rigor and structure expected.

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[industry-competitive-analyst-skill (2)]]
