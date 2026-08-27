# Studio Legale Pagliano — LP Architecture & Style Book

> Single source of truth for the Avv. Diego Pagliano landing page. Update this file whenever the LP changes.

---

## 1. Architecture (file map)

| Path | Role |
|---|---|
| `pagliano/index.html` | **The LP** (single file: HTML + inline CSS + inline JS). Deployed to Netlify. |
| `pagliano/templates/pagliano.html` | Byte-identical copy of `index.html` used by the local Flask preview (`pagliano/app.py`). **Always `cp index.html templates/pagliano.html` after editing.** |
| `pagliano/static/` | All assets: `hero-bg.png` (header photo), `chat-avatar.png` (Alessia), `chat-widget.js` (chatbot), `blog-*.jpg` (blog thumbs), `favicon.*` (brand icons). |
| `pagliano/app.py` | Local-only Flask proxy (NOT deployed). Serves the template + proxies `/api/intake` to the CRM. |
| Repo root `wsgi.py` + `crm/` | The real backend (CRM) on **Railway** — `web-production-ab54f.up.railway.app` (auto-deploys from `main`). |

### Deploy targets
- **LP:** Netlify `verdant-crumble-021449.netlify.app` (site `b060d5c1-…`), publish root = repo root (LP lives at `/pagliano/`).
- **Backend/CRM:** Railway `web-production-ab54f.up.railway.app` (project *compassionate-trust*). Push to `main` → auto-deploy.
- **CORS:** `crm/__init__.py` allow-list = Netlify domain + `localhost:5000/8877`. Add new origins there.

### Browser-facing endpoints
| Endpoint | Purpose | Payload |
|---|---|---|
| `POST /api/intake` | Consultation request (form + chatbot) | FormData: `fullname, email, phone, message/practice_area, source, gdpr_consent` → creates Contact + Case |
| `POST /api/appointments` | Appointment booking (chatbot) | JSON: `fullname, email, phone, event_date (ISO), title, description, location, gdpr_consent, source` → creates Contact + Event + Google Calendar sync |
| `GET/PATCH /api/appointments` + `.../confirm` `.../cancel` | Admin list / confirm / cancel | JWT-protected |

---

## 2. Style Book

### Brand palette (light theme — dark theme shares accent)
| Token | Value | Use |
|---|---|---|
| `--primary` / `--primary-dark` | `#0E2A47` / `#081B2F` | Navy — header, footer, chat header |
| `--accent` | `#698269` | **Dusty sage-green** (tuned down from the old vivid `#1FAE72`) — CTAs, links, icons, focus rings |
| `--accent-hover` | `#57734F` | Hover state for accent |
| `--bg` / `--surface` / `--border` | `#FFFFFF` / `#F6F8FA` / `#E2E6EB` | Page / cards / hairlines |
| Gold | `#D4AF37` | Favicon monogram, avatar ring, hero monogram "DP" |
| Scrim | `rgba(105,130,105,…)` (was `rgba(31,174,114,…)`) | Soft accent tints — keep consistent when adding |

### Typography
| Element | Font | Notes |
|---|---|---|
| Hero h1, section h2, logo, footer h4 | **Playfair Display** (serif) | The classy editorial voice |
| Card titles (`.area-card h3`, `.blog-body h3`) | **Inter** (sans, 650) | New — sans for UI titles |
| Body, labels, buttons, chat, trust band | **Inter** (sans) | Body 300–500, labels 600–700 uppercase |

### Iconography
- Thin-stroke inline SVG line icons (`class="ico"`, `stroke="currentColor"`, 1.7px, round caps) — no emoji in sections.
- Containers: `.trust-icon` emerald circle (white icon) · `.area-icon` 52px accent-tint square · `.blog-thumb` navy.

