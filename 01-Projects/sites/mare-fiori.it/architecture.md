# Marefiori — Site Architecture

**Project:** Marefiori (placeholder brand) — flower atelier, Porto Antico di Genova
**Type:** Marketing / portfolio case study landing page
**Stack:** Static HTML + CSS + vanilla JS (no build step, no framework)
**Deliverable owner:** Avibe Agency — Frontend Developer agent

## Design system — "Romantic Ligurian August"
| Token | Value |
|---|---|
| Paper / ink | `#FBF6F0` / `#3A2E2A` |
| Terracotta | `#C97B5A` (dark `#A85C3E`) |
| Sea | `#2F6B7A` (light `#7FB0BC`) |
| Coral / Pink | `#E58E78` / `#F0D3CE` |
| Gold | `#C7A36A` (soft `#E8D6B4`) |
| Display / Body | Cormorant Garamond / Jost (Google Fonts) |

All colors are CSS custom properties on `:root` and `[data-theme="dark"]`, so theming is a single attribute swap. Mobile-first: base styles target phones; `min-width: 560/900/1200px` enhance to multi-column.

## File structure
```
mare-fiori.it/
├── index.html          # full page (markup + inline <style> + <script>)
├── favicon.svg         # flower-on-waves mark (local)
├── robots.txt          # SEO crawler rules
├── sitemap.xml         # URL set for search engines
├── architecture.md     # this file
├── site-map.md         # section / URL tree
├── site-requirements.md# spec + acceptance criteria
├── plan.md             # prompting summary (reusable)
└── artefacts.md        # asset + endpoint inventory
```

## Functional modules (all in index.html `<script>`)
- **SITE_CONFIG** — single registry of external endpoints (Stripe, order/CRM/email webhooks, map). Replace placeholders before go-live.
- **CHATBOT_CONFIG** — avatar + endpoint/model placeholders; connect to any LLM later.
- **i18n** — `I18N` dictionary (en/it/ru); `applyLang()` swaps all `[data-i18n]` text + re-renders data-driven sections. Persisted in `localStorage`.
- **Render** — Collections, Gallery, Blog rendered from `COLLECTIONS` / `GALLERY` / `BLOG` data arrays (keeps copy in one place, i18n-friendly).
- **Theme** — `data-theme` on `<html>`, persisted.
- **Lightbox** — click/keyboard gallery viewer.
- **Chatbot widget** — bottom-right FAB + panel; quick replies; send → `CHATBOT_CONFIG.apiUrl` (falls back to WhatsApp CTA).
- **Reveal** — IntersectionObserver scroll animations; disabled under `prefers-reduced-motion`.

## Integration points (adoptable later)
| Capability | Where | Placeholder |
|---|---|---|
| Payments (Stripe) | `SITE_CONFIG.stripe` | `pk_live_XXXX` |
| Order submit | `#bookForm` → `SITE_CONFIG.orderEndpoint` | `/api/order` |
| CRM webhook | `SITE_CONFIG.crmWebhook` | `https://hooks.avibe.agency/...` |
| Email automation | `SITE_CONFIG.emailApi` | `https://api.avibe.agency/...` |
| Chat model | `CHATBOT_CONFIG.apiUrl` | `""` (fallback active) |
| Social links | footer `data-social` anchors | `href="#"` |

## SEO / indexability
- Semantic landmarks (`header/main/section/footer`), descriptive headings, `alt`/`aria`.
- Meta: description, keywords, canonical, Open Graph, Twitter card.
- JSON-LD `Florist` LocalBusiness (geo, hours, phone, address).
- `robots.txt` + `sitemap.xml` included.
- Ready for Google Business Profile association (fill NAP consistently).

## Validation
HTML well-formed (no unclosed/stray tags); inline JS passes `node --check`. Visual render not auto-verified in CI sandbox — open `index.html` in a browser to confirm.

## Links
- Parent: [[mare-fiori.it-INDEX]]
- Related: [[site-requirements]]
