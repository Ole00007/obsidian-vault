---
title: LexFlow — /api/public/intake contract review
created: 2026-09-15
tags: [lexflow, crm, api, intake, contract, agent-surface]
status: review
source: "kanban t_4c31dac3 (from frontend-developer)"
project: LexFlow
---

# LexFlow — /api/public/intake contract review (2026-09-15)

Answer to kanban card `t_4c31dac3` (raised by frontend-developer-lovable_react after site
commit `b9b406a` added `.well-known/openapi.yaml`, `.well-known/ai-plugin.json`,
`assets/webmcp.js`, refreshed `llms.txt` and upgraded the site schema).

Repo under review: `~/Desktop/projects/services/LEGAL/LEXFLOW Production/lexflow-crm`
(branch `lexflow_hermes_v1`, HEAD `fddbb7b`; remote `github.com/Ole00007/lexflow-crm`).
Prod: `https://web-production-031a6.up.railway.app`.

## Verdict

**The contract matches what I would build.** I recommend implementing it exactly as
written (same path, same JSON shape, same status codes), with the deltas below. Nothing
in the contract requires a schema change.

## Measured state (probed 2026-09-15, live prod + repo HEAD)

| Probe | Result |
|---|---|
| `GET /` | 200, `<title>aLEXy – Legal Intake & Status Suite</title>` — **still says aLEXy** |
| `GET /api/public/intake` / `POST` (JSON) | 404 `{"error":"Not found"}` — route does not exist |
| `POST /api/contacts` | 401 `{"msg":"Missing Authorization Header"}` (JWT required) |
| `GET /api/contacts` (anonymous) | 200 `[]` |
| `GET /api/cases` (anonymous) | 200 `[]` |
| `POST /api/chatbot` | 404 |
| `POST /submit` | 302 redirect to `/` (public, form-encoded, legacy intake) |
| `GET /health` | 200 ok |

### Corrections to the frontend's two security/CORS claims

1. **"Full contact list and case list are publicly readable" — NOT a data leak.**
   `GET /api/contacts` and `GET /api/cases` return **200 with an empty array** to an
   anonymous caller. `crm/workspace.py::get_visible_workspace_ids()` returns `[]` (not
   `None`) for anonymous callers by design, and `workspace_filter()` then filters
   `workspace_id IN []` — so zero rows are ever returned. The severity is cosmetic
   (should be 401, not 200-with-empty-list), not a leak. Worth changing for hygiene.
2. **CORS is already open for the live landing pages.** The deployed service returns
   `access-control-allow-origin` for `http://localhost:3000`,
   `https://poetic-kleicha-28d058.netlify.app` (LexFlow landing) and
   `https://verdant-crumble-021449.netlify.app` (Pagliano). Only the placeholder
   `lexflow.example.com` gets no ACAO header — expected, that domain does not exist yet.
   `crm/config.py` lines 34-38 already list the Netlify origins. So the frontend's
   "CORS allows localhost:3000 only" observation is stale against repo HEAD and prod.

## Deltas between the contract and the CRM data model

Field mapping is clean for the required fields:

- `name` → `contacts.fullname` (NOT NULL) ✅
- `email` → `contacts.email` (NOT NULL) ✅
- `phone` → `contacts.phone` ✅
- `consent_privacy` (required true) → `contacts.gdpr_consent` + `gdpr_consent_ts` ✅ (perfect fit, already exists)
- `message` → `contacts.notes` ✅
- `source` → `contacts.source` is `String(20)` with values manual/intake/booking/web/import → store `'web'`; the contract's *page identifier* does not fit 20 chars.
- `practice_area`, `consent_marketing`, `lang` → **no columns exist**. Either store them in `contacts.tags` (JSON list, already used) or add columns via migration.

Other deltas:

1. **Response `id` type.** Contract says `id: type: string`; `Contact.id` is an integer.
   Return `{"id": str(contact.id), "status": "created"}` to match literally, or relax the
   contract to integer. Cosmetic — pick one and make both sides agree.
2. **Contact only vs Contact + Case.** The contract promises "Contact created". The legacy
   `/submit` route creates a Contact **and** a Case. Decision needed — see below.
3. **Rate limiting already exists globally.** `flask-limiter` is installed and initialised
   with `default_limits=["2000 per day", "300 per hour"]` (`crm/extensions.py`), keyed on
   remote address. The contract's 429 just needs a tighter per-route limit (e.g.
   `@limiter.limit("5 per minute;20 per hour")`) on the new route.
