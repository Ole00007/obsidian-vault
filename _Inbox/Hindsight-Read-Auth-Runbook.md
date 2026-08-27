---
title: Hindsight Read-Auth Runbook
created: 2026-08-26
tags: [hindsight, security, auth, railway, avibe-hq, runbook]
status: pending
---

# Hindsight Read-Auth Runbook — enable read protection on avibe-hq

> Status: **PENDING** — deferred until scaling (see `_Meta/cron-jobs/self-improvement-log.md` decision 2026-08-26).
> Owner: operator-installer (owns the Railway `graceful-presence` deployment).

## Why

Live probe (2026-08-26) confirmed these endpoints return data **without any auth**:

| Endpoint | No-auth status | Exposes |
|---|---|---|
| `/health` | 200 ✅ | health/DB status only (no data — benign) |
| `/v1/default/banks` | 200 ⚠️ | bank metadata: fact_count, document count, timestamps |
| `/v1/default/banks/avibe-hq/stats` | 200 ⚠️ | full graph stats: node/link counts, fact-type breakdown |
| `/v1/default/banks/avibe-hq/memories` | 405 | write route — **already** auth-protected (`HINDSIGHT_API_KEY`) |

**Severity:** LOW today (metadata/stats only, no note content). Becomes a real liability once the
bank holds client conversation data (Alena-Krot, Studio-Romanelli, AVibe clients). Deferred until scaling.

## What to change (when scaling)

### Server side — Railway service `avibe-hindsight` (project `graceful-presence`)

1. **Require auth on read routes.** Hindsight's API reads keys from `HINDSIGHT_API_KEY` (already set).
   The exact mechanism depends on the Hindsight server build (hindsight-all package). Options:
   - If the server supports an `requireAuth`/`auth_required` config → enable it so `/v1/default/banks*`
     and `/stats` reject requests without `Authorization: Bearer <HINDSIGHT_API_KEY>`.
   - If not natively supported → place a lightweight auth proxy (Cloudflare Access / nginx basic-auth /
     Railway TCP proxy) in front of the service.
2. **Verify** after the change:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" https://avibe-hindsight-production.up.railway.app/v1/default/banks
   # expect 401/403 (was 200)
   curl -s -H "Authorization: Bearer $HINDSIGHT_API_KEY" \
     https://avibe-hindsight-production.up.railway.app/v1/default/banks/avibe-hq/stats
   # expect 200 with key
   ```
3. **Confirm Hermes still works** after locking reads — every client passes the key:
   - Hermes profiles: `hindsight/config.json` → `api_key` (or `HINDSIGHT_API_KEY` env)
   - Obsidian plugin: URL + key + bank `avibe-hq`
   - Test one profile: `hermes -p operator-installer chat -q "recall something from avibe-hq"`

### Client side — add the key where reads originate (so locking doesn't break Hermes)

Every profile with `memory.provider: hindsight` needs the key available:
- `~/.hermes/profiles/<name>/hindsight/config.json` → add `"api_key": "<HINDSIGHT_API_KEY>"`
- OR the profile `.env` → `HINDSIGHT_API_KEY=...`

Currently only `operator-installer` and `memory-curator` use hindsight; the profile-local
`hindsight/config.json` (added 2026-08-26, `bank_id: avibe-hq`) is the place to add `api_key`.

## Safety

- **Do NOT regenerate `HINDSIGHT_API_KEY`** — it's a pre-existing secret (AGENT_RULES Rule 4). Reuse.
- **Never commit the key.** Railway Service Variables only.
- Locking reads is reversible: remove the proxy/flag and reads return to open.
- This is a **tier-2 infra change** → requires Ole's explicit approval before executing.

## Decision log

- 2026-08-26 — Ole deferred execution until scaling (operator-installer busy with urgent job). Runbook written for when we scale. Reminder set to flag at that point.
