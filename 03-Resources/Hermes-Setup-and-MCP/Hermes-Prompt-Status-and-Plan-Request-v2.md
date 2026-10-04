# Prompt for Operator-Installer (Hermes) — Status Report + Forward Plan (v2)

**Rule for this session (today only, until Olesia changes it): NO code changes, NO merges, NO deploys. Report and plan only. Every finding must include evidence (link, command output, or file reference) — no unverified "done" claims.**

**Working mode — agile, no rigid plan:** We are not committing to a fixed multi-phase roadmap with locked dates. Work incrementally, adapt as we learn. The one non-negotiable requirement: **every change and every decision must be traced with its reasoning** — what changed, why, what alternative was considered and rejected, and when. This tracing happens continuously, not as a one-time report. Log it in the Delegation_Tracking sheet / Obsidian as you go, not retroactively.

---

## A. Confirm current base state

You reported: "base cross-section reflection: intake → Contacts/Kanban/Calendar — done."
Before I accept this as done, show me:
1. The exact test/verification steps you ran to confirm this, per tenant (ws7, ws9, ws10+cl1+cl2).
2. Whether this was DEPLOYED (give live URL + commit hash) or only LOCAL (give preview link).

## B. Marketing/drip-campaign work — incremental, not a locked plan

We're building this step by step: conflict-check gate → first drip email → multi-step drip with suppression rules → client portal notifications → full Contacts segmentation/bulk email. Don't treat this as a fixed phase-gated waterfall — build the smallest useful piece first (conflict-check + one follow-up email), get it verified and traced, then decide the next increment based on what we learn. Report your recommended next-smallest-step, not a full 5-phase timeline.

## C. Scheduling engine — n8n is the primary path, Celery/RQ is the fallback to keep in mind

**Decision: we are opting for n8n (no-code automation, official Railway one-click template: railway.com/deploy/n8n) as the primary engine for delayed/multi-step scheduling (24h/72h/7d drip delays, suppression rules), instead of building this in Celery or RQ.**

Reasoning: n8n's built-in Wait/Schedule nodes solve the same delayed-job problem Celery/RQ would solve, without us writing and maintaining custom scheduling code — and it comes with 220+ pre-built integration nodes (email, CRM actions, communication) that we'd otherwise build by hand.

**But do not discard Celery/RQ entirely — flag it as the fallback option** in these specific cases:
- If n8n's execution model can't cleanly call back into our Flask/Postgres app with the tenant-isolation guarantees we need (workspace_filter, RLS).
- If n8n hosting/scaling cost on Railway becomes a problem at volume.
- If a specific automation needs tighter, lower-latency coupling to our own codebase than an external workflow tool allows.

Report: (1) your plan to connect n8n to our Flask backend without bypassing tenant isolation, (2) a short cost/complexity comparison n8n vs Celery/RQ specifically for our stack, kept brief since this isn't a locked decision — just enough to sanity-check the choice. (3) Under what condition would you recommend switching to Celery/RQ instead.

## D. WebMCP — expose CRM and website actions to agents natively

Add WebMCP (Model Context Protocol for the web — webmcp.dev, spec at github.com/webmachinelearning/webmcp) in two places:
1. **LexFlow website** — one script tag integration so any AI agent can interact with site forms/actions directly.
2. **CRM (Superadmin)** — expose CRM actions (create intake, update case status, query contacts) as WebMCP tools, so Elisa or any future agent teammate can act on the CRM through a standard interface instead of us writing bespoke API glue per agent.

Report feasibility and smallest first step (e.g. just the CRM read-only query tools first, before write actions).

## E. Agentic work JSON — locate, don't build

Where, if anywhere, does a structured JSON representation of agentic work (tasks, triggers, agent-identity tags) currently live in the CRM? Report the exact file/table if it exists. If it doesn't exist yet, say so plainly.

## F. Architecture audit — read-only comparison against your own repo

Compare the current documented architecture against your actual local repo directory structure. Report:
1. Full current repo directory tree.
2. For each existing feature: what matches the documented plan, what diverges, and why.
3. For features not yet built: confirm they still follow the agreed direction — flag any unapproved divergence.

READ-ONLY. Report only, do not reconcile.

## G. Sub-agent delegation — priority to existing profiles first

Before spinning up any new agent profile, check whether an existing one already fits:
- **Backend-dev** (already running, already has audit/cron access) — owns: Contact-model implementation plan, RLS test runs, n8n↔Flask connection design, tenant-isolation checks on any automation.
- **Chatbot builder** (the profile that already built the Alessia website chatbot) — owns: Elisa's build/wiring too. Same category of work (conversational agent, LLM routing, guardrails), just scoped to the CRM instead of the landing page — one profile, not two, to avoid re-solving the same LLM-fallback problems twice.

Report which of the above (A-F) each existing profile can take on right now, running in **isolated auxiliary branches** (clearly named, e.g. `aux/n8n-conflict-check`, `aux/webmcp-crm`), fully traceable.

Every sub-agent result must be:
- Tested and verified before being reported as done.
- Stability-ranked (experimental / stable / production-ready).
- Merged to `main` ONLY after cross-check against the base state confirmed in Section A — never merged directly by a sub-agent.

Only verified, cross-checked results get written to Obsidian, with the reasoning trace (Section intro) attached — not just the outcome.

## H. Ownership and knowledge continuity

You (Operator-Installer) remain project owner. Prepare a transfer package — memory, skills, accumulated knowledge — that could be handed to an orchestrator profile for future projects, OR propose renaming/extending your own profile to formally take on that role. Report your recommendation; do not act on it yet.

---

**Reminder: this entire prompt is a reporting and planning request. Wait for Olesia's explicit approval before touching any code, branch, merge, or deploy. Trace every decision and its reasoning continuously as you go — this is not optional and not a one-time report.**
