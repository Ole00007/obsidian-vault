# LEXFLOW — Quality Manifesto: Best Shot from AI for SaaS Ever

> **Status:** Candidate standard for the Factory.  
> **Owner override:** Explicitly permitted (see § Override Clause).  
> **Applies to:** LexFlow website (Astro + Cloudflare Pages) and all future Factory projects by reference.  
> **Governance:** This document is the *candidate* source of truth. It becomes binding for a project only when the project owner adopts it explicitly. Until then, it is a reference architecture.

---

## 0. Override Clause — Owner Authority

**The project owner (you) retains absolute deploy authority.**

If you explicitly say **“deploy”**, **“ship it”**, **“push to production”**, or any unambiguous deploy command — **Hermes must deploy.**

### Required behaviour on override:

1. **Warn** — List every unchecked □ from the Definition of Done (§ 8) that will not pass.
2. **Mark** — Create/update a task in the CRM via Operator-installer with:
   - Title: `[OVERRIDE] <check name> — deployed without passing`
   - Tags: `override`, `technical-debt`, `post-deploy-fix`
   - Priority: set by you at override time
   - Linked to: this deployment commit + Cloudflare deployment ID
3. **Plan** — Add a concrete fix plan (what, where, estimated effort) in the task description.
4. **Deploy** — Execute the deployment immediately after steps 1–3.

**No negotiation. No “are you sure?” loops. No blocking.**  
You own the deadline, the demo, the investor call, the customer presentation. Hermes owns the quality radar and the debt register. Both jobs get done.

> **Note to Hermes:** You do not need to understand *why* the owner overrides. You only need to execute the four steps above faithfully. The explanation lives here in the manifesto — not in your prompt.

---

## 1. Core Thesis

LexFlow is not “a company website.” It is **the first public artefact of our SaaS & Web Marketing Factory.**

Every engineer, designer, marketer, AI agent who later builds under this flag (CRM, EdTech, Marketplace, LegalTech, any next product) will open this repo and say:

> “This is how it’s done. This is what production-grade looks like when AI doesn’t just write code — it makes architectural decisions.”

The site must be:

| Principle | What it means |
|---|---|
| **Self-documenting architecture** | Code structure *is* the documentation |
| **Impossible states unrepresentable** | TypeScript + Zod + build-time guards make invalid states uncompilable |
| **Conversion-engineered** | Every pixel justified by data or an explicit, testable hypothesis |
| **Accessibility as competitive moat** | Not compliance — UX advantage |
| **Performance-budgeted** | 0.8 s LCP on 3G, 0 JS blocking, AVIF/WebP, CSS < 15 KB gzipped |
| **Culturally native** | EN/IT/RU = three independent copy voices for three ICPs, not translations |
| **Agent-readable first** | `llms.txt`, JSON-LD, semantic HTML — LLMs “understand” this site better than humans |
| **Evolvable by design** | Next feature (blog, changelog, careers, partner portal, docs) adds without architectural refactor |

---

## 2. Non-Negotiable Architectural Decisions (Fixed Once)

### 2.1 Single Source of Truth — Always
- One `site.config.ts` generates: env vars, sitemap, robots, `llms.txt`, OpenAPI, `ai-plugin.json`, JSON-LD, navigation, CTA map.
- **No hardcodes. Ever.** `ORIGIN` = required env var; build **fails** without it.

### 2.2 Type-Safe Content Layer
- All copy, legal, pricing, FAQ → `.content.ts` files with Zod schemas (not HTML/MDX).
- Types = contract between copywriter, designer, developer, AI agent.
- Change price in one place → pricing page, JSON-LD Product, sitemap, `llms.txt`, email template, CRM webhook payload all rebuild.

### 2.3 Zero Runtime Dependencies for Critical Path
- Hero, nav, CTA, pricing, FAQ, contact = pure HTML + CSS.
- JS only for progressive enhancement (theme, lang, form enhance, analytics).
- **No client framework. No hydration. No layout shift.**

### 2.4 Design Tokens as Source
- One `tokens.json` → CSS custom properties, Tailwind config (if used), Figma variables, React Native tokens, email MJML variables.
- Tokens versioned. Design system = code, not a Figma file.

