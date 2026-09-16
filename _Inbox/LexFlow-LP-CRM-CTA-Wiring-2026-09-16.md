---
title: LexFlow LP — CRM CTA wiring finished (local only)
created: 2026-09-16
updated: 2026-09-16
tags: [lexflow, landing-page, cta, netlify, railway, kanban]
status: rework-done-in-review
task: t_198870bd
---

# LexFlow LP — CRM CTA wiring finished (local only)

Kanban task `t_198870bd` (frontend-developer-lovable_react), contract **local-only**.
Nothing deployed, nothing pushed. Preview: **http://127.0.0.1:8899/index.html** (`Сделано ЛОКАЛЬНО`,
server `serve_preview.py` PID 15315, detached). Round 2 handoff: commits `4b5d61d`, `47ed616`,
`293da63`, `55d5488` on `main` (ahead 7 / behind 0 vs `origin/main` `6632284`).

## Canonical CTA target — CHANGED in round 2 (Ole, 2026-09-16 16:15)

```
https://web-production-031a6.up.railway.app/admin/panel
```

**CRM entry door (superadmin), wired into all 7 CRM-facing links** in `index.html` (navbar, hero
badge, hero CTA, 2× closing CTA, footer App/Admin) and into the same 7 links + mock caption of the
publicly served `lexflow-landing-ready-for-deployment.html`.

Why it changed: Ole's correction via operator-installer — for *this* build the site CTA must open the
CRM entry so the project visibly closes end-to-end; the **per-tenant** workspace deep link
(`/login?ws=lexflow&back=…`, kept in commit `293da63`) is deferred to a **later, separate repoint
pass** that will carry the client-facing workspace login. The earlier rationale still holds for that
pass: the bare root auto-redirects a logged-in user by the domain-scoped JWT, so a Romanelli token in
the browser used to land in the wrong tenant (commit `6632284`).

Behaviour of the new door (verified): `/admin/panel` returns **200** `text/html` with no redirect
(HTML title `Super Admin — Workspaces & Accounts`); a signed-in operator gets the panel
(`h1: Super Admin — All Workspaces`), while a **cookie-less** browser is sent on to the CRM's own
page by the page's client-side gate (`window.location.href='/'`). That gate is JS-only, so the HTML
is served to anonymous clients — a CRM-side note, not something the landing can fix.

## Repo reality check (this is what made the task confusing)

- The landing repo **moved**: `~/LexFlow-landing` → `~/Projects/LEGAL_backup/LexFlow-landing`
  (remote `github.com/Ole00007/LexFlow-landing`). The brief's path `~/LexFlow-landing/index.html`
  is stale — the file is not there any more.
  (Update: a Repo Root Rule now says all repos belong at `/Users/olesiarasing/projects/<repo>`;
  the staged migration has not touched this repo yet, so the path above is still the live one.)
- `.netlify/netlify.toml` still points `publish` at the old `~/LexFlow-landing` path.
- The **live** LP is `https://poetic-kleicha-28d058.netlify.app/` (sha256 identical to
  `origin/main:index.html`). `poetic-kleicha-c96710`, `poetic-kleicha` and
  `lexflow-landing.netlify.app` all 404 — three slugs for one site in the old docs.
- ~~The CRM agrees with the live host: `crm/__init__.py` maps workspace `lexflow` → `LEXFLOW_SITE_URL`~~
  **Wrong citation (round-1 review):** there is no `LEXFLOW_SITE_URL` anywhere in the CRM repo and no
  `ws` handling in `crm/__init__.py`. The real binding is the workspace seed row in
  `lexflow-crm/migrations/versions/3a6b84c5d9f2_add_multitenant_workspaces.py:35`
  (`VALUES (1,'LexFlow Default','lexflow',…)`). Re-confirmed empirically in round 2: the deployed
  login page renders tenant "LexFlow Default" for `?ws=lexflow` and "LexFlow" for `?ws=default`.
- `https://web-production-ab54f.up.railway.app/` is **still alive** (302 → `/login`) but has
  **0 references** in the site — the repoint to `031a6` is intact. `lexflow-mvp-production`
  (the host in the stale duplicate page) returns **404**.

