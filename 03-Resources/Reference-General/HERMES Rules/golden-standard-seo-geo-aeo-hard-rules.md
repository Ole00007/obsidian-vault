# Golden Standard — SEO / GEO / AEO Hard Rules for Hermes

**Scope:** This is a permanent reference, not a one-off task list. It applies to every future deliverable — full websites, landing pages, and web applications alike. Before shipping any HTML/web deliverable, check it against this document. If a rule is violated, fix it before requesting deploy approval, not after.

---

## Rule 1 — Domain and Canonical Integrity (BLOCKER-LEVEL)

- **Never build against a placeholder domain.** No `example.com`, `.example`, or any fake origin may appear in `<link rel="canonical">`, `hreflang`, `sitemap.xml`, `robots.txt`, `llms.txt`, or any manifest file at any point past prototype stage. If the real domain isn't registered yet, say so explicitly instead of silently shipping a placeholder.
- **Every indexable page gets exactly one self-referencing canonical**, using the absolute real URL[cite:109][cite:111][cite:116][cite:118]. A homepage must canonicalize to `/`, never to `/index.html` or `/lexflow-index.html`, unless that literal path is what the server actually serves as root — confirm which before writing the tag.
- Treat any domain/canonical mismatch as **Priority 0**, ahead of every other fix. An agent or crawler that cannot resolve your canonical cannot cite, verify, or rank you — everything else is secondary until this is true.

## Rule 2 — Heading Hierarchy (H1 → H2 → H3, No Skips)

- Exactly **one H1 per page.** No duplicates, no missing H1.
- **No level-skipping.** If a section under H1 has sub-points, it goes H1 → H2 → H3, never H1 → H3.
- **Consistent semantic level across the whole project.** If "Related reading" or "Scope note" is H2 on one page, it is H2 on every page of the same type — an agent or classifier relies on level meaning being stable site-wide, not just page-by-page.
- Clean heading hierarchy is not cosmetic — it is how both Google's section extraction and LLM content chunkers determine what a passage is "about"[cite:120][cite:131].
- Widget-injected or JS-populated headings (cookie banners, chat widget names) must not pollute the document outline. If a heading tag is used for a non-content UI element, either give it `aria-hidden="true"` or use a non-heading element instead.

## Rule 3 — Answer-First Content Structure (AEO)

- Every major H2 section should be able to **stand alone as an answer** — lead with a direct 1–2 sentence answer, then elaborate[cite:120][cite:131].
- Keep paragraphs to 2–4 sentences maximum in content sections; longer blocks get broken into scannable bullets or numbered steps[cite:131].
- Every site/app must ship a real **FAQ section with `FAQPage` JSON-LD schema**, using natural client-language questions (not keyword-stuffed) — 6-10 real questions per major page or service is the target density[cite:124].
- Use question-phrased H2/H3 headings where the content is answering a question — this matches how users phrase prompts to AI engines[cite:131].

## Rule 4 — Structured Data (Schema.org / JSON-LD)

- Use **one primary schema type per page** (`Organization`, `FAQPage`, `Service`, `Product`, etc.) as JSON-LD, not microdata[cite:130].
- Structured data **must match visible content exactly** — never describe something in schema that the page doesn't actually show or offer. This is the machine-readable version of "no over-claiming."
- **Validate every schema block** with Google's Rich Results Test and the Schema.org validator before deploy — every single time, not just on first ship[cite:128][cite:130].
- Do not overinvest in exotic schema chasing AI visibility hacks — Google's own guidance is that foundational, accurate structured data plus genuinely helpful content outperforms schema gimmicks[cite:119].

## Rule 5 — Agent & Crawler Access (robots.txt / llms.txt)

