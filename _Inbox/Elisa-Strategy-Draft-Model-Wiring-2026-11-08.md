---
tags: [lexflow, elisa, backend]
project: LexFlow
home: 01-Projects/LexFlow
---
# Elisa: strategy draft kind, read cap, model wiring (2026-11-08)

**Branch:** `feat/elisa-strategy-draft` in `~/projects/lexflow/lexflow-crm-wt-demo2` (commits effca31, c33daba). Local only, not pushed.

## Delivered
- Draft kind `strategy`: internal note for the lawyer (facts with source, inferences, gaps, risks, next steps). Own prompt in `crm/agent/llm.py`.
- `read_document` cap now `LEXFLOW_AGENT_READ_MAX_CHARS` (default 3000, max 30000). Use 20000 for the 18.6 KB dossier.
- Tests: 38 agent tests pass. The 8 earlier failures came from a hard-coded date (2026-11-03) that went stale. Tests now use relative dates.
- Wider suite: 76 pass, 1 fails (`test_insights.py`, duplicate blueprint "insights"). It fails the same way on base 0bd3e5c, so it is not caused by this work.

## Model wiring (all env vars on the demo boot, nothing in code)
| Var | Value | Revoke / change |
|---|---|---|
| LEXFLOW_AGENT_LLM_URL | CURRENT: https://inference-api.nousresearch.com/v1 (Nous). OpenRouter dropped: free stepfun slug withdrawn (404), account returned 402 | change provider |
| LEXFLOW_AGENT_LLM_MODEL | stepfun/step-3.7-flash:free | swap id |
| LEXFLOW_AGENT_LLM_FALLBACKS | deepseek/deepseek-chat | paid, small, optional |
| LEXFLOW_AGENT_LLM_KEY | from OPENROUTER_API_KEY in the backend-dev profile .env (reference only) | rotate or delete at OpenRouter |
| LEXFLOW_AGENT_LLM_DOCS | 1 = documents may leave the server | **unset = Elisa back to offline rules at once** |

Verified with SYNTHETIC text only (live call returned a structured note). The real Rasing dossier has NOT been sent: leave DOCS unset until the free model's data policy is checked, or use the paid fallback only.

## Live test on the real dossier (2026-11-08)
- Owner approved sending his own separation files to the free model.
- Throwaway DB and upload folder; the 2 dossier files were uploaded as .txt case attachments over the real route (201). Elisa then listed them and drafted: "Draft a strategy proposal for matter Rasing separazione" -> structured internal note (facts with source file, inferences, gaps, risks, next steps).
- Model used: stepfun/step-3.7-flash:free via OpenRouter. Cost: 0.
- Fixes found by the test: "strategy" wording was not recognised as a draft request; the strategy draft was not reading case documents; draft was cut at 3300 chars; model added a sign-off. All fixed.
- Quality caveat: the note sometimes cites section numbers loosely and dropped the 24 Sep 2026 date in one run. It must be reviewed by the lawyer before use. The one-liner "will not fight" is correctly flagged as coming from a screenshot OCR, not the chat export.
- Full suite: 115 passed, 1 failed (test_insights, same failure on base). Commits on feat/elisa-strategy-draft, not pushed.
- NOT done: the live demo server on 5057 was not restarted (needs the port-5057 lock; no schema change, so Python restart only). Screenshot transcription not needed: the existing OCR summary was enough.

## Open
- Task t_03c96721 failed to spawn: "unknown workspace_kind: lexflow" (kanban config, operator-installer).
- test_insights duplicate blueprint: separate fix.

## Links
- Parent: [[LexFlow]]
- Related: [[Elisa-Legal-Assistant-Upgrade-2026-11-07]]

## Merge, restart, card (same day, later)
- Fast-forward merged feat/elisa-strategy-draft into integration/filters-roi-demo2 (fea5f1e). Not pushed.
- Demo on 5057 restarted by backend-dev under the port-5057 lock (released after). Boot script: ~/.hermes/profiles/backend-dev/cache/scratch/elisa_boot_5057.py (reads the key from the profile .env at start; same DB as Admy's demo, 6 documents on case 1).
- Live check on 5057: login 200, document list 6, strategy draft 3415 chars with dated quotes tied to source files.
- Card t_03c96721: spawn failure root cause = workspace_kind "lexflow" is not valid (allowed: scratch, dir, worktree). Set to dir + repo path and completed. Whoever creates cards must not use a custom kind.

## Update (2026-11-09): Nous models, profiles, docs
- Models now: Nous inference API, primary ~deepseek/deepseek-flash-latest (~$0.006/M in, $0.50/M out), fallback ~z-ai/glm-flash-latest. Key = the agent_key inside ~/.hermes/auth.json (NOT access_token, which gives 401). Short-lived: the boot script re-reads it every 5 min. Never stored in a file or note. A key pasted in chat is exposed: rotate it in the Nous portal.
- Client profiles (standard, executive, anxious, analytical, low_literacy, hostile) + optional assistant addressee. Live run on the Nous models: executive 83 words / 3 bullets, anxious 192, analytical 452 / 14 bullets, low_literacy 103 words / shortest sentences (13.3 words), hostile 72. Profiles change the output measurably.
- Bugs fixed on the way: strategy answers were EMPTY on long dossiers (reasoning model ran out of tokens; now 8000, env LEXFLOW_AGENT_LLM_STRATEGY_TOKENS); strategy result cut by a 4 KB tool cap and shown as 'Could not build the draft' (cap raised for strategy only); banner duplicated by the model.
- Docs: docs/ELISA.md (new, in repo) + README docs index. Rule from Ole: every approved change updates Elisa docs and CRM docs in the same commit.
- Where drafts and templates are stored: templates = code (crm/agent/drafts.py, profiles.py, llm.py prompts; checklists in crm/services/checklist_templates.py). Drafts are NOT persisted as documents: returned in chat, kept only in agent_runs.final_text / agent_audit. The lawyer saves one by attaching it to the matter (/api/attachments/). Elisa writes nothing to the vault.
- Merged (local, not pushed) into integration/filters-roi-demo2 at c5bacc6. Full suite 124 pass, 1 pre-existing fail (test_insights). 5057 restarted under lock, lock released.
- OPEN for Ole: (1) persona set of realistic client QUESTIONS not yet written; (2) no 'save draft to matter' action in chat (needs approval flow); (3) test_insights duplicate blueprint.
