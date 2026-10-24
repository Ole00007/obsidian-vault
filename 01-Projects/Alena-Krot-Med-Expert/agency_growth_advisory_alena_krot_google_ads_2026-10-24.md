---
title: Agency Growth Advisory - Alena Krot Google Ads Launch
created: 2026-10-24
tags: [agency-growth, alena-krot, google-ads, seo, aeo, geo, advisory]
related: [Alena-Krot-Med-Expert-INDEX, Agency Growth Advisory]
---

# Agency Growth Advisory — Alena Krot Google Ads Launch
*Prepared by: AGENCY-GROWTH (Avibe agency) — October 24, 2026*

## Source files reviewed
- `/Users/olesiarasing/Projects/Alena Krot/Alena_LP_SEO_AEO_GEO_Ads_Audit_v3.html` (deployed at https://alenakrot-audit.pages.dev/)
- `/Users/olesiarasing/Projects/Alena Krot/Alena_Krot_Campaign_Keywords.md`
- `/Users/olesiarasing/Projects/Alena Krot/Hermes_GoogleAds_Config_v2.json`
- `/Users/olesiarasing/Projects/Alena Krot/Hermes_GoogleAds_Prompt_v2.md`
- Live crawl of alenakrot.com (3 LPs, sitemap, robots.txt, analytics tags) — Oct 24, 2026

## Live crawl — real findings vs audit assumptions
- **sitemap.xml "Palermo missing" was a FALSE ALARM.** The audit checked the sitemap index (`/sitemap.xml`, 333 bytes). Palermo and Ventimiglia ARE present in the sub-sitemap `/sitemap_pages.xml` (51,735 bytes). Correct the LP_Audit row from "Needs check / P0" to "Verified — in sitemap_pages.xml."
- **robots.txt** has `Crawl-delay: 30` — explains the 3x crawl failure on 2026-10-23. Fix `crawl_landing_pages.py` to add `time.sleep(35)` between requests.
- **GA4 is installed** (`gtag('config', 'G-H2SM80CJHR')`, loaded via googletagmanager.com) BUT **Consent Mode v2 is NOT** — zero `gtag('consent', ...)` calls found. EU conversion tracking will undercount.
- **No Google Ads conversion tag** (AW-ID) on the site — Step 3 (tracking verification) is still needed.
- **Piwik/Matomo** (`_paq`, sbbanalytics.com, site ID 161468) runs alongside GA4 — redundant, potential GDPR conflict, potential monthly cost.
- **FR/RU Ventimiglia pages exist** (`/fr/medicina-estetica-ventimiglia` → 200, `/ru/...` → 200) but content is minimal (FR: only "médecin"; RU: "генуя" + "адрес").
- **No GBP widget** or Google Maps embed found on any LP.
- **Treatment terms** found in page body: laser, filler, botolino, biostimolazione, lipo, peeling, "tariffa" (Palermo).
- **Meta descriptions** all contain "Trattamenti personalizzati e naturali" — borderline ad-policy risk.
- **Schema types**: only `WebSite` — no `Physician`, `MedicalBusiness`, `LocalBusiness`, `Person`, `FAQPage`, `BreadcrumbList`.

## Three sections of the full advisory
Full advisory: `/tmp/agency_growth_alena_advisory.md`

### 1. What to ADD (7 items)
1. **Consent Mode v2** — P0, before launch (Step 5)
2. **GSC query cross-check** before bidding — P0, before Step 4
3. **Google Business Profile verification** — P0, 7-14 day window
4. **Ad extensions** (call, sitelink, structured snippet, callout) — P0, in RSA draft
5. **Entity bio page** for AEO/GEO — P1, weeks 1-2
6. **Cost_Traction_Log file** — P0, before Step 7
7. **Google Ads API read-only connector** — P1, before CRON jobs

### 2. How to OPTIMIZE the plan (7 items)
A. Meta descriptions / "Trattamenti" compliance rewrite — P0
B. Homepage above-fold Genova focus (URL frozen, content reorder only) — P1
C. Separate CTR/CPC caps for brand vs category ad groups — P1
D. Third ad group: "Brand + Geo" — P0
E. FR/RU Ventimiglia content expansion — P1
F. Simplify traffic model (remove impressions/2.5 frequency assumption) — P2
G. Fix crawl script to respect robots.txt crawl-delay — P1

### 3. How to OPTIMIZE COST (7 items)
A. Welcome bonus timing modeling (retroactive vs expiring credit) — P0
B. Tighten CRON CPC alert (>2x → >1.3x, per ad group) — P0
C. CPL-based escalation added to CRON ($60 target → pause at CPC > 2.4 EUR) — P1
D. Ad-group-level CPC caps, not flat 2.50 EUR — P1
E. Ventimiglia activation budget increase (8 → 10 EUR/day) when activated — P1
F. Free competitor keyword research (manual SERP, related searches) — P2
G. Remove Piwik/Matomo redundancy (keep GA4 + Google Ads) — P1

## What the audit got right (preserve)
- CPC ranges labelled as "modelled, not guaranteed" — no invented numbers
- Search-only, no PMax/DG (Health-sensitive category)
- Genova active, others paused (geo sequencing)
- GSC-first data hierarchy
- Flazio-only (no migration)
- Free crawl script (cost discipline)

## Pre-launch priority matrix
| P0 (blocking) | Editor access + bonus window | Meta rewrite + ad extensions | Consent Mode v2 + GA4 events | GSC query export | GBP verification | Cost log file | Tiered CPC + 3rd ad group |
| P1 (early) | Homepage Genova focus | Entity bio page | Remove Piwik | Search-terms review + negatives | | |

## Links
- [[Alena-Krot-Med-Expert-INDEX]]
- [[05-Daily/2026-10-24]]