### 2.5 Multilingual = Multi-Cultural
- Three independent content files: `content.en.ts`, `content.it.ts`, `content.ru.ts`.
- Shared Zod schema, different values.
- **No EN fallback.** Missing key in IT → build fails.
- RTL-ready architecture (for future languages).

### 2.6 Accessibility = Type System
- `aria-*` attributes generated from the same schemas as content.
- Focus management, skip links, landmarks in base layout.
- Auto-tests: axe-core in CI, keyboard-only navigation test suite.

### 2.7 Agent-Readable First
- `llms.txt` = first artefact of content strategy, not afterthought.
- JSON-LD on every page: Organization, WebSite, Product, FAQPage, BreadcrumbList, LocalBusiness (IT).
- Semantic HTML5: `<header>`, `<main>`, `<article>`, `<section>`, `<nav>`, `<aside>`, `<footer>` — no div soup.

### 2.8 Deployment = GitOps, Not Scripts
- Cloudflare Pages + Git integration (`main` = prod, `feat/*` = preview).
- Preview = full staging with unique URL.
- Env vars in Cloudflare dashboard, **never in code**.
- Rollback = `git revert` + push. No manual deploys.

### 2.9 Observability Built-In
- Web Vitals → Cloudflare Analytics / custom endpoint.
- Error boundary → Sentry (or self-hosted).
- Feature flags → LaunchDarkly / Unleash / custom.
- A/B test infra built-in, not third-party script.

---

## 3. Content & Conversion Strategy

### ICP
Italian lawyers, 5–20 people, no IT dept. Pain: admin overload, lost clients, document chaos.

### Positioning
> **“Not enterprise. Not a builder. A tool that understands your workflow out of the box.”**

### Hero (three independent voices)
| Locale | Copy |
|---|---|
| EN | “Case intake that doesn’t fall through the cracks.” |
| IT | “L'intake che non perde nessun cliente per strada.” |
| RU | “Входной воронкой, где ни один клиент не теряется.” |

### Trust Bar (above fold, static)
- “Used by Studio Legale X — 12 active matters, 0 lost intakes last month”
- “GDPR + ISO 27001 + ISO 27701 — not checkboxes, architecture”
- “Setup in 8 minutes. Team onboarding — 0 minutes.”

### Pricing = Decision Helper, Not Table
- One plan. Everything included. Price = single token.
- FAQ: “Why not per seat?” → honest answer about incentive alignment.

### Social Proof = Specific Outcomes
- “Avv. Parodi: save 1 hr/day on ‘how’s my case?’ calls”
- “L. Marchetti (office manager): ‘Set it up once, everyone uses it.’”

### CTA Map (single, typed, centralized)
| Key | Label | Destination | Auth | Notes |
|---|---|---|---|---|
| `primary` | Start Free Trial | `/signup` | Public | |
| `secondary` | Request Demo | `/demo` | Public | Calendly embed, tracked |
| `client` | Client Portal | `/portal` | Token | No password |
| `staff` | Staff Login | `/auth/staff` | Magic link | |
| `admin` | — | **Absent from public nav** | Internal | Direct link only for superadmin |

---

## 4. Technical Stack (Minimal, Justified, Immutable)

| Layer | Choice | Rationale |
|---|---|---|
| Build | **Astro** | Islands, partial hydration, content collections, type-safe |
| Styling | **CSS Custom Properties + Grid/Flex** | No framework debt, zero runtime |
| Types | **TypeScript strict + Zod** | All content/config validated at build |
| Images | **Astro Assets** | AVIF/WebP + widths + blurhash placeholders |
| i18n | **Astro i18n routing** (`/en/`, `/it/`, `/ru/`) | Native, type-safe, SEO-correct |
| Forms | **Progressive enhancement** | HTML form + fetch enhance + honeypot + rate limit |
| Analytics | **Cloudflare Web Analytics** | Privacy-first, no cookie banner |
| Deployment | **Cloudflare Pages Git integration** | `main` = prod, `feat/*` = preview |
| CI | **GitHub Actions** | Typecheck + lint + test + build + a11y + visual regression |