### Animations
| Where | Effect |
|---|---|
| Hero header photo | Ken-burns `30s` zoom/pan (`hero-kenburns`), navy scrim over, `prefers-reduced-motion` respected |
| Blog thumbnails | Ken-burns `18s` zoom + speeds to `7s` on hover |
| Mobile nav | Right-side drawer (`max-width 300px`, below 70px header, right-aligned) |
| Chat | Avatar (60/38/28px), gold ring in header, emerald ring on messages |
| Dropdowns | `.blog-more` max-height transition (0→560px) — "Leggi di più" accordions in Blog + Chi Sono |

### Components
- **Header:** sticky 70px, logo serif, Login → CRM, theme toggle, hamburger (≤700px drawer).
- **Hero:** photo bg + "Avv. Diego Pagliano" + 2 CTAs + circular avatar placeholder ("DP" gold monogram).
- **Trust band:** 4 items, 2-col on mobile.
- **Aree di Competenza:** 4 cards, emerald top-line on hover.
- **Chi Sono:** photo placeholder (gold "DP" watermark) + bio + "Leggi di più" → 2nd paragraph + credentials.
- **Contatti:** intake form → `/api/intake`.
- **Blog (Approfondimenti):** 3 cards, image thumbs + "Leggi di più".
- **Chat "Alessia":** floating avatar button → panel; see §3.

---

## 3. Chatbot "Alessia" — spec (UTD)

- **Code:** `pagliano/static/chat-widget.js` (vanilla JS IIFE, zero deps, ~590 lines). Loaded at `index.html:2092`.
- **UI markup:** `index.html:1855` (toggle) · `:1858` (panel) · `:1859–1866` (header: avatar, "Alessia — Assistente digitale dello studio legale").
- **State machine:** `state.step` + `state.flow`; option chips drive flows:
  - *Consulenza:* name → email → phone → desc → FormData → `/api/intake`
  - *Appuntamento:* name → email → phone → **sede/telefono** (options) → date (`dd/mm/yyyy`) → time → motivo → JSON → `/api/appointments` (`location` = "Studio Legale — Via Gropallo 10/2, 16122 Genova" or "Telefono")
  - *Servizi / Contatti:* static info chips
- **AI hook point:** replace `handleSend()` dispatcher (`chat-widget.js:559`) with a call to an AI endpoint; flows already collect structured fields you can pass as context. Backend APIs accept the payloads as-is.
- **Google Calendar:** `crm/services/calendar.py` (service account, `GOOGLE_CLIENT_SECRET_PATH`, scope `calendar.events`). Wired into appointments — runs **mock mode** until credentials are set on Railway; real sync stores `google_event_id` and deletes on cancel.

---

## 4. Gotchas

- **Masked phone:** LP displays `+39 380 527 9810` but `href="tel:+393****9810"` is masked in `index.html` — do not "fix" without approval (client decision). Chat widget uses the real number in links.
- **Sync law (never skip):** every `index.html` edit → `cp index.html templates/pagliano.html` **+ `md5` verify in the SAME command**, and report the hash. The file is only "synced" when both MD5s match.
- **Two copies exist on disk:** the working repo (`Desktop/projects/services/LexFlow-MVP/pagliano/`) and a STALE read-only backup clone at `~/pagliano_backup_readonly/…backup INCOMPL/`. If the user reports an "old" file, first `find /Users/olesiarasing -name pagliano.html` for duplicates — never assume the path you edited is the one they opened.
- **Flask preview caches templates** (`pagliano/app.py`): after LP edits, restart the process or you'll keep seeing the old page.
- **CORS:** browser → Railway calls need the origin in `crm/__init__.py`. Localhost tests = `localhost:5000` or `:8877`.
- **Favicon set:** `favicon.svg` + 16/32/180/192 PNGs, navy/gold "P" monogram, `theme-color #0E2A47`. Regenerate with `python3 /tmp/gen_favicon.py` (PIL).
- **Images:** AI-generated (FAL, via Nous subscription) — no extra cost. Keep ≤ ~50KB (800×400 JPG, q82) for web.

## Links
- Parent: [[pagliano-INDEX]]
- Related: [[PAGLIANO_SESSION_SUMMARY_2026-08-03]]
