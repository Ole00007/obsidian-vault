# Hospitality Agentic — Site Build (2026-10-14)

## Deliverable
Production-ready, mobile-first, trilingual (RU default / IT / EN) one-page site for the **Hospitality Identity & Agentic Service Network** (Liguria project). Built per Ole's prompt (authoritative over the pack's older design brief).

**Working path:** `/Users/olesiarasing/projects/HOSPITALITY/site/`
**Local preview:** `http://127.0.0.1:8793/index.html` (opened for Ole; NOT deployed — Netlify-ready, deploy pending Ole's go).

## Files
- `index.html` — one-page landing: header (logo, nav, RU/IT/EN switcher, CTA), hero (device mockup using `assets/hero-liguria.jpg`), problem (5), architecture (5-layer HTML/CSS/SVG diagram), modules (6 + detail modals), guest journey (5-stage timeline, agent vs human), hardware catalog (9 products + compliance badges), vape (risk-controlled, age-gate, disclaimer), Liguria launch (4 provinces + 90-day pilot + gates), financial preview (9 categories, no invented numbers), risks & compliance, 4 forms, footer, cookie banner, 3 JSON-LD schema blocks.
- `styles.css` — premium calm design system, exact palette (ink #0B1623, ivory #F6F2EA, olive #66704A, gold #B08D57, slate #52606D, white, red #9E3B32), serif headings, dark default + light theme, WCAG AA, reduced-motion.
- `app.js` — i18n engine (content.json, dotted paths, localStorage), lang switcher, UTM capture, 4-form validation + mailto fallback (no auto-send; `formEndpoint` empty by default), modals, reveal-on-scroll, cookie consent, vape age-gate, legal/thank-you render.
- `content.json` — 180 keys × 3 langs, full parity, all visible text centralized.
- `config.js` — contacts (+39 345 023 4084 / wa.me / alegra_007@proton.me), `formEndpoint: ""`, images.
- `legal/{privacy,cookies,disclaimer}.html`, `thank-you.html`, `_redirects`, `README.md`, `assets/hero-liguria.jpg`.

## Build process
3 parallel subagents against a shared `BUILD_CONTRACT.md` (content/i18n, structure/design, behavior/legal). I reconciled Agent A/B key drift (added 60 keys to content.json, fixed `optN`→`options.N` in index.html), wired the vape age-gate, and fixed a mobile horizontal-overflow bug (`min-width:0` on `.hardware-card`).

## Cross-check (passed)
0 missing i18n keys · 4 Netlify-ready forms (honeypot, UTM, GDPR consent, mailto fallback) · vape disclaimer + age-gate present · tel/wa/mailto correct · 3 JSON-LD schema blocks · 0 invented financial numbers · all nav anchors · RU→IT switcher verified · no console errors · mobile 390px no overflow.

## Notes / TODOs (also in README)
- `formEndpoint` empty → mailto fallback; wire a Netlify Form → webhook → n8n → CRM/email/Telegram when ready.
- Legal/compliance TODOs: CE/RED/EMC/RoHS cert, CRA, Alloggiati Web, GDPR/DPA, vape licensing via licensed partner only (no public promotion), native RU/IT copy review.
- Deploy: Netlify drag-drop of `site/` or git; Forms auto-detect via `data-netlify`.

## Links
- Parent: [[Hospitality-INDEX]]
- Related: [[2026-10-14]]
- Related: [[LexFlow-Web-Site-Mobile-Audit-2026-10-14]]
