# LexFlow Web-Site — SEO / AEO / GEO Origin Plan (2026-09-16)

**Status: PLAN — no code, no deploy. Awaiting Ole's decisions (see §7).**
**Raised by:** frontend-developer (kanban t_ee09cd1c) · **Planned by:** operator-installer
**Repo:** `/Users/olesiarasing/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site`
**Branch at plan time:** `feat/heading-align-cta-merge` @ `23678b7`

---

## 1. The issue in one paragraph

The site hardcodes a placeholder origin (`ORIGIN = "https://lexflow.example.com"`,
`templates/build-lang-sites.py:42`). That single constant is the absolute home address the
site advertises about itself: canonical tags, hreflang alternates, og:url, JSON-LD `url`/`logo`/`@id`,
all 48 sitemap `<loc>` entries, the `Sitemap:` line in `robots.txt`, the demo link in `llms.txt`,
`ai-plugin.json` and `openapi.yaml`, and even the `back=` parameter on the "Sign in" links.
Today every one of those tells Google and every AI crawler that the canonical home of this
site is a domain that does not exist — so nothing about the site can be resolved, verified
or cited. For a legal product, that is an AEO **trust** failure before it is an SEO one.

## 2. Measured evidence (commands re-runnable, scripts attached)

Audited the committed tree (59 HTML files) with `audit_origin.py`:

| Defect | Pages affected (before fix) |
|---|---|
| Placeholder origin in `canonical` | **54** |
| Placeholder origin in `og:url` | **51** |
| Placeholder origin in JSON-LD `url` | **48** |
| **Canonical points at the WRONG page** | **9 real pages** |
| No canonical at all | 5 (404.html + 4 duplicate `(1)` files) |
| Multiple canonicals on one page | 0 |

**Finding the ticket did not have — a second, independent bug.** Seven live English article
pages declare `canonical`/`og:url`/JSON-LD `url` as the *matter-tracker* article, so Google is
asked to treat them as duplicates of one other page (they would simply not be indexed):

```
lexflow-article-adoption-in-small-firm.html      -> .../lexflow-article-matter-tracker.html
lexflow-article-ai-assisted-operations.html      -> .../lexflow-article-matter-tracker.html
lexflow-article-client-communication.html        -> .../lexflow-article-matter-tracker.html
lexflow-article-crm-migration.html               -> .../lexflow-article-matter-tracker.html
lexflow-article-law-firm-automation.html         -> .../lexflow-article-matter-tracker.html
lexflow-article-law-firm-workflows.html          -> .../lexflow-article-matter-tracker.html
lexflow-article-security-privacy.html            -> .../lexflow-article-matter-tracker.html
cookie-policy.html                               -> .../privacy.html
```
The article build stamped a template head and never rewrote it. The `/it/` and `/ru/` copies
of the same pages are correct (they pass through `rewrite_head`), so EN and IT/RU disagree
about which page is canonical — the worst possible signal.

**And a third: fixing `ORIGIN` alone does not fix the site.** I made `ORIGIN` env-driven and
rebuilt from a pristine copy — the placeholder survived in **24 canonicals, 21 og:url, and all
48 JSON-LD `url` fields**, because the English pages and every JSON-LD block are never
rewritten by the build; they keep whatever the source file happens to contain. Proven by
`audit-after.txt` (env-driven ORIGIN only) vs `audit-after3.txt` (full fix). The ticket's step 1
is necessary but **not sufficient** — hence §4 P0.2/P0.3.

## 3. Blast-radius map (what one constant feeds)

| Consumer | File / mechanism | Stamped by build? |
|---|---|---|
| canonical, og:url | every page (EN hand-baked, IT/RU rewritten) | partially |
| hreflang ×4 per page | `hreflang_block()` line 331 | yes |
| JSON-LD `url`/`logo`/`@id` | inline `<script type="application/ld+json">` | **no** |
| 48 sitemap `<loc>` + alternates | `write_sitemap()` line 464 | yes |
| `robots.txt` `Sitemap:` line 25 | hand-maintained | **no** |
| `llms.txt` line 58 (demo link) | hand-maintained | **no** |
| `.well-known/ai-plugin.json` (api/logo/legal, 3 URLs) | hand-maintained | **no** |
| `.well-known/openapi.yaml` (contact/license/server, 3 URLs) | hand-maintained | **no** |
| "Sign in" `back=` parameter (3 pages) | inline link | **no** |

The four hand-maintained files are exactly the ones an AI agent reads first — which is why an
agent asking "does this endpoint exist?" gets a contradiction from a manifest pointing at a
dead host.

## 4. The plan