4. **Existing legacy public route.** `POST /submit` (`crm/routes/views.py:393`) is public,
   form-encoded, creates Contact + Case, logs activity, accepts file uploads, and returns a
   302 redirect — not JSON, and not under `/api/*` so Flask-CORS adds nothing. It works for
   a classic form POST but cannot serve the site's `fetch()` JSON flow.

## Decisions Ole must make before implementation

- **D1 — Contact only, or Contact + Case?** Recommend **Contact only** (`status='lead'`,
  `lifecycle_stage='lead'`, `source='web'`), matching the contract. Note the consequence:
  a contact-only lead appears in Contacts but **not** in the dashboard or calendar. If the
  intake must reflect across Contacts + Calendar + dashboard, we should also create an
  intake Case — but then the contract's response shape should say so.
- **D2 — Where do `practice_area`, `lang`, `consent_marketing` go?** Recommend `tags`
  (no migration, already JSON-backed) rather than new columns.
- **D3 — Workspace routing for public leads.** Recommend defaulting to the `lexflow`
  workspace and optionally honouring `?ws=<slug>` for future per-tenant sites. Must **not**
  hardcode a workspace id (prod ids start at 7; `crm/routes/views.py` carries a warning
  about a past ForeignKeyViolation from hardcoding id 1).
- **D4 — Ship the aLEXy → LexFlow naming fix?** Text-only edit, 3 files:
  `templates/index.html`, `templates/status.html`, `static/mockup.html`. Local test, then
  separate deploy go.

## Blocked-card status (asked on `t_4c31dac3`)

- `t_d6065167` — blocked; 2 crashed runs. Questions answered here.
- `t_85d62411` — blocked; 2 crashed runs. Q1–Q4 answered here.
- `t_8c6d4642` — blocked; 2 crashed runs. This is a **different, substantial task**
  (site EN capability claims vs real CRM, report-only); it is *not* answered by this note
  and should be unblocked to run fresh.
- Root cause of all six crashed runs: `worker exited cleanly (rc=0) without calling
  kanban_complete or kanban_block` — the profile could not reach a model (Nous auth).
  operator-installer now resolves to `deepseek/deepseek-v4.1-flash` via **openrouter**, and
  this card ran end-to-end, so the blocker is empirically resolved.

## Follow-up review — kanban `t_35c677e0` (Elisa copy + functions list)

Frontend opened a Package-1 proposal card (`t_35c677e0`) asking whether the "basic
functions available now" list matches live, plus status of the three blocked cards.
Reviewed at Web-Site HEAD `88f6cc9`; re-probed prod. **No writes to the site repo.**

**Corrections issued:**

1. `GET /api/contacts` / `GET /api/cases` are `200 []` — empty, not readable data
   (anonymous workspace filter returns no rows). Hygiene, not exposure.
2. `site-config.js` is not "WhatsApp only": `chatbotUrl` is set (path `/api/chatbot`,
   which 404s and is *unused*), and the WhatsApp number is still a `TODO`.
3. Missing from the list: `POST /submit` → 302 (live public write, form-encoded, no CORS),
   and CORS already allows the Netlify origin.
4. Scope qualifier demanded: "calendar / cloud storage / notifications not live" is true
   of the *site → CRM lead path* only — those features DO exist in the CRM. Writing it
   unqualified would re-introduce the understatement bug Ole already corrected.

**Chatbot copy premise is false at HEAD.** All three `COPY` dicts are complete and
identical — 44 top-level keys each (en 33–69, it 72–108, ru 111–147). Nothing renders
`undefined`. Only two genuinely missing keys are *referenced in code*:
`c.urgencyLabel` (line 263, un-localised summary) and `c.needDescribe` (line 276).
Real work = add those two keys ×3 languages, plus optionally the one-line merge
`Object.assign({}, COPY.en, COPY[lang()])` as insurance. `t()` returns the whole dict,
so per-key fallback must be a merge, not a lookup.

**Elisa has no chat logic at all.** `CHAT_PATH` (line 28) is dead code; the only `fetch`
is `POST` to `CFG.intakeEndpoint` (line 312). Wiring it to `/api/chatbot` needs new chat
code, not a config change. Payload delta for backend: Elisa sends
`source='lexflow-website-elisa'` (**21 chars** — overflows `contacts.source` `String(20)`),
plus `status`/`urgency`; forms.js sends `page` (`location.pathname`). None have columns.

**Card status:** `t_d6065167` + `t_85d62411` superseded (answered here / on `t_4c31dac3`);
`t_8c6d4642` (site-claims audit) still unstarted, needs unblock; `t_7bf4de1f` (backend-dev)
held blocked pending Ole's D1–D4.

