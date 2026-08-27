# Marefiori — Site Requirements & Acceptance Criteria

> Restated in professional language from the client brief. All items below are implemented in `index.html` unless marked *Placeholder*.

## 1. Brand & context
- Placeholder brand: **Marefiori** — a flower atelier at **Porto Antico di Genova**.
- Mood: "Romantic Ligurian August" — warm late-summer coastal light, soft floral romance, honeymoon/emotional register.
- Phone: **+39 345 023 4084** (WhatsApp + header/footer). Email: ciao@mare-fiori.it.

## 2. Required sections
- [x] Hero (name + mood tagline + video/poster slot)
- [x] Brand story / Genova harbor connection (client photo slot: `assets/harbor.jpg`)
- [x] Collections/services — Bouquets, Event florals, Honeymoon & anniversary
- [x] Gallery (clickable lightbox) — incl. **new emotional-bouquet tile** after "On the water"
- [x] Location/contact — Porto Antico + map embed
- [x] CTA / order form

## 3. Visual & UX
- [x] Palette and typography per design system (terracotta, sea blues, corals/pinks, gold; Cormorant + Jost).
- [x] **Mobile-first** responsive layout; verified breakpoints 560 / 900 / 1200px.
- [x] **Light/Dark theme** toggle (persisted).
- [x] **Language toggle** EN / IT / RU with full correct translations of all visible copy.
- [x] Gallery opens a full-screen lightbox (click + keyboard, Esc/arrows).
- [x] WhatsApp icon in header and footer.
- [x] Social icons in footer with endpoints ready for real webhooks/profiles.
- [x] Reduced-motion support.

## 4. Imagery
- [x] Stock sourced from **Pexels** (free license), hotlinked CDN. For production, vendor into `assets/`.
- [x] Hero video: **Mixkit #25988** "Sunshine over the Mediterranean" → `assets/hero.mp4` (drop-in).
- [x] User-supplied (3): `harbor.jpg`, `yacht.jpg`, `happy-girl.jpg` — graceful gradient fallback until provided.

## 5. Chatbot
- [x] Bottom-right widget, happy smiling lady + bouquet avatar (Pexels 13975904).
- [x] Pre-built quick replies + free input; **configurable endpoint** (`CHATBOT_CONFIG`) to connect any AI model later; graceful WhatsApp fallback.

## 6. Content
- [x] Blog / Journal Q&A: Ligurian flowers, types of bouquets, event services, prices, flower care, home delivery (+ garden design).

## 7. SEO / indexability
- [x] Semantic HTML, meta description/keywords/canonical, Open Graph, Twitter card.
- [x] JSON-LD `Florist` LocalBusiness.
- [x] `robots.txt` + `sitemap.xml`.
- [x] Ready for Google Business Profile + future CRM/email automation, Stripe payments, order flow.

## 8. Integration rules (apply to all similar jobs)
1. Every external endpoint lives in one registry (`SITE_CONFIG` / `CHATBOT_CONFIG`) and is a clearly-marked placeholder until wired.
2. Social/footer links use `href="#"` + `data-*` markers so real URLs/webhooks drop in without markup changes.
3. Blog/collections/gallery are data-driven so copy & i18n stay in one place.
4. Mobile-first; respect `prefers-reduced-motion`.
5. No hard-coded secrets in client code (Stripe secret stays server-side).

## 9. Acceptance criteria
- HTML validates (no unclosed/stray tags); JS passes syntax check.
- All toggles (lang, theme, menu, lightbox, chatbot) function without console errors.
- Page renders correctly at 360px, 768px, 1280px widths.
- All visible copy translates correctly across EN/IT/RU.
- No broken-image icons for missing user photos (gradient fallback).

## Links
- Parent: [[mare-fiori.it-INDEX]]
- Related: [[site-map]]
