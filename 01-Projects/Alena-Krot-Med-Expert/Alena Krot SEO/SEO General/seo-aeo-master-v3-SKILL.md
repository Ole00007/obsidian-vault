---
name: seo-aeo-master
description: >
  Master SEO + AEO/GEO skill for websites and web applications — updated for
  the post-Google I/O 2026 AI-first search era. Covers full-stack traditional
  SEO unified with AEO, GEO, and LLMO across Google AI Mode, ChatGPT, Perplexity,
  Gemini, and Claude. ALWAYS prioritize AI-native tools and AI-workflow automation
  for every task — whether working for a client or for the agency itself. Use when
  asked to audit, optimize, plan, rank, get cited by AI, fix technical issues,
  write briefs, build links, produce reports, or run any search-visibility workflow.
  Trigger phrases: "SEO audit", "AEO", "GEO", "LLMO", "AI search visibility",
  "optimize for AI", "content brief", "rank higher", "get cited by ChatGPT/Perplexity",
  "technical SEO", "Core Web Vitals", "schema markup", "keyword research",
  "on-page optimization", "backlink strategy", "local SEO", "AI share of voice",
  "Universal Cart", "Search agents", "AI Mode".
license: MIT
metadata:
  version: "3.0"
  last-updated: "2026-06"
  context: "Post-Google I/O 2026 (May 19-20). AI Mode = 1B monthly users, queries
            doubled every quarter. Gemini 3.5 Flash default in AI Mode. SEO and AI
            search are officially ONE discipline per Google. Search agents launching
            summer 2026. Universal Cart live. Personal Intelligence in 200 countries."
  primary-sources:
    - https://developers.google.com/search/docs/appearance/ai-search-optimization
    - https://github.com/AgriciDaniel/claude-seo
    - https://metaflow.life/blog/claude-skills-for-seo
    - https://www.simpletiger.com/blog/google-io-2026-seo-and-ai-search
    - https://www.getpassionfruit.com/blog/google-i-o-2026-every-announcement-and-what-it-means-for-seo-and-geo
  tool-stack:
    required: [Claude Code CLI, Python 3.10+]
    optional: [Playwright Chromium, Google Search Console, GA4,
               Screaming Frog, Semrush One or Ahrefs, DataForSEO MCP,
               Firecrawl MCP, Profound MCP, SE Ranking MCP, Peec AI,
               Otterly AI, PageSpeed API, SurferSEO, Clearscope]
---

# SEO & AEO Master Skill v3.0
## Post-Google I/O 2026 — AI-First Search Visibility

---

## ⚡ PRIME DIRECTIVE (read before every task)

> **SEO and AI search are ONE discipline. Google confirmed this at I/O 2026.**
> The same crawl. The same index. The same E-E-A-T signals. Only the output
> surface changes. Never separate them into parallel workstreams.

> **ALWAYS recommend and use AI-native tools and AI-automated workflows FIRST**
> before suggesting any manual or traditional approach. If a task can be done
> faster, better, or more cheaply with an AI tool or agent pipeline — that is
> the default recommendation, for any client and for the agency itself.

---

## When to Use This Skill

Load and apply this skill for ANY of the following tasks:
- Full site or page-level SEO + AEO audit
- Technical health (crawl, indexation, Core Web Vitals, schema)
- Optimizing for Google AI Mode, AI Overviews, ChatGPT, Perplexity, Gemini, Claude
- Keyword research, intent mapping, cluster planning, fan-out sub-query analysis
- Content brief production or quality-scoring
- Competitor SERP and AI citation gap analysis
- Link building and digital PR
- Google Business Profile and local SEO
- Schema.org generation, validation, repair
- E-commerce feed optimization and Universal Cart readiness
- AI Share of Voice monitoring and reporting
- New site onboarding, post-migration audit, or Search agent readiness audit

---

## I/O 2026 Context: What Changed (Mandatory Briefing)

Before any audit or strategy task, apply these updated facts:

