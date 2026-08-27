# LP Specs — Studio Legale Associato Romanelli — Audit SEO/AEO/GEO

## Project Identity
- **Client:** Studio Legale Associato Romanelli — Genova
- **Domain:** studio-romanelli.it
- **Agency:** AVIBE Agency
- **Date:** 9 Agosto 2026
- **File:** `web-site-0.3-audit-seo-aeo-geo-studio-romanelli.html`

## Tech Stack
- **Format:** Single self-contained HTML5 (CSS + JS inline)
- **CSS:** Custom properties (navy/gold/paper palette), no frameworks
- **JS:** Vanilla (IntersectionObserver, localStorage, DOM toggle)
- **Images:** Local PNGs in `artefacts/` subfolder
- **Fonts:** Georgia (serif headings), Helvetica Neue (sans body)

## Colour System
| Token | Light | Dark |
|-------|-------|------|
| --navy | #152238 | #0d1627 |
| --gold | #b08d57 | #c4a46b |
| --paper | #faf8f4 | #13151a |
| --ink | #20211f | #e8e6e0 |

## Features Implemented
- [x] Sticky nav with section-anchored menu (6 items, 00–05)
- [x] Hero image background (sala riunioni) with gradient overlay
- [x] Dark/light theme toggle (localStorage persisted)
- [x] Italian/English language toggle (localStorage persisted)
- [x] Scroll reveal animations (IntersectionObserver)
- [x] Image gallery with glow hover effect
- [x] Accordion dropdowns (anomalie sitemap, KPI baseline)
- [x] Clickable WhatsApp FAB
- [x] Cookie consent banner + preference modal
- [x] Google Maps embed (AVIBE Agency, Corso Italia Genova)
- [x] Bilingual content (every section IT/EN paired)
- [x] Responsive mobile layout (hamburger menu, stacked grids)

## Page Structure
1. Cookie banner (fixed bottom)
2. Top bar (AVIBE brand + lang/theme controls)
3. Sticky nav (section anchors)
4. Hero cover (image + overlay + title + meta)
5. Gallery (4 images grid)
6. Section 00 — Summary (score panels)
7. Section 01 — Architecture (cards + dropdown table)
8. Section 02 — Technical SEO (badge cards)
9. Section 03 — Local SEO/GEO (table + callout)
10. Section 04 — AEO/Generative Search (cards)
11. Section 05 — Action Plan (numbered steps + KPI dropdown)
12. Section 06 — Methodological Note (basement/footer)
13. Map — AVIBE Agency location
14. Footer — contacts, links, credits
15. WhatsApp FAB (fixed bottom-right)

## Section 06 Rule
Nota metodologica is NOT in the nav menu — stays only in the footer/basement area.

## Copy Rules
- Italian first, English toggle
- Every `<p>`, `<h4>`, `<span>` has `lang="it"` and `lang="en"` paired
- `data-lang="en"` on `<body>` toggles visibility
## Links
- Parent: [[Studio-Romanelli-INDEX]]
- Related: [[Studio-Romanelli-INDEX]]
