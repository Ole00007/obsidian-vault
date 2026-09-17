# LexFlow Web-Site — CRM Repoint to the New Site (2026-09-17)

**Status:** DONE locally, **not deployed** (CRM commit `6ef25da` on `lexflow_hermes_v1`, unpushed)
**Kanban:** `t_8586ceed` (operator-installer) — Ole's direct request
**Authority for this change:** the CRM repo itself (`github.com/Ole00007/lexflow-crm`,
working copy `~/Desktop/projects/services/LEGAL/LEXFLOW Production/lexflow-crm`).
This note is a record/pointer, not a second source of truth (§9).

## What Ole asked
Repoint the LexFlow CRM's website/home/logo link to the new site
(`lexflow-site.pages.dev/#hero`) and remove legacy Netlify references.

## Key finding — the "/#hero" form in the ticket is not usable
Probed production directly (2026-09-17):

| URL | Result |
|---|---|
| `https://lexflow-site.pages.dev/` | **HTTP 404** — "404 — Page not found" |
| `https://lexflow-site.pages.dev/lexflow-index.html` | **HTTP 308** → `/lexflow-index` (Cloudflare Pages clean URLs) |
| `https://lexflow-site.pages.dev/lexflow-index` | **HTTP 200**, homepage, exactly **1** `id="hero"` ✓ |
| `https://lexflow-site.pages.dev/lexflow-index#hero` | **HTTP 200**, anchor resolves ✓ |

So the site has **no root entry point**, and the anchor must hang off the clean URL
`/lexflow-index`, not `/`. The CRM was pointed at **`https://lexflow-site.pages.dev/lexflow-index#hero`**.

## Changes (CRM repo, commit `6ef25da`, 6 files)
- `crm/__init__.py` — extracted the per-workspace site map into `public_site_url(slug)`,
  now the single server-side source of truth, and repointed the `lexflow` entry.
- `crm/routes/views.py` — `/login` "← Torna al sito" now falls back to the tenant's public
  site instead of `#`. The marketing site links to `/login?ws=lexflow` with **no** `?back=`,
  so before this the back-link was hidden — a dead end from the CRM login page.
- `crm/config.py` — dropped the legacy Netlify CORS origin, added the new marketing origin.
- `templates/base.html` + `templates/kanban.html` — the "Return to main website" client-side map.
- `docs/UX-Test-Report-2026-09-04.md` — noted the legacy origin was removed (kept historical integrity).

## Verification (local, real output)
- 12/12 rendered routes HTTP 200; legacy-origin refs = **0** in source **and** rendered output.
- Exactly one `id="hero"` live on the homepage; identical in `dist/` (EN/IT/RU).
- `/admin` is **not** referenced anywhere on the marketing site.
- `py_compile` clean on the three touched Python files.

## Deliberately left alone (flagged for Ole)
- **Pagliano's client LP on Netlify (verdant-crumble) — retained.** It is a *different client's*
  live site, not legacy LexFlow; removing its CORS origin would break that LP's API calls.
- **`docs/LexFlow_Agentic_Roadmap.json` history note** mentioning the old Netlify auto-deploy —
  a factual record of a past commit, not a live reference.
- **Railway env overrides.** The new URL is only the *default*: if `LEXFLOW_SITE_URL` or
  `CORS_ORIGINS` are set in Railway variables, prod still uses the old values. Not checked.

## Blocked / follow-up
- Follow-up card **`t_b92d36cc`** → `frontend-developer-lovable_react`: decide a root entry point
  (root `index.html` vs `_redirects` in `templates/build-dist.py`) so the bare domain stops 404-ing.
- Deploy is **gated**: pushing `6ef25da` triggers a Railway production deploy and needs Ole's
  explicit go.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Quality-Debt-Register-2026-09-17]]
- Related: [[LexFlow-Web-Site-SEO-AEO-GEO-Origin-Plan-2026-09-16]]
