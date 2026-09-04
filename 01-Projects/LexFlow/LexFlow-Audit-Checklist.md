---
title: LexFlow — Audit Checklist (audit know-how)
created: 2026-09-03
updated: 2026-09-03
tags: [lexflow, audit, security, multitenant, checklist]
status: CURRENT ✅
---

# LexFlow — Audit Checklist (audit know-how)

> **RULE (Ole, 2026-09-03):** When a bug/fix is done for ONE tenant and we did NOT work on that
> function/amendment/debug for OTHER tenants, IMMEDIATELY run a brief audit of the SAME bug on the
> other tenants and fix if necessary. Do not make Ole repeat herself per-tenant (imagine 100 tenants).
>
> **CROSS-AUDIT RULE (Ole, 2026-09-03):** BEFORE every local test AND before any deploy,
> operator-installer and backend_dev cross-audit each other's code changes — operator-installer
> reviews backend_dev's code, backend_dev reviews operator-installer's code. Report to user,
> THEN deploy. **No exceptions.**
>
> **Maintenance rule:** every time the audit finds a NEW bug pattern, ADD it to this checklist so
> future audits cover it automatically. Keep comments terse so re-reading is fast.

## How to run (fast path)
1. For the just-fixed feature, grep the codebase for the same pattern across ALL tenant branches/pages.
2. Hit the LIVE endpoint(s) for 2–3 representative tenants (lexflow, romanelli, pagliano) + anon + superadmin.
3. Verify: (a) tenant isolation (each sees own rows only), (b) entry points pin ?ws=, (c) return-to-site maps, (d) admin/API guards.
4. Fix what fails; log new findings here.

## Checklist

### A. Entry / navigation
- [ ] Landing "Try Demo / Open app / Admin" buttons → `/login?ws=<tenant>` + `back=<site>` (NOT bare `/` or `/admin`)
- [ ] `/login?ws=<slug>` returns 200 for every active tenant slug
- [ ] Return-to-site link: `siteMap` (base.html AND kanban.html) has the tenant → correct LP; server `site_map` too
- [ ] After logout → empty state (no stale JWT branding); re-login with ANY tenant creds → that tenant only
- [ ] No bare-origin hrefs left in the LP (grep `href="https://web-production-031a6.up.railway.app/"` and `/admin`)

### B. Tenant isolation (data)
- [ ] `/api/cases|tasks|contacts|calendar` for tenant admin → only own workspace ids (parent sees own + subs)
- [ ] Superadmin writes default to lexflow; no hardcoded ws ids
- [ ] Anonymous → 401 or empty lists (never full-table)
- [ ] `/admin` + `/admin/matter` → scoped shell; foreign matter → 404
- [ ] Attachment download scoped by `get_visible_workspace_ids`
- [ ] `/status/<token>` public by design — confirm only own-case data

### C. Admin/API guards
- [ ] CROSS-AUDIT gate (2026-09-03): before ANY local test / deploy — operator-installer ↔ backend_dev mutual code review completed + reported to user (no exceptions)
- [ ] Cross-tenant admin endpoints (`/api/admin/users`, `/users/<id>`, `/role`, DELETE, `/stats`) → SUPERADMIN only (2026-09-03 fix, commit 8ae0cd8)
- [ ] Webhooks: mandatory HMAC signature w/ real secret, scoped writes, no orphan NULL workspace rows (2026-09-01 fix, commit a2781f5)
- [ ] No route lists/mutates WITHOUT `@jwt_required` + workspace scoping
- [ ] `/book` fallback — not `Workspace.get(1)` (latent, views.py:294 — TODO)

### D. Shared-origin session
- [ ] localStorage JWT key is domain-scoped; tenant switch = different browser/profile or logout+relogin (by design)
- [ ] OPTIONAL defense-in-depth (TODO): workspace-mismatch guard on ?ws=; per-tenant JWT key namespace

### E. Known bug patterns (append as discovered)
- 2026-09-01: webhooks unauthenticated + NULL workspace_id → FIXED a2781f5
- 2026-09-02: landing "Try Demo" → bare origin → stale JWT → wrong tenant branding → FIXED 6632284/4290a68/3a88e5f
- 2026-09-03: /api/admin/* cross-tenant enumeration (any tenant admin) → FIXED 8ae0cd8
- 2026-09-03: kanban.html has its OWN siteMap copy (not inherited from base.html) — always patch both

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Workspace-2026-08-31-Inventory]] · [[LexFlow-Architecture-Email-Resend]]
