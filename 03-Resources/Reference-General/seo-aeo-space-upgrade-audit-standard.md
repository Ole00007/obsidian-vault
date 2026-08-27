# SEO & AEO Space Upgrade — Audit Standard vNext

## Purpose
This document updates the working standard for future SEO + AEO audits in this Space, using the latest Alena Krot HTML audit format as the default baseline and integrating practices observed from selected Italian SEO experts.[cite:54][cite:55][cite:56][cite:57][cite:58][cite:59][cite:64]

## Default deliverable format
The default audit output format for the next site audits should be the **latest Alena Krot HTML audit format** unless a more professional evidence-backed format is found later that clearly improves readability, dashboarding, or decision support.[cite:59]

### Why keep the Alena Krot HTML format as default
- It is already aligned with the current workflow and avoids unnecessary redesign overhead during active client delivery.
- It can be progressively upgraded with better dashboards, comparison blocks, KPI modules, and AI citation tracking.
- It supports a modular structure, which is useful when auditing service businesses first and then adapting for the next vertical, such as real estate.

## What to inherit from the expert sources

### 1) Gianluca Fiorelli / iloveseo.net
Observed best practices include:
- Strong emphasis on **semantic and entity/keyword research**, topical architecture, and structured data as strategic foundations.[cite:55][cite:57]
- Search strategy built around **taxonomy and ontology**, not just isolated keywords.[cite:55]
- International and AI-search orientation, including visibility in search and LLM environments.[cite:56][cite:60]
- Tool preferences publicly associated with Fiorelli include **Sitebulb, Sistrix, Ahrefs, and Semrush**.[cite:56]

**Adopt into the standard:**
- Every audit must include an **entity map**, topical cluster view, and semantic gap review.
- Every page-level recommendation must connect to search intent, entity clarity, and internal linking structure.
- Add a dedicated section for AI-search extractability and citation readiness.

### 2) Enrico Altavilla / motoricerca.info / MindSoup
Observed best practices include:
- Deep **technical SEO** orientation, grounded in long experience with search, software, and site architecture.[cite:58]
- Current positioning around **SEO + AI consulting**, not SEO in isolation.[cite:64]
- Practical focus on helping companies avoid implementation mistakes and operational self-sabotage.[cite:64]
- Editorial/search philosophy centered on clarity, usefulness, and reader-first content.[cite:67]

**Adopt into the standard:**
- Every audit must have a **technical risk register** with severity, impact, and fix owner.
- Recommendations must be implementation-aware, not generic; each issue should state likely cause, business impact, and exact next step.
- Add a “do not break” section for CMS/platform constraints, especially on enterprise or hosted site builders.

### 3) Fabio Antichi / Roberto Serra references
Observed best practices include:
- Evaluation based on **case studies, business KPIs, conversion quality, CAC, lead value, and revenue**, not vanity rankings alone.[cite:59]
- SEO should be connected to broader business performance and realistic expectations.[cite:59]
- Presence, authority, and consistent market positioning matter alongside execution.[cite:59]

**Adopt into the standard:**
- Every audit must include a **business KPI layer** in addition to rankings and traffic.
- Every roadmap must separate **leading indicators** (crawlability, indexation, rankings) from **business outcomes** (qualified leads, calls, appointments, revenue contribution).
- Every executive summary must explicitly state what will move visibility versus what will move business performance.

### 4) Process methods from Advanced SEO Tool coverage
The referenced workflow emphasizes:
- Initial **brainstorming** to understand company, market, and product.[cite:61]
- Mapping the **customer journey** and digital touchpoints.[cite:61]
- Keyword strategy scored by **difficulty** and **strategic importance**.[cite:61]
- Explicit KPI definition, re-engagement thinking, budget allocation, and timing by phase.[cite:61]

**Adopt into the standard:**
- Every audit must include:
  - business/context intake,
  - customer journey mapping,
  - keyword cluster prioritization,
  - timeline,
  - budget/tool assumptions,
  - KPI framework.

## Standard audit sections for all future HTML audits
The Alena Krot HTML format should be upgraded to include these mandatory sections:

1. **Executive summary**
- Current status
- Top 5 issues
- Top 5 opportunities
- Expected impact by 90/180/365 days

