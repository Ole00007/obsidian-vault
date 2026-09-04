---
title: LexFlow — Architecture: Email notifications (Resend) fact-check
created: 2026-09-02
updated: 2026-09-02
tags: [lexflow, crm, architecture, email, resend, notifications]
status: CURRENT ✅
---

# LexFlow — Email notifications (Resend) — integration fact-check

> Fact-checked 2026-09-02 (operator-installer). Verdict: **integration IS deployed inside the same
> Railway project** (`perceptive-achievement` → service `web` → `web-production-031a6`), wired into the
> same Flask app — but the **RESEND_API_KEY currently in Railway env is INVALID**, so no email is
> actually delivered today. It is NOT a separate/hanging Railway project, and NOT "Resend-only".

## Where the code lives (all inside the CRM repo)

| Artifact | Path | Role |
|---|---|---|
| Email service | `crm/email_service.py` | `send_email()`, `send_booking_notification()` via Resend |
| Notification service | `crm/notification_service.py` | `send_email()` + `send_whatsapp()` (UltraMsg) + combined notify |
| Resend dep | `requirements.txt` → `resend>=2.0.0` | installed at deploy |
| Env keys (Railway prod) | `RESEND_API_KEY`, `EMAIL_FROM`, `EMAIL_FROM_NAME`, `ADMIN_EMAIL` | set on `web-production-031a6` |

## Call sites (who sends email)

| Route | File:line | When |
|---|---|---|
| `POST /submit` (intake form) | `crm/routes/views.py:259` | new intake → ADMIN_EMAIL ("New intake: …") |
| `POST /api/intake/<slug>` (LP intake) | `crm/routes/views.py:621` | new intake → workspace owner ("New intake from <ws>") |
| `POST /api/admin/reset-password` | `crm/routes/views.py:519` | superadmin resets user password → target email |
| Change email / password | `crm/routes/auth.py:96-112` | user changes own login email/password → old email |
| Booking notification | `crm/email_service.py:48` | client + owner on appointment booking |

## Live evidence (Railway logs, 2026-09-02)

```
WARNING:crm.notification_service:Email failed to olesya00007@yahoo.com: API key is invalid
```

Meaning: code IS executing the send path, but Google/Resend rejects the configured `RESEND_API_KEY`.
No successful send observed in recent logs.

## Flow diagram (current state)

```
[Client landing page]  ──POST /api/intake/<slug>──▶  [Flask app: web-production-031a6]
                                                          │  (perceptive-achievement / Railway)
[CRM /submit form]     ──POST /submit──▶                   │
                                                          ▼
                                              create Contact + Case (ws X)
                                                          │
                                                          ▼
                                    notification_service.send_email()
                                                          │
                                                          ├─ RESEND_API_KEY  ← ⚠️ INVALID in env
                                                          │
                                                          ▼
                                                   [Resend API]
                                                          │
                                                          ▼
                                            ✗ "API key is invalid" (log)
                                            emails NOT delivered today
```

## Fix to unblock (pending Ole approval)
1. Regenerate/verify the Resend API key (Resend dashboard → API Keys) — the old one is invalid/revoked.
2. Set the NEW key in Railway env `RESEND_API_KEY` (web service, production) → auto-redeploy.
3. Verify a real intake triggers a delivered email (check Resend dashboard "Emails" tab + app logs).

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Workspace-2026-08-31-Inventory]] · [[LexFlow-MultiTenant-Test-Setup]]
