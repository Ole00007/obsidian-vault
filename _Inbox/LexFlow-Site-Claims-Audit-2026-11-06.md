---
tags: [lexflow, audit, claims, compliance, security]
project: lexflow
home: 01-Projects/LexFlow
created: 2026-11-06
---

# LexFlow — site capability claims vs the real CRM (verification audit, report only)

Task: kanban `t_8c6d4642` (from frontend-developer-lovable_react, on Ole's instruction).
No site file, no CRM file was edited. Everything below was read from code and probed over HTTP.

## Evidence base / repo paths

- Marketing site (source, **NOT deployed**): `/Users/olesiarasing/projects/lexflow/lexflow-website`
- Live marketing site (older build, what customers actually see): `https://poetic-kleicha-28d058.netlify.app/`
- CRM deployed baseline: `/Users/olesiarasing/projects/lexflow/lexflow-crm` @ `ddec0aa` (branch `lexflow_hermes_v1`, prod origin). Newer code commits (`215bcc2`, 2026-10-29) are local only.
- Production CRM: `https://web-production-031a6.up.railway.app` → **404 "Application not found"** (Railway edge fallback), day 3 of the 2026-11-04 regression.

## Verdicts

### A. Integrations and count
- A1 "Email & messenger automatic notifications" — PARTIALLY TRUE. Automatic email fires on intake, calendar-event creation, attachment upload, password reset; WhatsApp via UltraMsg. Delivery is credential-conditional (SMTP_*/RESEND_API_KEY; Resend sandbox sender cannot reach arbitrary client addresses).
- A2 "More than 10 integrations" — FALSE. ~6 surfaces exist, none customer-selectable in-product.
- A3/A4 "+5 / +10 more integrations at your request/choice" — UNSUPPORTED BY PRODUCT (service promise, no mechanism, no config surface).
- A5 Inconsistent arithmetic: 10+5=15+ (tier2) vs 20+10=30+ (tier3) vs "20+" elsewhere. Real today ≈ 6.
- A6 Real list: outbound email (Resend/SMTP); outbound WhatsApp (UltraMsg); Telegram bot send + deep links (flag-gated, default OFF); Google Calendar OAuth pull+push (superadmin, `lexflow` workspace only); inbound HMAC webhook; public intake API + Elisa LLM agent (opt-in). No Slack/Drive/Dropbox/Notion/Zapier/S3.

### B. Calendar / notifications
- B1 Google Calendar sync — PARTIALLY TRUE. Real bidirectional code, but manual superadmin trigger, no cron, single-tenant (`lexflow`) scope; deadlines are not pushed (CalendarEvent rows only).
- B2 Automatic — PARTIALLY. Event/intake emails are automatic; task notifications are DB rows only ("mock-first ... no SMTP/webhook/push dispatch yet"); Telegram/WhatsApp buttons behind `NOTIFY_BUTTONS_ENABLED` (default false). No scheduler anywhere.
- B3 In-app — notifications exist as rows; no reminders are generated (no cron).

### C. Billing / payments
- C1 "automate ... billing" — FALSE. No invoice/payment/billing code at all.
- C2 "Coming soon: time and expense tracking, payments" — CORRECT (none live). The wrong direction is elsewhere: live site calls **Workflow Automation** "coming soon" while tasks/kanban/gantt are live, and pricing sells Time & Expense + Billing & Invoicing as Enterprise features that do not exist.

### D. Security / compliance
- D1 "Zero-Knowledge Document Security" — FALSE. No crypto code; uploads land plaintext in a local `uploads/` dir; DB metadata in clear. Not defensible.
- D2 GDPR — PARTIAL. Consent capture, privacy page, tenant isolation, no trackers; missing DSAR export/erasure, retention enforcement, DPA records, verified EU hosting region.
- D3 ISO "working towards" — ACCURATE and not understated (no certificate evidence in repo). Live site still asserts the certificates as held.
- D4 Encryption — neither app-level at rest nor end-to-end. TLS in transit only. Also undermines "bank-grade 256-bit encryption".
- D5 "Token-secured link" — FALSE. `/status/<token>` casts to int and reads the matter by id; `Case` has no token column; `submit` generates a token then discards it. Sequential matter IDs expose client name, practice area and description to anyone. No account is required (that part is true).

### E. Core product
- E1 TRUE with qualifier — matters/activities/deadlines/intake/client status page all exist; there is no "approved update" workflow and the client page hardcodes documents/timeline to empty.
- E2 PARTIAL — matter appears in dashboard/cases immediately; dashboard is workspace-scoped, not role-based; no auto-triage or auto-assignment.
- E3 PARTIAL — no login needed, status reflects on reload (no push); documents/timeline never render; link is a raw matter id, not a unique token.
- E4 "AI-driven metadata enrichment ... automatically" — FALSE. Attachments store filename/mime/size only; extraction+extractive summary happen on demand inside the Elisa agent; LLM summaries need opt-in env.
- E5 "Role-Based Dashboards for every seat" — PARTIAL. Roles exist (user.role, firm-team roles, task roles) and tenant isolation is real, but there is one dashboard for every seat.
- E6 per-area workflows — `practice4_p` court date automation FALSE; `practice7_p` multi-jurisdiction document automation FALSE; `pa3_wf` conflict check FALSE (status label only) and "restricted to assigned team" FALSE (workspace-wide visibility); hearing dates tracked PARTIAL, no reminders; `pa5_wf` document checklist FALSE (agent calls a `/api/checklist/next-actions` endpoint that does not exist); `pa6_wf` filing deadlines PARTIAL (deadline types exist, no reminders); `pa11_wf` chronology FALSE.

### F. Pilot metrics
- F1 Disclaimer exists in the repo build; the live build has no pilot section and instead publishes testimonials as real ("Feedback collected during beta testing ... Real names, written consent obtained") plus a live "Studio Legale X" placeholder.
- F2 Provenance unverifiable / effectively synthetic-adjacent: no analytics, no time tracking, no onboarding timing anywhere in the CRM, so none of the four indicators is measurable. `/admin/load-demo` is not in the current CRM (only `backups/app.py..bak`, `templates-legacy-bak`). Disclaimer is necessary but not sufficient for publication; on the live site it is absent entirely.

### G. Else
- Claims the product does not do: zero-knowledge, token-secured link, AI metadata enrichment, per-role dashboards, 7 of 8 per-area automations, 20+ integrations, cloud storage (it is a local disk path), documents on the client page. Live build adds ISO-held and real-testimonial claims.
- What the product does and the site understates: automatic email/WhatsApp/Telegram notifications, bidirectional Google Calendar sync, HMAC-secured inbound webhook, the Elisa AI assistant with an approval gate, kanban + Gantt + progress diagrams, per-task role assignment, multi-tenant workspaces with a superadmin console, Italian legal deadline vocabulary.
- Deployment gap: the corrected pages 404 on the live host — none of the claims-register corrections ever shipped. The live site's Sign in button points at a CRM that returns 404 today.

## Recommended correction order (not applied)
1. Hard-blockers: D1 (zero-knowledge), D5 (token link), E4 (AI enrichment), A2/A5 (integration count), live-build ISO/testimonial claims.
2. Rewrite, don't delete, the understatements: notifications, calendar sync, workflow automation, Elisa.
3. Either measure the pilot numbers or label them illustrative; never restore the old "real names, written consent" line.
4. Ship the repo build before any further copy work — the site currently being served is a different, older artifact.

## Links
[[LexFlow]] [[LexFlow_Claims_Register]] [[AGENT_RULES]]
