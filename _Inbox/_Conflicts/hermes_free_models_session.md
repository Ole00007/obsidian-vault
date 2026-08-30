# Hermes Agent — Free Models, Provider Setup & Session Reference

## Free Models Available with No Credits

All models below are free to use via Hermes. Each entry includes the exact model ID to paste in Hermes, the API key link, and the Hermes click path.

### OpenRouter (existing key — no new setup needed)

| Model | Model ID | Strength | API key link | Hermes path |
|---|---|---|---|---|
| DeepSeek Chat V3 | `deepseek/deepseek-chat-v3-0324:free` | Coding, reasoning, general | https://openrouter.ai/keys | Desktop → Models → + Add Model → OpenRouter |
| Llama 4 Maverick | `meta-llama/llama-4-maverick:free` | General, long context | https://openrouter.ai/keys | Desktop → Models → + Add Model → OpenRouter |
| Gemma 3 27B | `google/gemma-3-27b-it:free` | Coding, instruction | https://openrouter.ai/keys | Desktop → Models → + Add Model → OpenRouter |
| Qwen3.6 Plus | `qwen/qwen3.6-plus:free` | Best free coding model | https://openrouter.ai/keys | Desktop → Models → + Add Model → OpenRouter |
| Mistral Small 4 | `mistralai/mistral-small-4:free` | Coding + reasoning + vision | https://openrouter.ai/keys | Desktop → Models → + Add Model → OpenRouter |

Browse all free models: https://openrouter.ai/models?q=free

### NVIDIA NIM (free credits on signup, no credit card)

Sign up: https://build.nvidia.com

| Model | Model ID | Strength |
|---|---|---|
| Hermes 3 Llama 3.1 70B | `nousresearch/hermes-3-llama-3.1-70b` | NousResearch native, agentic |
| Llama 4 Maverick | `meta/llama-4-maverick` | Coding, reasoning |
| Qwen3 Coder | `qwen/qwen3-coder` | Code generation specialist |

Hermes path: Desktop → Settings → Providers → + Add Provider → NVIDIA NIM → paste key

### Google AI Studio (free for existing Google accounts)

API key: https://aistudio.google.com/apikey

| Model | Model ID | Context | Strength |
|---|---|---|---|
| Gemini 2.5 Flash | `gemini-2.5-flash` | 1M tokens | Multimodal, long docs, coding |

Hermes path: Desktop → Models → + Add Model → Google or Custom endpoint → `https://generativelanguage.googleapis.com/v1beta`

### GitHub Models (free with any GitHub account)

Token: https://github.com/settings/tokens → Generate new token (classic)

| Model | Model ID | Strength |
|---|---|---|
| Llama 4 Scout | `meta/llama-4-scout` | General, coding |
| Phi-4 Reasoning | `microsoft/phi-4-reasoning` | Coding, math, reasoning |

Hermes path: Desktop → Models → Custom endpoint → `https://models.github.ai/inference` → paste token

### Mistral (free Experiment plan ~1B tokens/month)

Console: https://console.mistral.ai

| Model | Model ID | Strength |
|---|---|---|
| Mistral Small 4 | `mistral-small-4` | Coding, reasoning, Apache 2.0 |

Hermes path: Desktop → Models → Custom endpoint → `https://api.mistral.ai/v1`

### Hugging Face (free monthly inference credits)

Token: https://huggingface.co/settings/tokens

Hermes path: Desktop → Settings → Providers → + Add Provider → Hugging Face → paste token

---

## Task → Model Mapping

| Task | Model | Provider | Cost |
|---|---|---|---|
| Daily chat, planning | DeepSeek Chat V3 :free | OpenRouter | Free |
| Coding — LexFlow build | Qwen3.6 Plus :free | OpenRouter | Free |
| Coding — serious sessions | Claude Sonnet 4 (when credits added) | OpenRouter | Paid |
| Long docs, research | Gemini 2.5 Flash | Google AI Studio | Free |
| Hermes-native agentic tasks | Hermes 3 Llama 3.1 70B | NVIDIA NIM | Free credits |
| Code review, reasoning | Phi-4 Reasoning | GitHub Models | Free |
| Experimentation | Browse HF catalog | Hugging Face | Free credits |
| Lightweight code tasks | Mistral Small 4 | Mistral | Free |