## Re-measurement 2026-11-06 (54 days later) — the premises changed, and one of them is a P0

Re-probed from the Mac on 2026-11-06 22:05 CET. **The service the site is pointed at is gone:**
`https://web-production-031a6.up.railway.app` answers `404 {"status":"error","code":404,
"message":"Application not found"}` with `server: railway-hikari`, `x-railway-fallback: true`,
`x-railway-edge: cdg1` — two probes, identical. This is the Railway edge fallback: no service is
bound to that hostname. It directly contradicts `docs/LexFlow_Agentic_Roadmap.json` `open_p0
P0-PROD-DOWN`, which says *"RESOLVED 2026-10-27 — prod back at 200 … /health 200, / 200 verified
2026-10-27"*. Either the service was re-created under a new hostname after that date, or it went
down again and nobody re-probed. **The roadmap P0 needs re-baselining on the next status run.**

**What is live instead:** `https://lexflow-web-production.up.railway.app` —
`GET /api/health` → 200 `{"status":"ok","database":"healthy","document_storage":"healthy",
"service":"lexflow"}`; `/api/openapi.json` → 200, **FastAPI `LexFlow` v0.3.0, "Local-first digital
case file system for law firms", 106 paths**; front end is Next.js (`<title>LexFlow</title>`,
`lang="hr"`); `/login` 200.

| Probe (2026-11-06) | Result | Reading |
|---|---|---|
| `GET /api/contacts` | 404 | endpoint gone in this build |
| `GET /api/cases` (anon) | 401 `{"detail":"Not authenticated"}` | properly gated, no exposure |
| `POST /api/chatbot` | 404 | does not exist |
| `POST /submit` | 404 | does not exist here |
| `GET /api/public/contact/{slug}` | **404 `{"detail":"Kontakt obrazac nije dostupan."}`** | route EXISTS, form DISABLED for every tenant |
| `POST /api/public/contact/{slug}` `{}` | 422, missing `name`,`email`,`oib`,`subject`,`message` | route EXISTS and validates |
| `GET /api/public-contact-settings` (anon) | 401 | enabling it needs auth |
| `OPTIONS/GET` with `Origin: https://poetic-kleicha-28d058.netlify.app` | **no `access-control-allow-origin`** | site origin still blocked |
| same with `Origin: https://lexflow-site.pages.dev` | no ACAO | not allowlisted either |

Slugs tried for an enabled public form — `lexflow`, `romanelli-studio`, `orasing`, `pagliano`,
`tommasoferro`, `cl1`, `demo`, `test`, `lexflow-crm` — **all 404**. No tenant has the public form on.

### Revised verdict per question

**Q1 — the route already exists; what is missing is (a) enabling it per tenant and (b) making it
fit.** Live contract is `POST /api/public/contact/{slug}`, 201 on success, with a `website`
honeypot field (default `""`). It is **not** the site's contract: it requires `oib` (Croatian
personal tax number) and `subject`, and has **no** `consent_privacy`, `practice_area`, `lang`,
`source` or `page`. For Italian visitors `oib` is a hard blocker → either it becomes optional for
non-Croatian tenants or the site gains an OIB-style field it should not have. The Flask CRM repo
(`~/projects/lexflow/lexflow-crm`, branch `lexflow_hermes_v1`, HEAD `9af129c`) does have a public
`POST /submit` (form-encoded, resolves `?ws=` → `lexflow` → first active workspace, find-or-create
`Contact(status='lead')` + `Case`), but that host is the dead one, so it is moot until something is
bound.

**Q2 — CORS is still genuinely open, but now on a different service than the 2026-09-15 answer
described.** The old note said "already done in production" — true of the Flask build
(`crm/config.py` lists `verdant-crumble-021449.netlify.app`, `lexflow-site.pages.dev`,
`localhost:3000-5003`), false of the live FastAPI/Next build: no ACAO header for either site
origin, and `OPTIONS` returns 400/404 with no ACAO. Needs the real Cloudflare origin allowlisted in
the live service's config.

**Q3 — naming is already correct on the live service.** `/`, `/login`, `/api/health`
(`"service":"lexflow"`) and the OpenAPI `info.title` all say **LexFlow**; no `aLEXy` anywhere on
that host. In the Flask repo `aLEXy` now survives in exactly one file —
`static/mockup.html` (5 hits: title, two body paragraphs, a span, the footer copyright) — the
`templates/index.html` / `templates/status.html` occurrences from the 2026-09-15 note are already
fixed at HEAD. Cosmetic cleanup only, and deploy-gated.

