# Template SITE-AUDIT 1_ENNEFEX — oct 2026 (v3, updated 21 Oct 2026)

Reusable bilingual (IT/EN) website-audit report, built in the style and structure of the *1_ENNEFEX* example (dark & gold theme, sticky header, hero + score card, evidence-labelled findings, comparison tables, priorities list, language toggle, back-to-top button) plus a **Growth** page (animated diagrams, PNG illustrations and a break-even calculator) to help close the deal.
Reference production use: **Goldoni 6 audit (17 Oct 2026, updated 21 Oct 2026)**. Scope of every audit: **technical + text layer only** (market/competitive business analysis is a separate skill and is offered, not assumed).

---

## HARD RULES — apply to every HTML file prepared, no exceptions

1. **Hamburger ("sandwich") menu on mobile and tablet (≤ 1100 px), always.** One button (`.menu-toggle`, 44 px tap target, `aria-expanded`, `aria-controls="site-menu"`) opens/closes the page menu; it closes on link tap, `Esc` and outside tap; the language toggle stays visible in the header. Implemented by `assets/menu.js` + the `menu-toggle` / `site-nav` rules in `css/extra.css`; the single-file build inlines the same code.
2. **External links stay clickable on any host** (Cloudflare Pages `*.pages.dev`, Netlify, plain hosting): absolute `https://` URL, `target="_blank"`, `rel="noopener noreferrer"`. They are never rewritten by `lang.js` (same-origin links only) and never intercepted by page JavaScript. This covers the footer client link (e.g. `goldoni6.it ↗`).
3. **Always share both** the single HTML file **and** the ZIP bundle (`_bundle/` with pages, `css/`, `assets/`, `images/`) when the full audit report is requested; after any change, re-check the ZIP and re-share it.
4. **Evidence labels and honesty:** every finding labelled; never claim "all good" or a result without evidence; scenarios and calculators are labelled as simulations, not forecasts.
5. **Bilingual IT/EN** in the same file, Italian default; **motion respects `prefers-reduced-motion`**; no content is hidden when JavaScript is off.

## 0. What changed in v3 (21 Oct 2026)

- Hamburger menu + header restructure (`.header-right` holds menu, language toggle and burger); header is sticky again on phones.
- **New page `crescita.html` (Growth):** PNG illustration, animated "growth ladder" (three packages), animated 5-step path to direct bookings, break-even calculator (inputs editable: stay value, OTA commission, direct-channel cost, shifted bookings, package), 8-week deliverables timeline, "why now" and call-to-action buttons.
- **Images (`images/*.png`):** `residence-growth-hero.png`, `package-ladder.png`, `guest-journey.png` — generic hospitality illustrations in the theme palette (no text inside; alt text in IT/EN). Replace or remove if the sector is not hospitality.
- **Footer address** moved into `config.json` (`AGENCY_PLACE_IT/EN`), e.g. "Corso Italia, Genova, Italia".
- Earlier v2 changes kept: one-line "Da sapere" footer note, shared pricing appendix with non-overlapping package ladder, one source per website with sequential numbering, evidence legend, next-steps box, impersonal/plural voice, `lang.js` fix for language persistence over http(s), `theme-color` meta, `noindex`.

## 1. Package contents

| Path | Purpose |
|---|---|
| `index.html` | Summary: hero image, score card, critical callouts, opportunity, evidence legend, verified / not verified, coverage, critical points, public findings, strengths, next steps |
| `tecnico.html` | Site audit: technical settings, layout (incl. mobile menu check), text quality, text presentation, Search Console and Business Profile, links |
| `canali.html` | External channels (OTAs, directories, maps, listings): same fact compared across sources, not-found list, fix |
| `faq.html` | FAQ block: journey illustration, why enlarge, ready-to-publish answers, answers to complete with the owner |
| `competitors.html` | Comparable operators: table + takeaways |
| `seo.html` | SEO / AEO / GEO: layers, actions, structured-data starter, phases, multilingual test questions, chatbot rules |
| `crescita.html` | Growth page (deal-closing): ladder, path, calculator, timeline, why now, CTA |
| `roadmap.html` | Priorities, data needed, tools used, optional pricing appendix (shared), sources |
| `css/base.css`, `css/style.css` | Original theme files (unchanged) |
| `css/extra.css` | Additions only: lists, callouts, source markers, FAQ accordion, hamburger menu, figures, animated diagrams, calculator, buttons, print |
| `assets/lang.js`, `assets/nav.js` | Language toggle (v2 fix) and back-to-top (unchanged) |
| `assets/menu.js`, `assets/growth.js` | Hamburger menu; reveal-on-scroll animations + calculator |
| `images/` | Three PNG illustrations |
| `config.json`, `fill_template.py` | Placeholder values; fills `{{KEYS}}` → `dist/` (`--single` also builds one self-contained file with images inlined) |

## 2. Quick start

1. Edit `config.json` (client name, domain, URL, location, dates IT/EN, agency, agency place IT/EN).
2. Replace every `[square brackets]` text with the real finding (IT + EN). Remove rows/cards you do not need; never invent data.
3. Growth page: set package names and prices in the ladder **and** the `data-min` / `data-max` attributes of the calculator options; cite one source per website for any commission or cost figure.
4. Run `python3 fill_template.py --single`.
5. Check `dist/` (multi-page, for Netlify / Cloudflare Pages) and `dist/audit-single.html` (one file; menu, hamburger and language toggle work inside previews).
6. Deliver **both** the single HTML and the ZIP of the multi-page bundle.

