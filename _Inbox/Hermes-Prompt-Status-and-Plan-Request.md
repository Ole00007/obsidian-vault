# Prompt for Operator-Installer (Hermes) — Status Report + Forward Plan
**Rule for this session (today only, until Olesia changes it): NO code changes, NO merges, NO deploys. Report and plan only. Every finding must include evidence (link, command output, or file reference) — no unverified "done" claims.**

---

## A. Confirm current base state

You reported: "base cross-section reflection: intake → Contacts/Kanban/Calendar — done."
Before I accept this as done, show me:
1. The exact test/verification steps you ran to confirm this, per tenant (ws7, ws9, ws10+cl1+cl2).
2. Whether this was DEPLOYED (give live URL + commit hash) or only LOCAL (give preview link).

## B. Marketing/drip-campaign roadmap — plan only, do not build yet

We are scoping a 5-phase incremental rollout. Report your assessment of each phase: feasibility, estimated time, and what could realistically run in parallel via delegated sub-agents vs. what must be sequential.

- **Phase 2:** Conflict-check gate + first drip (one follow-up email at 24h). Real marketing value for law firms — prioritize this first.
- **Phase 3:** Multi-step drip (24h / 72h / 7 days) + suppression rules so a contact who already replied is never re-sent a follow-up.
- **Phase 4:** Client portal notifications — case status changes become visible to the client.
- **Phase 5:** Full Contacts segmentation + bulk email, integrated with the Contacts redesign already delegated to backend-dev.

For each phase, report: dependencies on earlier phases, which tenant should pilot it first (default: Romanelli), and whether it touches shared code paths (sequential-only) or can be built in isolation (parallel-safe).

## C. Celery/RQ evaluation

Evaluate and report — do not implement:
- Estimated implementation time and cost (dev hours) to introduce Celery or RQ for reliable multi-step drip scheduling (24h/72h/7d delays need durable job scheduling, not simple cron).
- Which one fits better given our current Railway + Flask + Postgres stack, and why.
- What breaks or needs migration if we adopt this now vs. deferring.

## D. Agentic work JSON — locate, don't build

Where, if anywhere, does a structured JSON representation of agentic work (tasks, triggers, agent-identity tags) currently live in the CRM? Report the exact file/table if it exists. If it doesn't exist yet, say so plainly — do not describe a plan as if it were already built.

## E. Architecture audit — read-only comparison against your own repo

Compare the current documented architecture (as discussed with Olesia/Perplexity) against your actual local repo directory structure. Report:
1. Full current repo directory tree (so this can be visually compared going forward).
2. For each existing feature: what matches the documented plan, what diverges, and why (plus/minus assessment).
3. For features not yet built: confirm they still follow the previously agreed plan — flag anything where your repo structure suggests a different approach was taken without sign-off.

This is READ-ONLY. Do not reconcile or fix any divergence found — just report it.

## F. Sub-agent delegation for parallel work

Report which of the above (A-E) can be delegated to sub-agents right now, running in **isolated auxiliary branches** (clearly named, e.g. `aux/phase2-conflict-check`, `aux/celery-eval`), fully traceable. Every sub-agent result must be:
- Tested and verified before being reported as done.
- Stability-ranked (e.g. experimental / stable / production-ready).
- Merged to `main` ONLY after cross-check against the base state confirmed in Section A — never merged directly by a sub-agent.

Only verified, cross-checked results get written to Obsidian. Unverified or in-progress work stays out of the vault.

## G. Ownership and knowledge continuity

You (Operator-Installer) remain project owner. Separately: prepare a transfer package — memory context, skills, and accumulated knowledge from this project — that could be handed to an orchestrator profile for future projects, OR propose renaming/extending your own profile to formally take on that orchestrator role. Report your recommendation; do not act on it yet.

---

**Reminder: this entire prompt is a reporting and planning request. Wait for Olesia's explicit approval before touching any code, branch, merge, or deploy.**
