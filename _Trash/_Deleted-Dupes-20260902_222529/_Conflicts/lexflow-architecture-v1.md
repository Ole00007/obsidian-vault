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
