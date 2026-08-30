---
name: site-tech-audit
description: >
  Rapid one-page technical audit of any website using only browser
  console/network tools plus optional free browser extensions. Use when the
  user shares a URL, screenshot, or console log and wants a quick technical
  teardown of a site's stack, performance signals, tracking/analytics setup,
  and security posture — separate from the deeper industry-competitive-analyst
  skill, which covers business/market analysis. This skill covers the TECH
  layer only. Always ask the user for explicit permission before enabling
  browser extensions or plugins, and name exactly which ones you intend to use.
license: Proprietary
metadata:
  target_audience: analysts, auditors, founders auditing any website's tech stack
  domain_year: 2026
  output_format: one-page technical summary (markdown or single Excel sheet)
---

# Site Tech Audit (One-Page)

## When to Use This Skill
Trigger this skill when the user:
- Shares a URL and asks for a "tech audit," "site audit," or "what's this site built with"
- Pastes a browser console/network log and asks what can be inferred from it
- Wants a quick technical due-diligence pass on a competitor or target site before deeper business analysis

This skill is TECH-ONLY. For market size, competitors, and business-case strengths/weaknesses, hand off to the `industry-competitive-analyst` skill.

## Step 0 (Mandatory): Ask About Tooling
Before starting, ask the user:
1. "Do you want a no-extra-tools audit (console + network tab only), or should I use additional free browser extensions for deeper detection?"
2. If they want deeper detection, confirm which extensions are acceptable to reference/use (see list below) — never assume permission.

## Tier 1 — No Extra Tools (Console + Network Tab Only)
With just the browser's built-in DevTools (Console + Network + Elements tabs), you can reliably see:
- **Server/CDN**: response headers (`Server`, `X-Powered-By`, `CF-Ray` for Cloudflare, `X-Vercel-*`, etc.)
- **Frontend framework hints**: JS bundle filenames, inline script tags, global window objects (`window.React`, `window.__NEXT_DATA__`, `window.Shopify`, etc.) visible in Console
- **Third-party scripts/trackers loaded**: every external `<script src>` call visible in Network — analytics (GA4, GTM, Meta Pixel), chat widgets (Intercom, Drift), payment SDKs (Stripe.js, PayPal SDK)
- **API endpoints called**: XHR/fetch calls in Network tab reveal backend API base URLs and sometimes the data provider (e.g. a VIN-report app calling a specific third-party report API)
- **Cookies and storage**: Application tab shows cookies, localStorage keys — often reveals A/B testing tools, session/auth providers
- **Console errors/warnings**: framework version warnings, deprecated API usage, exposed debug logs
- **Page load waterfall**: request count, total page weight, largest contentful resource — rough performance signal
- **robots.txt / sitemap.xml**: crawlable via direct URL, reveals site structure and disallowed paths
- **View-source / HTML meta tags**: CMS generator tags (e.g. `<meta name="generator" content="WordPress 6.x">`), Open Graph tags, schema.org markup

## Tier 2 — With Free Browser Extensions (Ask User First)
Name these explicitly and confirm before using:
- **Wappalyzer** (Chrome/Firefox extension) — detects CMS, frameworks, analytics, ecommerce platform, CDN, programming language in one click, exportable to CSV
- **BuiltWith** (browser extension or builtwith.com lookup) — broader technology profile, historical stack changes
- **Lighthouse** (built into Chrome DevTools, no install needed) — performance, accessibility, SEO, and best-practices score out of 100
- **EditThisCookie / Cookie-Editor** — full cookie audit for consent/tracking compliance checks
- **HTTP Headers** extension or `curl -I <url>` — full response header dump without opening DevTools
- **WhatRuns** — alternative to Wappalyzer, similar detection scope

## Mandatory Workflow for Every Site Audit
1. Ask Step 0 tooling question.
2. Run Tier 1 checks; list findings under: Server/Hosting, Frontend Stack, Third-Party Scripts, API Endpoints Observed, Cookies/Storage, Performance Signal, CMS/Meta Signals.
3. If approved, run Tier 2 and merge findings (mark clearly which tier each finding came from).
4. Flag anything with security or compliance relevance (missing HTTPS enforcement, exposed API keys in JS, third-party trackers without visible consent banner).
5. Summarize as ONE PAGE — a single markdown page or a single Excel sheet, never multi-page unless the user explicitly asks for more depth.
6. Offer to hand off findings to `industry-competitive-analyst` skill if the user wants business/market context added.

## One-Page Output Template
| Section | Content |
|---|---|
| Site & Date | URL, audit date |
| Hosting/CDN | Server header findings |
| Frontend Stack | Framework, JS libraries |
| Third-Party Scripts | Analytics, trackers, chat, payment SDKs |
| API/Data Sources Observed | Endpoints called, inferred data providers |
| Performance Signal | Lighthouse score or request count/weight |
| Security/Compliance Flags | HTTPS, exposed keys, missing consent banner |
| Tooling Used | Tier 1 only / Tier 1+2 (name extensions) |

## Escalation Rule
If the user needs authenticated-area auditing, headless-browser automation, or repeated scheduled monitoring, say so explicitly and recommend a coding-capable mode/tool (e.g. a script using Playwright/Puppeteer) rather than manual DevTools inspection.

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[Point3_Console_Tech_Audit_Extended]]
