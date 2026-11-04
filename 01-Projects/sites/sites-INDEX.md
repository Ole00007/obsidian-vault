---
title: sites — Index
created: 2026-08-26
tags: [index, hub]
status: active
---

# sites — Index

Inventory of websites and web applications tracked in Obsidian or found in the
current Cloudflare account. This is a working inventory, not proof that any
project meets the LEXFLOW quality manifesto.

**Checked:** 2026-11-03. Cloudflare account listings returned 6 Workers and 3
Pages projects. All nine URLs returned HTTP 200 via `curl`; this confirms
reachability only. Netlify CLI is not installed, so Netlify coverage below is
limited to URLs recorded in Obsidian and is not an account-wide inventory.
Source-path/deployment mappings marked unconfirmed need owner/project
verification. No listed site is certified as fully meeting the manifesto.

## Deployed websites — Cloudflare

| Site / application | Class | Local source path | Deployment | Reachability | Manifesto |
|---|---|---|---|---|---|
| AI & Crypto guide | Static information guide | `/Users/olesiarasing/Downloads/ai-crypto-compliance/public/index.html` | Workers: [ai-crypto-compliance](https://ai-crypto-compliance.olesya00007.workers.dev/) | HTTP 200, checked 2026-11-03 | Not audited; do not treat as quality example |
| Goldoni 6 audit | Hospitality site audit | `/Users/olesiarasing/projects/HOSPITALITY/GOLDONI6/_bundle/index.html` | Workers: [goldoni6](https://goldoni6.olesya00007.workers.dev/) | HTTP 200, checked 2026-11-03 | Not verified |
| avibe-hospitality | Hospitality product/marketing site | `/Users/olesiarasing/projects/HOSPITALITY/site/index.html` (Pages-source mapping unconfirmed) | Pages: [avibe-hospitality](https://avibe-hospitality.pages.dev/) | HTTP 200, checked 2026-11-03 | Not verified |
| avibe-hospitality raw variant | Hospitality product/marketing site | `/Users/olesiarasing/projects/HOSPITALITY/raw/index.html` | Workers: [hospitality-raw](https://hospitality-raw.olesya00007.workers.dev/) | HTTP 200, checked 2026-11-03 | Not verified |
| ENNEFEX audit | Client website audit | `/Users/olesiarasing/projects/ENNEFEX/ennefex site audit 15 oct 2026_bundle/index.html` | Workers: [ennefex](https://ennefex.olesya00007.workers.dev/) | HTTP 200, checked 2026-11-03 | Not verified |
| LexFlow landing | SaaS product landing page | `/Users/olesiarasing/projects/lexflow/lexflow-website/` (`wrangler.toml`, build output `dist/`) | Workers: [avibe-lexflow-landing](https://avibe-lexflow-landing.olesya00007.workers.dev/) | HTTP 200, checked 2026-11-03 | Not verified |
| Romanelli Studio | Professional services / legal studio | `/Users/olesiarasing/projects/LEGAL_backup/Romanelli-studio/index.html` | Workers: [romanelli-studio](https://romanelli-studio.olesya00007.workers.dev/) | HTTP 200, checked 2026-11-03 | Not verified |
| LexFlow multi-page website | SaaS marketing site | `/Users/olesiarasing/Desktop/projects/Products & Services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site/` | Pages: [lexflow-site](https://lexflow-site.pages.dev/) | HTTP 200, checked 2026-11-03 | Existing quality-debt records; not a full pass |
| Alena Krot audit | Healthcare / professional audit landing page | **Source not found.** An older note records `/Users/olesiarasing/Projects/Alena Krot/Alena_LP_SEO_AEO_GEO_Ads_Audit_v3.html`, which is currently missing. | Pages: [alenakrot-audit](https://alenakrot-audit.pages.dev/) | HTTP 200, checked 2026-11-03 | Not verified |

## Deployed websites — Netlify

These are Netlify URLs documented in Obsidian and checked for HTTP reachability
on 2026-11-03. Netlify project ownership/source was not independently
enumerated because the Netlify CLI is unavailable.

| Site / application | Class | Local source path | Deployment | Reachability / status | Manifesto |
|---|---|---|---|---|---|
| LexFlow legacy landing | Legacy SaaS landing page | `/Users/olesiarasing/projects/LEGAL_backup/LexFlow-landing/index.html` | [poetic-kleicha-28d058.netlify.app](https://poetic-kleicha-28d058.netlify.app/) | HTTP 200; documented as frozen legacy surface | Not verified |
| Avv. Pagliano | Client legal-services website | `/Users/olesiarasing/Obsidian/01-Projects/AVibe-CRM/LexFlow/pagliano/index.html` | [verdant-crumble-021449.netlify.app](https://verdant-crumble-021449.netlify.app/) | HTTP 200 | Not verified |
| LexTaskFlow architecture schema | Product architecture/demo page | Local source path not located | [muzloto-apr-1f8f19.netlify.app](https://muzloto-apr-1f8f19.netlify.app/) | HTTP 200; older notes identify this page | Not verified |
| Netlify reference site | Reference used in a LexFlow comparison brief; ownership and source unconfirmed | Local source path not located | [coruscating-pegasus-c96710.netlify.app](https://coruscating-pegasus-c96710.netlify.app/) | HTTP 200; not counted as a confirmed owned deployment | Not applicable |
| `lexflow.netlify.app` | Unknown / password-protected project | Local source path and ownership not confirmed | [lexflow.netlify.app](https://lexflow.netlify.app/) | HTTP 401; contents/ownership unknown | Not assessed |

### Historical Netlify URLs (not live)

Obsidian records these as stale or never deployed; do not use as production
links: `https://poetic-kleicha.netlify.app/` (stale), `https://lexflow-landing.netlify.app/`
(404), and `https://lexflow-lp.netlify.app/` (never deployed).

## Local websites — no deployment identified

Each HTML file below exists locally under
`/Users/olesiarasing/Obsidian/01-Projects/sites/`. No corresponding deployment
was identified in the checked Cloudflare account or the Netlify URLs recorded
in Obsidian.

| Site | Absolute local source path | Status |
|---|---|---|
| Bar del Porto | `/Users/olesiarasing/Obsidian/01-Projects/sites/bar-del-porto/index.html` | Local only; no deployment identified |
| Beauty Studio | `/Users/olesiarasing/Obsidian/01-Projects/sites/beauty-studio/index.html` | Local only; no deployment identified |
| Firenze Segreta | `/Users/olesiarasing/Obsidian/01-Projects/sites/firenze-segreta/index.html` | Local only; no deployment identified |
| Genova Segreta | `/Users/olesiarasing/Obsidian/01-Projects/sites/genova-segreta/index.html` | Local only; no deployment identified |
| Liguria Viaggi | `/Users/olesiarasing/Obsidian/01-Projects/sites/liguria-viaggi/index.html` | Local only; no deployment identified |
| Mare Fiori | `/Users/olesiarasing/Obsidian/01-Projects/sites/mare-fiori.it/index.html` | Local only; no deployment identified |
| Massage Studio | `/Users/olesiarasing/Obsidian/01-Projects/sites/massage-studio/index.html` | Local only; no deployment identified |
| Nail Studio | `/Users/olesiarasing/Obsidian/01-Projects/sites/nail-studio/index.html` | Local only; no deployment identified |
| Parruchiere | `/Users/olesiarasing/Obsidian/01-Projects/sites/parruchiere/index.html` | Local only; no deployment identified |
| avibe-hospitality site preview | `/Users/olesiarasing/projects/HOSPITALITY/site/index.html` | Local preview documented as not deployed; Pages mapping above still needs confirmation |
| LexFlow landing visual variant | `/Users/olesiarasing/projects/LEGAL_backup/lexflow-landing-visual/index.html` | Local prototype; no deployment identified |

## Web applications and backend services

These are application services, not static website deployments. Statuses below
come from existing Obsidian records and were not re-tested in this inventory.

| Application | Local source path | Deployment | Last recorded status |
|---|---|---|---|
| LexFlow CRM | `/Users/olesiarasing/projects/lexflow/lexflow-crm/` | [Railway production](https://web-production-031a6.up.railway.app/) | Production deployment recorded; current health not re-verified |
| LexFlow Chatbot | `/Users/olesiarasing/projects/LEGAL_backup/LexFlow-Chatbot/` | [Railway](https://lexflow-chatbot-production.up.railway.app/) | Previously recorded live; current health not re-verified |
| Avibe Hindsight service | `/Users/olesiarasing/projects/avibe-hindsight/` | [Railway health endpoint](https://avibe-hindsight-production.up.railway.app/health) | Previously recorded healthy; current health not re-verified |
| LexFlow MVP legacy service | Local source path not found | [Railway](https://lexflow-mvp-production.up.railway.app/) | Older inventory recorded HTTP 404; legacy/superseded |

## Inventory and quality rules

- When presenting this inventory, always include the absolute local source path
  for each site or application. If it is unknown or missing, say so explicitly.
- Include deployed sites, application/backend services, and local-only projects;
  show the host and current verification date when checked.
- HTTP reachability is not a quality audit. Mark a project as meeting the
  manifesto only after checking its applicable Definition of Done items and
  recording evidence; no project in this inventory is currently certified.
- Update this index rather than creating a parallel sites/apps inventory.

## Notes

- [[mare-fiori.it/mare-fiori.it-INDEX]]