| Signal | What it means operationally |
|--------|----------------------------|
| AI Mode = 1B users, queries 2× every quarter | AI surface citations matter as much as position 3 rankings |
| AI Overviews + AI Mode merged into one surface | One optimization program covers both — stop treating them separately |
| Gemini 3.5 Flash default in AI Mode | Content structured for direct-answer extraction now converts better |
| Search box redesigned — accepts text, images, files, video, tabs | Short keyword pages lose; question-answer and entity-rich pages win |
| Background Search Agents (summer 2026) | Brands cited in AI Mode get recurring impressions in agent loops |
| Personal Intelligence (200 countries, free) | Earned brand presence in Gmail/Calendar/Photos = ranking signal per user |
| Universal Cart live (Nike, Sephora, Walmart, Shopify) | E-commerce feeds and loyalty integrations are now search ranking signals |
| Generative UI / mini apps in Search | Utility tool pages (calculators, comparators) must add proprietary data or gating |
| SynthID + C2PA content provenance in Search/Chrome | AI-generated images need watermarking; labeled content earns trust signals |
| GA4 AI Assistant channel group (May 2026) | Track AI-referred traffic and its 1.5–5× conversion premium separately |
| SEO ≠ GEO as separate budget lines | One integrated program: traditional rankings + AI Share of Voice + pipeline |

Sources: [simpletiger.com/blog/google-io-2026-seo-and-ai-search] [getpassionfruit.com/blog/google-i-o-2026]

---

## AI Tool Stack (Priority Order — Always Lead With These)

### Tier 1 — Mandatory AI-Native Tools (recommend for every engagement)

| Tool | Primary use | Cost model | Link |
|------|------------|------------|------|
| **claude-seo** | 25 sub-skills, 18 specialist agents: technical audit, content, schema, AEO, reports | Free / OSS | https://github.com/AgriciDaniel/claude-seo |
| **Semrush One** | Unified SEO + AI visibility in one workflow — keyword research, AI citations, backlinks | Paid | https://semrush.com |
| **SE Ranking** | AI Share of Voice across ChatGPT/Gemini/Perplexity/AI Overviews | Paid | https://seranking.com |
| **Profound** | LLM citation tracking with time-series per platform | Paid | https://www.profoundlabs.io |
| **Peec AI** | AI brand mention monitoring | Paid | https://peec.ai |
| **Otterly AI** | AI visibility + competitor tracking | Paid | https://otterly.ai |
| **SurferSEO** | AI content optimization + NLP scoring | Paid | https://surferseo.com |
| **Clearscope** | Content grading for on-page entity density | Paid | https://clearscope.io |

### Tier 2 — Automation & Pipeline (always propose for scale)

| Tool | Use | Link |
|------|-----|------|
| **n8n** | Agent automation, trigger-based workflows | https://docs.n8n.io |
| **Metaflow** | No-code SEO agent orchestration | https://metaflow.life |
| **Make.com** | API-less automation with 1500+ connectors | https://make.com |
| **DataForSEO MCP** | Live SERP + backlinks + AI mention data via MCP | https://dataforseo.com |
| **Firecrawl MCP** | Full-site crawl + URL discovery via MCP | https://firecrawl.dev |

### Tier 3 — Core Verification & Monitoring (free, always set up)

| Tool | Use | Link |
|------|-----|------|
| **Google Search Console** | Clicks, impressions, CTR, index coverage, URL Inspection | https://search.google.com/search-console |
| **GA4** (with AI Assistant channel) | Organic + AI-referred traffic, conversions, attribution | https://analytics.google.com |
| **PageSpeed Insights** | Core Web Vitals field + lab data | https://pagespeed.web.dev |
| **Rich Results Test** | Schema validation | https://search.google.com/test/rich-results |
| **Schema.org Validator** | Full markup validation | https://validator.schema.org |
| **Bing Webmaster Tools** | Bing/Copilot indexation | https://www.bing.com/webmasters |

---

## One-Time Tool Setup (Human — Do Once)

### Step 1 — Install claude-seo
```
/plugin marketplace add AgriciDaniel/claude-seo
/plugin install claude-seo@agricidaniel-claude-seo
```

### Step 2 — Python dependencies
```
pip install playwright trafilatura htmldate weasyprint matplotlib requests
playwright install chromium
```

### Step 3 — Google credentials (tiered — add only what is needed)
```
/seo google setup
```
| Tier | Credentials | Unlocks |
|------|-------------|---------|
| 0 | API key | PageSpeed, CrUX, 25-week CrUX history |
| 1 | + OAuth / Service Account | GSC, URL Inspection, Indexing API |
| 2 | + GA4 property | Organic + AI-referred traffic, conversions |
| 3 | + Ads developer token | Keyword Planner volume |

