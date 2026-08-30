# Point 3 — Console/Tech Audit: What You Can See, With and Without Extra Tools (Extended)

## Direct Answer
A browser's built-in DevTools (Console + Network + Elements + Application tabs) already reveal most of a site's technical fingerprint with zero extra installs. Free browser extensions and standalone web tools add depth in specific areas: stack detection, SSL/TLS grading, DNS/security-header validation, and historical technology tracking.

## Tier 1 — No Extra Tools (Browser DevTools Only)

| Signal | Where to look | What it tells you |
|---|---|---|
| Server/CDN identity | Network tab → response headers (`Server`, `X-Powered-By`, `CF-Ray`, `X-Vercel-*`) | Hosting provider, CDN, sometimes backend language |
| Frontend framework | Console → global objects (`window.React`, `window.__NEXT_DATA__`, `window.Shopify`); Elements → script filenames | React/Next.js/Vue/Shopify/WordPress fingerprints |
| Third-party scripts | Network tab → all external `<script src>` requests | Analytics (GA4, GTM), Meta Pixel, chat widgets (Intercom, Drift), payment SDKs (Stripe.js) |
| API endpoints | Network tab → XHR/Fetch filter | Backend base URL, and often the exact data provider being called |
| Cookies/local storage | Application tab | Session/auth providers, A/B-testing tools, consent-state flags |
| Console errors/warnings | Console tab | Framework version deprecation warnings, exposed debug logs |
| Page-weight/request count | Network tab → summary bar | Rough performance signal without running a full audit |
| Crawl structure | Direct visit to `/robots.txt` and `/sitemap.xml` | Disallowed paths, full site map |
| Meta/CMS signals | View-source → `<meta name="generator">`, Open Graph tags, schema.org markup | CMS platform, SEO/social metadata setup |

## Tier 2 — With Free Extensions or Standalone Tools (name explicitly, ask user first)

| Tool | Type | What it adds beyond Tier 1 |
|---|---|---|
| **Wappalyzer** | Browser extension | One-click stack detection (CMS, JS framework, analytics, ecommerce platform, CDN), exportable to CSV |
| **BuiltWith** | Browser extension / builtwith.com | Broader technology profile plus historical stack-change tracking over time |
| **Lighthouse** | Built into Chromium DevTools (no install) | Performance, accessibility, SEO, and best-practices score out of 100 |
| **WhatRuns** | Browser extension | Alternative stack detector, similar scope to Wappalyzer |
| **Cookie-Editor / EditThisCookie** | Browser extension | Full cookie inventory for consent/tracking compliance checks |
| **HttpsOrNot / ismycodesafe.com / scantower.io / barrion.io** | Free standalone web tools (no install) | SSL/TLS certificate grading, HTTP security-header validation (HSTS, CSP, X-Frame-Options), DNS record checks, cookie-flag audits — all in one pass, letter-graded[web:142][web:144][web:146][web:148][web:149] |

## Why the Standalone Security Tools Matter
Beyond stack detection, a genuinely useful "tech audit" should include a security posture check, since missing HTTPS enforcement or absent security headers are common real findings in a one-page audit. Free tools like ismycodesafe.com and barrion.io run passively (no signup, no payloads sent) and return: HTTP security-header presence, SSL/TLS certificate validity and cipher strength, cookie-flag correctness (Secure/HttpOnly/SameSite), DNS record health, and CORS configuration — all within about 60 seconds[web:142][web:144][web:148][web:149].

## Recommended Combined Workflow for a One-Page Audit
1. Run Tier 1 checks manually (console + network + view-source) — always available, zero permission needed beyond looking at the page.
2. Ask the user: "Should I also reference Wappalyzer/BuiltWith for stack detection and a free SSL/header scanner for security posture?"
3. If approved, merge Tier 2 findings into the same one-page template, clearly labeling which tier each line came from.
4. Always flag: missing HTTPS enforcement, absent CSP/HSTS headers, exposed API keys in client-side JS, and third-party trackers loading without a visible consent mechanism — these are the highest-signal red flags for both technical debt and regulatory (GDPR) exposure.

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[site-tech-audit-skill]]