2. **Business context**
- Offer and positioning
- Target audiences
- Main conversion actions
- Geographic focus
- Constraints of CMS/host/provider

3. **AI-first search briefing**
- AI Mode / AI Overviews implications
- Direct-answer extraction readiness
- Entity clarity
- AI citation readiness
- Brand mention consistency

4. **Technical audit**
- Crawl/indexation
- Core Web Vitals
- templates, metadata, canonicals, sitemap, robots
- structured data coverage
- media provenance if AI visuals are used

5. **Semantic + content architecture**
- Entity map
- Topical clusters
- Existing content gaps
- Cannibalization risks
- Internal linking opportunities

6. **Traditional SERP gap**
- Core non-brand keywords
- Ranking competitors
- Missing landing pages
- Content depth comparison

7. **AI citation gap**
- Google AI Mode / Overviews
- Perplexity
- ChatGPT
- Gemini
- Cited domains by platform and query

8. **Local / vertical layer**
- For local businesses: GBP, reviews, NAP, service-area pages
- For service businesses: treatment/service pages, trust signals, FAQs
- For real estate: property-type clusters, neighborhood/entity pages, agent schema, listing freshness, local authority signals

9. **Schema markup plan**
- Current schemas
- Missing schemas
- Entity relationships
- Priority JSON-LD implementations

10. **KPIs and measurement**
- SEO leading indicators
- AI visibility indicators
- Conversion indicators
- GA4 / Search Console / CRM mapping

11. **Roadmap and effort model**
- 30/60/90 days
- 6-month roadmap
- owner per task
- effort and priority

12. **Tool stack used / recommended**
- Tier 1 AI-native tools
- automation options
- validation tools

## Tool stack standard for this Space
Prioritize AI-native tools first, then automation, then manual verification.

### Tier 1
- Perplexity PRO for research and synthesis
- Semrush for keyword, competitor, backlink, and visibility data
- claude-seo style workflows for structured SEO tasks
- Optional: SE Ranking / Profound / Otterly / Peec AI for AI share-of-voice monitoring

### Tier 2
- n8n / Make / Metaflow for recurring automations
- Looker Studio or custom dashboard layer when reporting volume increases

### Tier 3
- Search Console
- GA4
- PageSpeed Insights
- Rich Results Test
- manual SERP and AI citation spot checks

## Data views to add to the HTML audit
To make the current Alena-style format more professional, add the following dashboard blocks:

- Visibility snapshot cards: indexed pages, top 10 keywords, AI mentions, local review count
- Opportunity matrix: impact vs effort
- Competitor gap heatmap
- AI citation comparison by platform
- Topical cluster map
- Schema coverage chart
- KPI timeline / milestone tracker

## Decision on format
**Decision:** use the latest Alena Krot HTML audit structure as the standard format for the next audit cycle unless a clearly superior expert-inspired format is identified later.[cite:59]

### Planned upgrades to that format
- More dashboard tiles and summary charts
- Separate AI citation gap panel
- Separate entity and semantic architecture panel
- Stronger KPI/business outcome section
- Vertical-specific modules (medical, then real estate)

## Adaptation for the next audited site: real estate agent
The next audit should keep the same shell but swap in real-estate-specific modules:
- location cluster strategy by neighborhood/city
- listing/indexation freshness
- agent and office entity schema
- property type pages
- local authority and review acquisition
- FAQ content for buyers, sellers, renters, investors
- AI-answer visibility for local property intent queries

## Recommended workflow for the next audit
1. Intake and business/context capture.
2. Pull live data from Semrush and Search Console.
3. Build entity map and topical clusters.
4. Run technical audit.
5. Run SERP gap and AI citation gap.
6. Draft roadmap with KPI ladder.
7. Render in the upgraded Alena-style HTML format.
8. Export supporting markdown summary when needed.

## Working rule going forward
Use one unified SEO + AEO + GEO audit program. Do not split classic SEO and AI visibility into separate workstreams. Build every audit around technical integrity, semantic clarity, entity strength, measurable business KPIs, and AI citation readiness.[cite:55][cite:57][cite:59][cite:64]

## Links
- Parent: [[Reference-General-INDEX]]
- Related: [[Point3_Console_Tech_Audit_Extended]]
