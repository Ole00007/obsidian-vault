# LexFlow Multi-Tenant Architecture (as of 2026-09-01)

## Diagram

```
┌────────────────────┐   ┌──────────────────────────────┐   ┌────────────────────┐
│ LexFlow LP          │   │ Romanelli LP                  │   │ Pagliano LP         │
│ poetic-kleicha       │   │ romanelli-studio               │   │ verdant-crumble      │
│ (Netlify, static)    │   │ .olesya00007.workers.dev       │   │ (Netlify, static)   │
│                      │   │ (Cloudflare Workers, static)   │   │                     │
└──────────┬───────────┘   └──────────────┬─────────────────┘   └──────────┬──────────┘
           │ /login?ws=lexflow            │ /login?ws=romanelli-studio     │ /login?ws=pagliano
           ▼                              ▼                                ▼
                    ┌──────────────────────────────────────────┐
                    │        ONE Flask app (Railway)             │
                    │        Jinja2 templates + vanilla JS       │
                    │        No React, no per-tenant code branch │
                    └───────────────────┬────────────────────────┘
                                        │ JWT (localStorage, per-browser/device)
                                        ▼
                    ┌──────────────────────────────────────────┐
                    │        ONE Postgres DB (Railway)           │
                    │        workspace_id column per row         │
                    │        app-level workspace_filter() only    │
                    │        (native RLS NOT enabled — see D12)   │
                    └──────────────────────────────────────────┘
```

## Key facts

| Layer | Hosting | Type | Notes |
|---|---|---|---|
| LexFlow LP | Netlify (`poetic-kleicha`) | Static | Tenant 1, ws7 |
| Romanelli LP | Cloudflare Workers (`romanelli-studio.olesya00007.workers.dev`) | Static | Tenant 4, ws10/ws11 |
| Pagliano LP | Netlify (`verdant-crumble`) | Static | Tenant 3, ws9 |
| Backend | Railway | Flask, single instance | Shared by all tenants |
| Database | Railway | Postgres, single instance | Shared, row-isolated via `workspace_id` |

## Isolation model

- **Code/templates:** 100% shared across all tenants — one deploy affects everyone.
- **Data:** separated by `workspace_id` column + app-level `workspace_filter()`. No native Postgres RLS (deliberate decision, D12/D14 — row-level filtering, not schema-per-tenant or physical DB-per-tenant).
- **Branding:** favicon + "Secure Workspace" banner rendered per `?ws=` param resolved at login.
- **Session:** JWT in `localStorage`, scoped per physical browser/device — no cross-device leakage via client storage.

## Open risk items (unresolved as of this doc)

1. **CDN/edge cache on authenticated API responses** — unverified whether Netlify/Cloudflare/Railway edge caches `/api/*` responses. Must confirm `Cache-Control: private, no-store` on all authenticated endpoints.
2. **Uploads broken** — both new-intake form and new-task form failing on document upload; root cause not yet confirmed (ephemeral disk vs frontend/backend field mismatch).
3. **Native RLS** — not built. App-level filter only. Backend dev has cloned reference pattern (untested). Planned as non-blocking hardening track, one table first, pgTAP-tested in CI before merge.
4. **LexFlow LP routing bug** — "LexFlow CRM" button currently routes to `/kanban` directly instead of `/login?ws=lexflow`, allowing a stale token to auto-login as the wrong tenant. Fix held pending cache/CDN investigation (don't want to fix the wrong root cause first).

## Hard rule in effect

Render-before-merge gate: no visual/UX change merges or deploys without a local preview reviewed and explicitly approved first. See `hermes-render-control-rule.md`.

---

# Agentic-layer model routing — fleet-wide (Hermes, update 2026-11-16)

This appendix records the Hermes **agentic** layer (the flock building/operating LexFlow), distinct from the LexFlow web architecture above (LPs → Flask app → Postgres).

## Ports & local endpoints — ADR-style decision log
Values are recorded as dated decision records (value + status + owner + supersedes), **not bare constants** — a bare port number goes stale the moment it changes. Update the row in the same PR/commit as the change (§21 Doc-Sync on Merge; pattern: GitHub `architecture-decision-record` / AWS ADR metadata — owner, status, history preserved).

| ADR | Surface | Current value | Status (2026-11-16) | Owner | Supersedes |
|---|---|---|---|---|---|
| ADR-LXF-001 | LexFlow CRM demo (`/graph`) | `127.0.0.1:5057` | **live** (PID 63889, `/graph` 200, `/static/favicon.svg` 200; boot: `elisa_boot_5057.py` in backend-dev scratch, mtime 2026-11-16 15:05) | backend-dev | legacy doc claim `:5002` |
| ADR-LXF-002 | Hermes web dashboard | `127.0.0.1:9119` | live (PID 24389), launched `--open-profile smoothy_op_dir` | Smothy/Admy | — |
| ADR-LXF-003 | Landing preview (local only) | `127.0.0.1:8090` | live (LP main `55d5488`) | frontend | — |

## Model provider posture (post-2026-11-16 fix)
- **All 22 registered profiles + the root/default surface → `model.provider: nous`** (Nous Portal). The credential is SHARED/global by design: `~/.hermes/shared/nous_auth.json` (oauth_device_code, scope `inference:invoke`) + a `nous` entry in top-level `~/.hermes/auth.json`. Per-profile `auth.json` pools do NOT carry `nous` — that is normal; nous resolves from the shared store. Verified: `hermes -p <any> auth status nous` → `nous: logged in`.
- Default models preserved per profile (cheap tier: deepseek-v4-flash, gemini-3.5-flash, claude-haiku-4.5), all validated against the live Nous catalog. `agency-growth`'s dead pin (`poolside/laguna-s-2.1:free`) fixed → `deepseek/deepseek-v4-flash`. This follows the spirit of AGENT_RULES §12 (no hardcoded/broken model pins).
- **Dashboard** serves `http://127.0.0.1:9119`, launched with `--open-profile smoothy_op_dir`.

## Operator control-plane layer
- The Hermes host gateway (PID 67628) serves all profiles; dashboard is a separate surface on :9119. Both are distinct from the LexFlow Railway backend — do not conflate.
- Settings/config edits restricted to **Admy + Smothy** (AGENT_RULES §20).

## Links
- Parent: [[LexFlow-Platform-Plan-2026-10-24]]
- Related: [[LexFlow-Agent-Roster-and-Ecosystem]]
