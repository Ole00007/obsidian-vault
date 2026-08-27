# Marefiori — Prompting Summary / Reusable Plan

This document captures the approach so it can be replayed for similar Avibe "Our Works" landing-page jobs.

## Context block (who they are, what they can decide autonomously)
- **Avibe Agency** — builds portfolio case-study landing pages from creative briefs.
- **Frontend Developer agent** interprets the mood brief itself (no creative-direction questions); asks only on hard technical blockers (missing brand assets, stack unknown).
- Autonomous decisions: palette, typography, layout, copy register, stock sourcing, animation style.

## Task block (business context · mood · deliverable · deadline · format)
- Business: flower atelier, Porto Antico di Genova.
- Mood: "Romantic Ligurian August" (warm terracotta / sea blue / coral / gold; airy serif).
- Deliverable: one responsive landing page, production-ready.
- Default format: **self-contained static HTML/CSS/JS** (portable, embeddable) — switch to React component only if the client site is React/Next.
- Deadline-driven; ship a working artifact, not a description.

## Build sequence (proven)
1. Load design skills (`claude-design`, `popular-web-designs`); set up todo plan.
2. Pick stack: static HTML (portable) unless told otherwise.
3. Verify stock asset URLs with `curl -I` (HEAD) before wiring; never invent links.
4. Build sections: Hero → Story → Collections → Gallery → Visit/map → CTA → Footer.
5. Progressive enhancements: clickable gallery lightbox, language i18n, theme toggle, chatbot, SEO (meta/JSON-LD/sitemap/robots).
6. Centralize endpoints in one `SITE_CONFIG` object; mark all placeholders.
7. Validate: HTML structure parser + `node --check` on inline JS. Note that visual render is not auto-verified in sandbox.
8. Produce planning artefacts (architecture, site-map, requirements, plan, artefacts) in the project folder for reuse.

## Reusable rules (carry to next job)
- Endpoints clear & adoptable later (single registry + `data-*` markers).
- Social icons present with ready-to-insert webhooks.
- Blog/Q&A section for SEO + depth.
- Site indexable (meta, OG, JSON-LD, sitemap, robots).
- Mobile-first; `prefers-reduced-motion` respected.
- Stock from free libraries: **Pexels** (photos), **Mixkit** (video), **OpenStreetMap** (map, no key).
- Client supplies ≤3 hero/brand photos; agent sources couple + flower imagery.
- Keep brand/contact as clear placeholders to swap later.

## Open questions for client
- Real brand name, final copy, exact address/hours.
- Confirm React vs static for their site stack.
- Stripe account + backend for payments; CRM/email provider for automation.

## Links
- Parent: [[mare-fiori.it-INDEX]]
- Related: [[architecture]]