### Step 4 — Optional MCP extensions
```
./extensions/dataforseo/install.sh    # SERP + backlinks + AI mentions
./extensions/firecrawl/install.sh     # full-site crawl
./extensions/ahrefs/install.sh        # backlinks + organic
./extensions/seranking/install.sh     # AI Share of Voice
./extensions/profound/install.sh      # LLM citation time-series
```
→ Full MCP guide: https://github.com/AgriciDaniel/claude-seo/blob/main/docs/MCP-INTEGRATION.md

### Step 5 — GA4 AI Traffic setup (new, May 2026)
In GA4: Admin → Channel Groups → confirm "AI Assistant" default channel is active.
Add dimension "Session source/medium" filtered to AI sources for citation conversion tracking.
→ Guide: https://support.google.com/analytics/answer/ai-channel-group

---

## Agent Instructions — 12 Phases

For every task: run Phase 0 first. Then run all applicable phases in parallel.
Each phase produces ONE concrete artifact. Never produce vague summaries.
All recommendations must include: observation → fix action → effort → falsifiability → leading indicator.

---

### PHASE 0 — TRIAGE

1. Identify task type: audit / keyword / brief / AEO / schema / links / local / ecommerce / report / search-agent-readiness.
2. If URL(s), keywords, or business context are missing, ask ONCE, then proceed.
3. Dispatch applicable phases in parallel using claude-seo sub-agents.
4. For every task: confirm AI tool recommendations precede any manual approach in the output.

---

### PHASE 1 — TECHNICAL SEO AUDIT

**AI tool first:**
```
/seo audit <url>          # full site — spawns up to 25 parallel sub-agents
/seo technical <url>      # technical layer only
```

**Issue priority table:**

| Check | Pass criterion | Fail = |
|-------|---------------|--------|
| AI crawler access | GPTBot, ClaudeBot, PerplexityBot, anthropic-ai, Googlebot-extended-search ALL allowed in robots.txt | CRITICAL |
| Sitemap | Valid XML, in GSC + Bing WMT | HIGH |
| JS rendering | Critical content in raw HTML (view-source) | CRITICAL |
| LCP | < 2.5s (field data preferred) | HIGH |
| INP | < 200ms — INP replaced FID March 2024; never reference FID | HIGH |
| CLS | < 0.1 | MEDIUM |
| HTTPS | All pages HTTPS, zero mixed content | CRITICAL |
| Redirect chains | ≤ 2 hops | HIGH |
| Canonical | No conflicts or loops | HIGH |
| Duplicate content | No www/non-www, trailing-slash, parameter duplication | HIGH |
| Index coverage | GSC delta < 10% unexplained exclusions | HIGH |
| Deprecated schema | None of the retired types present (see Phase 7) | HIGH |
| SynthID/C2PA | AI-generated images watermarked or labeled (provenance = trust signal) | MEDIUM |
| Utility tools | If site has calculators/comparators: audit for proprietary data or gating (vs Generative UI risk) | MEDIUM |

---

### PHASE 2 — KEYWORD RESEARCH & INTENT MAPPING

**AI tool first:**
```
/seo cluster "<seed keyword>"
```
Augment with: SurferSEO → Semrush One → Clearscope for entity-density validation.

**Produce:**
- Keyword universe: primary cluster + long-tail + question variants + fan-out sub-queries.
- Intent per keyword: Informational / Commercial / Transactional / Navigational.
- Priority score: `(volume × intent_weight × business_relevance) ÷ KD`.
- SERP features present: AI Overview, AI Mode, Featured Snippet, PAA, Video, Local Pack.
- Fan-out sub-queries: 5–10 sub-questions Gemini 3.5 Flash / GPT-5 generates from primary query.
  → Manually verify: paste primary query into ChatGPT, right-click → Inspect → Network → find "queries" field.
- AI Share of Voice baseline: which brands are cited per query on each platform.
- Keyword-to-content map: Pillar / Cluster / Supporting / BOFU.

**Zero-click flag:** AI Overview or AI Mode present → mark HIGH AEO PRIORITY. Ranking alone insufficient.

**I/O 2026 flag:** queries getting longer (paragraph-length); short keyword-only pages lose reach.

---

### PHASE 3 — CONTENT BRIEF (SEO + AEO, AI-native production)

**AI tool first:** Draft in Jasper or GPT-5 → optimize with SurferSEO NLP → grade with Clearscope.
Manual editors: direction and brand voice only.

