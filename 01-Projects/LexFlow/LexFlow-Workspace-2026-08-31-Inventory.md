---
title: LexFlow — Workspace inventory (2026-08-31)
created: 2026-08-31
updated: 2026-09-03
tags: [lexflow, crm, multitenant, workspaces, inventory]
status: CURRENT ✅
---

# LexFlow — Workspace inventory (2026-08-31)

> **STRICT RULE (Ole, 2026-09-01 rev.):** This inventory is the single source of truth for all
> LexFlow workspaces. **Update at the END of each session** (not on every change run). When it
> is updated, reflect every workspace created/changed/re-pointed/credential change that happened
> during the session, then notify Ole. Do NOT let it go stale between sessions.
>
> **ARCHITECTURE DECISION RULE (Ole, 2026-09-01):** At the end of each session, either (a) record
> any architecture decision taken this session, or (b) explicitly confirm the architecture is
> UNCHANGED. Current architecture: single Flask app + one shared Postgres, row-level isolation by
> workspace_id (NOT separate DBs per client); single frontend codebase (Jinja2 + vanilla JS, no
> React); RLS (DB layer) built but NOT yet tested/merged — pending joint staging test.

## Roadmap v2 — surgical update (2026-09-03, afternoon session)
- `docs/LexFlow_Agentic_Roadmap.json` (repo `lexflow_hermes_v1`) updated + committed locally — **NOT pushed** (awaiting push approval).
- **`process_rules.cross_audit` (NO exceptions):** BEFORE every local test AND before any deploy, operator-installer and backend_dev cross-audit each other's code changes (operator-installer reviews backend_dev's code, backend_dev reviews operator-installer's code) → report to user → THEN deploy.
- **`process_rules.implementation_plan_gate`:** backend_dev submits an implementation plan BEFORE code ONLY when (a) the user explicitly requests it OR (b) operator-installer has a genuine doubt — NOT routine.
- **T-007 Contacts redesign = two-model split CONFIRMED (Ole):** Internal staff directory (workspace-filtered) + Client-Facing (lifecycle/consent/tags) — see Contact model section below.
- **T-017 (NEW, backlog):** `SEAT_LIMIT_DEFAULT` config value — 5 seats/tenant, DB-configurable, no redeploy.
- **T-018 (NEW, backlog):** Agentic AI-personalized email automation spec — confirmed missing, needs its own spec.

## Team working agreements (2026-09-03)
- **operator-installer = coordinator/orchestrator:** delegates specialist work (backend-dev, frontend-dev, memory-curator); does NOT take all tasks on its own shoulders.
- **Cross-audit rule** (see Roadmap v2 above): mutual code review before every local test / deploy — no exceptions.
- **Implementation-plan gate:** only on user request or genuine doubt — not routine.

## Contact model — two-split CONFIRMED (T-007, 2026-09-03)
- **Internal staff directory** (`firm_team`): workspace-filtered. backend-dev delegated to implement the Internal backend (deleg `deleg_377ec25e`); operator-installer's `firm_team.py` draft is the starting point.
- **Client-Facing model:** lifecycle / consent / tags — **field audit pending user confirmation** (next step).

## Live tenant table (prod `web-production-031a6`, project `perceptive-achievement`)

| # | Tenant | Workspace slug (id) | LP URL | LP → backend | Admin login (role) |
|---|--------|--------------------|--------|-------------|--------------------|
| 1 | LexFlow | `lexflow` (ws7) | poetic-kleicha-28d058.netlify.app | ✅ 031a6 (repointed, 0 ab54f) | olesya00007@yahoo.com / crm0826 (superadmin) |
| 2 | AVIBE Agency | `avibeagency` (ws8) | none yet — flag when deployed | — | alegra_007@proton.me (admin) |
| 3 | Avv.Pagl | `pagliano` (ws9) | verdant-crumble-021449.netlify.app | ✅ 031a6 | ms.okuneva@internet.ru (admin) |
| 4 | Romanelli Audit | `romanelli-studio` (ws10) + `romanelli-audit` (ws11) | romanelli-studio.olesya00007.workers.dev | ✅ 031a6 (buttons → `/login?ws=romanelli-studio` AREA RISERVATA) | **preview@romanelli.test / Romanelli0826** (admin, ws10) + audit@lexflow.test (ws11) |
| 5 | Avv. Tommaso Ferro | `tommasoferro` (ws12) | none yet | — | ferro@lexflow.it (admin) |
| 6 | aLEXy (v0 heritage) | heritage CRM | coruscating-pegasus-c96710.netlify.app | ab54f/login — **DO NOT FIX** (future chatbots/AI-assistant workspace) | aLEXy@lexflow.it (admin) |

## Romanelli — current state (fixed & deployed 2026-08-31)
- **Login:** `preview@romanelli.test` / `Romanelli0826` → `https://web-production-031a6.up.railway.app/login?ws=romanelli-studio`
- Entry flow verified live: workers.dev → 🔐 AREA RISERVATA (nav + CRM FAB) → login → Romanelli Secure Workspace dashboard. `olesya00007@google.com` kept as Ole's own access (admin ws10).
- Site repo `Ole00007/Romanelli-studio` cleaned: stale nested `lexflow-crm/` (53MB, secret-bearing) removed from history (backup `/tmp/romanelli_lexflow_crm_bak`); Worker redeployed (Version `c15cde68`).