## State after round 2

| Branch | HEAD | CRM CTAs |
|---|---|---|
| `main` | `55d5488` | **7/7 on `/admin/panel`**, 0 legacy, 0 dead `#` — both HTML pages |
| `origin/main` | `6632284` | 7/7 on the deep link (this is what is live; the duplicate page there still carries 7 legacy refs) |
| `visual-redesign-hold` | `7c5d8cb` | 7/7 on the deep link; `index.html` still has 1 dead `#` footer link |
| `fix-try-demo` | `3b881e7` | same as above (stale feature branch) |

Rendered-DOM verification of the preview (headless Chrome harness that traps `fetch`/XHR/`sendBeacon`):
7 anchors on `/admin/panel`, 1 distinct CRM href, 0 `/login?ws=lexflow`, 0 bare-root, 0 legacy hosts,
0 dead `#`, **0 network calls**, title `LexFlow — Studio Legale X`, lang `it→en→it`, theme
`dark→light→dark`, 6 sections, Alessia chip → IT string then EN after a language switch. Served bytes
hash == `HEAD:index.html` (`46c22a40…`), 3× 200 **after** the Chrome sweep.

## Round 1 review defects — closed in round 2

1. **Preview URL dead** — root cause reproduced on the replacement too: stock `python3 -m http.server`
   keeps its LISTEN socket and answers nothing after a headless-Chrome sweep. Replaced with
   `serve_preview.py` (ThreadingHTTPServer, daemon threads, 20 s request timeout, HTTP/1.1) started
   detached by `start_preview.sh`, so the URL survives the agent session. Re-verified 3× 200 after the
   browser runs.