### P0 — local fix, no deploy, no approval needed (owner: frontend-developer, reviewed by operator-installer)
1. **`ORIGIN` becomes configuration** — `os.environ.get("ORIGIN", <default>)`, trailing slash stripped.
   *(Already prototyped and verified in a scratch copy — see §5.)*
2. **Canonical correctness pass**: force `canonical` + `og:url` + the JSON-LD `url` to the page's
   own absolute URL on **every** page, EN included. This fixes the 9 wrong-canonical pages and
   guarantees "one canonical per page, pointing at itself" structurally rather than by hand.
3. **Origin rotation + drift guard**: at the end of every build, replace any retired origin
   (`OLD_ORIGINS`, default `https://lexflow.example.com`) with `ORIGIN` across every published
   file (HTML, `robots.txt`, `llms.txt`, `sitemap.xml`, `site.webmanifest`, `.well-known/*`,
   `assets/*`), then **abort the build** if any retired origin survives in a page. A host swap
   then becomes a config edit, and a half-swapped tree cannot be published.
   *In practice (P1) this also runs as a one-shot stamp over the already-built tree.*
4. **`/` must resolve.** There is no root `index.html` — only `lexflow-index.html` (confirmed:
   `git ls-files | grep '^index'` → nothing). Ship `dist/_redirects` with
   `/ /lexflow-index.html 200` (rewrite, not a redirect) and keep
   `canonical = /lexflow-index.html` so there is exactly one canonical URL. Promote `/` to the
   canonical only if Ole wants the shorter URL later — that is a URL-structure decision (§7.4).