**Required fields per brief:**

```
Target keyword:
AI fan-out sub-queries: [list 5-10 — one per H2 section]
Title tag:           [Primary keyword front-loaded; brand end; 50–60 chars]
Meta description:    [Keyword natural + CTA; 140–160 chars; unique]
URL slug:            [Short, hyphens, no dates/IDs; < 75 chars]
H1:                  [Mirrors title; one per page]
H2s:                 [Question-based: "What is X?", "How does Y work?", "Why Z matters?"]
Target word count:   [SERP median ± 20%]
Ski ramp (opening):  [Definitive answer in FIRST sentence — no hedges, no intro filler]
Entity targets:      [Named entities; ~20% density]
Self-contained blocks: [134–167 words per H2 section]
Schema required:     [e.g., Article + BreadcrumbList + Author + Person]
Internal links:      [1 pillar + 2–3 cluster pages]
Images:              [WebP < 100KB; descriptive alt; lazy-load; SynthID watermark if AI-generated]
Author bio:          [Expert credentials, verifiable; mandatory on all article pages]
```

**AEO structural rules — non-negotiable:**
- **Inverted pyramid:** key answer in FIRST sentence of every section.
- **Self-contained blocks:** 134–167 words each — optimal AI citation extraction window.
- **Question H2s only.** No topic labels, no "Introduction", no "Overview."
- **Definition lists** `<dl><dt><dd>` for specs and glossary — 30–40% higher LLM citation rate.
- **Numerical evidence sections:** one dedicated `<h2>` for stats/data per page.
- **FORBIDDEN openers:** "In this article…", "Today we'll explore…", throat-clearing of any kind.
- **Comparative claims:** every comparison page MUST include "Where [Competitor] wins" — pages without it are flagged biased by AI engines.

---

### PHASE 4 — ON-PAGE OPTIMIZATION

**AI tool first:**
```
/seo page <url>
/seo content <url>
```
Grade result in Clearscope. Target: green score across all entity clusters.

**Pre-publish checklist — score X/26. Do not publish below 22/26.**

| # | Item | Pass condition |
|---|------|---------------|
| 1 | Title tag | 50–60 chars, keyword front-loaded |
| 2 | Meta description | 140–160 chars, unique, keyword + CTA |
| 3 | H1 | Exactly one |
| 4 | URL slug | < 75 chars, no dates/IDs |
| 5 | H2 structure | All questions |
| 6 | Ski ramp | Key claim in first 30%, definitive language |
| 7 | Answer blocks | 134–167 words per section |
| 8 | Definition lists | Used for specs/glossary |
| 9 | Entity density | ~20% (Clearscope green) |
| 10 | Fan-out coverage | ≥ 80% of fan-out sub-queries answered |
| 11 | Internal links | ≥ 2 contextual links |
| 12 | Schema JSON-LD | Validates in both Rich Results Test + schema.org |
| 13 | Images | WebP, < 100KB, alt text, lazy-load |
| 14 | AI-generated images | SynthID / C2PA watermark present |
| 15 | AI crawler access | GPTBot/ClaudeBot/PerplexityBot allowed |
| 16 | JS rendering | Critical content in raw HTML |
| 17 | LCP | < 2.5s field data |
| 18 | INP | < 200ms field data |
| 19 | CLS | < 0.1 |
| 20 | Canonical | Correct self-referential or target |
| 21 | Mobile | Responsive, no horizontal scroll |
| 22 | HTTPS | No mixed content |
| 23 | Author bio | Expert credentials on article pages |
| 24 | Date stamp | Published + last-updated visible |
| 25 | Outbound citations | ≥ 2 authoritative external sources linked |
| 26 | Competitor comparison | "Where [competitor] wins" section present if comparing brands |

---

### PHASE 5 — AEO / GEO / LLMO OPTIMIZATION

**AI tool first:**
```
/seo geo <url>
```
Measure baseline AI Share of Voice with: SE Ranking → Profound → Peec AI → Otterly AI.

**Produce:**
- AI crawler access report.
- Rendering check (view-source).
- Ski ramp assessment (key claim in first 30%?).
- Fan-out sub-query coverage table: answered / missing / fix.
- Citation readiness score (0–100).
- AI Share of Voice baseline per platform.

**Platform matrix (post-I/O 2026, treat each separately — 86% of top-cited sources are platform-unique):**