2. **`lexflow-landing-ready-for-deployment.html`** — its 7 legacy refs repointed (kept, not deleted:
   retiring a published page is Ole's call). The live copy still shows the old links until a deploy.
3. **Bare-root CRM POST from the Alessia widget** — removed with its dead `sending`/`error` strings,
   `extractReply`/`safeText` and `isSending`; chip clicks now only update the message (IT/EN) and the
   WhatsApp CTA is the single working action. The real endpoint stays documented for the follow-up.
4. **False `LEXFLOW_SITE_URL` citation** — corrected (see above); `back=` inert is moot now that no
   page passes `back=`.

## Open items for Ole

1. Footer says "ISO 27001:2022 · ISO/IEC 27701:2025" as if held — the product's own
   `ai-plugin.json` says the certification is *in progress, not held*. Wording needs his call.
2. No privacy policy page exists for this landing (privacy/cookie URLs 404 on Netlify).
3. Deploy decision is gated: live is still the pre-Romanelli-redesign build with the old CTA target.
4. Stale deploy config (`publish` path) and the stale duplicate page still publicly served.
5. **Alessia widget → real intake** needs Ole's sign-off on new name/email/GDPR fields + IT/EN consent
   copy (visual change). Follow-up card **`t_62cbf086`** (assignee operator-installer, parent
   `t_198870bd`): wire `POST /api/intake/lexflow` (needs `fullname`+`email`; CORS already allows the
   Netlify origin + localhost dev ports; it creates a real Contact+Case and emails both parties).
6. CRM-side: make the `/admin/panel` door a server-side redirect to the branded login rather than a
   client-side JS gate.
7. Second site, separate repo: `LEXFLOW Web-Site` (multi-page EN/IT/RU) has 63 correct deep
   links and 0 bare-root CTAs, but is **not deployed anywhere**, and 3 `back=` params point at
   the non-resolving placeholder `lexflow.example.com`.

## Process lesson (kanban)

The **review** run (28) stayed alive after its own `changes_requested` verdict and committed the rework
itself (`ee4836f` → amended `293da63`) while the rework run (30) was verifying the same files —
a duplicate worker on one card and one repo. The rework was verified independently rather than redone,
but the dispatcher should not let a review run keep committing to the card it just returned. Retry
diagnosis: `git status` clean then dirty with commits you never made, and two PIDs from
`ps -eo pid,lstart,command | grep "work kanban task <id>"`.

Full report + audit scripts + desktop/mobile screenshots:
`~/.hermes/kanban/workspaces/t_198870bd/` (`LEXFLOW-LP-CTA-WIRING-REPORT-2026-09-16-v3.md`,
`audit_branches.py`, `build_r2_harness.py`, `parse_audit.py`, `repoint_to_admin_panel.py`,
`serve_preview.py`, `start_preview.sh`, `lp_v3_desktop.png`, `lp_v3_mobile.png`).

## Operator-installer independent verification (2026-09-16 16:25)

Cross-checked the handoff against the live artifacts (not the report). Results:

- **OK** — served bytes `sha256 46c22a40…` == `HEAD:index.html` on `main` `55d5488`; preview
  `http://127.0.0.1:8899/index.html` answers 200 (PID 15315).
- **OK** — 7 distinct CRM hrefs in the *served* bytes, all `/admin/panel`; 0 legacy hosts, 0 dead `#`.
- **OK** — `POST https://web-production-031a6.up.railway.app/api/intake/lexflow` with `{}` →
  `400 {"error":"Name and email are required"}`, i.e. the endpoint is real and a safely-invalid probe
  writes no record.
- **OK** — `OPTIONS` preflight from `https://poetic-kleicha-28d058.netlify.app` → 200 with
  `access-control-allow-origin` echoing the Netlify origin and POST in `allow-methods` (set by the
  Railway `CORS_ORIGINS` env var, **not** the repo default at `crm/config.py:33`).
- **Handler re-read** — `lexflow-crm/crm/routes/views.py:268-337` creates a Contact + Case in the
  LexFlow workspace, logs 2 activities, emails the workspace owner, and returns
  `201 {success,contact,case}` for JSON callers.
- **WARN** — `gdpr_consent` is read and timestamped (`:293,303`) but **not enforced**: a submit with
  `gdpr=false` still creates the record. If the widget ships a consent checkbox, either the endpoint
  enforces it or the copy must not claim consent blocks submission.
- **WARN** — the public route carries no explicit `@limiter.limit`; it inherits
  `default_limits=["200 per day","50 per hour"]` per IP (`crm/extensions.py:15-18`) over
  `memory://` storage, so the ceiling is per worker process, not global. Spam path exists but is bounded.

### Decision package for `t_62cbf086` (Alessia widget → real intake)

The widget today is: launcher → panel with one message, **4 urgency chips** (low/medium/high/critical),
and a WhatsApp CTA (`wa.me/393450234084`). It has no name/email inputs and makes 0 network calls.
Wiring it to `POST /api/intake/lexflow` therefore adds visible fields — a **design change gated on Ole's
preview sign-off**, per the standing design rule.

| Item | Proposal |
|---|---|
| required | `fullname`, `email`, consent checkbox |
| optional | `phone`, `practice_area`, `message` (the message already composes the urgency sentence) |
| chips | keep 4 chips, map to the urgency sentence in `message` (no API field for urgency) |
| CTA | `Invia richiesta / Send request` = the POST; WhatsApp stays as a secondary link |
| success | swap panel body to a thank-you state (endpoint returns `201`) |
| consent copy | cannot link to a policy page — **none exists** on this landing (open item 2 above) |

Consent copy draft (needs Ole's word choice):

- IT: `Ho letto l'informativa privacy e acconsento al trattamento dei dati per essere ricontattato.`
- EN: `I have read the privacy notice and consent to the processing of my data so I can be contacted.`

Legal caveat: the entity is still "Studio Legale X" and no P.IVA exists
([[LexFlow-Legal-Publishing-Blockers]]), so an "informativa privacy" that does not exist yet is
referenced by this line. Wiring the widget without the policy page is a **compliance risk Ole must accept
or block**. A safer interim wording avoids the claim of an existing notice but is weaker GDPR-wise.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-Public-Intake-Contract-2026-09-15]]
- Related: [[LexFlow-Web-Site-Build-2026-09-07]]
- Related: [[LexFlow-MultiTenant-Test-Setup]]
