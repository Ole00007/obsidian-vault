# Template SITE-AUDIT 1_ENNEFEX — oct 2026

Reusable bilingual (IT/EN) website-audit report, built in the style and structure of the *1_ENNEFEX* example (dark & gold theme, sticky header with menu, hero + score card, evidence-labelled findings, comparison tables, priorities list, language toggle, back-to-top button).
First production use: **Goldoni 6 audit (17 Oct 2026)**. Scope of every audit: **technical + text layer only** (market/competitive business analysis is a separate skill and is offered, not assumed).

---

## 1. Package contents

| Path | Purpose |
|---|---|
| `index.html` | Summary: hero, score card, critical callouts, evidence legend, verified / not verified, coverage, critical points, public findings, strengths |
| `tecnico.html` | Site audit: technical settings, technical layout, text quality, text presentation, Google Search Console and Business Profile, internal / external links |
| `canali.html` | External channels (OTAs, directories, maps, listings): same fact compared across sources, not-found list, fix |
| `faq.html` | FAQ block: why enlarge, ready-to-publish answers (accordion), answers to complete with the owner |
| `competitors.html` | Comparable operators: table + takeaways |
| `seo.html` | SEO / AEO / GEO: layers, recommended actions, structured-data starter, local approach and phases, multilingual test questions, chatbot knowledge rules |
| `roadmap.html` | Priorities, data needed from the client, tools used, optional internal pricing appendix, sources |
| `css/base.css`, `css/style.css` | Original theme files (unchanged) |
| `css/extra.css` | Additions only: lists, callouts, snippet chip, source markers, FAQ accordion, code blocks, footer notes, mobile header, print |
| `assets/lang.js`, `assets/nav.js` | Original language toggle (`?lang=` is preserved across pages) and back-to-top button (unchanged) |
| `config.json` | Values for the `{{PLACEHOLDERS}}` |
| `fill_template.py` | Fills placeholders → `dist/`; `--single` also builds one self-contained file |

## 2. Quick start

1. Edit `config.json` (client name, domain, URL, location, dates IT/EN, agency, agency place IT/EN).
2. Replace every text in `[square brackets]` in the HTML pages with the real finding (IT + EN). Remove rows or cards you do not need; never invent data.
3. Run `python3 fill_template.py --single`.
4. Check `dist/` (multi-page, for Netlify / Cloudflare Pages) and `dist/audit-single.html` (one file; menu and language toggle work inside previews).
5. Deploy `dist/` or send the single file. Both carry `noindex, nofollow`.

## 3. Placeholders (`config.json`)

| Key | Example |
|---|---|
| `CLIENT_NAME` | Residence Hotel Goldoni 6 |
| `DOMAIN` | goldoni6.it |
| `CLIENT_URL` | https://goldoni6.it/ |
| `LOCATION` | Rimini, Italia |
| `AUDIT_DATE_IT` / `AUDIT_DATE_EN` | 17 ottobre 2026 / October 17, 2026 |
| `AGENCY` | Avibe Agency |
| `AGENCY_PLACE_IT` / `AGENCY_PLACE_EN` | Genova, Italia / Genoa, Italy |

Structured-data placeholders use `[[double square brackets]]` so the script never touches them.

## 4. Writing rules (carry over to every audit)

1. **Evidence labels are mandatory** on every finding: *Verificato / Verified* (seen directly), *Da anteprima di ricerca / Snippet-level* (search results or third-party snippets), *Non verificato / Not verified* (access, screenshots or exports needed), *Raccomandazione / Recommendation* (auditor proposal).
2. **Never write "all good" without evidence.** Layout, spacing, clipping, image sharpness, heading hierarchy and font sizes need a rendered page, screenshots or a DevTools / Lighthouse export. Say what is needed.
3. **Text audit scope:** spelling, grammar, punctuation, clarity, tone, consistency, calls to action; presentation (heading hierarchy, sizes, line breaks, density, readability). Colours are excluded.
4. **No design changes:** only checks, additions and copy corrections.
5. **Cross-source consistency** is a headline check: the same fact (distance, hours, classification, phone, name, address, services) must be compared on the client site and every external channel; state the measurement method (on foot / by car / straight-line).
6. **Do not publish conflicting data.** Put open items in the "to complete with the owner" table and mark them internal.
7. **Cite sources** (`[n]` markers link to the Sources list). Official documentation first; mark unofficial sources as such.
8. **Bilingual by default:** every block exists in IT and EN (`<span lang="it">` / `<span lang="en">`); IT is the default language. Quoted client copy stays in its original language and spelling.
9. **Honest limits:** if a page could not be fetched, say so; a failed retrieval does not prove the site is inaccessible.
10. **Pricing appendix** (optional, internal): label asking prices vs market averages, VAT status and source; do not extrapolate where no source exists.

## 5. Workflow for each audit

0. Ask the tooling question: *no-extra-tools* (console + network + public sources) or *with free extensions*; name every extension and wait for explicit permission.
1. Run Tier 1 checks (server/CDN, frontend hints, third-party scripts, API calls, cookies/storage, performance waterfall, robots/sitemap, meta tags).
2. If approved, run Tier 2 (e.g. Wappalyzer, BuiltWith, Lighthouse, cookie tools, `curl -I`) and mark the tier of each finding.
3. Collect external channels (OTAs, directories, maps) and build the consistency tables.
4. Fill the template; keep unverified items visibly labelled.
5. QA (below), deploy, send the URL.
6. Offer the separate competitive / market analysis; ask the delivery format (HTML report, Excel / Google Sheets, deck).
7. Escalate to a script (Playwright / Puppeteer) for authenticated areas, headless automation or scheduled monitoring.

## 6. QA checklist before sending

- [ ] No `{{...}}` or `[...]` placeholder left in visible text (except deliberate internal fields).
- [ ] IT and EN blocks match (sections, numbers, labels, priorities).
- [ ] Every finding has an evidence label and, where possible, a source marker.
- [ ] Menu works on all pages; language toggle works; `?lang=` preserved in the multi-page version.
- [ ] No horizontal scroll at ~360 px; tables scroll inside their wrapper.
- [ ] Internal pricing appendix kept or removed on purpose; footer notes match the decision.
- [ ] `noindex` present unless the client asks otherwise.

## 7. Footer notes (default text)

The footer carries three short notes: internal pricing appendix (quoting), unverified content (items that remain "not verified"; FAQ templates to complete are Italian only), and indexing (`noindex`). Edit them in `index.html` … `roadmap.html` footers or in `FOOT_NOTES` of the generator if you rebuild.

## 8. Styling notes

- Theme tokens come from `style.css` (`--color-gold`, `--space-*`, `--text-*`, …); `extra.css` only adds rules and defines the missing `--radius-full` token and `.source-link` class.
- Fonts (Cormorant Garamond, Satoshi) load from the internet as in the original; offline they fall back to system fonts.
- Mobile: the header is static below 720 px because seven menu items would otherwise occupy ~200 px of the viewport.
- Print: header and back-to-top hidden; every page of the single-file version prints.

## 9. Known limits

- The template is a content structure, not an automatic auditor: findings must come from real checks.
- `fill_template.py` replaces only `{{UPPER_CASE}}` keys; bracketed hints are manual.
- Evidence about external platforms changes quickly; re-check before sending.
- Chatbot costs, model plans and regional price benchmarks are quoted only where a source exists.

## 10. Version

- v1 — 17 Oct 2026 — derived from the Goldoni 6 audit; structure and style follow the 1_ENNEFEX example.
