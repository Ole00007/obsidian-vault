# Marefiori — Artefacts & Inventory

## Generated files
| File | Purpose |
|---|---|
| `index.html` | Full landing page (markup + style + script) |
| `favicon.svg` | Local flower-on-waves favicon (vector) |
| `favicon.png` | Generated flower-on-waves logo (1024×1024), downloaded locally |
| `robots.txt` | Crawler rules |
| `sitemap.xml` | Search-engine URL set |
| `architecture.md` | System / module overview |
| `site-map.md` | Section & URL tree |
| `site-requirements.md` | Spec + acceptance criteria |
| `plan.md` | Reusable prompting summary |

## Image assets (libraries used)
**Photos — Pexels** (`https://pexels.com`, free license, hotlinked CDN):
| Use | Pexels ID | Subject |
|---|---|---|
| Collections · Bouquets | **29601972** | Close-up wedding bouquet (Italian-venue feel) |
| Collections · Event florals | **35130782** | Elegant table centrepiece |
| Collections · Honeymoon | **31052815** | Romantic couple with flowers |
| Gallery · Summer bouquet | **35640555** | Pink roses bouquet |
| Gallery · Coral & gold | **14025720** | Roses close-up |
| Gallery · Tied with feeling (NEW) | **17993659** | Hands exchanging bouquet (emotional accent) |
| Gallery · Atelier corner | **31917406** | Couple in flower field (also hero poster) |
| Chatbot avatar | **13975904** | Smiling woman holding flowers |

**Video — Mixkit** (`https://mixkit.co`, free license):
| Use | ID / Title | Drop-in path |
|---|---|---|
| Hero background | **#25988 "Sunshine over the Mediterranean"** | `assets/hero.mp4` |

**Map — OpenStreetMap** (`https://openstreetmap.org`, free, no API key):
- Embed centred on Porto Antico di Genova (lat 44.4056, lon 8.9298).

**Favicon logo PNG (generated):** downloaded locally as `favicon.png` (1024×1024). Source: `https://v3b.fal.media/files/b/0aa79890/59IxWNHC3XaliVzgD9LFt_jYQlcizF.png`. SVG `favicon.svg` remains the vector fallback.

**Instagram reels** referenced by client as style examples (not used as assets — external, license-cleared sourcing done via Pexels instead):
- C-VfAZStK76, DKzndE-tSn5, C_qgPbtNtyg, C6vaQ6atA6U, C4AG6YvxSj0

## Client photos — sourced as Pexels stand-ins (swap for client shots later)
- Story / harbor → Pexels `11849088` (Genoa waterfront)
- Gallery "On the water" → Pexels `9650653` (speedboat)
- Gallery "A summer smile" → Pexels `247350` (smiling woman)
- Hero poster → Pexels `22227592` (Cinque Terre coast)
- Hero video → Mixkit #25988 (drop `assets/hero.mp4` when available)

## Endpoint inventory (all placeholders — wire before go-live)
| Key | Current value | Notes |
|---|---|---|
| `SITE_CONFIG.phone` | `+393450234084` | tel: + wa.me |
| `SITE_CONFIG.whatsapp` | `+393450234084` | wa.me link |
| `SITE_CONFIG.email` | `ciao@mare-fiori.it` | |
| `SITE_CONFIG.stripe.publishableKey` | `pk_live_XXXX` | secret stays server-side |
| `SITE_CONFIG.orderEndpoint` | `/api/order` | order form POST |
| `SITE_CONFIG.crmWebhook` | `https://hooks.avibe.agency/mare-fiori/crm` | insert real |
| `SITE_CONFIG.emailApi` | `https://api.avibe.agency/mare-fiori/email` | insert real |
| `CHATBOT_CONFIG.apiUrl` | `""` | set to LLM/chat endpoint |
| `CHATBOT_CONFIG.model` | `""` | e.g. `gpt-4o-mini` |
| Footer social | `href="#"` + `data-social` | IG / FB / Pinterest / TikTok |

## Verification status
- HTML well-formed; inline JS passes `node --check`.
- All image/video/map URLs HEAD-verified `200` (except `assets/*` user files, which show gradient fallback).
- Visual render not auto-verified (sandbox browser unavailable) — open `index.html` in a browser to confirm.

## Links
- Parent: [[mare-fiori.it-INDEX]]
- Related: [[architecture]]
