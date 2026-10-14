# LexFlow Web-Site — Mobile-Friendliness Audit (2026-10-14)

## Context
Ole opened `https://lexflow-site.pages.dev/lexflow-index` on his phone and reported the menu is missing — expected a hamburger/sandwich dropdown. Task: audit mobile-friendliness before making any changes.

Working copy: `~/Desktop/projects/Products & Services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site` (branch `feat/heading-align-cta-merge`, HEAD `4e526a0`). Live build hash-verified identical to local (`lexflow-index.html` `5ab27835…`, `assets/style.css` `8da550d5…`), so the audit reflects the deployable state.

## Findings (severity → evidence)

### CRITICAL — no mobile navigation at all
- `assets/style.css:351-352` → `@media(max-width:860px){ .nav-links{display:none} }` hides the 6 main links (About CRM, How It Works, Features & Pricing, Practice Areas, FAQ, Blog) on any screen ≤860px.
- **No hamburger/burger/sandwich element exists** in the HTML (0 matches across all pages), and **no menu-toggle logic** in any of the 6 JS assets (`site-config.js`, `i18n-ui.js`, `i18n.js`, `webmcp.js`, `elisa-widget.js`, `forms.js`).
- Footer links only Privacy / Terms / Cookie Policy (+ `#` socials) — it does not provide the main nav.
- Net effect: on a phone the site's primary pages are unreachable except by editing the URL.

### HIGH — hero stays 2-column on mobile
- The hero `.wrap` has an inline `style="display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:center"`. Inline styles beat the stylesheet and no `!important` override exists, so the grid never collapses.
- At 390px the columns shrink to ~161px / ~133px → headline (h1 30px) and CTAs wrap into many lines; the Romanelli image is squished.
- Present in 5 EN pages + it/ru copies: `lexflow-index.html`, `lexflow-how-it-works.html`, `lexflow-practice-areas.html`, `lexflow-pricing.html` (the 5th is the legacy `lexflow-index (1).html` scratch artefact).

### MEDIUM — "Sign in" hidden on small phones
- `assets/style.css:364` → `@media(max-width:480px){ .nav-cta .btn-ghost{display:none} }` removes the primary auth action ≤480px.

### LOW — pricing compare table overflow risk
- `compare-table` font drops to 12px at ≤860 but tables don't wrap → potential horizontal overflow on narrow phones (pricing page).

## Fix — IMPLEMENTED + DEPLOYED (2026-10-14, on Ole's direct go)
1. **Mobile nav:** hamburger button added to every page's `<nav>`; `assets/style.css` turns `.nav-links` + `.nav-cta` into an expandable panel under the bar when `nav.menu-open` (≤860px). Toggle in `assets/i18n-ui.js` (aria-expanded, outside-click, Escape, close-on-resize-to-desktop). `ctrl_menu` labels added EN/IT/RU.
2. **Hero:** `@media(max-width:860px){ .page-hero .wrap{display:block !important; grid-template-columns:1fr !important; gap:24px !important} }` stacks the inline-grid hero on phones.
3. **Sign in:** the ≤480px hide was removed; Sign in now lives inside the mobile menu.
4. Regenerated `it/`+`ru/` (build-lang-sites.py) and `dist/` (build-dist.py). Committed `8eb5448` on `feat/heading-align-cta-merge`.
5. **Deployed** `wrangler pages deploy dist/ --project-name lexflow-site --branch main` → deployment `99c55ccd`, production `https://lexflow-site.pages.dev`. Live-verified (hamburger + CSS + toggle served; root `/` 301 → `/lexflow-index`). Ran on Ole's direct instruction — flagged to operator-installer.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-SEO-AEO-GEO-Origin-Plan-2026-09-16]]
- Related: [[LexFlow-Web-Site-CRM-Repoint-2026-09-17]]
- Related: [[2026-10-14]]
