---
title: LexFlow Web-Site — Quality Debt Register ([OVERRIDE] DoD S5, deployed 14/15 failing)
created: 2026-09-17
tags: [lexflow, web-site, technical-debt, override, quality-manifesto, kanban]
status: review
source: "kanban t_3c7158f8 · commit bd4b683 · Cloudflare deploy c7b6aec0-66f7-43f0-b419-a918604491b3"
project: LexFlow
---

# LexFlow Web-Site — Quality Debt Register

Debt register required by **LEXFLOW-Quality-Manifesto §6 step 2** (and §0 Override Clause).
Owner invoked deploy authority; the site was promoted to production with **14 of 15
Definition-of-Done checks (§5) not passing**. Nothing here is a surprise defect — each
item was known and knowingly accepted at override time.

- Manifesto: `~/Obsidian/03-Resources/Reference-General/HERMES Rules/LEXFLOW-Quality-Manifesto.md`
- Deployment commit: `bd4b683` (branch `feat/heading-align-cta-merge`, HEAD)
- Cloudflare deploy: `c7b6aec0-66f7-43f0-b419-a918604491b3` (Preview → promoted to prod, owner override)
- Live origin: `https://lexflow-site.pages.dev`
- Kanban card: `t_3c7158f8` (assignee `operator-installer`)

---

## 0. Independent verification performed 2026-09-17 (operator-installer)

Every claim below was re-derived from the local repo and the live site — not copied
from the card body.

| Claim | Method | Result |
|---|---|---|
| dist size 14.1 MB | `du -sh dist/` | **CONFIRMED — 14 MB** |
| Heavy unoptimised PNGs | file sizes in `dist/assets/` | **CONFIRMED** — romanelli-* 908 KB–1.2 MB ×6, `lexflow-blog-team.png` 1.2 MB, `lexflow-chat-avatar.png` 1.1 MB, `lexflow-calendar-visual.png` 704 KB, `lexflow-kanban-visual.png` 348 KB; all PNG |
| Commit `bd4b683` on branch `feat/heading-align-cta-merge` | `git log`, `git branch` | **CONFIRMED** — it is HEAD |
| No git remote | `git remote -v` | **CONFIRMED — empty** |
| `intakeEndpoint = null` | `assets/site-config.js:42` (+ dist copy) | **CONFIRMED** |
| `/signup`, `/demo`, `/portal`, `/auth/staff`, `/admin` absent | live fetch of each | **CONFIRMED all 404** |
| `/admin` absent from public nav | href sweep over `dist/` | **CONFIRMED — 0 refs** |
| Accessibility statement page missing | `dist/` filename sweep + live `/accessibility` | **CONFIRMED — 404** |
| ORIGIN = pages.dev, 0 × `lexflow.example.com` | grep (1187 pages.dev refs) | **CONFIRMED** |
| robots.txt Sitemap line correct | live `robots.txt` | **CONFIRMED** |
| llms.txt live + honest limits section | live `llms.txt` | **CONFIRMED** |
| External Google Fonts on critical path | `dist/lexflow-index.html` `<link>` | **CONFIRMED** (LCP cause) |
| 48 sitemap `<loc>`, 51 HTML files in `dist/` | grep + find | **CONFIRMED** |

---

## 1. The 15 §5 checks — status and fix plan

