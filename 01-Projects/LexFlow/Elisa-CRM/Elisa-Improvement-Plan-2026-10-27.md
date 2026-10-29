---
title: Elisa — profile review and improvement plan
date: 2026-10-27
author: backend-dev
status: PLAN — waiting for Ole's confirmation; nothing is being built
tags: [lexflow, elisa, agent, improvement-plan, phase-0-estimate]
---

# Elisa — profile review (evidence from the code)
Repo (local): `/Users/olesiarasing/projects/lexflow/lexflow-crm-wt-merge` — branch `lexflow_hermes_v1` (pushed, flag `AGENT_ENABLED` off on prod).
Files: `crm/agent/brain.py` (397 lines, RuleBrain + HttpLLMBrain), `runner.py`, `tools.py`, `guard.py`, `intents.py`, `llm.py`, `drafts.py`, `doctext.py`; route `crm/routes/agent.py`; UI `templates/_elisa_bubble.html`; tests `tests/test_agent.py`. ~2,000 lines.

## Why she is "barely functional" (root causes)
1. **No conversation memory.** Every message is sent as a fresh `goal` (`routes/agent.py` → `runner.run_goal(goal)`); only the tool-call history inside ONE turn exists. So "yes please", "are you thinking?", "what is blocking me here?" have no referent, and after "For which matter should I draft it?" the answer "Rasing separazione" is a brand-new goal.
2. **No pending-question state** (slot filling): she asks for the matter but cannot remember she asked.
3. **Mostly rules, not a model.** Default brain = `RuleBrain` (regex intents). The LLM brain is used only if env is set; its prompt is one line plus raw JSON of `goal` + tool history, temperature 0, no page/matter/user/date context, no native tool-calling.
4. **Chips are templates with "…"** ("Summarize document …", "Create task … for matter …") — clicking them inserts unusable placeholder text.
5. **No feedback while working** (no typing indicator) → "are you thinking?".
6. **Missing tools for natural questions:** "what is blocking me?" (blocked/awaiting-Ole list), "what changed today", deadlines.

## Improvement plan (in order)
| # | Piece | What | Time | Cost (USD) |
|---|---|---|---|---|
| 1 | Conversation state | client keeps last 10 messages + `pending` object; server validates size; follow-ups ("yes", "that one") resolved; slot-filling for matter | 0.5–1 d | $4–8 |
| 2 | Context injection | current page/matter id, user role+workspace, today's date, top open/blocked tasks passed to the brain (data-wrapped, size-capped) | 0.5 d | $3–6 |
| 3 | Real LLM brain | native tool-calling (OpenAI-style `tools`), proper system prompt (persona, capabilities, "ask before writing", IT/EN), temperature 0.2, retry + fallback chain, token floor kept | 1 d | $6–12 |
| 4 | New tools | `list_blocked` (reads the bus/board data), `agenda_today`, matter fuzzy search by name, deadline lookup, "what can you do" | 0.5–1 d | $4–8 |
| 5 | UX | typing indicator, chips built from the user's REAL data (real matter names), clear model-unavailable message, reset chat, mobile check | 0.5 d | $3–6 |
| 6 | Eval + safety | 25 scripted dialogues incl. yesterday's conversation, cost per turn, injection tests, no-write-without-approval tests | 0.5 d | $3–6 |
**Total: ~3–4 working days, ~$23–46 build.** Run cost per turn ≈ $0.0006 on the primary model (≈3K in / 0.5K out tokens). Estimate from scope comparison, not measured.
Parallel: 1+2 sequential (backend); 5 (Fronty-class, cheap model) in parallel with 3; 4 + 6 (Admy-class gate) after 3. Critical path: 1 → 3 → 6.

## Models (Nous Portal catalog, prices per 1M tokens in/out, checked 2026-10-27 against the live /models list)
- **Primary (cheap, capable, tool use, Italian):** `anthropic/claude-haiku-5.5` — $0.10 / $0.50.
- **Fallback 1 (cheap, strong tool calling):** `deepseek/deepseek-v4.1-flash` — $0.106 / $0.513.
- **Fallback 2 (most capable FREE on the catalog):** `reflection/beam-1.0-501b-a23b:free` — $0 (501B MoE, 262K ctx). NOT tested yet by us; `stepfun/step-3.7-flash:free` is the free model we have actually tested (reasoning model, needs the token floor). Keep it as the emergency #3 if beam fails the eval.
- Config = env only, no code: `LEXFLOW_AGENT_LLM_MODEL`, `LEXFLOW_AGENT_LLM_FALLBACKS` (comma list) — never hard-code models (AGENT_RULES §12). Pick the final order after step 6 eval (same 25 dialogues on each model).
- Privacy: model calls with matter text need the explicit opt-in `LEXFLOW_AGENT_LLM_DOCS=1` (client-confidentiality decision stays with Ole).


## Eval result (2026-10-29, 10 free-text prompts, EN+IT incl. an injection attempt, live via Nous)
| Model | valid JSON | right choice | avg latency |
|---|---|---|---|
| anthropic/claude-haiku-5.5 | 10/10 | 10/10 | 2.6 s |
| deepseek/deepseek-v4.1-flash | 10/10 | 10/10 | 2.6 s |
| ornith/ornith-1.5-122b:free | 9/10 | 9/10 | 6.1 s |
| stepfun/step-3.7-flash:free | 9/10 | 8/10 | 10.8 s |
| poolside/laguna-s-2.1:free | 6/10 (HTTP 429 rate limit) | 6/10 | 3.0 s |
| upstage/solar-mini4:free | 9/10 | 5/10 | 2.6 s |
| reflection/beam-1.0-501b-a23b:free | 2/10 (empty replies) | 2/10 | 3.4 s |
**Decision (changes the earlier order):** primary Haiku 5.5 -> fallback 1 DeepSeek v4.1 Flash -> fallback 2 (best free) `ornith/ornith-1.5-122b:free` -> fallback 3 `stepfun/step-3.7-flash:free`. Beam is NOT used: "most capable on paper" failed in practice. Small sample (10 prompts) - re-run when models change (`elisa_eval.py` in backend-dev scratch).

## Built so far (local, commits 829d235, 0ad2359, 603b4d6)
Conversation state (history + pending), offline follow-ups/small talk, blocked intent, rules-first HybridBrain (model only for requests the rules do not know, via the fallback chain), list_tasks fixed (sorted, soonest due, "open" = not finished), chips from real matter names. Left: page/matter context from the URL, latency trim (model path ~6-10 s for two steps), more test dialogues.

## Decision needed from Ole
Confirm: (a) do the plan as written, (b) model order above, (c) start now or after the Harvey-like brainstorm. I build nothing until you confirm.

## Links
- Parent: [[LexFlow-Platform-Plan-2026-10-24]]
- Related: [[LexFlow-Session-Summary-and-Operating-Blueprint-2026-10-27]], [[LexFlow-Harvey-Like-Tools-Estimate-and-Pitch-2026-10-26]]
- Important: [[Elisa-Naming-Disambiguation]] — CRM Elisa and website chatbot Elisa are distinct agents; do not confuse their data or training artifacts.