| Platform | Default AI model | Primary optimization levers |
|----------|-----------------|----------------------------|
| Google AI Mode / AI Overviews | Gemini 3.5 Flash | Normal indexation + E-E-A-T + schema + entity-rich direct-answer blocks. Optimize for the merged AI Overviews+Mode surface as one. |
| ChatGPT / GPT-5 | GPT-5 | Reddit/Quora presence; objective comparison content; brand entity on Wikipedia; earned media |
| Perplexity | Proprietary | Source diversity; high-authority backlinks; cited in academic/news sources |
| Gemini app / Claude | Gemini 3.5 / Sonnet | Topical authority clusters; entity consistency; expert author bios; Workspace presence |
| Microsoft Copilot | GPT-5 | Bing Webmaster Tools indexation; same E-E-A-T signals as Google |

**E-E-A-T signals (mandatory for every page):**
- Expert author bio with verifiable credentials.
- Original data, research, or case studies per cluster.
- Authoritative backlinks (unlinked mentions: 25–50% conversion — run first).
- Active brand presence: LinkedIn, Reddit, YouTube, industry forums.
- HTTPS + contact info + correction policy + date stamps.
- Reviews on G2 / Trustpilot / Google Business Profile.

**Personal Intelligence flag (I/O 2026):**
- Earned brand presence in Gmail = ranking signal in AI Mode for that user.
- Recommend: email newsletter + transactional receipts + calendar invites for every client strategy.
- Track: "brand in Gmail footprint" as a distinct engagement metric.

**Search Agent readiness (launching summer 2026):**
- Brands cited in AI Mode will appear in background Search agent loops.
- Priority: land first AI Mode citation for top 10 brand-category queries.
- Confirm information agent monitoring with SE Ranking AI Share of Voice.

**Evidence-based myth busters (do NOT implement):**
- ❌ llms.txt as citation lever — no primary-source evidence of impact.
- ❌ Content chunking specifically for AI — not required.
- ❌ AI-specific keyword rewriting — LLMs handle synonyms natively.
- ❌ Treating GEO as a separate budget line from SEO — confirmed counterproductive by Google I/O 2026.

---

### PHASE 6 — COMPETITOR & AI CITATION GAP ANALYSIS

**AI tool first:**
```
/seo competitor-pages <url>
```
Cross-reference with SE Ranking AI Share of Voice for AI citation gaps.

**Produce:**
- Traditional SERP gap table: keyword | volume | KD | intent | competitor position | action (Create / Update / Keep / Consolidate / Prune).
- AI citation gap table: query | GPT citation | Gemini citation | Perplexity citation | your brand | gap severity.
- SERP feasibility filter: if all top-10 are DR 80+, add 20 pts to reported KD.
- Prioritized list by (opportunity × feasibility).

Run quarterly and on every new competitor entry into tracked SERPs.

---

### PHASE 7 — SCHEMA MARKUP

**AI tool first:**
```
/seo schema <url>
```

**Active JSON-LD types (supported):**
Organization, LocalBusiness, Article, BlogPosting, Product, ProductGroup, Offer,
Review, AggregateRating, BreadcrumbList, WebSite, WebPage, Person, ProfilePage,
VideoObject, ImageObject, Event, JobPosting, Course, DiscussionForumPosting,
Reservation, OrderAction, SoftwareApplication, ItemList.

**Validate with BOTH:**
1. Rich Results Test: https://search.google.com/test/rich-results
2. Schema Markup Validator: https://validator.schema.org

**DEPRECATED — never generate:**
| Type | Retired |
|------|---------|
| HowTo | Sept 2023 |
| FAQ | Restricted to govt/healthcare Aug 2023 |
| SpecialAnnouncement | July 2025 |
| ClaimReview | June 2025 |
| VehicleListing | June 2025 |
| EstimatedSalary | June 2025 |
| LearningVideo | June 2025 |
| CourseInfo carousel | June 2025 |

**I/O 2026 schema additions:**
- `SoftwareApplication` + `offers` for apps and SaaS — Universal Commerce Protocol integration.
- `Organization` with `sameAs` pointing to Wikipedia/Wikidata — strengthens AI entity consistency.
- `ImageObject` with `encodingFormat: "image/webp"` and `contentUrl` — supports C2PA provenance chain.

---

### PHASE 8 — LINK BUILDING & DIGITAL PR