5. **Curated `dist/` output.** Publish a whitelist, never the repo root. Measured today: the repo
   root would serve **141 tracked files**, of which **53 are not site content** — including
   4 tracked duplicate pages (`lexflow-index (1).html` etc. → duplicate content at a crawlable
   URL), 15 stale HTML copies under `templates/` (including another copy of the homepage and of
   `privacy.html`/`terms.html`), internal `.md`/`.csv` analysis
   (`ENRICHMENT-REPORT-2026-09-13.md`, `claims-register.csv`, pricing/claims material), a
   tracked **`.DS_Store`**, plus 8 untracked strays (6 probe HTML files, `templates/__pycache__/`,
   `templates/pre-h2-promotion-20260915/`). Curated `dist/` = **88 files, 0 forbidden** (verified).
   *(Deleting the tracked duplicates from the repo is a deletion → needs Ole's OK, §7.6.)*
6. **`sitemap.xml` `lastmod` is frozen at 2026-09-13** while pages have changed since. Derive it
   from the build date or file mtime so Google's recrawl signal is honest.

### P1 — interim publish on Cloudflare Pages (owner: operator-installer; **GATED**, see §7.1/§7.2)
7. Create the Cloudflare Pages project, set `ORIGIN` to the Pages hostname, rebuild, publish the
   curated `dist/`. `robots.txt`, `llms.txt`, `ai-plugin.json`, `openapi.yaml` all resolve.
8. Verify live (§6 acceptance), then re-run Google-facing steps.

### P2 — on domain close (owner: operator-installer)
9. Point the Pages project at the custom domain, then set `ORIGIN` to the real domain
   (`OLD_ORIGINS` = the interim host + the placeholder), rebuild, publish. Add a redirect from
   the interim host to the custom domain so any early links don't dangle.
10. Re-submit the sitemap and re-check canonicals on the live host.

### P3 — post-deploy search & agent hygiene (owner: operator-installer; **needs Ole's Google account**)
11. Search Console: verify ownership (DNS TXT or HTML file — Ole supplies/approves the token),
    submit `sitemap.xml`, request indexing of `/`, `/it/`, `/ru/` plus the 9 articles.
12. AI-crawler access check: `robots.txt` already allows GPTBot, ChatGPT-User, ClaudeBot,
    Claude-Web, PerplexityBot, Google-Extended, anthropic-ai, Applebot-Extended, cohere-ai —
    confirm from the live host and spot-check `llms.txt` is fetchable and self-consistent.
13. Validate the JSON-LD (Organization / WebSite / SoftwareApplication / FAQPage / BlogPosting)
    against the live URLs and confirm no off-domain `@id` remains.

### P4 — decide `ai-plugin.json` (owner: Ole, §7.5)
14. Recommendation: **keep the file** (harmless, some agents still read manifests), but remove it
    from the AEO narrative — the story is `llms.txt` + JSON-LD + `assets/webmcp.js`. OpenAI
    stopped new plugin installs after 2024-03-19, so it is dead weight for its named purpose.
    Do not delete it in the same change as the origin fix (keep the diff reviewable).

## 5. Prototype already verified (this is the proof the plan is implementable)

I prototyped P0.1–P0.3 in a scratch copy — **the repo itself was not touched**:

- `build-lang-sites-ORIGIN.patch` (134 lines) — env-driven ORIGIN, canonical/og/JSON-LD self-stamp,
  origin rotation, drift guard.
- Rebuilt from a **pristine** copy with `ORIGIN=https://lexflow-site.netlify.app`:
  build exits 0, `every data-i18n key had a translation in both languages`,
  `rewrote 18 English pages`, `sitemap.xml written with 48 URLs`,
  `origin rotation: 28 files rewritten`, `origin drift guard: PASS`.
- Post-build audit: **placeholder in canonical / og:url / JSON-LD = 0 / 0 / 0**;
  cartesian mismatch gone on every real page; the only remaining "canonical ≠ own URL" hits are
  the 6 untracked probe files that P0.5 removes from the publish set.
- Article JSON-LD now self-referential, e.g.
  `lexflow-article-security-privacy.html` → `"url": ".../lexflow-article-security-privacy.html"`.
- Content not damaged: EN titles/langs intact (the build's own guard asserts it), `data-i18n`
  element counts unchanged (index 108, blog 97, crm-migration article 30), hreflang reciprocity
  spot-checked EN ↔ `/it/` ↔ `/ru/`.
- `dist/` whitelist build: 88 files, 0 forbidden.

## 6. Acceptance criteria (a fix is "done" only when all pass on the **live** host)

1. `ORIGIN` is env-driven; no code edit is needed for the domain swap.
2. `grep -r "lexflow.example.com" dist/` → **0 hits** (HTML + txt + json + yaml + xml).
3. Every published page has exactly **one** canonical and it equals the page's own absolute URL.
4. `sitemap.xml`: every `<loc>` on the live origin, returns **200**; count == published indexable
   pages; `lastmod` current.
5. hreflang: 4 alternates (en / it / ru / x-default) per content page and **reciprocal** across
   all three languages; EN-only legal pages carry none (as now).
6. `robots.txt` `Sitemap:` line and `llms.txt` demo link point at the live origin;
   `/.well-known/ai-plugin.json`, `/.well-known/openapi.yaml`, `/assets/webmcp.js` fetch 200.
7. `dist/` contains no `templates/`, no `(1)` files, no `.md`/`.csv`/`.DS_Store`/`__pycache__`,
   no probe files.
8. `curl -I` → 200 on `/`, `/llms.txt`, `/robots.txt`, `/sitemap.xml`,
   `/.well-known/ai-plugin.json`, one `/it/` page, one `/ru/` page, one article page.
9. No regression: EN pages keep their own title/H1; IT/RU pages keep baked translations;
   the intake/contact block and WhatsApp links still work.

## 7. Human confirmation required (nothing below is auto-approved)

| # | Decision | Why it needs Ole |
|---|---|---|
| 7.1 | **Interim hostname** — the exact Cloudflare Pages project name that becomes `ORIGIN` | it becomes the site's stated home for weeks; Ole owns the Cloudflare account |
| 7.2 | **Permission to publish** the corrected `dist/` | any deploy is a gated action; per standing rule "NEVER deploy without a separate go" |
| 7.3 | **Domain close timing** — when `lexflow.com` DNS is fixed / which domain is actually bought | I can't buy or verify the domain; P2 is blocked on it |
| 7.4 | **`/` vs `/lexflow-index.html`** as the canonical home | URL structure is permanent-ish; my recommendation is the `/` rewrite in P0.4 |
| 7.5 | **Fate of `.well-known/ai-plugin.json`** (keep / drop) | product/positioning call |
| 7.6 | **Delete the 4 tracked duplicate `(1)` pages** (and optionally the stale `templates/` HTML) from the repo | deletion of tracked files |
| 7.7 | **Search Console token** for P3 | needs Ole's Google account |

## 8. Cost / effort

No recurring cost. Cloudflare Pages free tier for hosting; the fix is a code change plus one
config value. Estimated implementable in one focused session; the domain-close step (P2) is a
one-line config change by design.

## 9. Not in scope here

Netlify landing (`~/LexFlow-landing`, separate project, already live as `poetic-kleicha`) is
untouched. The `/api/public/intake` contract remains "defined, not enabled" — the site's
WhatsApp fallback stays. UX/design work on `feat/heading-align-cta-merge` is untouched: the
origin fix changes `<head>` metadata only, so it will rebase cleanly onto it.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Build-2026-09-07]], [[LexFlow-Web-Site-Enrichment-Elisa-2026-09-13]]
- Handoff artifact: `01-Projects/LexFlow/_from-repos/LexFlow-Web-Site-Origin-Fix-2026-09-16/`