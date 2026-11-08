---
title: LexFlow Public Intake Endpoint — Decisions 2026-11-06
created: 2026-11-06
tags: [lexflow, crm, api, cors, decision]
project: LexFlow
home: 01-Projects/LexFlow
status: active
---

# LexFlow Public Intake Endpoint — Decisions (2026-11-06)

Closes the decision gap that kept Kanban `t_d6065167` (and its duplicates `t_85d62411`, `t_8c6d4642`)
open since 2026-09-13. Owner: `smoothy_op_dir` (operator-installer, orchestrator).

## Measured state today (2026-11-06, 20:57 CET)

| Probe on `https://web-production-031a6.up.railway.app` | Result |
|---|---|
| `/` `/health` `/api/health` `/login` `/submit` | **404** `{"status":"error","code":404,"message":"Application not found"}`, `x-railway-fallback: true` |
| `POST /api/public/intake` | 404 (route never existed) |

Prod is still down — same Railway-edge signature as 2026-09-26, tracked as P0 on Kanban
`t_9f758266` (needs Ole's Railway access). **No live verification of any endpoint is possible
until that is fixed.**

Repo facts (`/Users/olesiarasing/projects/lexflow/lexflow-crm` @ `lexflow_hermes_v1`):
- `grep -rn "api/public" --include=*.py` → 0 hits. Endpoint never implemented on any branch except `legacy-recovered/main`.
- `aLEXy` naming: `templates/index.html` + `templates/status.html` already renamed (commit `a65a723`);
  **`static/mockup.html` still has 5 occurrences** (lines 6, 764, 779, 876, 886). No `.py` occurrence.
- CORS already wired via `flask_cors` in `crm/__init__.py:215` with `CORS_ORIGINS` from `crm/config.py:36`
  (`verdant-crumble-021449`, `lexflow-site.pages.dev`, localhost 3000/5000-5003). `poetic-kleicha-28d058` missing.
- `flask-limiter` already installed; `get_remote_address` key, no `ProxyFix` — behind Railway that would bucket
  every visitor together, so `ProxyFix(x_for=1)` is part of the fix.

## Decisions taken (orchestrator-owned, no longer waiting on Ole)

1. **Path** `POST /api/public/intake` — matches the published contract in
   `/Users/olesiarasing/projects/lexflow/lexflow-website/.well-known/openapi.yaml`; the site already reads
   one config value, so the path is fixed.
2. **Contact-only in v1** (contract says "Contact created"). Case creation stays an open Ole decision.
3. **Mapping**: `name`→`fullname`, `source`=`web`, `status`/`lifecycle_stage`=`lead`,
   `consent_privacy`→`gdpr_consent`+`gdpr_consent_ts`, `practice_area`/`lang`/`consent_marketing`→`notes` text +
   JSON `tags` (there is no column for them; no migration in v1).
4. **Workspace routing**: body `workspace` slug only if in `PUBLIC_INTAKE_ALLOWED_SLUGS`
   (`lexflow,pagliano,romanelli-studio`), else `PUBLIC_INTAKE_WORKSPACE_SLUG` (default `lexflow`), else first active
   workspace. Never a hardcoded id (prod ids start at 7 — an FK violation already happened once).
5. **Rate limit** `5/min; 30/hour` per real client IP, JSON 429. **CORS** restricted to `/api/public/*` with
   POST+OPTIONS, no credentials; `/api/*` not widened.
6. **Dedupe**: same email in the same workspace → append to the existing contact (`status: existing`), never a
   duplicate row.

## Fan-out

- `t_cc5e446d` → `backend-dev`: implement + pytest + real local smoke on port 5058, worktree
  `/Users/olesiarasing/projects/lexflow/lexflow-crm-wt-public-intake`, branch `feat/public-intake`.
- `t_23b03b7e` → `smoothy_op_dir`: independent cross-audit + smoke on port 5059 (CROSS-AUDIT rule).
- **Deploy gate stays closed**: any push to `lexflow_hermes_v1` needs Ole's explicit per-push authorisation, and
  prod must be restored first (`t_9f758266`).

## Links

- Parent: [[LexFlow-Project-Status]]
- Related: [[LexFlow-Public-Intake-Contract-2026-09-15]]
- Related: [[LexFlow-CRM-Where-We-Stand-2026-10-10]]
