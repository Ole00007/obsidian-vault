---
title: LexFlow — session summary (26–27 Oct 2026) and operating blueprint for a power AI user
date: 2026-10-27
author: backend-dev (written at Ole's request; memory-curator to fold into the protocol)
status: DRAFT v1 — evidence from the sessions; assessment/ranking of agents is deliberately NOT done here (Ole: end of project / weekly cron)
tags: [lexflow, protocol, blueprint, working-style, agents, retrospective]
---

# 1. What happened (facts)
**26 Oct** — Elisa (in-app agent, renamed, website portrait bubble); clickable dashboard cards; "← Main site" on all pages; model-written summaries/drafts (provider-agnostic, opt-in); who-is-responsible on graph/Gantt/Kanban (owner + executor agent + collaborators + blocked-by + subagent run COUNT) via `GET /api/roadmap/bus`; Kanban follows the A–E blocked proposal; mobile 390 px overflow fixed on all pages; backup tag `backup-ui-bus-2026-10-26` + bundle in `~/projects/lexflow/_backups/`; locks for shared things (`~/projects/.locks/`: deploy, repo-move, port-5057, railway-vars); Fronty and Admy paused, T-019/T-021 closed.
**27 Oct** — "empty diagrams" = expired login (24 h JWT; pages show empty instead of redirecting). Fixed locally: superadmin never-expire login (opt-in env, default off, commit `ddec0aa`), local self-healing sign-in, 25 outstanding tasks refilled from the Kanban board + plan. Admy pushed `19b5401..396bea2` (deploy success, health 200); flags keep the new sections hidden on prod. Open: push `ddec0aa`, set 2 Railway flags (card `t_f4894d06`, Admy authorised to do it himself, asks Ole only for what only Ole can do). Harvey-like plan: estimate, pitch timing, brainstorm brief (see Links). Hindsight: decided not a risk.

# 2. How I (backend-dev) think and work — so you can predict and steer me
1. **Evidence before claims**: every "done" has command output (HTTP code, test count, sha). If I can't verify, I say so.
2. **Reproduce first**: the "empty diagrams" bug was reproduced with a bad token before any fix; the cause was not the data.
3. **Smallest reversible change, backup first**: tag + bundle + DB copy before risky work; opt-in flags default OFF so prod is unchanged.
4. **Delegate by cost and role**: cheap/gate/audit work → Admy; UI polish → Fronty; rules/profiles → Smothy; memory docs → memory-curator. I keep backend heavy lifting and the integration.
5. **One source of truth**: Kanban = who does what; roadmap JSON = plan status; Obsidian = knowledge. I add to them, never fork them.
6. **Honest limits**: infra crashes (worker timeouts) are reported as infra, not hidden.

# 3. How the team collaborates (current mechanics that worked)
- **Kanban board = agent bus.** One card per unit of work, body = exact paths + acceptance + report path; comments carry status; blocked = waiting on a human.
- **Locks** for the 4 shared resources (deploy only Admy; port-5057 only holder restarts; railway-vars; repo-move only when idle).
- **Gate chain**: builder ≠ tester → Admy gate → local merge → Ole sees it running → push/deploy.
- **Report-by-exception**: agents notify with one line + file path; Ole reads the file with the agent that wrote it.

# 4. What went wrong (and the fix to bake in)
| Problem | Cost | Fix |
|---|---|---|
| Roadmap JSON stale (last_updated 24 Oct; wrong executors) | graph shows wrong executors | daily status run must update it from the board; CEO owns |
| Worker crashes on infra (Kanban owner refused, 5 s timeout) → card "gave up" → blocked, silent | a day lost on the push | dispatcher alert + one auto-retry; owner of the board checks "gave_up" daily |
| Session expiry looked like data loss | morning panic | demo servers self-heal login; pages redirect to /login on 401 (TODO, small) |
| Two agents touching the same thing (Fronty/Admy/me on graph) | double work, conflicts | one owner per card, "surgical only" rule, pause others |
| Repo moved while working | broken paths | repo-move lock |
| Template cache needed restarts | many approvals | auto-reload on demo servers (hard rule, done) |

# 5. Best structure for MINIMUM involvement of Ole (proposal)
1. **Ole gives outcomes, not steps** ("be ready for the 13:00 demo", "public link for 3 lawyers"). One orchestrator turns it into cards.
2. **One orchestrator + one gatekeeper + specialists**: operator-installer (orchestrator, owns roster/rules/weekly review), Admy (CEO/gate/deploy), backend-dev, Fronty, memory-curator, Smothy only if his control role is not duplicated with operator-installer (earlier note: two orchestrator identities = single-source risk).
3. **Pre-approved lanes**: standing "yes" for local build/test/commit/branch/restore; Ole is asked only for: push/deploy of risky items, Railway/credentials, anything billing or legal. Everything else = act, then report in ≤10 lines.
4. **Ready-state definition on every card**: acceptance check + report path + who gates. No card without them.
5. **Proactive duty**: after each task the agent proposes the next one and creates the card (owner, parents) — Ole only reorders priorities.
6. **Weekly rhythm** (Ole's cron): per agent — cards done, cycle time, crashes, rework, idle days, cost; head of staff/CEO writes the review; improvement = a card (new skill/tool/prompt), found by researching available skills online. Under-active agent → named, given a concrete task or a skill, re-measured next week.
7. **Evidence in the review, not impressions**: use board runs (created/claimed/crashed/completed), commits, test counts.

# 6. Ole's working style (to preserve in memory)
Wants outcomes visible running locally, not described; broad delegated authority and unattended completion; direct paths/URLs; concise answers; hard stop on "pause"; wants agents proactive and autonomous; wants to learn how the agents think so he becomes a power AI user; weekly assessment of every participant; credit-aware but not token-starved.

# 7. Roster opinion (backend-dev's take)
Agree on fixing roles. Reduce only DUPLICATED control roles (orchestrator/CEO/head admin overlap) — that lowers cost (fewer handoffs, fewer contexts loaded). Do NOT merge specialists (backend/frontend/audit): bigger roles mean bigger contexts and more errors, so cost goes up. Rule: one owner per kind of decision.

# 8. Instructions for memory-curator
Fold sections 2–5 and the lessons into `[[LexFlow-Reusable-Build-Protocol-2026-10-25]]` (update in place, no duplicate note), add the working-style block to the user profile note, and keep this file as the dated source. Do not store secrets.

## Links
- Parent: [[LexFlow-Platform-Plan-2026-10-24]]
- Related: [[LexFlow-Reusable-Build-Protocol-2026-10-25]], [[LexFlow-Harvey-Like-Tools-Estimate-and-Pitch-2026-10-26]], [[LexFlow-Harvey-Brainstorm-Brief-2026-10-26]]
