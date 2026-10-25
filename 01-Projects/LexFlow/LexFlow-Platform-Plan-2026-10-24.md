---
title: LexFlow platform plan — team-aware Gantt, deadlines/calendar, notifications, Harvey-style insights, LexRoom, in-app agent
date: 2026-10-24
author: backend-dev (for Ole)
status: DRAFT for Admy + Smoothy opinion
---

# Ole's request (2026-10-24, verbatim intent)
1. Gantt weekly: diagram and month header are not visually glued → fix.
2. Show team members responsible per task inside the timeline (fetched from "Team"), in different letter colours per role. Example "Rasing separazione": case owner E.Romanelli · docs supply O.Rasing · legal assistant Elisa. Make it agent-usable: clickable link to the docs vault so an agent can pull the documents needed at this stage, and/or flag the lawyer.
3. Deadlines on some tasks + verify they are reflected in the Calendar.
4. Telegram and WhatsApp notification buttons.
5. Harvey-style diagrams (app-usage statistics, like harvey.ai front page / Command Center); key feature to add; LexFlow ↔ Lexroom integration; an AI agent that lives inside LexFlow; GitHub survey of similar agents/harnesses.
Rules: every agent works on its OWN isolated branch/worktree; Ole allows all actions on isolated branches; merge only after cross-test (+Admy test) per the usual building rule; nobody pushes/deploys; no two agents do the same task; agents review another agent's work only in the test phase.

# Research findings (evidence)
- Harvey platform pillars (harvey.ai): Agents, Vault, Knowledge, Spaces, **Command Center** ("analytics, benchmarking, agentic insights"), Contract Intelligence, Horizon Scanning, **Intake**, Connector Library (MCP), **Legal Work Orchestration** ("assign, execute, review legal work with agents and your team"). → LexFlow already has Intake, Kanban/Gantt/graph (orchestration), vault notes; missing: Command Center analytics, agent layer, connector layer.
- Lexroom (lexroom.ai, Italian): natural-language legal research with verifiable sources (12M+ sources), drafting from templates, document/file analysis, Word add-in, private libraries; uses OpenAI/Gemini via API + Elastic + Pinecone; EU-only servers, ISO 27001. No public developer API found on the site (resellers mention "API" only generically) → integration must be a **partnership/API request** or a deep-link + "Send to Lexroom" handoff; do not scrape.
- GitHub / literature: CaseMark **linc** (legal agent on the open-source `pi` harness, MCP skills via agentskills.legal); **Parthenon Law** (Model / Harness / Agent roles / Knowledge / deterministic Tools / Skills; anti-leakage learning loop; github.com/HHHHHejia/parthenon-skills); **Harvey LAB** open harness contract (tasks = filesystem workspaces, rubric scoring); JudicialMind **Legal Agency** (30 MIT-licensed agent definitions); OpenContracts (Django, PydanticAI, AGPL); `mike` OSS legal AI platform; Clio/MyCase MCP servers (oktopeak) as the pattern for "agent over practice-management API"; claude-for-legal (skills + MCP connectors).
- Pattern to copy: agent = harness (tools over LexFlow REST API + vault read-only) + skills (SKILL.md per matter stage) + mandatory human gates ("flag the lawyer") + audit trace per action.

