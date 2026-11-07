# ELISA — what she can do & how to make her a great legal assistant
**Status 2026-11-07 · demo2 CRM (case "Separazione Alessia Rasing" L-01) · 6 documents prepared**

---

## 1. What Elisa can already do (live proof)
From `crm/agent/guard.py` TOOL_SPECS + `crm/agent/llm.py`, verified live on case 1:
- **list_documents / read_document / summarize_document** — reads matter attachments (✅ verified: listed all 3 dossier docs, read the one-pager). Summaries via `llm.summarize` (extractive fallback if no LLM).
- **draft_document** — kinds: `client_update`, `document_request`, `deadline_reminder` (lang it/en). ✅ produced a strategy-structured client_update in Italian from the evidence.
- **create_task / update_task_status / list_tasks** — case task management.
- **create_calendar_event** — deadlines/hearings onto a calendar.
- **draft_notification** — client comms.
- **Full rule/template brain** works even **offline** (no LLM needed) — the "can't reach my language model" fallback is purely graceful degradation, not a hard failure.

## 2. What she cannot do yet (gaps → become great)
1. **No true "strategy"/"analysis" draft kind** — `draft_document` only allows the 3 correspondence kinds. A strategy is forced into `client_update`.
2. **LLM currently broken at runtime** — the key configured (`Nous access_token`) returns **401 invalid/out-of-funds** from `/v1/chat/completions`. She works today **only offline/rules**, no real model writing.
3. **read_document caps at 3,000 chars** — the full dossier (18.6 KB) is truncated; she reads slices, not the whole.
4. **No cross-case memory** — she sees per-run context, not a client history across matters.
5. **No attachment "kind" awareness** — files upload as text; she can't tell a contract from a chat export.

## 3. Upgrade spec — how to make Elisa a great legal assistant
An **as-you-were plan** for the avvocato, roughly by value:
1. **Working model (prerequisite — Becky).** Add a real inference key + model (OpenRouter/OpenAI-compatible; see `llm.py` header — one env swap, no code). E.g. a capable cheap model for drafting + keep self-hosted/offline fallback. Doc-text opt-in stays gated by `LEXFLOW_AGENT_LLM_DOCS=1`. ⚠️ current 401 = no model at all.
2. **Add `strategy` (and `analysis`, `brief`?) to allowed draft kinds** — 1-line change in `guard.py` (+ a proper system prompt in `llm.polish_draft`), so a strategy is a first-class artifact, not a dressed client_update.
3. **Raise/parameterise `read_document max_chars` cap** (currently hard 3,000) → let a `max_chars` up to full dossier size, so she reasons over **all six docs**, not a slice.
4. **Legal-assistant system prompt** in `llm.polish_draft`: cite only verified evidence, distinguish evidence vs inference, flag gaps (voice/deleted), no invented dates, no legal advice. Mirrors the dossier-compilation skill's rules → feeds straight into her drafting.
5. **Attachment tagging** (doc kind: chat-export / contract / ledger / summary) so she routes appropriately.
6. **Cross-matter client context** — a per-client summary record she reads at run start (or the case-notes field).
7. **Timeboxed: offline "skeleton" strategy** (rules template already drafts 4-part structure) so she's useful even with no LLM.

## 4. Elisa's self-reference (her own words, captured from the running agent)
When asked to reflect honestly on her capabilities, the agent replied (rules-fallback, because the key is 401):
> "I can't reach my language model right now, so I can only do the basics: your tasks, the agenda, documents and client-update drafts."
This is itself the strongest evidence for gap #2 — restore the model and she can reason in full.

## 5. Where the work should land
- **Model + key + draft kinds + read cap → backend-dev (Becky).** This is a server/config change in demo2 `crm/`; she owns the boot + env.
- **System prompt / evidence-discipline → reuse the `evidence-dossier-compilation` skill** in the prompt source so Elisa inherits the same verbatim/evidence-vs-inference rules the dossier was built with.
- **Cross-case memory + tagging → product decision (Ole)**, then backend implements.

## Links
- Parent: [[Separazione-Strategy-2026-11-07]]
- Related: [[Separazione-Swarm-Workflow-2026-11-07]]
