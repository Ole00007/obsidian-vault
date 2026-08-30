# Hermes Global Rules — avibe-hindsight Scope Block

> Add this block to Hermes' general/global rules settings. All rules below
> are explicitly scoped to the `avibe-hindsight` project only and MUST NOT
> be applied to, or override, any other Hermes agent, project, or workflow.

---

## Rule 1 — Project Scope Declaration

```
This entire rule block applies ONLY when the active project/repo is
"avibe-hindsight" (Hermes-Obsidian-Hindsight shared memory setup).
If the current working context is any other project, IGNORE all rules
in this block and defer to that project's own configuration.
```

## Rule 2 — LLM Provider: OpenRouter, FREE-ONLY (avibe-hindsight scope ONLY)

Within avibe-hindsight scope only:
- All LLM calls for Hindsight fact extraction and Reflect synthesis
  MUST use OpenRouter (`https://openrouter.ai/api/v1`), authenticated via
  `OPENROUTER_API_KEY` (= `HINDSIGHT_API_LLM_API_KEY`). No other provider
  may be substituted within this scope.
- **NO paid models** — free-tier only until we scale and generate real revenue.
- Free fallback chain (all $0, validated 2026-08-30):
    1) nvidia/nemotron-3-ultra-550b-a55b:free   (primary)
    2) nvidia/nemotron-3.5-lightning:free        (fallback 1)
    3) nvidia/nemotron-3-super-120b-a12b:free    (fallback 2)
    4) nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free (fallback 3)
- If all models fail or are rate-limited, HALT and alert the user. Do NOT
  silently fall back to any paid API.
- This rule does not restrict, override, or reference the
  model/provider configuration of any other Hermes agent or project.
```

## Rule 3 — Shared Bank Name Consistency

```
Within avibe-hindsight scope only:
- The Hindsight memory bank ID MUST be "avibe-hq" across every
  connection point: Hermes (all 4 devices), Obsidian plugin (all
  vaults), and the Railway-hosted Hindsight server itself.
- Do NOT rename, alias, or create a second bank without explicit
  user instruction. A second bank (e.g. "avibe-clients") is only
  created intentionally for Phase 2 client-data separation, never
  as a side effect of setup or migration work.
```

## Rule 4 — Credential Handling

```
Within avibe-hindsight scope only:
- HINDSIGHT_API_KEY is a self-issued secret (not obtained from any
  vendor dashboard). If it already exists in Railway env vars or
  local config, REUSE it. Do not regenerate unless the user
  explicitly requests rotation.
- HINDSIGHT_API_LLM_API_KEY = OPENROUTER_API_KEY per Rule 2.
- Never print, log, or commit either key value in plaintext to
  GitHub, chat output, or any file that is not .gitignore'd.
```

## Rule 5 — Do-Not-Touch Zone

```
Within avibe-hindsight scope only:
- Do NOT modify the existing Railway deployment structure, TLS/domain
  setup, or Postgres service configuration already deployed and
  pushed to GitHub. Only additive changes (new scripts, new fallback
  logic, new documentation) are permitted unless the user explicitly
  requests a structural change.
```

## Rule 6 — Model Failover Script Ownership

```
Within avibe-hindsight scope only:
- The file scripts/model_failover.sh is the single source of truth
  for LLM fallback logic. Hindsight's LLM calls should route through
  this wrapper rather than a hardcoded single model string wherever
  the deployment target supports a custom command/entrypoint.
- Any edit to the fallback order must update both this rules file
  and the script in the same commit to avoid drift.
```

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[hermes-standing-rules]]
