---
title: "Carrozzeria 2DI leads app — LexFlow public-intake reuse analysis"
created: "2026-09-15"
tags: ["lexflow", "leads", "rate-limiting", "lead-intake", "reuse", "hindsight"]
status: "analysis-done"
---

# Carrozzeria 2DI leads app → LexFlow public-intake reuse analysis

> Reusable patterns extracted from the reference implementation at `<...>/For Obsidian SYNC/Carrozzeria/leads` (the Django "Carrozzeria 2DI" project). Sources: the `Carrozeria 2DI` notes vault (`<...>/For Obsidian SYNC/Carrozzeria 2DI/`) plus the `leads/` Django app. **Read-only analysis — nothing was modified in the Carrozzeria project.**

## What the leads app provides (verified)

### `models.py`
`LeadStatus` (NEW / IN_PROGRESS / CLOSED / SPAM); `Lead` (name, phone, email, message, branch FK, converted_order FK, consent_given, consent_text, created_at, status, source_page).

### `services.py`
`process_submission()` — validation → honeypot → reCAPTCHA (only when consent present) → rate limit → atomic save → attempt recording → notification, with notification failure caught and logged so a dead mailer never loses a lead. `hash_ip` (HMAC-SHA256 of SECRET_KEY + ip); `LeadSubmissionAttempt` DB journal with sliding 1-hour window; `RATE_LIMIT_MAX_SUBMISSIONS = 5`.

### `forms.py`, `recaptcha.py`, `views.py`, `urls.py`, `admin.py`
LeadForm (honeypot, consent_given, clean_phone, clean_honeypot); recaptcha (server-side siteverify, 5 s timeout, RECAPTCHA_ENABLED kill-switch, fails closed on network error, skipped when cookie-consent is absent); thank-you route (`grazie/`); LeadAdmin (list_display, list_filter, search_fields, readonly consent_text).

### `tests` (7 modules)
`test_submission`, `test_rate_limit`, `test_form_without_consent`, `test_email_failure`, `test_forms`, `test_models`, `test_console_email`.

## Job A — Hindsight sync status

- **Notes vault** `…/For Obsidian SYNC/Carrozzeria 2DI` → reconcile returned `HTTP 404 "Application not found"` for bank `avibe-hq`. Root cause: 13 top-level folders contain spaces (`00 Meta`, `01 Client`, `02 Delivery`, …); the API parses a doc ID's first path segment as an "application" name, and spaces cannot be resolved. The vault is read-only, so the folder names cannot be renamed. The API + token + bank are verified live via the smoothy profile's monthly reconciles on the space-free main AVibe vault.
- **Code folder** `…/For Obsidian SYNC/Carrozzeria` → **not synced** to HindSight: the reusable pattern lives in `.py` files, which the sync does not index (it ingests only `.md`). The folder's 12 `.md` files are verification/accessibility reports, not reusable references. Exclusions that would apply on a future sync: `.git`, `.venv`, `node_modules`, `static/`, `.env`, `.env.example`.

## Reuse mapping for `lexflow-crm` public-intake

1. **LeadSubmissionAttempt + HMAC-hashed IP rate limiting → ADOPT (adapt)** — highest value: replaces `flask-limiter` `memory://` (broken across gunicorn workers / Railway restarts). Concrete change: move the rate-limit journal to a shared DB model (`RateLimitAttempt` with `ip_hash` = HMAC-SHA256(SECRET_KEY, ip) and `created_at`), per-worker cleanup + 5-per-hour count in `crm/services/public_intake.py`; apply at the API layer, not worker-local memory.

2. **Explicit `consent_text` snapshot → ADOPT** — stronger GDPR evidence than a boolean + timestamp. Concrete change: add `consent_text` TextField to the intake/lead record; persist the exact text the visitor consented to.

3. **Honeypot + `clean_honeypot` → ADOPT (adapt)** — free bot filtering, no third-party dependency. Concrete change: hidden honeypot field in the form/validation; reject if populated before any DB write.

4. **Graceful reCAPTCHA → ADOPT (adapt)** — server-side siteverify, 5 s timeout, `RECAPTCHA_ENABLED` kill-switch, fails closed on network error, skipped when cookie-consent is absent. Concrete change: public-intake reCAPTCHA (or equivalent opaque challenge) behind an env flag; decide whether to keep it per-region (cookie-consent skip).

5. **Phone normalisation → ADAPT** — `clean_phone` strips spaces/parens/dots/dashes, validates 7–15 digits. Concrete change: apply the same normalisation to the intake phone; reject otherwise.

6. **`source_page` on every lead → ADOPT** — exact analogue of LexFlow's `source` (currently `String(20)` — Elisa `source='lexflow-website-elisa'` overflows it). Concrete change: `source` = `String(100)` on the intake model / contacts model.

7. **Service-layer separation → ADOPT** — `process_submission()` owns validation → honeypot → reCAPTCHA → rate limit → atomic save → attempt recording → notification, with notification failure caught + logged. Concrete change: extract `crm/services/public_intake.py` with this sequence; a dead mailer never loses a lead.

8. **Localised `thank_you` route + `LeadStatus.SPAM` → ADOPT** — first-class status + dedicated thank-you route. Concrete change: add `SPAM` status to the contact/lead model and a thank-you/status route (201 `{id, status}`).

9. **Test set → ADOPT** — the shape LexFlow's new endpoint should use. Concrete change: add `crm/tests/test_public_intake_*` mirroring these modules (incl. `test_form_without_consent`, `test_email_failure`, `test_rate_limit`).

## Top finding — multi-worker rate-limit storage

LexFlow's `flask-limiter` `memory://` does not work correctly across gunicorn workers or on Railway restarts. The Carrozzeria pattern (DB-backed, hashed-IP journal, atomic window cleanup) is the correct fix and should be implemented before delivery, independent of the reCAPTCHA / GDPR decisions above.

## Test plan (concrete)

Mirror the 7-module Carrozzeria test shape into `crm/tests/test_public_intake_*`; include `test_form_without_consent` (cookie-consent skip), `test_email_failure` (notification caught, lead still saved), `test_rate_limit` (5/hour per hashed IP), and `test_submission` under a locmem backend, plus a live-mailing test variant.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Public-Intake-Contract-2026-09-15]]