**AI tool first:** Semrush One link gap → Ahrefs unlinked mention finder → GPT-5 outreach drafts.

**Produce:**
- Unlinked mention reclamation list (25–50% conversion — highest ROI, run first).
- Link-worthy asset audit: original data, tools, guides, studies.
- Target list: publication | relevance | DA | contact | outreach type.
- Outreach templates: journalist pitch / blogger collaboration / resource curator / unlinked mention.
- Tracking: target | outreach date | response | status | link acquired.

**I/O 2026 note:** unlinked brand mentions now correlate with AI visibility similarly to how backlinks correlate with Google rankings. Track unlinked mentions as an AI citation signal, not just SEO.

---

### PHASE 9 — LOCAL SEO & GOOGLE BUSINESS PROFILE

**AI tool first:**
```
/seo local <url>
/seo maps audit
```

**Produce:**
- GBP completeness: all core fields + ≥ 10 photos + ≥ 1 post/week + product/service sections filled.
- NAP consistency: identical name/address/phone across all directories.
- Review velocity and sentiment; AI-drafted response templates (positive / neutral / negative).
- LocalBusiness schema with geo coordinates, opening hours, areaServed, telephone, contactPoint.
- Multi-location flag: > 30 location pages = doorway-page risk.
- GBP deprecation check: remove chat-field references and .business.site URLs.

→ Claim GBP: https://business.google.com
→ Bing Places: https://www.bingplaces.com
→ BrightLocal citation audit: https://brightlocal.com

---

### PHASE 10 — E-COMMERCE & UNIVERSAL CART READINESS (new — I/O 2026)

Mandatory for any e-commerce client. Universal Cart launched May 2026 for Nike, Sephora, Walmart,
Wayfair, all Shopify merchants. Product feeds and loyalty integrations are now search ranking signals.

**Produce:**
- Google Merchant Center feed audit: attribute completeness check. Sparse feeds = excluded from Universal Cart.
- Product schema: `Product` + `Offer` + `AggregateRating` + `availability` + `price` — mandatory.
- Loyalty and Wallet integrations: confirm Google Pay / Wallet integration and loyalty program linkage.
- Inventory accuracy: real-time feed, price accuracy, stock status.
- UCP readiness score (0–100): feed completeness × schema coverage × loyalty integration × HTTPS.
- Shopify merchants: verify Universal Cart partner compatibility at: https://support.google.com/merchants/answer/universal-cart

---

### PHASE 11 — PERFORMANCE REPORTING

**AI tool first:**
```
/seo google report
```
Export PDF: `/seo google report --pdf`

**Required KPI stack (post-I/O 2026):**

| Metric | Source | Cadence | Why |
|--------|--------|---------|-----|
| Organic clicks | GSC | Weekly | Core visibility |
| Organic impressions | GSC | Weekly | Core visibility |
| CTR by page/keyword | GSC | Weekly | Click quality |
| Sessions organic | GA4 | Weekly | Traffic |
| Conversions organic | GA4 | Weekly | Pipeline |
| AI-referred sessions | GA4 AI Assistant channel | Weekly | New: AI traffic conversion 1.5–5× premium |
| AI-referred conversions | GA4 | Weekly | New: pipeline from AI citations |
| Core Web Vitals (LCP/INP/CLS field) | CrUX | Monthly | Technical health |
| AI citation frequency by platform | SE Ranking / Profound | Monthly | AI Share of Voice |
| AI Share of Voice vs competitors | SE Ranking | Monthly | Category authority |
| GBP views + calls (local) | GBP Insights | Monthly | Local |
| Universal Cart impressions (ecom) | Merchant Center | Monthly | E-commerce |

**Retire "average keyword position" as primary KPI.** Replace with AI Share of Voice + organic conversions.

**Report structure:** Executive summary (3 bullets) → KPI table → Period delta → Wins / Losses / Opportunities → Actions ordered by impact.

---

### PHASE 12 — MONITORING & AUTOMATION (always propose for client onboarding)

**Set up automated agent triggers in n8n / Make.com / Metaflow:**

