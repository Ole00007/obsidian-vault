---
name: award-winning-ux-ui-designer
description: Master skill for creating Awwwards-caliber designs for SaaS, B2B/B2C web apps, iOS, and Android products. Combines UX research, native platform guidelines, accessible design systems, AI-augmented workflows, and safe file-delivery protocol for index.html and other web deliverables.
license: MIT
metadata:
  target_audience: Product Designers, UX/UI Designers, Web & Mobile Developers
  design_year: 2026
  file_integrity: mandatory-audit-before-share
---

# Award-Winning Product & UX/UI Design Master

## When to use this skill
Use when the user requests designing, auditing, or conceptualizing digital products — B2B/B2C SaaS, multi-tenant web apps, or native iOS/Android apps. Covers dashboards, cross-platform design systems, accessibility, and any task that produces a shareable HTML/web deliverable.

---

## Core competencies (5 pillars)
1. **UX research & SaaS logic** — retention, cognitive load, onboarding, JTBD framing.
2. **Platform-specific UI** — Apple HIG (iOS), Material Design 3 (Android), Awwwards-level web (glassmorphism, micro-interactions, dark mode, kinetic type).
3. **Scalable component architecture** — atomic design, Figma variables/auto-layout, multi-theme systems.
4. **Accessibility (a11y)** — WCAG 2.2, keyboard nav, screen-reader semantics, contrast compliance.
5. **AI-augmented workflows** — prompt templates for research synthesis, asset generation, rapid prototyping.

---

## Design workflow

1. **Deconstruct the brief** — product type, persona, JTBD, business goal, critical user flow, friction points.
2. **Define visual direction** — aesthetic descriptor, light/dark palette (hex codes), platform-native patterns (iOS tab bar blur vs. Android Material You), web layout structure and micro-animations.
3. **Architect the design system** — atoms/molecules/organisms, grid (8pt default), responsive breakpoints, design tokens.
4. **Accessibility audit** — concrete guidance per component (focus states, touch targets, ARIA, Dynamic Type support).
5. **AI workflow advice** — 1-2 ready-to-use prompt templates for this specific product.

### Example output shape
For a brief like "B2B SaaS financial dashboard + companion iOS app," structure the answer as: UX Strategy → Visual Direction → Component Architecture → Accessibility → AI Prompt. Keep each section concrete: real hex codes, real component names, real ARIA attributes — never placeholders like "TBD" or "appropriate colors."

---

## File delivery protocol — index.html and other web files

This protocol is mandatory any time a file (index.html, style.css, app.js, etc.) is generated or edited for the user.

### 1. Always deliver clean, unlocked files
- Plain UTF-8 HTML. No encryption, no obfuscation, no minification that hides logic, no password lock.
- Sharable, downloadable, and re-editable by the user or any connected agent (Hermes, Claude Code, Computer).

### 2. Run a file-lock audit before every share
Report this table with the delivered file:

| Check | Result |
|---|---|
| Encryption / password protection | None found |
| Obfuscation (eval, atob, minified blobs) | Zero occurrences |
| Encoding | Valid plain UTF-8 |
| Structure | Standard `<!doctype html>`, fully readable |
| "password"/"lock" text matches | Confirmed as copy/CSS only, not technical locks (list each match) |

State explicitly: **"File-lock audit — confirmed clean"** before delivering.

### 3. Surgical edit rules
When the user asks for a change or a "surgical" edit:
- Touch only what was explicitly requested.
- Never modify image blobs, copy text, i18n `data-t` attributes, or layout structure beyond the exact ask.
- Mark every edited region with a search-friendly comment marker, e.g. `<!-- EDIT:2026-07-26-hero-cta -->` ... `<!-- /EDIT -->`.
- Keep a short change log entry for every edit: what changed, why, and the marker used.

### 4. Asset handling
- Prefer external `assets/` paths for new images (easier for Hermes/git/Netlify integration).
- If an asset is absent, generate one rather than leaving a placeholder.
- Exception: legacy inline visuals the user has explicitly locked as-is (e.g., a chat/launcher avatar embedded inline on a landing page) stay inline until the user says otherwise.

### 5. Documentation on every delivery
Include:
- A short **CHANGELOG** — as HTML comments at the top of the file and/or a companion file (e.g., `PROJECT_V[n]_CHANGES.md`).
- A **change table** listing: date, section/marker, what changed, reason. Keep it traceable and reusable across sessions.

```markdown
| Date | Marker | Change | Reason |
|---|---|---|---|
| 2026-07-26 | hero-cta | Updated button copy | User request: sharper CTA |
```

### 6. Deliverable checklist (run before sharing any file)
- [ ] File is plain UTF-8, no lock, no obfuscation.
- [ ] Audit table generated and shown to user.
- [ ] Edits marked with search comments.
- [ ] Change log / changes file updated.
- [ ] Only requested regions touched — copy, i18n, images, layout untouched unless asked.
- [ ] New images use `assets/` path unless legacy-inline exception applies.
- [ ] File shared via `share_files` as a downloadable artifact.

---

## End-of-session habit
At the end of a working session, suggest the user:
1. Summarize the session (what changed, what's pending).
2. Iterate this skill with any new blueprints, debugging notes, or efficiency lessons learned.

---

## Accessibility quick-reference

| Context | Requirement |
|---|---|
| Data tables (web) | `<th scope>`, `aria-sort`, full keyboard tab-targeting |
| Buttons/inputs (mobile) | Minimum 44x44px touch targets |
| Dynamic type (iOS) | Support Apple Dynamic Type without breaking chart layouts |
| Color contrast | WCAG 2.2 AA minimum — 4.5:1 body, 3:1 large text |
| Focus states | Visible on every interactive element, including custom components |

---

## AI prompt templates (reusable)

**Research synthesis:**
"Act as a Senior UX Researcher. Analyze this transcript of a [persona] interview and extract the top 3 friction points regarding [task]. Format as actionable UI features."

**Rapid prototyping:**
"Generate 3 UI state variations (empty, loading, error) for a [component name] in a [product type], following [design system name] tokens. Return as annotated HTML/CSS."

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[industry-competitive-analyst-skill (2)]]
