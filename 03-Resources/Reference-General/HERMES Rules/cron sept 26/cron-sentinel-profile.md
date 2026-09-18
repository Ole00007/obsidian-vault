
# Cron Sentinel Agent Profile

## Purpose
Cron Sentinel is a **restricted scheduled agent** for LexFlow. It reads daily session traces, build/deploy logs, selected GitHub workflow runs, approved Obsidian operational notes, and other explicitly allowed sources, then sends you a concise daily or weekly operational digest.

It is not a replacement for existing multifunctional agents. It is a narrow support agent for recurring audits, summaries, and risk flagging.

## Access boundaries
Cron Sentinel may:
- Read session logs for approved agents when those logs are stored in a shared, approved location.
- Read GitHub Actions workflow run metadata and downloadable logs for approved repositories.
- Read approved Obsidian notes through a local API or a mounted read-only export.
- Read selected deployment and runtime telemetry from Cloudflare Workers and connected services.
- Produce summaries of successes, failures, obstacles, flagged risks, and outstanding tasks.
- Create a report or send a message to you.

Cron Sentinel may not:
- Modify Memory Curator files, prompts, skills, memory stores, or synchronization rules.
- Write to Obsidian unless you later approve that scope.
- Send customer emails, modify CRM records, deploy code, merge branches, or change infrastructure.
- Access any source not explicitly listed in its allowlist.

## Can it read all agent sessions?
Only **if** all of the following are true:
1. The session logs are actually persisted somewhere retrievable.
2. Cron Sentinel is given credentials or filesystem access to that location.
3. No narrower ACL, repository permission, local file permission, or vault restriction blocks access.
4. Hermes/profile rules permit that agent-to-agent visibility.

So the answer is: **not automatically, but yes if you deliberately expose those logs and do not set narrower limits**. Cron Sentinel should still use an explicit allowlist rather than open-ended read access.

## Recommended ingestion sources
- Hermes cron/session output stored in a dedicated reports directory.
- GitHub Actions workflow runs and downloadable logs.
- Cloudflare Workers scheduled jobs, deployments, and workflow telemetry.
- Obsidian notes via Local REST API in read-only practice mode.
- Optional exported CSV/JSON task snapshots from LexFlow systems.

## Best-in-class job shape
Use a two-lane design:

### Lane A — deterministic collector
No LLM required.
- Pull logs, notes, and status feeds.
- Normalize into plain text or JSON bundles.
- Deduplicate repeated failures.
- Strip secrets and PII where possible.
- Stop early if there is nothing new.

### Lane B — summarizer
LLM only when interpretation is needed.
- Summarize the bundle.
- Separate facts from inferences.
- List successes, failures, obstacles, risks, and outstanding tasks.
- End with recommended follow-ups for you.

This pattern is cheaper and safer than letting one always-on agent do everything.

## Model policy
The provider can be swapped later. Keep a provider-agnostic model policy document and map it to equivalent classes when changing providers.

### Main local model via Ollama
1. **qwen3:8b** or the nearest current Qwen 3 instruct/tool-use variant in your Ollama library — best default for local summarization, structured outputs, and tool use support in Ollama.[web:148][web:158][web:152]

### Supplementary local models via Ollama
2. **qwen2.5:7b-instruct** or nearest current Qwen 2.5 instruct variant — strong backup for summarization and extraction.[web:151][web:158]
3. **llama3.1:8b-instruct** or nearest current Llama 3.1 tool-capable variant — broad compatibility fallback.[web:158]
4. **qwen2.5-coder:7b** or nearest current coder/tool variant — useful when the digest includes logs, scripts, shell traces, or GitHub workflow diagnostics.[web:158]

### Free Nous Portal / free-catalog fallbacks
Because the Portal free catalog changes over time, pin by **model class**, then validate the live exact IDs before installation.

Main free Portal class:
- **A current free fast general text model from the Nous Portal free catalog** for operational summarization and classification.[web:163][web:166][web:171]

Three supplementary free Portal classes:
- **A current free lightweight reasoning model** for incident grouping.[web:163][web:166][web:171]
- **A current free code-aware model** for GitHub workflow logs.[web:163][web:166][web:171]
- **A current free multilingual small model** for Italian/English mixed notes and status messages.[web:163][web:166][web:171]

## If you choose a different provider later
Map by capability, not by brand:
- Local small general summarizer
- Local backup summarizer
- Local code/log analyst
- Free remote general summarizer
- Free remote code/log analyst

That makes migration to OpenRouter, Together, Fireworks, Anthropic, OpenAI, or another provider straightforward.

## Skills
Cron Sentinel should have only these skills/tools:
- Shell skill for file discovery and safe text extraction.
- GitHub skill for workflow runs, artifacts, and logs.
- Read-only Obsidian notes skill.
- Optional Cloudflare telemetry read skill.
- Structured reporting skill.

## Recommended providers
- **Primary**: Ollama local, because it is private, cheap after setup, and sufficient for recurring summaries.[web:148][web:152]
- **Free remote fallback**: Nous Portal free catalog when a local model fails or is unavailable.[web:163][web:166][web:171]
- **Alternative later**: equivalent free or low-cost models on another provider with the same role categories.

## Implementation notes
- Use a read-only token for GitHub Actions access whenever possible.[web:150][web:164]
- Use Obsidian Local REST API with a dedicated API key and read-only route policy if supported by your setup.[web:149][web:153]
- For Cloudflare scheduled execution, use Cron Triggers and optionally Workflows for longer jobs.[web:109][web:142][page:1]
- For Hermes scheduled runs, pin provider and model per job and attach only the required skills.[web:110][web:141][web:172]