---

## SOUL.md Prompt Modules

### Starter SOUL.md (paste into `~/.hermes/SOUL.md`)

```text
You are Hermes, a concise and proactive operator.
Prefer action over explanation when tools improve correctness.
Inspect current state before making changes.
After changes, run the smallest meaningful verification first, then broader checks if risk is higher.
Use primary sources when facts matter.
Minimize interruptions: give progress updates quietly and ask questions only when blocked.
Store durable facts in memory and reusable workflows as skills.
Never expose secrets.
```

### Agent loop

```text
Operate in a disciplined loop.
Read the latest goal, state, and results.
Choose the single best next action.
Prefer doing the work over describing it.
Reassess after each result.
Stop only when the outcome is complete or blocked.
Report outcomes, files, and blockers clearly.
```

### Evidence priority

```text
When facts matter, prefer:
1. Authoritative APIs or primary sources.
2. Original web pages.
3. Durable memory.
4. Model background knowledge only when better sources are unavailable.
Cross-check important claims before presenting them.
```

### Communication mode

```text
Use two modes:
- Notify for progress updates that do not require a reply.
- Ask only when a decision, credential, or permission blocks progress.
Minimize interruptions. Continue autonomously when the next step is clear.
```

### Error recovery

```text
When a step fails:
1. Verify the instruction, method, and parameters.
2. Use the error details to correct the attempt.
3. Try one alternative method.
4. If multiple methods fail, explain the blocker and request the minimum input needed.
```

### Verification

```text
Before declaring completion:
- inspect current state before editing;
- run the smallest meaningful verification after changes;
- broaden verification when the change is risky;
- never claim success without evidence.
```

---

## Key Links Reference

| Purpose | Link |
|---|---|
| OpenRouter — your API keys | https://openrouter.ai/keys |
| OpenRouter — browse free models | https://openrouter.ai/models?q=free |
| OpenRouter — add credits (when ready) | https://openrouter.ai/credits |
| NVIDIA NIM — sign up & get API key | https://build.nvidia.com |
| Google AI Studio — API key | https://aistudio.google.com/apikey |
| GitHub — personal access token | https://github.com/settings/tokens |
| Mistral — console & API key | https://console.mistral.ai |
| Hugging Face — tokens | https://huggingface.co/settings/tokens |
| Hermes quickstart docs | https://hermes-agent.nousresearch.com/docs/getting-started/quickstart |
| Hermes prompt assembly docs | https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly |
| Hermes providers docs | https://hermes-agent.nousresearch.com/docs/integrations/providers.md |
| Hermes VS Code / ACP integration | https://hermes-agent.ai/integrations/vscode |
| Hermes AGENTS.md (repo) | https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md |
| Community skills marketplace | https://skills.sh |

---

## Glossary

| Term | Definition |
|---|---|
| SOUL.md | Master instruction file for an agent's identity, tone, rules, and operating style. |
| MEMORY.md | Stores durable facts Hermes should always know. Persists across sessions. |
| USER.md | Personal profile snapshot injected into every session. |
| Profile | Fully isolated Hermes instance: own SOUL.md, memory, skills, sessions, crons. |
| Skill | Reusable named procedure (e.g. research_brief, pr_review). |
| ACP | Agent Communication Protocol — connects VS Code to a running Hermes instance. |
| Orchestrator | Hermes profile that receives tasks, decomposes them, spawns sub-agents. |
| Sub-agent | Specialist profile focused on a narrow domain. Spawned by the orchestrator. |
| :free suffix | OpenRouter suffix restricting the call to the zero-cost model version. |
| NVIDIA NIM | NVIDIA hosted inference — free credits on signup, no credit card. |
| Cron job | Scheduled task Hermes runs automatically. |
| Gateway | Messaging channel Hermes listens on (Telegram, Discord, Slack). |
| Multi-agent mode | config.yaml setting enabling concurrent worker sub-agents. |
| MCP | Model Context Protocol — standard for supplying structured tool context to models. |
| Self-improving loop | Hermes built-in mechanism to refine skills based on past task outcomes. |

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[Hermes_Obsidian_Windows_Install_Guide]]
