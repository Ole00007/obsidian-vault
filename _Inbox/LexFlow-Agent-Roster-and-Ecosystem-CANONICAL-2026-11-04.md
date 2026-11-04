---
tags: [lexflow, roster, ecosystem, canonical]
project: LexFlow
home: 01-Projects/LexFlow/
status: CANONICAL (supersedes ROSTER.md body, ecosystem-index §1, Roster-Consolidation-Proposal, 14-Day-Roadmap profile counts)
version: v4.0
date: 2026-11-04
---
# LexFlow Agent Roster + Ecosystem — CANONICAL (v4.0, 2026-11-04)

**This is the single source of truth for profile count and roster.** The four older notes now only point here (see §6). Measured live 2026-11-04 ~18:20 CET by backend-dev (card t_ab254a40).

## 0. Answer in one block
- **FULL DIRECTORY:** `/Users/olesiarasing/.hermes/profiles/` (live profiles); kanban `~/.hermes/kanban.db`; vault `/Users/olesiarasing/Obsidian/`; code root `/Users/olesiarasing/projects/` (LexFlow CRM: `/Users/olesiarasing/projects/lexflow/lexflow-crm`, worktrees `/Users/olesiarasing/projects/lexflow/lexflow-crm-wt-*`).
- **VERSION:** v4.0 (previous: ecosystem-index 2026-09-19/10-06 "24", Proposal 2026-09-16 "23", Roadmap r4 2026-09-16 "22", ROSTER.md "3 agents" = a template).
- **DATE:** 2026-11-04.
- **PROFILE COUNT: 23 runnable = 22 named profiles + `default`** (`hermes profile list`, 23 rows, all gateways "running").
- **LATEST ACTIVE PROFILE:** `memory-curator` and `backend-dev` tie at **2026-11-04 18:13:46** (state.db `sessions`, max started_at; kanban task_runs 18:13:44 both). Latest *LexFlow product-code* author: `backend-dev` (CRM commit 0d1ead1, 2026-11-03 09:07). Latest UI: `frontend-developer-lovable_react` 2026-11-04 17:03:58. Per rule AGENT_RULES §16 the LexFlow **ownership ladder** is Admy (`admy_ceo`) → Backy (`backend-dev`) → Smothy (`smoothy_op_dir`); Admy's last session was 2026-11-03 09:07:02 (not the most recent).

## 1. Why the four sources disagreed (all reconciled)
| Source | Said | Reality |
|---|---|---|
| ROSTER.md | 3 agents | Unfilled template (admy/memy/backy), never a count. Names map: memy = `memory-curator`, backy = `backend-dev`. |
| Consolidation-Proposal 2026-09-16 | 23 | Snapshot at 09-16 incl. `librarian` (since retired). Proposal never executed: chatbot_builder, email-digest-agent, tester **still exist**. |
| ecosystem-index.md | "24" (lists 23 names) | Lists `operator-installer` and `telegram-utility-agent`; first is a leftover dir, second deleted 2026-10-21 (`profiles/.deleted/`). Misses `cron-sentinel`. |
| 14-Day-Roadmap r4 | 22 | Snapshot 09-16; since then +`cron-sentinel` (10-21+), −`telegram-utility-agent`, −`operator-installer`(10-21). |

## 2. Roster — 22 named profiles + default (live)
Sessions = rows in that profile's `state.db`; last = max started_at. Channel: Telegram bot token present in `.env` (checked key presence only, no values). All other profiles notify via kanban card + NOTIFY/daily note (no own Telegram bot).