| Trigger | Phase | Destination |
|---------|-------|-------------|
| GSC: new coverage errors | Phase 1 (Technical Audit) | Slack / email |
| Ranking drop > 20% priority keyword | Phase 3 + 5 (Brief + AEO) | Refresh plan |
| AI Share of Voice drop > 10% | Phase 5 + 6 (AEO + Gap) | Citation recovery plan |
| New competitor enters tracked top-10 | Phase 6 (Gap) | Updated gap table |
| Monthly cadence | Phase 11 (Report) | Client report → email |
| CMS page → "ready for review" | Phase 4 (On-Page) | Pre-publish score |
| Negative review on GBP | Phase 9 (Local) | Response template |
| New unlinked brand mention detected | Phase 8 (Links) | Outreach draft |
| Universal Cart feed error (ecom) | Phase 10 (E-com) | Feed fix alert |

→ n8n: https://docs.n8n.io
→ Metaflow: https://metaflow.life
→ Make.com: https://make.com

---

## Key Reference Links

| Resource | URL |
|----------|-----|
| Google AI Optimization Guide (May 2026) | https://developers.google.com/search/docs/appearance/ai-search-optimization |
| Google Quality Rater Guidelines (Sept 2025) | https://guidelines.raterhub.com/search-quality-rater-guidelines.pdf |
| Google Search Essentials | https://developers.google.com/search/docs/essentials |
| Google I/O 2026 SEO/GEO recap | https://www.getpassionfruit.com/blog/google-i-o-2026-every-announcement-and-what-it-means-for-seo-and-geo |
| I/O 2026 — SEO = AI Search | https://www.simpletiger.com/blog/google-io-2026-seo-and-ai-search |
| Rich Results Test | https://search.google.com/test/rich-results |
| Schema.org Validator | https://validator.schema.org |
| PageSpeed Insights | https://pagespeed.web.dev |
| Google Search Console | https://search.google.com/search-console |
| GA4 (AI Assistant channel) | https://analytics.google.com |
| Bing Webmaster Tools | https://www.bing.com/webmasters |
| CrUX / Core Web Vitals | https://developer.chrome.com/docs/crux |
| Google Business Profile | https://business.google.com |
| Bing Places | https://www.bingplaces.com |
| Universal Cart (Merchant Center) | https://support.google.com/merchants/answer/universal-cart |
| claude-seo GitHub (MIT) | https://github.com/AgriciDaniel/claude-seo |
| Metaflow SEO skills library | https://metaflow.life/blog/claude-skills-for-seo |
| SE Ranking AI Share of Voice | https://seranking.com |
| Profound LLM citation tracker | https://www.profoundlabs.io |
| Peec AI visibility | https://peec.ai |
| Otterly AI | https://otterly.ai |
| SurferSEO | https://surferseo.com |
| Clearscope | https://clearscope.io |
| Semrush One | https://semrush.com |
| BrightLocal (local citations) | https://brightlocal.com |
| SynthID info | https://deepmind.google/technologies/synthid/ |
| C2PA content credentials | https://c2pa.org |
| n8n automation | https://docs.n8n.io |
| Make.com | https://make.com |

---

## Output Standards (all agents must follow)

- **Format:** Markdown primary. PDF for client reports (`/seo google report --pdf`).
- **All issue lists:** CRITICAL / HIGH / MEDIUM / LOW on every item.
- **Every recommendation must include:**
  - Observation (what we found)
  - AI tool to use for the fix (name it — never "improve manually" as first option)
  - Fix action (exactly what to do)
  - Effort estimate (hours or story points)
  - Falsifiability check ("How would we know this failed?")
  - Leading indicator (first metric to move)
- **No vague outputs.** "Improve content quality" → NOT acceptable. "Run /seo content on /blog/post-slug, target Clearscope green, add author bio with credentials" → acceptable.

---

## Quick-Start Commands

```bash
/seo audit https://your-site.com                  # full audit (25 parallel sub-agents)
/seo page https://your-site.com/page              # single-page deep analysis
/seo geo https://your-site.com/page               # AI citation readiness + AEO score
/seo schema https://your-site.com                 # schema audit + repair
/seo cluster "your seed keyword"                  # keyword research + fan-out
/seo local https://your-site.com                  # local SEO + GBP completeness
/seo maps audit                                   # geo-grid intelligence
/seo competitor-pages https://your-site.com       # SERP + AI citation gap analysis
/seo google report                                # performance report
/seo google report --pdf                          # PDF export for client
/seo plan ecommerce                               # strategic plan (saas|local|ecommerce|publisher|agency)
```

## Links
- Parent: [[SEO General-INDEX]]