## Workspaces in prod Postgres (all present)
ws7 lexflow · ws8 avibeagency · ws9 pagliano · ws10 romanelli-studio · ws11 romanelli-audit · ws12 tommasoferro · ws13 romanelli-cl1 · ws14 romanelli-cl2

## Full tenant inventory (2026-09-02)

| # | Tenant | WS slug (id) | Parent | LP / platform | LP → backend | Admin login |
|---|--------|--------------|--------|---------------|--------------|-------------|
| 1 | LexFlow (own) | `lexflow` (ws7) | — | Netlify `poetic-kleicha-28d058` | ✅ 031a6 | olesya00007@yahoo.com (superadmin) |
| 2 | AVIBE Agency | `avibeagency` (ws8) | — | none yet | — | alegra_007@proton.me (admin) |
| 3 | Avv.Pagl | `pagliano` (ws9) | — | Netlify `verdant-crumble-021449` | ✅ 031a6 (button → `/kanban` — REPOINT PENDING: `/login?ws=pagliano`) | ms.okuneva@internet.ru (admin) |
| 4 | Romanelli Studio | `romanelli-studio` (ws10) | — | Cloudflare Worker `romanelli-studio.olesya00007.workers.dev` | ✅ 031a6 (`/login?ws=romanelli-studio`) | preview@romanelli.test / Romanelli0826 (admin) |
| 5 | Romanelli Audit | `romanelli-audit` (ws11) | — | (same Worker) | ✅ 031a6 | audit user (ws11) |
| 6 | Tommaso Ferro | `tommasoferro` (ws12) | — | none yet | — | ferro@lexflow.it (admin) |
| 7-16 | Romanelli Client 1..10 | `romanelli-cl1..cl10` | ws10 (client-of-client sub-tenants) | — (CRM-internal) | — | clN@romanelli.test (admin) — **LOCAL TEST ONLY, not yet in prod (prod has cl1,cl2 only)** |

## Email (Resend) — see [[LexFlow-Architecture-Email-Resend]]
- Code lives in the SAME repo/app (`crm/email_service.py`, `crm/notification_service.py`), env keys on `web-production-031a6`.
- **Verdict: deployed in same project, but `RESEND_API_KEY` is INVALID → emails NOT delivered** (log: "API key is invalid"). Fix pending: new key in Railway env.

## LOCAL TEST (operator test locally convention, 2026-09-02)
- Created cl1..cl10 sub-tenants under romanelli-studio on a throwaway sqlite DB.
- Full flow per cl: intake → contact → case → task(follow-up) → calendar event. **PASS 10/10** (contacts/kanban/calendar all reflect, workspace-scoped).
- Local instance: `http://localhost:8090` (login `cl1@romanelli.test` / `cl10826` … `cl10@romanelli.test` / `cl100826`).
- NOT deployed — awaiting Ole "go" to consider prod seeding of cl3..cl10.

