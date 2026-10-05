---
title: "Canva × Fronty × Hermes — Package Intake & D1-15 Fix"
created: 2026-10-05
tags: [hermes, mcp, obsidian-mcp, canva, fronty, ops]
status: active
---

# Canva × Fronty × Hermes — Package Intake & D1-15 Fix

## What the package is

A Canva × Fronty × Hermes integration delivered 2026-10-03 as `Canva_Fronty_Package`:

- `Canva_Fronty_Tracker.csv` — 25 tasks across 2 days (D1-01 … D2-10)
- `Canva_Templates.csv` — 17 templates, 6 verticals
- `Canva_Field_Contract.csv` — 14 fields every template must receive
- `Smoothy_Final_Prompt.md` — operator-installer's operating instructions
- `Fronty_Prompt.md` — Fronty agent's instructions

**Source path:** `/Users/olesiarasing/Downloads/Canva_Fronty_Package/`
**Goal:** set up Canva MCP access so the Fronty agent can create designs from templates.

## D1-15 — FIXED (root cause deeper than the brief)

The brief described D1-15 as "two config type errors". The types were real, but fixing them
exposed the actual blocker underneath.

### Three defects, all in one MCP entry

| # | Defect | Before | After |
|---|--------|--------|-------|
| 1 | `args` was a quoted **string**, not a YAML list | `'["obsidian-mcp", "…"]'` | proper YAML list |
| 2 | Vault path **did not exist** | `~/Obsidian/HERMES` | `~/Obsidian` |
| 3 | Stale npm cache version won | `obsidian-mcp` → v1.0.6 | `obsidian-mcp@2.0.1` |

### Root cause of the root cause

The npm cache (`~/.npm/_npx/`) held **two** copies of `obsidian-mcp`:

- index **20** → `71f996a9bd0fcec9` → `obsidian-mcp ^1.0.6` (stale)
- index **24** → `1eddcb5200a425a4` → `obsidian-mcp ^2.0.1` (current)

Hermes' npx-cache optimisation (`tools/mcp_tool_config.py::_npx_cached_bin`, ~line 236)
iterates `os.listdir` and takes the **first** entry declaring the package. That was the **v1**
copy. v1 has a different CLI contract: it treats the first positional argument as a **vault
path**, so `serve --vault …` produced:

```
Error: Vault directory does not exist: serve
```

Recorded **4,852 times** in `errors.log` on 2026-10-05 alone — the gateway blocker.

### Verification

```
hermes -p smoothy_op_dir mcp test obsidian-mcp
  ✓ Connected (2311ms)
  ✓ Tools discovered: 12
```

Backup: `config.yaml.bak-d1-15-20261005-184501`

## Corrections to the brief (evidence over instruction)

Two claims in the brief did **not** survive checking:

1. **`PGCONNECT_TIMEOUT` is not in this profile.** `smoothy_op_dir` has no `postgres` MCP
   entry at all (only `composio` + `obsidian-mcp`), and zero postgres errors today. The
   unquoted integer `10` lives in **18 other profiles**; the default config is already
   correctly quoted (`'10'`). It is **latent**, not active: no gateway is running, and
   `@modelcontextprotocol/server-postgres@0.6.2` has no connection string configured, so it
   cannot work regardless.
2. **"Confirm `hermes gateway start` works" needs a service first.** No hermes launchd plist
   exists on this machine (`~/Library/LaunchAgents/` has none), so `gateway start` has
   nothing to start — it requires `hermes gateway install`, a system change needing owner
   approval.

## D1-05 — ANSWERED (read-only)

The `canva` MCP entry already exists and must **not** be duplicated:

- Lives in `/Users/olesiarasing/.hermes/config.yaml` line **802**
  (`url: https://mcp.canva.com/mcp`, `enabled: true`)
- Duplicated into **18** profile configs — **not** in `smoothy_op_dir`
- Login method: Hermes **OAuth** via `hermes mcp login canva`
  (browser PKCE, or `--flow device` for RFC 8628)

Live probe:

```
POST https://mcp.canva.com/mcp → HTTP 401
www-authenticate: Bearer realm="OAuth",
  resource_metadata="https://mcp.canva.com/.well-known/oauth-protected-resource/mcp"
```

Both `.well-known` discovery documents return **200**. So the 401 means *not authorised
yet* — the URL is correct, and D1-07 (owner consent) is the fix, not a new entry.

## Owner tasks outstanding

| ID | Owner must do | Gate for |
|----|---------------|----------|
| D1-01 | Sign in at canva.com/developers (Olesya00007@gmail.com) | D1-09 |
| D1-02 | Create private app "Fronty Hermes Canva Connector" | D1-03 |
| D1-03 | Put Client ID + secret into `.env` (names only) | D1-04 |
| D1-07 | Click through the Canva consent screen | D1-08 |

**Sequencing decision (Ole, 2026-10-05):** fix the aLEXy Google-API leak **before**
registering on Canva. A live key in a public repo is actively exploitable; Canva can wait.

## Links

- Parent: [[Hermes-Setup-and-MCP]]
- Related: [[aLEXy]]
- See also: [[Agent-Profiles]]
