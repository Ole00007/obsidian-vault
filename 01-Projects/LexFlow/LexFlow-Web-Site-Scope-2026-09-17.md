---
title: LexFlow — Web-Site Scope & Status 2026-09-17
created: 2026-09-17
tags: [lexflow, website, scope, status]
status: active
---

# LexFlow — Web-Site Scope & Status (2026-09-17)

Current scope and state of the LexFlow marketing website after the 2026-09-17 session.

## Deployed (production, live)
- **URL:** https://lexflow-site.pages.dev (Cloudflare Pages, project `lexflow-site`)
- **Deployment:** `1cba771c` · branch `main` · source commit `0a6f5bd`
- **ORIGIN:** `https://lexflow-site.pages.dev` — single source (build-lang-sites.py:42); 0 placeholder domains in source + dist + live
- **Consent UI:** Privacy Notice is a real clickable link → privacy.html; Cookie Policy removed (banner + prefs modal); dead JS removed
- **Privacy:** §5 "Cookies & tracking technologies" expanded (owner template, placeholders preserved)
- **Anchor:** `id="hero"` on homepage (EN/IT/RU) — the CRM backlink target
- **Verified live:** 0 `/admin` exposure, 0 placeholders, canonical/hreflang/robots/sitemap correct

## GitHub (public)
- **Remote:** github.com/Ole00007/lexflow-website (PUBLIC)
- **Branches pushed:** `main`, `feat/heading-align-cta-merge`, `content/humanization-20260917`
- **Secret scan:** clean (full history) — safe to be public
- **Content export:** `content-export-20260917/` — 19 pages, 3038 blocks (en 1043 / it 998 / ru 997), re-import by `content_id`

## Handed to operator-installer
- **CRM repoint** (`t_8586ceed`, Ole's direct request): CRM website/home link → `https://lexflow-site.pages.dev/#hero`, remove legacy Netlify refs
- **Hard rule** (`t_228db57d`): no parallel source of truth / no duplicate registries (user-mandated permanent standard)
- **Daily status cron** (`2573e20ab61f`, 09:00): operator updates LexFlow CRM project status + schedules unfinished tasks

## Pending / blocked
- **Legal identity:** P.IVA, entity, registered address, PEC — placeholders only, no fabrication; site NOT "promoted" until P.IVA supplied
- **Cloudflare Git integration:** dashboard-native connect (production branch = main, build = `python3 templates/build-lang-sites.py && python3 templates/build-dist.py`, ORIGIN in CF env)
- **Composio (Smothy):** MCP wired via tool-router session + `x-api-key` (working); durable OAuth JWT route blocked by Composio SDK being v2-era (0.7.21 latest); auto-refresh wrapper built at `~/.hermes/composio-refresh/refresh.mjs` (untested/unscheduled)

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Quality-Debt-Register-2026-09-17]]
- Related: [[LexFlow-Web-Site-CRM-Repoint-2026-09-17]]
