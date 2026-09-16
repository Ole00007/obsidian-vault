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

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Enrichment-Elisa-2026-09-13]]
- Related: [[LexFlow-Web-Site-Build-2026-09-07]]
- Related: [[LexFlow-Audit-Checklist]]