| # | Profile | Active role | Default model | Sessions | Last session | Channel |
|---|---|---|---|---|---|---|
| – | default | Hermes default instance | deepseek/deepseek-v4-flash | n/a | n/a | gateway |
| 1 | admy_ceo | **LexFlow primary orchestrator** (ladder #1) | deepseek-v4-flash-0731 | 134 | 2026-11-03 09:07 | kanban |
| 2 | backend-dev (Backy) | Flask API/DB engineer, ladder #2 | anthropic/claude-sonnet-5.5 | 70 | **2026-11-04 18:13** | kanban |
| 3 | smoothy_op_dir (Smothy) | Master orchestrator/installer, ladder #3; owns the operator-installer role | deepseek-v4.1-flash-1017 | 354 | 2026-11-04 09:44 | Telegram + kanban |
| 4 | memory-curator (Memy) | Vault/memory hygiene, only note-mover, builds daily agent report | stepfun/step-3.7-flash:free | 324 | **2026-11-04 18:13** | Telegram (HOME_CHANNEL) + kanban |
| 5 | frontend-developer-lovable_react | UI/React/LP engineer | deepseek-v4-flash-0731 | 151 | 2026-11-04 17:03 | Telegram + kanban |
| 6 | personal-assistant | Life/business admin | google/gemini-3.5-flash | 20 | 2026-10-25 | kanban |
| 7 | agency-growth | SEO-HERO growth | poolside/laguna-s-2.1:free | 10 | 2026-10-24 | kanban |
| 8 | chatbot_builder | Chatbot builder (now has a model; Elisa widgets) | openai/gpt-5.4-mini | 8 | 2026-10-25 | kanban |
| 9 | crm-outreach-agent | CRM + outreach (premium route) | anthropic/claude-opus-4.8 | 4 | 2026-10-25 | kanban |
| 10 | sales-crm | Sales pipeline/outreach | deepseek-v4-flash | 4 | 2026-10-25 | kanban |
| 11 | ads-expert | Google/Meta Ads | gemini-3.5-flash | 0 | – | kanban |
| 12 | chatseo-agent | Conversational SEO research | gemini-3.5-flash | 0 | – | kanban |
| 13 | content-creator | Content/copy | gemini-3.5-flash | 0 | – | kanban |
| 14 | cron-sentinel | Restricted scheduled reporting for LexFlow | meituan/longcat-2.5-preview:free | 0 | – | kanban |
| 15 | customer-rel-manager | Customer communications | gemini-3.5-flash | 0 | – | kanban |
| 16 | email-digest-agent | 06:00 digest (unmerged, no sessions) | claude-haiku-4.5 | 0 | – | kanban |
| 17 | gsc-agent | Search Console | gemini-3.5-flash | 0 | – | kanban |
| 18 | marketing-analyst | Market/competitor research | gemini-3.5-flash | 0 | – | kanban |
| 19 | seo-aeo-expert | SEO/AEO admin | gemini-3.5-flash | 0 | – | kanban |
| 20 | seo-cron-agent | SEO scheduler | gemini-3.5-flash | 0 | – | kanban |
| 21 | seo-swarm-agent | SEO swarm coordinator | gemini-3.5-flash | 0 | – | kanban |
| 22 | tester | QA/debug (no model configured) | – | 0 | – | kanban |

### 2a. Names that are NOT profiles (do not count)
- `operator-installer` — **retired profile** (marker in `profiles/.deleted/` since 2026-10-21). A residual dir (SOUL.md, skills, logs; no config/state.db; not in `hermes profile list`) remains and kanban still carries 22 cards/22 runs assigned to it (last run 2026-10-29, last card 2026-11-04 09:16). Its role = `smoothy_op_dir` (AGENT_RULES §16 "smoothy_op_dir / operator-installer"). Residual dir should be removed by Ole's go.
- `lexflow-crm-elisa`, `lexflow-intake-elisa` — **empty dirs** (created 2026-10-29), not registered profiles; Elisa is a product agent (see Elisa-Naming-Disambiguation), not a Hermes profile.
- `telegram-utility-agent`, `librarian` — deleted (markers in `.deleted/`; librarian→memory-curator).

## 3. Hard rules (kept from ROSTER.md)
1. Any move/rename/delete → append to NOTIFY and tell affected agents (moves by memory-curator only, §15).
2. Never touch files locked in `~/projects/.locks/`.
3. Never delete; archive.

## 4. Ecosystem pointers (non-roster sections of ecosystem-index.md remain valid there)
Repos, deployments, MCP, cron, kanban, standards: `01-Projects/LexFlow/ecosystem-index.md` §2–§9 (its §1 now points here). Railway CRM: web-production-031a6.up.railway.app. Daily status cron: operator-installer-owned `lexflow-daily-status-crm` (§10.3; now Smothy).

## 5. Open items for Ole
- Approve retire of residual `operator-installer` dir and the 2 empty elisa dirs.
- Consolidation proposal of 2026-09-16 (merge chatbot_builder/email-digest-agent/tester): still undecided; 12 of 22 profiles have 0 sessions.

## 6. Replaced copies
ROSTER.md (body → pointer), ecosystem-index.md §1 (→ pointer), Agent-Roster-Consolidation-Proposal and 14-Day-Roadmap (superseded banner added at top; history preserved, not deleted).

## Links
- Parent: [[LexFlow]]
- Related: [[ecosystem-index]] · [[ROSTER]] · [[AGENT_RULES]]
