# avibe-hindsight — Runtime Rules (scope: this project only)

Apply these rules for ALL work in this repo and Railway deployment.  
These rules DO NOT apply to any other Hermes agent, profile, or project.

---

## Rule 1 — Scope
Everything below applies ONLY to the avibe-hindsight project (Railway project `graceful-presence`, service `avibe-hindsight`, bank `avibe-hq`).

## Rule 2 — LLM Provider (FREE-ONLY until revenue)
OpenRouter only (`https://openrouter.ai/api/v1`, via `OPENROUTER_API_KEY`/`HINDSIGHT_API_LLM_API_KEY`).  
**NO paid models — free-tier only until we scale and generate real revenue.** Never silently fall back to a paid model.
Free fallback chain (all $0, validated 2026-08-30 via OpenRouter `/models`):
1. `nvidia/nemotron-3-ultra-550b-a55b:free` — primary (text-only; NVIDIA free pool overloads transiently → 500s)
2. `nvidia/nemotron-3.5-lightning:free` — fallback 1
3. `nvidia/nemotron-3-super-120b-a12b:free` — fallback 2
4. `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` — fallback 3 (omni; may cover vision)

If all models fail/rate-limit, halt and alert.  
If the pending task involves an image or scanned document and the model lacks vision, halt and alert — do NOT silently degrade to text-only.
NOTE: the deployed `hindsight-api` runs a single `HINDSIGHT_API_LLM_MODEL` with **no fallback wired in**. This chain is the canonical order (scripts/model_failover.sh, Rule 6) but must be wired into the server/LLM call path by operator-installer (Railway deploy) to take effect. Until then, rely on the server's async +60s retry — no memory is lost on 500s.

## Rule 3 — Bank name
Bank name `avibe-hq` must be used consistently across Hermes (all 4 devices), the Obsidian plugin (all vaults), and the Railway Hindsight server.

## Rule 4 — Secrets
`HINDSIGHT_API_KEY` and `OLLAMA_API_KEY` are pre-existing secrets. Reuse them if already set. Do not regenerate unless explicitly instructed. Never print or commit any key in plaintext.

When using OpenRouter: set `OPENROUTER_API_KEY` in Railway variables, `HINDSIGHT_API_LLM_PROVIDER=openai`, `HINDSIGHT_API_LLM_BASE_URL=https://openrouter.ai/api/v1`, and choose free-tier models.

## Rule 5 — Railway deployment structure
Do not modify the existing Railway deployment structure (services, TLS/domain, Postgres plugin). Additive changes only.

## Rule 6 — Failover script
`scripts/model_failover.sh` is the single source of truth for LLM fallback logic. Keep it and Rule 2 in sync.