---
title: LexFlow Public Intake — Cross-Audit 2026-11-06
created: 2026-11-06
tags: [lexflow, cross-audit, api, public-intake, cors, review]
status: active
project: lexflow
home: 01-Projects/LexFlow
---

# LexFlow Public Intake — Cross-Audit (2026-11-06)

Independent review + independent local smoke of the public lead endpoint `POST /api/public/intake`, produced by backend-dev on card `t_cc5e446d`. Audit card `t_23b03b7e`. **Verdict: PASS — no blocking defects.**

## What was audited

| | |
|---|---|
| Branch | `feat/public-intake` @ `25f2d45` |
| Base | `lexflow_hermes_v1` @ `55b644b` |
| Worktree | `/Users/olesiarasing/projects/lexflow/lexflow-crm-wt-public-intake` |
| Diff scope | 5 files, +300/-6: `crm/routes/public.py` (new), `crm/__init__.py`, `crm/config.py`, `static/mockup.html`, `tests/test_public_intake.py` (new) |
| Smoke port | **5059** (implementer used 5058; `port-5057` lock untouched) |
| Contract | `/Users/olesiarasing/projects/lexflow/lexflow-website/.well-known/openapi.yaml` |

Nothing pushed, nothing deployed. Worktree left clean and unmodified — the reviewer edited no implementation file.

## Result per checklist item

1. **Scope** — exactly the 5 expected files, nothing unrelated.
2. **Route** — `/api/public/intake` accepts `OPTIONS, POST` only (no GET → write-only). No `@jwt_required`. 201 `{"id":"…","status":"created"}`, 400 `{"error":"validation failed","fields":[…]}` + `{"error":"unknown workspace"}`, 429 `{"error":"rate limited"}` — all within the contract.
3. **Consent & dedupe** — `consent_privacy` enforced; `gdpr_consent=1` + `gdpr_consent_ts` on 13/13 smoke rows. Repeat email in the same workspace returns `status:"existing"` on the **same id**, notes appended, no duplicate row. Same email in another workspace correctly creates a separate contact.
4. **Workspace resolution** — no literal id anywhere. Unknown slug → 400. A **real but unlisted** slug (`romanelli-cl1`) also → 400, so the allowlist is genuinely enforced. Explicit slugs route correctly (pagliano→ws2, romanelli-studio→ws3), absent → default slug.
5. **CORS** — ACAO for the site origin, poetic Netlify and localhost dev; `Max-Age 600`; **no** `Access-Control-Allow-Credentials`; arbitrary origin gets no ACAO. Resolved origin list contains no `*`.
6. **Rate limiting** — `ProxyFix(x_for=1)` active at runtime; 6 posts from one IP → `201×5, 429`, JSON body; a different IP is unaffected.
7. **`aLEXy` purge** — `grep -rni alexy templates/ static/` → zero hits; all 5 occurrences in `mockup.html` replaced with "LexFlow".
8. **Tests re-run independently** — 14/14 new tests pass; full suite 1 failed / 69 passed. The failure (`test_agent.py::test_elisa_chat_tasks_and_agenda`) reproduces identically on base `55b644b` → **pre-existing**.
9. **Smoke** — 201 / 400 / 429 / preflight allowed+denied / 405 on GET / malformed JSON / oversized field / SQLi+XSS payload stored literally with the table intact.
10. **No secrets, no PII** — no credentials in the new code (the `config.py` secret-shaped hits are pre-existing lines); all fixture emails synthetic `@example.com`; the route returns only `id` + `status`.

## Handoff gap closed

The implementer flagged that activity logging was **unverified** (their smoke queried the wrong table name). I verified it: the table is `activity_log` (singular), 14 rows were written, and `workspace_id` is **correct per tenant** (ws 2, 1, 3 — not silently defaulted to 1). A repeat submission logs `action='updated'` against the same contact id.

## Findings (none blocking)

1. **Railway `CORS_ORIGINS` overrides the config default.** If that env var is set in production, the site and poetic-Netlify origins must be present in it or the live site is CORS-blocked while localhost passes. *Must be checked before any future deploy.*
2. **CORS is not a write boundary.** A non-browser client can POST from anywhere — proven with a raw curl that created a contact. Guards are the honeypot + 5/min, 30/hr per IP. The default allowlist includes two real client tenants (`pagliano`, `romanelli-studio`), so the public internet can write into them. **Ole's decision required.**
3. **Consent not refreshed on repeat submission** — `gdpr_consent` / `gdpr_consent_ts` are set only on create; an existing contact who re-consents keeps a stale `False`. Follow-up card `t_3da3e3ab`.
4. **`ProxyFix` trust is app-wide and unconditional** — safe behind Railway's single hop; if the app is ever exposed without it, `X-Forwarded-For` rotation resets a client's bucket (demonstrated on localhost).
5. **Cosmetic contract drift** — the honeypot returns `{"status":"accepted"}`, a third shape not in the OpenAPI contract. Bots only.

Noted, not a finding: anonymous `GET /api/contacts` returns 200 with `[]` — `@jwt_required(optional=True)` there is pre-existing on base and leaks no data.

## Deploy status

**Gate CLOSED.** Nothing pushed or deployed; prod stays down per `t_9f758266` (`web-production-031a6` → Railway edge 404), so the endpoint is unreachable by visitors regardless. Before any deploy: satisfy finding 1, take the finding 2 decision, and note `lexflow_hermes_v1` remains ~13 commits ahead of origin and unpushed.

## Links

- Parent: [[LexFlow-Roadmap]]
- Related: [[LexFlow-Web-Site-Agent-Surface-2026-09-15]]
- Related: [[LexFlow-Cross-Feature-Consistency-Audit]]