## Open follow-ups
- [x] Main landing `poetic-kleicha-28d058` repointed ab54f → 031a6 (commit da19b36 deployed; verified 8 refs → 031a6, 0 ab54f).
- [x] Romanelli LP entry buttons → AREA RISERVATA (`/login?ws=romanelli-studio&back=<site>`).
- [x] SECURITY (2026-09-01, commit a639362): closed `/admin` + `/admin/matter` data leak (anonymous could see ALL clients' cases; now auth-required + scoped to visible workspaces). Fixed `/submit` 500 (workspace fallback hardcoded to non-existent ws#1 → now resolves auth→?ws→lexflow→first active). Fixed `GET /api/tasks` 500 (out-of-range duedate year 92026 → boot-time heal + strict date parse + safe to_dict). Fixed 'toast is not defined' on /tasks (added global toast() in base.html). Verified live: anon /admin → 302 /login; Romanelli /admin shows only ws10 cases; /submit creates case #40 in ws7; /api/tasks 200.
- [x] ISOLATION AUDIT (2026-09-01, backend-dev reviewer, read-only): checks 1-6+8 PASS — superadmin sees only ws7 + writes default ws7; Romanelli sees only ws10+cl1+cl2; anonymous → empty/401; /admin & /admin/matter scoped; attachment download scoped. ❗ FINDING (high): chatbot webhooks (crm/routes/webhooks.py) are UNAUTHENTICATED + UNSCOPED — HMAC signature optional (checked only if header present, hardcoded default secret 'your-webhook-secret-change-in-config'), so anonymous caller can POST case-status-changed/task-completed to ANY workspace + create events rows with workspace_id=NULL. Needs fix (require JWT+scope, or mandatory signature w/ real secret). Low: /status/<token> public by design (tracking links); /book falls back to Workspace.get(1) on bad slug.
- [ ] AVIBE / Ferro LPs: none yet — set URL when deployed.
- [ ] aLEXy (tenant 6) heritage LP: leave on ab54f for now; future chatbot/AI workspace.
- [ ] Calendar grid (Google-style Month/Week/Day) — MERGED + DEPLOYED (commit cc29045); live on /calendar for all workspaces.
- [ ] Google Calendar ↔ LexFlow sync (ws7): CODE DONE + DEPLOYED (commit 2fbe436, endpoint POST /api/admin/google-cal-sync). Isolated to 'lexflow' ws only (Romanelli untouched, verified). BLOCKED: needs GOOGLE_CALENDAR_API_KEY + GOOGLE_CALENDAR_ID env vars in Railway (CLI set was declined by Ole — needs his approval or manual dashboard set). CAVEAT: API key reads PUBLIC calendars only; private needs OAuth (client_secret + refresh token).
- [x] Task form: 'New Task' label + doc upload (dropZone) confirmed live (was user-side cache). Task + attachment creation verified live (201).
- [x] Intake: hidden ws field pins intake to logged-in user's workspace (Romanelli intake → ws10, appears in his Contacts/dashboard + doc attached). Commit 1869db3.
- [x] CALENDAR EVENT EMAIL NOTIFY (2026-09-03, commit `c81f8af`): creating a calendar event now auto-sends email to (1) client (resolved from linked contact via contactid → caseid fallback) and (2) superadmin/owner (NOTIFY_SUPERADMIN_EMAIL → ADMIN_EMAIL → first superadmin). Fires at event creation, not cron; non-fatal on mail failure. Verified locally (event 201 → both emails captured: Okuneva + Yahoo). Deployed, health 200.
- [x] WORKSPACE FEATURES (2026-09-03, commit `2919fae`): PATCH /api/workspace/<id> rename (superadmin/owner/parent-admin), POST /api/workspace/<id>/user add login, workspace_panel Rename+Add login buttons, client sub-tenant docs VIEW/UPLOAD but NOT DELETE (403; superadmin/parent only), return-site fallback romanelli-cl* → Romanelli worker. Verified 8/8 locally.
- [x] TRY DEMO BUG FIX (2026-09-03, overnight): LexFlow landing "Try Demo" was landing users in Romanelli workspace (cross-tenant confusion, NOT a data leak). Root cause: landing buttons pointed at CRM `/` and `/admin`, which auto-redirect logged-in users to `/dashboard` by the JWT stored in domain-scoped localStorage — if a Romanelli token exists in the browser, Try Demo showed Romanelli. Fixed BOTH sides: (1) landing `LexFlow-landing` commit `6632284` (branch fix-try-demo → origin/main, visual-redesign commits 52f1bc6/01e12aa kept on hold branch) — all 7 buttons now go to `/login?ws=lexflow&back=poetic-kleicha`; (2) CRM commits `4290a68` (base.html + crm/__init__.py) + `3a88e5f` (kanban.html) — siteMap gains 'lexflow' → poetic-kleicha so "Return to main website" links correctly. Verified live: landing 7× login?ws=lexflow; /kanban siteMap includes lexflow; /login?ws=lexflow = 200.
- [x] ADMIN API GUARD (2026-09-03, commit `8ae0cd8`): backend-dev audit found `/api/admin/users`, `/users/<id>`, `/users/<id>/role`, DELETE `/users/<id>`, `/stats` guarded only by role=='admin' with NO workspace filter — any tenant admin could enumerate all users + global stats across all workspaces. Now SUPERADMIN-only (UI never calls these; panel uses already-guarded /api/admin/workspaces + /reset-password). Also added id=returnSiteLink to base.html. Verified locally: romanelli admin → 403 on all 5, superadmin → 200, anon → 401. PASS. (Live re-check deferred — terminal command blocked while Ole asleep.)
- [x] INTAKE NOTIFY + ROADMAP ISOLATION (2026-09-03, commit `9bc7a23`): (1) intake `/api/intake/<slug>` + `/submit` now email BOTH owner AND client (auto-confirmation to submitter, non-fatal). (2) WhatsApp to owner via UltraMsg (best-effort, never crash; ADMIN_PHONE env; skipped with warning if unset). (3) `/kanban/roadmap` workspace-aware: superadmin/lexflow = agentic roadmap (docs JSON); OTHER firms = per-person staff board (`staff_board.html`: FirmTeamMember columns x cases by ownerid, scoped); anonymous → redirect (no leak — Romanelli could see T-001 before, now isolated). (4) Nav: Firm Team link (base + kanban), dynamic Roadmap/Staff Board label, Matters page + Add staff member + Staff Board. (5) Phone/WhatsApp labels on intake forms. Cross-audit: operator↔backend-dev GO (WhatsApp 20/20; zone PASS; roadmap leak closed verified live: romanelli roadmap 200 Staff Board, T-001 absent; anon 302). ⚠️ ENV GAP: Railway CLI broken → ULTRAMSG_INSTANCE_ID/ULTRAMSG_TOKEN/ADMIN_PHONE unverified on Railway; WhatsApp skipped until set.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-MultiTenant-Test-Setup]] · [[LexFlow-Workspace-UX-Overhaul]]
