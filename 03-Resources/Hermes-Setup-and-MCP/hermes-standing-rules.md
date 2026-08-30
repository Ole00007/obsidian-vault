# Hermes Standing Rules — avibe-hindsight Project

Persistent rules for any Hermes session touching this project. Apply automatically, 
no need to re-confirm each time unless the user changes them explicitly.

---

## Rule 1 — Correct Hermes Restart Procedure

Never restart Hermes by sending `exit` to an interactive session or by bouncing 
the gateway from multiple terminals — this causes stale state and connection 
churn. If a restart is genuinely needed, do exactly this and nothing else:

```
set -a && source ~/.hermes/.env && set +a && hermes gateway run
```

Then, in a separate terminal:

```
hermes dashboard
```

Verify health with `hermes gateway status`, `lsof -iTCP:8642`, or `curl` — never 
assume a browser page loading means the service is fully healthy.

## Rule 2 — LLM Provider: Ollama Cloud Only
## Rule 2 — LLM Provider: OpenRouter, FREE-ONLY
`HINDSIGHT_API_LLM_PROVIDER=openai` with `HINDSIGHT_API_LLM_BASE_URL=https://openrouter.ai/api/v1` (OpenRouter's OpenAI-compatible endpoint), key `OPENROUTER_API_KEY`/`HINDSIGHT_API_LLM_API_KEY`. **NO paid models — free-tier only until we scale and generate real revenue.** Free fallback chain: `nvidia/nemotron-3-ultra-550b-a55b:free` → `nvidia/nemotron-3.5-lightning:free` → `nvidia/nemotron-3-super-120b-a12b:free` → `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`. Never set `HINDSIGHT_API_LLM_BASE_URL` to `localhost` — inside a Railway container, `localhost` refers to the container itself.

## Rule 3 — No Hardcoded Model Names

`HINDSIGHT_API_LLM_MODEL` must remain a single environment variable value, never 
hardcoded into a Dockerfile, docker-compose file, or script logic. The model 
will change; nothing else should need to change when it does.

## Rule 4 — Validate Model Name Before Every Deploy That Changes It
Never rely on manually browsing model libraries. Run this instead, and block 
the deploy if the model isn't present / not $0 (free):
```bash
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models \
  | jq -r '.data[] | select(.id=="<model-id>") | "\(.id) prompt=\(.pricing.prompt)"'
```


## Rule 5 — Auth Secret Is Off-Limits

`HINDSIGHT_API_KEY` is self-issued (`openssl rand -hex 32`), already saved in the 
password manager, and already deployed. Never regenerate, rename, or touch it 
unless the user explicitly asks.

## Rule 6 — Bank ID Consistency

Every Hermes and Obsidian config touching this project must use bank ID 
`avibe-hq`. Check this field before saving any new memory config on any device — 
a mismatch fails silently with no error, so it must be checked at config time, 
not discovered later.

## Rule 7 — Secrets Never Committed

Never write API keys, `HINDSIGHT_API_KEY`, or `.env` contents into any file that 
touches GitHub, even a private repo. Use `.gitignore` on any local `.env` file 
before it's created.

## Rule 8 — Remind to Save Credentials

Any time a new API key, OAuth token, or password is generated or obtained during 
a session, remind the user to save it in their password manager before moving on — 
do not assume it's been saved just because it was used once.

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[hermes_rules_avibe_hindsight]]