| # | §5 check | Status at deploy | Fix | Effort |
|---|---|---|---|---|
| 1 | TypeScript strict: 0 errors | FAIL | Only satisfiable by the §8 Astro rebuild. Not fixable in-place. **Owner decision.** | part of ~11 h scaffold |
| 2 | Zod validation of content files | FAIL | `content.*.ts` + Zod schemas during Astro migration (§2.2) | ~2 h |
| 3 | Build dist < 500 KB gz + optimised images | FAIL (14 MB) | AVIF/WebP + responsive widths (~−85%) + lazy-load below fold. **Highest-value quick win — also unlocks #4** | ~1–2 h |
| 4 | LCP < 800 ms on emulated 3G | FAIL / unverified | After #3: Lighthouse CI gate + self-host fonts (`font-display: swap`) | ~1 h after #3 |
| 5 | CLS = 0, TBT < 50 ms | UNVERIFIED | Lighthouse CI (same pipeline as #4), capture baselines | ~1 h |
| 6 | axe-core: 0 violations WCAG 2.2 AA | UNVERIFIED | axe-core in CI; expect JS-filled empty headings (cookie banner) + icon-only links without names | ~1 h + fixes |
| 7 | Keyboard navigation operable | UNVERIFIED | Manual keyboard-only pass: nav, cookie banner, forms, Elisa widget | ~1 h manual |
| 8 | Screen-reader smoke test (NVDA/VoiceOver) | FAIL | VoiceOver pass: home + pricing + one article × 3 locales | ~1 h manual |
| 9 | All 3 locales: pages, links, hreflang | PARTIAL | 49/49 pages 200 + canonical/4 hreflang verified; missing exhaustive link crawl. Add lychee (or similar) over `dist/` in CI | ~30 min |
| 10 | canonical/hreflang/sitemap/robots/llms.txt/JSON-LD, 0 placeholders | **PASS** | — (see finding **N-1** below: one residual placeholder domain outside `lexflow.example.com`) | ~15 min |
| 11 | Visual regression: 0 unexpected diffs | FAIL | No approved baseline, no tooling, no vision in the image-work session. Capture baseline once owner approves the look, then add to CI | ~1 h |
| 12 | Forms: submit / honeypot / rate limit | FAIL | Needs `POST /api/public/intake` (tracked `t_7bf4de1f`, blocked on owner decisions D1–D4), then wire `intakeEndpoint` + honeypot + rate limit | ~3 h |
| 13 | CRM backlink / 0 legacy Netlify refs | PARTIAL | No Netlify refs; "Sign in" → CRM login OK. Missing GitOps: connect repo to Cloudflare Pages Git integration + add a git remote | ~30 min |
| 14 | CTA map: all 5 destinations + `/admin` absent | FAIL (partial) | `/admin` absent ✓, hero/demo CTAs work ✓; `/signup`, `/demo`, `/portal`, `/auth/staff` **do not exist** (verified 404). "Start Free Trial" is not backed by a real signup → relabel honestly until routes exist. **Owner product decision.** | ~30 min + product call |
| 15 | Accessibility statement page | FAIL | Add honest accessibility statement with complaints contact. Blocked on legal contact values (`t_051169c7`) | ~30 min |

---

## 2. New findings — beyond the original register

**N-1 — `hook.example.com` placeholder shipped in 45 live pages (contradicts check #10's "0 placeholders").**
Each of 45 `dist/**.html` files carries an HTML comment:
`<!-- WEBHOOK: id=WH-01 | endpoint: https://hook.example.com/lexflow/demo-request | trigger: CTA button click "Book a Demo" -->`
It is **inert** (`webhookBase: null`, every `webhooks.*` value `null`), so nothing is sent —
but it is a visible `example.com` placeholder in production page source. The card's check #10
was scoped to `lexflow.example.com` only, so this was missed. Fix: strip the comment at build
time (~15 min). Low severity, but it is exactly the "0 placeholders" claim.

**N-2 — the repo violates the Repo Root Rule (§8.1), and lives in the TCC-protected zone.**
`lexflow-site` sits at
`/Users/olesiarasing/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site`.
The rule requires `/Users/olesiarasing/projects/<repo>`; `~/Desktop/projects` is frozen legacy
and `~/Desktop` is TCC-protected (intermittent `Operation not permitted` for agent tooling).
This is also the reason the project has **no git remote** (item 13) — a GitOps/Cloudflare-Pages
Git integration cannot even be set up in the current location. Migration is a batch operation
run by `operator-installer` **with Ole's explicit go** (AGENT_RULES §8.2).

**N-3 — build output (`dist/`) is committed to git** (commit `fd2d5f1` "Add curated dist/ build").
So there are two copies of the generated site in the repo, and the "single-source build"
guarantee (§2.1) is only as good as the discipline of whoever re-runs the generator. Minor,
but it inflates the repo (59 MB total vs 14 MB dist) and muddies the §8 rebuild story.

---

## 3. Decision required from Ole (blocking)

The card is explicit: **do not action without owner sign-off on the rebuild-vs-patch decision.**

**Option A — Astro rebuild (§8, manifesto direction).** ~11 h focused. Gets items 1, 2, 3, 5, 6,
9, 11, 13, 15 architecturally right, and produces the Factory starter kit (§7). Treats the
current static implementation as legacy. Recommended by the frontend-developer.

**Option B — patch the static site.** Cheaper on paper, but items 1 and 2 (TS strict, Zod content)
are **unachievable in-place** — there is no TS and no content layer. Patching can only close
#3, #4, #5, #6, #9, #10, #15 and part of #14. It does not reach the standard; it reduces the debt.

**Options C — hybrid:** patch only the two live-risk items now on the *existing* site — #3
(image weight / LCP, 14 MB of PNGs on every visitor) and #10/N-1 (placeholder sweep) — and
schedule the rebuild for the rest. This is the smallest change that removes real user-facing
harm on the already-live production site.

Everything that would change the live site is additionally gated by the **Design Gate** (Ole's
localhost review before any deploy) and by **§5.1/5.2 of AGENT_RULES** (no silent deploys).

---

## 4. Recommended follow-up cards (not yet created — awaiting the decision)

| Item | Owner profile |
|---|---|
| Astro rebuild scaffold + content migration + CI gates | `frontend-developer-lovable_react` |
| Image optimisation (AVIF/WebP, responsive widths, lazy-load) | `frontend-developer-lovable_react` |
| Lighthouse CI + axe-core + lychee CI pipeline | `frontend-developer-lovable_react` |
| `POST /api/public/intake` then wire `intakeEndpoint` | `backend-dev` (existing `t_7bf4de1f`) |
| Accessibility statement page | `frontend-developer-lovable_react` (blocked on `t_051169c7`) |
| Repo move `~/Desktop/...` → `~/projects/lexflow-site` + add git remote | `operator-installer` (Ole's go per batch, §8.2) |
| Honest CTA relabelling ("Start Free Trial") | owner product decision first |

## Links

- Parent: [[01-Projects/LexFlow/LexFlow-INDEX|LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Cross-Test-PreDeploy-2026-09-16]]
- Related: [[LexFlow-Web-Site-SEO-AEO-GEO-Origin-Plan-2026-09-16]]
- Related: [[LexFlow-Legal-Publishing-Blockers]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Reference: [[AGENT_RULES]]
