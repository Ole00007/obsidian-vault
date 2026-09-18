# Agile Mode Note — Addressed to Admy, Smoothy, and Memo

**Purpose:** a short, standalone reminder to sit alongside `AGENTS.md`, `PROMPT_ADMY.md`, and `PROMPT_SMOOTHY.md`. This is not a new rule — it is a tone-setting clarification of how the existing plan should be held.

## The core message

We work in **agile mode**, not waterfall mode. The backlog, the dependency chains, the parallel swimlanes, and every date in the roadmap are a **working hypothesis**, not a contract. When reality diverges from the plan — an audit turns up a different field name, a dependency takes longer than expected, a task needs resequencing — that is normal, expected, and not a failure by anyone.

**No agent should treat a deviation from the initial plan as an incident to panic over, hide, or route around.** The correct response to "this isn't going the way the plan said" is to report it plainly and let the plan adjust — not to force the plan to be right retroactively, and not to freeze up waiting for perfect certainty before moving.

## What changes in practice

- Escalation questions (as defined in `PROMPT_ADMY.md` and `PROMPT_SMOOTHY.md`) are a **normal, healthy part of the workflow**, not a sign that something went wrong. Ask them freely and often.
- Missing a date, needing to resequence a task, or discovering a wrong assumption in `docs/ARCHITECTURE.md` or `docs/INTEROP_CONTRACTS.md` should be reported the same way a routine status update is reported — calmly, with facts, without over-apologizing or stalling.
- The plan is expected to be **adjusted, not defended**. If evidence says the roadmap needs to change, the roadmap changes.

## The regular review mechanism

There is a **standing cron-job-style review cadence** for the plan itself, not just for task status:

- **Admy** owns the decision of whether a plan adjustment is minor (handled inline, logged, and moved on) or significant enough to need explicit user approval.
- **Smoothy** flags any operational/technical drift he observes during building (Cloudflare config surprises, dependency delays, resequencing needs) into that same review rhythm, rather than quietly absorbing it.
- **Memo** is the one who actually runs the recurring review job: syncing what changed, what was adjusted, and why, into the audit/decision trail (`docs/DECISIONS.md` and the memory/Obsidian/Hindsight stack), so nothing gets lost even when the plan moves fast.

Together, Admy, Smoothy, and Memo are responsible for **communicating adjustments to the rest of the crew (Backy, Fronty, Daty, Crunchy, Sally, Mr. Beast, Smarty) whenever a change is significant enough that someone else's task, assumption, or dependency would be affected.** Not every micro-adjustment needs a broadcast — but anything that changes another agent's inputs, blockers, or expectations does.

## One-line summary to carry forward

**Plans bend, agents don't panic, Admy/Smoothy/Memo keep everyone informed, and the audit trail keeps up regardless of how fast things move.**
