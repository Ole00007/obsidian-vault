# LexFlow Web-Site — Root Entry Point (2026-09-17)

**Status:** DONE locally, **not deployed** (website commit `4e526a0` on `feat/heading-align-cta-merge`, unpushed)
**Kanban:** `t_b92d36cc` (frontend-developer-lovable_react) — design gate, in review
**Authority for this change:** the website repo itself (`github.com/Ole00007/lexflow-website`,
working copy `~/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site`).
This note is a record/pointer, not a second source of truth (§9).

## Problem
The bare domain `https://lexflow-site.pages.dev/` returned **HTTP 404** — the site had no root
entry point. `dist/` shipped neither a root `index.html` nor a `_redirects` file. Anyone typing,
sharing, or printing the bare domain landed on a 404.

## Decision — option (b): `_redirects` redirect, NOT a duplicate `index.html`
- **Option (a)** (`dist/index.html` as a copy of the homepage) would create a *second* URL serving
  identical homepage content — a duplicate canonical form, which the task forbids.
- **Option (b)** keeps `/lexflow-index` as the single canonical (CRM links to it, sitemap lists it,
  Pages clean-URLs the `.html` form) and makes `/` a pure alias via redirect.
- Status code **301** (permanent) to consolidate link equity; **302** is the conservative alternative.

## Changes (website repo, commit `4e526a0`, 2 files)
- `_redirects:7` — the rule: `/ /lexflow-index 301`
- `templates/build-dist.py:29` — `ROOT_FILES` allowlist now includes `"_redirects"`

## Generated dist/ diff
- **added** `dist/_redirects` (459 bytes)
- **no** `dist/index.html` (correct — no duplicate canonical form)
- regenerated via `python3 templates/build-dist.py` → 89 files, 14.0 MB

## Local preview (verified)
Command: `npx --no-install wrangler pages dev dist/ --port 8788 --local --compatibility-date=2026-08-11`
(compat date pinned because the local workerd binary predates today's date; the redirect rule parsed:
"Parsed 1 valid redirect rule")

What I saw:
- `GET /` → **301** → `http://localhost:8788/lexflow-index`
- `GET /lexflow-index` → **200**, homepage, exactly **1** `id="hero"` ✓
- `curl -L /` → final 200 at `/lexflow-index`, `<title>LexFlow — Legal SaaS for Modern Law Firms</title>`

Note: `_redirects` is consumed by the Pages runtime as a config file (not served as a static asset —
wrangler's local 502 on `GET /_redirects` is expected; the rule itself works). A `.wrangler/` cache
dir was left by the preview (untracked, harmless, can be deleted).

## Deploy gate
Not pushed. Deploying `dist/` to Cloudflare Pages needs Ole's explicit go/no-go on the root-entry
approach (301 vs 302 vs option a).

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-CRM-Repoint-2026-09-17]]
- Related: [[LexFlow-Web-Site-Quality-Debt-Register-2026-09-17]]