- **Explicitly allow legitimate AI search crawlers** in robots.txt: `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, and equivalents — unless there's a deliberate business reason to block training crawlers while still allowing search-time agents[cite:123][cite:133].
- Test robots.txt changes against at least one URL that should be blocked, one that should pass, and one borderline wildcard case, before deploy[cite:129].
- **`llms.txt` is the currently-adopted format** for giving AI systems structured context about the site — use it[cite:106][cite:114][cite:115]. Content must not be locked behind JavaScript-only rendering, logins, or paywalls if it needs to be agent-readable — critical content should be server-side rendered or present in initial HTML[cite:131].
- **Do not rely on `ai-plugin.json` / `description_for_model`** as a primary AEO strategy — this is the OpenAI ChatGPT plugin manifest schema, and OpenAI deprecated the plugin store itself in 2024[cite:107][cite:113]. It's harmless to keep as a redundant signal, but it must never be the only place a critical fact (compliance status, feature availability) is declared. Facts must always live in `llms.txt` and on-page content first.

## Rule 6 — No Over-Claiming, No Dead-End Promises

- **A CTA may never promise a destination or feature that doesn't exist.** "Start Free Trial" is banned copy unless a real trial signup flow exists and is linked. If it doesn't exist yet, the button must say what it actually does (e.g., "Request a Demo," "Talk to Sales").
- **One label per distinct destination, one destination per label.** If three buttons all point at the same anchor/form, they must share one label. Synonym-labeling the same action (e.g., "Book a Demo" / "Request Demo" pointing at the same place) is decision fatigue and gets removed on sight.
- Any compliance or certification badge (GDPR, ISO 27001, ISO/IEC 27701, SOC2, etc.) shown on a page must reflect **actual, current status** — "in progress" and "held" are not interchangeable, and the real status must also be stated plainly in `llms.txt` so agents don't infer a stronger claim than is true.

## Rule 7 — Accessibility Is Not Optional

- **Every interactive element needs an accessible name.** Icon-only buttons/links (WhatsApp, social icons, chat toggles) must carry `aria-label` — an icon with no text and no label is invisible to screen readers and unparseable by agents.
- No decorative or consumer-grade emoji inside CTAs, buttons, or professional/enterprise copy. Emoji are fine in casual chat widget text, never in a primary conversion element.
- Minimum 44×44px touch targets, visible focus states on every interactive element, and full keyboard navigation — WCAG 2.2 AA is the floor, not the ceiling, on every project regardless of size.

## Rule 8 — Legal & Contact Consistency

- **Never ship placeholder legal text** (`[LEGAL COMPANY NAME]`, `[REGISTERED ADDRESS]`, bracket placeholders of any kind) to a live URL, even flagged as "review before launch" in a code comment — if it's not launch-ready, it doesn't go live, full stop.
- **One canonical contact address per purpose**, stated consistently everywhere it appears (site footer, `llms.txt`, privacy policy, cookie policy). If there are genuinely two purposes (sales vs. privacy/DPO), label each role explicitly — never present two unlabeled addresses as interchangeable "the" contact.
- The legal entity name on privacy/cookie/terms pages must be the real, current operating entity, consistently — not a placeholder, not a legacy project codename, not different from the entity named elsewhere on the same page.

## Rule 9 — Content Freshness & Verification Discipline

- Update statistics, dates, and examples with current data — AI answer engines have a strong recency bias and will deprioritize stale content[cite:131].
- Before submitting any audit or "all clear" report, verify findings against the **actual live deployed files**, not a local or stale branch. If a finding depends on a build-time variable (like domain/origin), state explicitly whether it was checked pre- or post-build.
- If you flag something as a defect and later determine it wasn't one, say so directly in the same report — a self-correction is a sign of a trustworthy audit, not a weakness. Silent omission of a wrong call is worse than admitting it.

---

## Pre-Deploy Checklist (Apply to Every Project)

- [ ] Real domain everywhere (canonical, hreflang, sitemap, robots.txt, llms.txt) — zero placeholders
- [ ] One H1, no heading-level skips, consistent semantic levels site-wide
- [ ] FAQPage schema present and validated
- [ ] One JSON-LD schema type per page, validated, matches visible content
- [ ] robots.txt explicitly allows legitimate AI crawlers, tested against sample URLs
- [ ] No CTA promises a feature/destination that doesn't exist
- [ ] No duplicate-labeled CTAs pointing at the same destination
- [ ] Every icon-only interactive element has an accessible name
- [ ] No emoji in CTAs or professional copy
- [ ] WCAG 2.2 AA: 44px touch targets, visible focus states, full keyboard nav
- [ ] Zero bracket placeholders on any live legal page
- [ ] One consistently-labeled contact address per purpose
- [ ] Audit performed against live deployed files, not a stale branch

This document supersedes any project-specific instruction that conflicts with it. When in doubt on a new project, this is the standard to build to from the first commit — not a retrofit applied after launch.
