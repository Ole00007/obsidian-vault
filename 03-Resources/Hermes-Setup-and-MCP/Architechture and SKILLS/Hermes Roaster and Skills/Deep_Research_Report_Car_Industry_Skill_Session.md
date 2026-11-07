# Deep Research Report: Car-Industry Analyst Skill — Legal Sources, Console Tech Audit, Excel Iteration, Site-Audit Skill, and Skill Marketplaces

*Corrects the earlier placeholder that was mistakenly shared instead of this report.*

## 1. Character Count of the Skill Created

The `industry-competitive-analyst` skill (v2, the EU/Italy-specific version built in that session) was **9,147 characters** including YAML frontmatter and full body.

## 2. Legal Regulation Sources — EU & Italy, Fixed Hierarchy

A two-tier sourcing model was established so the agent never presents a secondary/aggregator summary as binding law:

| Tier | Source | Scope | Role |
|---|---|---|---|
| 1 — Primary EU | **EUR-Lex** (eur-lex.europa.eu) | Official Journal of the EU, regulations, directives, consolidated texts, EU case law | The binding legal text — always the final citation for "what the law says" |
| 1 — Primary Italy | **Normattiva** (normattiva.it) + **Gazzetta Ufficiale** (gazzettaufficiale.it) | Consolidated Italian law ("multivigente"), original enacted decrees | Binding Italian national law |
| 2 — Secondary/aggregator | **vLex** (vlex.com) | 100+ jurisdictions, case law, AI-assisted comparative research (Vincent AI), 1B+ documents | Interpretation, case law, cross-border comparison — never the final word on binding text |
| 2 — Secondary/aggregator | **Lexroom.ai** | AI-aggregated EU/national regulation + jurisprudence summaries | Fast first-pass research, always verified against Tier 1 before being quoted as authoritative |

Rule fixed into the skill: vLex and Lexroom.ai are used strictly for interpretation, case law, and comparative practice — the actual binding requirement is always traced back to and cited from EUR-Lex or Normattiva/Gazzetta Ufficiale.

## 3. What a Console Reveals — With and Without Extra Tools

**Tier 1 — No extra tools (browser Console + Network + Elements tabs only):**
- Server/CDN identity via response headers (`Server`, `X-Powered-By`, `CF-Ray`, `X-Vercel-*`)
- Frontend framework hints from JS bundle names and global window objects (`window.React`, `window.__NEXT_DATA__`, `window.Shopify`)
- Every third-party script loaded (analytics, tag managers, chat widgets, payment SDKs) visible in Network
- API endpoints called via XHR/fetch — reveals the backend base URL and likely data provider
- Cookies and localStorage keys — reveals A/B-testing tools, session/auth providers
- Console errors/warnings — framework version flags, deprecated API usage
- Rough performance signal from total request count and page weight
- `robots.txt` / `sitemap.xml` — crawlable directly, reveals site structure
- View-source meta tags — CMS generator tag, Open Graph tags, schema.org markup

**Tier 2 — With free browser extensions (must ask user first, name explicitly):**
- **Wappalyzer** — CMS/framework/analytics/ecommerce stack detection, exportable to CSV
- **BuiltWith** — broader technology profile and historical stack changes
- **Lighthouse** — built into Chromium DevTools, no install needed; performance/accessibility/SEO score out of 100
- **Cookie-Editor / EditThisCookie** — full cookie/consent audit
- **HTTP Headers extension** (or a direct header request) — full response header dump
- **WhatRuns** — alternative stack-detection tool

This distinction became the backbone of the dedicated `site-tech-audit` skill (see companion file), which always asks the user's permission before invoking Tier 2 tools and delivers findings as a single-page summary.

## 4. Excel Output Iteration — Legal & Local-Precision Financial Sheets

The `industry-competitive-analyst` skill's default deliverable was iterated from a generic competitor workbook into a fixed six-sheet template:

| Sheet | Required Content |
|---|---|
| Overview | Scope statement, glossary, sheet index with hyperlinks |
| Competitors | Business model, pricing, data sources, strengths, weaknesses per competitor |
| Legal & Regulatory | Tier-1 binding rules (EU + local), Tier-2 case law/practice notes, open legislative risks |
| Financial & Market Sizing | Global figure **and** precise local/national market volume for the scoped geography, cited separately, with growth rate |
| Strengths-Weaknesses | Conditional-formatting heatmap scorecard + comparison chart |
| Architecture (B2B) | Per-customer-segment workflow, moat levers, billing model |

Key rule added: financial sizing must never stop at a global/EU-wide figure — it must break down to the exact national/regional market volume for the user's scoped geography, citing local statistical agencies, chambers of commerce, or sector associations wherever available, and stating explicitly when no local-precision figure could be found.

## 5. Site-Audit Skill — Delivered Separately

A dedicated `site-tech-audit` skill was created (see the companion `site-tech-audit-skill.md` file), scoped to the tech layer only, structured around:
- A mandatory Step 0 asking the user whether to use Tier 1 (console/network only) or Tier 2 (named free extensions)
- A fixed one-page output template (Site & Date, Hosting/CDN, Frontend Stack, Third-Party Scripts, API/Data Sources Observed, Performance Signal, Security/Compliance Flags, Tooling Used)
- An explicit hand-off point to the `industry-competitive-analyst` skill when business/market context is also needed

## 5.1 Skill Marketplaces Benchmarked

Five directories were identified as the best sources to benchmark competitive-research and business-analysis skill patterns against:
- **Agensi** (agensi.io) — curated, security-scanned marketplace with 1,600+ skills and creator revenue-share
- **ClaudeSkills.info** — large free directory aggregating SKILL.md files from GitHub
- **skills.sh** — command-line-focused install directory with a large community catalog
- **awesome-claude-skills** (GitHub, multiple forks: travisvn, ComposioHQ, BehiSecc) — curated lists of 1,000+ production-ready skills
- **awesomeskill.ai** — browsable marketplace pulling SKILL.md files from GitHub

## Note on This Report

This document replaces the earlier placeholder artifact that was mistakenly shared with only the word "placeholder" visible — that was a tooling error, not an intentional empty deliverable. All findings above reflect the actual research and skill iterations completed across that session.

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[Deep_Research_Report_Car_Industry_Skill_Session (1)]]