## 3. Placeholders (`config.json`)

| Key | Example |
|---|---|
| `CLIENT_NAME` | Residence Hotel Goldoni 6 |
| `DOMAIN` | goldoni6.it |
| `CLIENT_URL` | https://goldoni6.it/ |
| `LOCATION` | Rimini, Italia |
| `AUDIT_DATE_IT` / `AUDIT_DATE_EN` | 17 ottobre 2026 · agg. 21 ottobre / October 17, 2026 · upd. October 21 |
| `AGENCY` | Avibe Agency |
| `AGENCY_PLACE_IT` / `AGENCY_PLACE_EN` | Corso Italia, Genova, Italia / Corso Italia, Genoa, Italy |

Structured-data placeholders use `[[double square brackets]]` so the script never touches them.

## 4. Writing rules (carry over to every audit)

1. **Evidence labels are mandatory** on every finding: *Verificato / Verified*, *Da anteprima di ricerca / Snippet-level*, *Non verificato / Not verified*, *Raccomandazione / Recommendation*.
2. **Never write "all good" without evidence.** Layout, spacing, clipping, image sharpness, heading hierarchy, font sizes and the mobile menu need a rendered page, screenshots or a DevTools / Lighthouse export.
3. **Text audit scope:** spelling, grammar, punctuation, clarity, tone, consistency, calls to action; presentation (heading hierarchy, sizes, line breaks, density, readability). Colours excluded.
4. **No design changes:** only checks, additions and copy corrections.
5. **Cross-source consistency** is a headline check (distance, hours, classification, phone, name, address, services); state the measurement method.
6. **Do not publish conflicting data;** put open items in the "to complete with the owner" table.
7. **Cite sources:** one reference per website, numbered in sequence, every entry cited, official documentation first.
8. **Growth page honesty:** no invented uplift or traffic figures; the calculator uses the client's own inputs and sourced commission ranges, and says it is a simulation.
9. **Pricing appendix (optional, shared):** say whether figures are asking prices or market averages, VAT status and source; package ranges must not overlap.
10. **Voice:** impersonal or plural, never first-person singular, in client-facing text.

## 5. Workflow for each audit

0. Ask the tooling question (no-extra-tools vs named free extensions; wait for explicit permission).
1. Tier 1 checks → 2. Tier 2 (if approved, mark tiers) → 3. external channels and consistency tables → 4. fill the template → 5. QA → 6. deploy and send URL → 7. offer the separate competitive/market analysis and ask the delivery format (HTML + ZIP, Excel/Sheets, deck) → 8. escalate to a script (Playwright/Puppeteer) for authenticated areas, headless automation or scheduled monitoring.

## 6. QA checklist before sending

- [ ] No `{{...}}` or `[...]` left in visible text (except deliberate internal fields).
- [ ] IT and EN blocks match; every finding has an evidence label and a source marker where possible.
- [ ] Sources: one per website, sequential numbers, every entry cited.
- [ ] **Hamburger menu works at 360–1100 px** (open, close on link/Esc/outside tap); desktop shows the inline menu on one row.
- [ ] **Footer client link opens in a new tab** with the correct absolute URL on the deployed host.
- [ ] Language persists across pages over http(s); no horizontal scroll at ~360 px.
- [ ] Growth page: package prices match the pricing appendix and calculator `data-min/max`; animations run once, and are static with reduced motion.
- [ ] Images load (PNG in `images/`, or inlined in the single file); alt text present.
- [ ] Pricing appendix kept/removed on purpose; footer note matches; `noindex` present unless the client asks otherwise.
- [ ] HTML file and ZIP bundle have identical page content and were both re-shared after the last change.

## 7. Footer note (default, one line)

"Da sapere: l'appendice prezzi (Roadmap) è condivisa con il cliente · le voci «non verificate» sono dichiarate come tali · report con noindex." Edit it if the pricing appendix is removed or the indexing decision changes.

## 8. Styling notes

- Theme tokens come from `style.css`; `extra.css` only adds rules (and defines `--radius-full`, `.source-link`).
- Fonts (Cormorant Garamond, Satoshi) load from the internet as in the original; offline they fall back to system fonts.
- Hamburger breakpoint is 1100 px because eight menu items do not fit the content width below it.
- Print: header and back-to-top hidden; animations forced to their final state.

## 9. Known limits

- A content structure, not an automatic auditor: findings must come from real checks.
- `fill_template.py` replaces only `{{UPPER_CASE}}` keys, does not renumber sources, and does not translate.
- The PNGs are hospitality illustrations; swap them for other sectors.
- Evidence about external platforms changes quickly; re-check before sending.

## 10. Version

- v1 — 17 Oct 2026 — derived from the Goldoni 6 audit.
- v2 — 21 Oct 2026 — one-line footer, shared pricing appendix, package ladder, one source per site, legend and next steps, lang.js fix.
- v3 — 21 Oct 2026 — hamburger menu hard rule, external-link rule, Growth page (animated diagrams, calculator, PNGs), footer address in config.