**Q4 — explicit blockers.**
1. **The source of the service that actually answers today is not on this machine.** Not under
`~/projects` (no `next.config.*`, no repo whose code contains `document_storage` or
`"Not authenticated"`), not under `~/projects/LEGAL_backup`, and the legacy
`~/Desktop/LexFlow/LexFlow Review Build` no longer exists. I cannot change that service's CORS or
relax `oib` until Ole says where that repo lives / who owns it.
2. **No Railway access** — the 2026-09 roadmap records the CLI token 403ing on Backboard GraphQL,
   so I cannot read its variables, enable the public form for a tenant, or redeploy.
3. **Ole's decision on `oib`** (drop/optional vs a different field) — it changes the public schema.
4. **Real site origin** (Cloudflare) for the CORS allowlist — frontend-dev's 27-page site is *not*
   deployed anywhere yet: `poetic-kleicha-28d058.netlify.app` serves an older build titled
   "LexFlow — Studio Legale X" with no `site-config.js` reference, so `intakeEndpoint` cannot be
   pointed at anything meaningful yet.
5. Deploy/push of any fix stays behind Ole's per-push authorisation (PUSH GATE).

**Not a blocker:** the "unauthenticated `GET /api/contacts` and `/api/cases` expose the full
contact and case list" claim is **false on today's live service** — `/api/contacts` 404 and
`/api/cases` 401. It was already false on the Flask build (`200 []`, anonymous callers resolve to
no visible workspace). It should be retired from the site's copy.

Repo paths this section refers to: `/Users/olesiarasing/projects/lexflow/lexflow-crm` (branch
`lexflow_hermes_v1`, `static/mockup.html`, `crm/config.py`), `/Users/olesiarasing/projects/lexflow/
lexflow-website` (branch `main`, `assets/site-config.js` line 42 `intakeEndpoint: null`,
`assets/forms.js` `payloadOf` lines 102–117), and the live service
`https://lexflow-web-production.up.railway.app` (unknown repo — see blocker 1).

## Roadmap re-baseline 2026-11-06 22:08 CET (card `t_ba26097d`) — landed, additive only

The re-baseline this section asked for is now in the authority:
`docs/LexFlow_Agentic_Roadmap.json` on branch `lexflow_hermes_v1` @ commit `99e42f8` (local, unpushed).
Additive edits: `P0-PROD-DOWN` carries a `rebaseline_2026_11_06_2208` block (the 2026-10-27
"RESOLVED" stamp is explicitly marked **not re-confirmed**), `P0-PROD-DOWN-REGRESSION-2026-11-04`
carries the 22:08 re-confirmation, and a new entry `P0-PROD-IDENTITY-UNCONFIRMED-2026-11-06` records
that `web-production-031a6` is Railway edge-404 while `lexflow-web-production` serves a healthy
FastAPI 0.3.0 + Next.js build **whose identity and source repo are UNCONFIRMED**. No P0 was flipped
open or closed; no roadmap task column changed.

Independent probe set behind it (2026-11-06 22:08 CET, `curl -D -`): `web-production-031a6` `/` 404
(0.29 s), `/health` 404 (0.26 s), `/login?ws=lexflow` 404 (0.33 s) — all `server: railway-hikari`,
`x-railway-fallback: true`, `x-railway-edge: cdg1`; `lexflow-web-production` `/api/health` 200,
`/` 200 (Next.js HIT, `lang="hr"`), `/login` 200, `/api/openapi.json` 200 (106 paths), anon
`/api/cases` 401, `/api/contacts` 404 `{"detail":"Not Found"}` — the 404 there is a **missing route**
in that build, not a gate. Local source search for the live build (`Local-first digital case file
system`, `case-intelligence`, `smart-scan` over `/Users/olesiarasing/projects`) → **0 hits**.

The one question left for Ole is unchanged from blocker 1 above and now recorded in the roadmap's
`open_p0`: which Railway service is the real production, and where does the FastAPI 0.3.0 / Next.js
source repo live?

- Repo: `/Users/olesiarasing/projects/lexflow/lexflow-crm` (worktree
  `/Users/olesiarasing/projects/lexflow/lexflow-crm-wt-merge`, branch `lexflow_hermes_v1`, `99e42f8`).

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Enrichment-Elisa-2026-09-13]]
- Related: [[LexFlow-Web-Site-Build-2026-09-07]]
- Related: [[LexFlow-Audit-Checklist]]