# Workstreams (one owner each; owned files listed to avoid collisions)
| WS | Scope | Branch | Owns (only these) |
|----|-------|--------|-------------------|
| A | Gantt: glue weekly/month header; team roles per task, coloured; vault link + "flag lawyer" action API | feat/gantt-team-roles | crm/routes/gantt.py, static/js/gantt/*, static/css/gantt/*, templates/gantt.html, models/task_assignee.py (new), migration, tests/test_gantt_team.py |
| B | Deadlines on tasks + Calendar reflection check (and fix if not reflected) | feat/deadlines-calendar | crm/routes/calendar*.py, crm/models/calendar*, seed for deadlines, tests/test_deadline_calendar.py |
| C | Telegram + WhatsApp notification buttons (deep links now; Bot API send when env token set; opt-in, no real sends in tests) | feat/notify-buttons | crm/routes/notify.py (new), static/js/notify/*, templates partial, tests/test_notify.py |
| D | Harvey-style "Command Center" insights page: app-usage stats diagrams from real CRM tables | feat/insights-command-center | crm/routes/insights.py (new), templates/insights.html, static/js/insights/*, static/css/insights/*, tests/test_insights.py |
| E | LexFlow Agent: design + working spike of an agent living inside LexFlow (tool layer over REST, vault read, human gate, trace) | feat/lexflow-agent-spike | crm/agent/* (new), docs/agent/*, tests/test_agent_*.py |
| F | Product research note: key differentiating feature + LexFlow↔Lexroom integration options (no code) | none (vault note only) | ~/Obsidian/_Inbox/ only |
| T | Test phase: cross-test of every branch by an agent that did NOT build it; then Admy | integration/* | read-only |
Shared files (crm/__init__.py blueprint registration, templates/base.html nav): owner of the edit is **backend-dev at merge time** — builders add their blueprint registration on their own branch and list it in their hand-off; conflicts resolved by backend-dev in the integration branch.

# Questions for Admy and Smoothy
Admy: (1) Is the split correct for the roles of the Team (case owner / docs supply / legal assistant) in the real Studio workflow? (2) Allocation: which profile builds which WS, no overlap. (3) Risks for tenant isolation / prod. (4) Is Lexroom the right integration target vs alternatives? (5) What is the key feature you would add?
Smoothy: (1) Machine/runtime: can this box run ≥6 parallel agents + the 5057 server safely (CPU/RAM/disk, sleep)? (2) Telegram/WhatsApp: which bot/accounts/tokens already exist (references only, never secrets)? (3) Anything in PC settings needed (keep-awake, ports, firewall, launchd)? Ole explicitly authorises you to change settings needed for this.

# Decisions after Admy + Smoothy review (2026-10-24 evening)
- Machine: 8 GB M2, swap thrashing → max 3 concurrent builders, waves not parallel (Smoothy). Ports: A=5060 B=5061 C=5062 D=5063 E=5064; 5057 = backend-dev review server.
- Wave 1 (dispatched): A gantt-team-roles (backend-dev, DONE+tested, commit 5fc5554) · B deadlines-calendar (sales-crm) · C notify buttons, deep links first, separate LexFlow bot token, consent required, WhatsApp = wa.me only (crm-outreach-agent) · F research note (personal-assistant, no code).
- Wave 2 (serial, after merge+test): D insights (3-4 real diagrams, aggregates only) then E agent spike (chatbot_builder instead of operator-installer, depends on A + F).
- Lexroom: no public API → deep-link handoff + partnership request only (Admy).
- Key feature hypothesis (Admy): matter-stage checklist that tells the team/agent what is missing next — F evaluates it.
- Every WS: feature flag default off, tenant-scoped tables, no PII in analytics, persisted agent audit trace.

## Wave 1 result (2026-10-25)
- A (gantt team roles) + B (deadlines→calendar) + C (Telegram/WhatsApp buttons) merged LOCALLY into lexflow_hermes_v1 as 4ed492b (rollback tag `pre-merge-wave1-2026-10-25`); NOT pushed.
- Cross-tests: B tested by crm-outreach-agent → NO-GO (datetime filter 500, flag not a kill-switch, dead Delete/Edit on reflected calendar entries) → fixed; C tested via attack script → 1 MINOR fixed (non-integer member_id 500); Admy final gate → GO (28 pytest + 108 plain-script assertions, parity with base flags off, single alembic head i0d1e2f3a4b5, tenant isolation 26/26).
- Railway gate checklist: migrations to head on staging, flags enabled one at a time (CALENDAR_DEADLINES_ENABLED, NOTIFY_BUTTONS_ENABLED, GANTT_VIEW_ENABLED, GRAPH_VIEW_ENABLED, CONTEXT_NOTES_ENABLED), SECRET_KEY + JWT_SECRET_KEY set, separate LEXFLOW_TELEGRAM_BOT_TOKEN only when used. Agent-read path: doc names/contents/flag reasons are UNTRUSTED input.
- Infra lesson: OpenRouter credits exhausted (personal-assistant, sales-crm failed mid-run); `tester` profile has no model/key. Working profiles for builds/tests: chatbot_builder (nous), crm-outreach-agent, admy_ceo.
- Research note: [[LexFlow-Product-Research-KeyFeature-Lexroom-Agent-2026-10-24]]. Wave 2 (serial): D insights, matter-stage checklist (key feature), then E agent spike.

## Links
- Parent: [[LexFlow-Context-Graph-and-Gantt-Local-2026-10-24]]
- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]