---

## 5. Definition of Done — All-or-Nothing

The site is **“deployed” ONLY when ALL □ pass in CI:**

□ TypeScript strict: 0 errors  
□ Zod validation: all content files valid  
□ Build: success, dist < 500 KB gzipped (HTML+CSS+JS), images optimized  
□ LCP < 800 ms on emulated 3G (Lighthouse CI)  
□ CLS = 0, TBT < 50 ms  
□ axe-core: 0 violations WCAG 2.2 AA  
□ Keyboard navigation: all interactive elements reachable & operable  
□ Screen reader: NVDA/VoiceOver smoke test passed  
□ All 3 locales: pages render, links work, hreflang correct  
□ Canonical/hreflang/sitemap/robots/`llms.txt`/JSON-LD: valid, 0 placeholder domains  
□ Visual regression: 0 unexpected diffs vs approved baseline  
□ Forms: submit works, honeypot blocks bots, rate limit triggers  
□ CRM backlink: points to new hero, 0 legacy Netlify refs  
□ CTA map: all 5 destinations work, `/admin` absent from public nav  
□ Accessibility statement: page exists, honest, contact for complaints

**If ANY □ fails → deploy does not happen.**  
No exceptions. No “fix later.” No “it’s minor.”

---

## 6. Override Procedure (Operational Summary for Hermes)

> **Trigger:** Owner says “deploy” / “ship it” / “push to production” (any unambiguous command).

**Hermes MUST:**

1. **WARN** — Output a concise list of every unchecked □ from § 5 that will not pass.
2. **MARK** — Via Operator-installer, create/update CRM task:
   - Title: `[OVERRIDE] <check name> — deployed without passing`
   - Tags: `override`, `technical-debt`, `post-deploy-fix`
   - Priority: per owner instruction
   - Links: deployment commit SHA + Cloudflare deployment ID
3. **PLAN** — Add fix plan (what, where, effort estimate) to task description.
4. **DEPLOY** — Execute deployment immediately.

**No confirmation prompts. No “are you sure?”. No delay.**

---

## 7. What This Unlocks for the Factory

This repo becomes the **starter kit** for the entire roster:

| Next product | What changes |
|---|---|
| CRM marketing site | Fork → swap `content.ts`, `tokens.json` → deploy |
| EdTech landing | Same + different ICP, different trust bar |
| Marketplace | Extend schema, add listing pages |
| Docs site | Same design system, different content type |
| Email templates | MJML tokens from same `tokens.json` |
| Investor deck | Same narrative, same proof points |

**Do it right once → reuse everywhere. No “every project its own way.”**

---

## 8. Execution Order (Today)

| Step | Work | Est. |
|---|---|---|
| 1 | Scaffold Astro project with this structure | 30 min |
| 2 | Migrate content to typed collections | 2 h |
| 3 | Configure `tokens.json` + CSS custom properties | 1 h |
| 4 | Implement layout + hero + trust bar + pricing + FAQ + footer | 3 h |
| 5 | Configure i18n routing + 3 content files | 2 h |
| 6 | Configure CI pipeline with all □ gates | 1 h |
| 7 | Configure Cloudflare Pages Git integration | 30 min |
| 8 | Deploy preview → full validation → merge → prod | 1 h |
| **Total** | **~11 h focused** | **1 day** |

**No “fix old first, then think.”**  
**Yes: “build right from zero, migrate content, archive old repo.”**

---

## 9. Governance & Versioning

| Field | Value |
|---|---|
| Document version | 1.0-candidate |
| Author | Factory Owner (you) |
| Steward | Hermes (Frontend Developer profile) |
| Review cadence | Per-project adoption; factory-wide review quarterly |
| Override clause | **Permanent — cannot be removed by agent** |
| Parallel source of truth | **Forbidden** |
| Cron jobs / scheduled tasks | **Forbidden** |
| Permanent rules created by agent | **Forbidden** |
| Tomorrow reminder | Update ecosystem index manually |

---

> **End of Manifesto.**  
> When you say **deploy**, we deploy. The debt gets tracked. The standard stays real.