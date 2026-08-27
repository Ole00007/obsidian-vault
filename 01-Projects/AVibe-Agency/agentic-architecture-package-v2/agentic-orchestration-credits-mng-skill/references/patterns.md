# Visual Explanation Patterns

## 1. Iterated Architecture with Costs
Request (Airtable, free) -> Hermes orchestrator ($5-20/mo hosting) -> OpenRouter model routing (pay-per-task, cents) -> Composio tool connector (free/small fee) -> Airtable result (free/~$20/mo plan).
Always attach a cost banner: "Estimated total: ~$30-60/month + small pay-per-task AI fees."

## 2. Operational Orchestration for Cron Jobs
Timer -> Hermes wakes a fresh agent -> Agent does the job -> Result delivered.
Examples: daily competitor report, weekly Airtable cleanup, nightly backup check.
Key point: no human needs to press a button.

## 3. Swarm Pattern
One shared mission at the center, four roles around it (Planner, Builder, Reviewer, Reporter), all reading/writing one shared Obsidian memory vault.
Key point: multiple agents, one goal, no confusion.

## 4. Build-Test-Deploy Pipeline
Idea/Spec -> Build (Claude Code/Codex) -> Test -> Fix loop (auto-correct + retest) -> Deploy.
Hermes supervises every step and logs progress to Obsidian.

## 5. Other Job Types (extend as needed)
- Data/Ops jobs (Oracle + Airtable): scheduled sync, validation, reporting.
- Research jobs: Planner assigns research sub-tasks to Builder agents, Reviewer cross-checks sources, Reporter compiles findings to Obsidian/Airtable.

## Links
- Parent: [[references-INDEX]]
