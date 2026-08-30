# Hermes Starter Kit

Brief setup guidance for building Hermes agents with ideas borrowed from leading agentic systems.

## What this file contains

This file gives a practical starting stack, identifies useful prompt patterns to borrow, and shows where to inspect Hermes' own prompt assembly model.

## Start here

Hermes works best as a layered system rather than one giant master prompt. Use `SOUL.md` for stable identity and operating style, project context files for local rules, skills for repeatable procedures, and memory files for durable facts.[page:1]

## Recommended build order

1. Create a minimal `SOUL.md` for identity, verification, source quality, tool discipline, and secrets policy.[page:1][web:4]
2. Add `.hermes.md` or `AGENTS.md` inside each project for repo-specific instructions.[page:1]
3. Create a few reusable skills such as research briefing, PR review, competitor scan, and weekly reporting.[web:5][page:1]
4. Define a memory policy so only durable facts go into memory.[web:4][page:1]

## Useful patterns to borrow

| Pattern | Why it helps | Best home |
|---|---|---|
| Explicit agent loop | Keeps the agent action-oriented and iterative.[cite:1] | `SOUL.md` |
| Source-priority rule | Improves factual discipline in research tasks.[cite:1] | `SOUL.md` |
| Notify vs ask split | Reduces interruptions during long workflows.[cite:1] | `SOUL.md` |
| Todo discipline | Helps long tasks stay grounded.[cite:1] | Skill or workflow convention |
| Planner-style decomposition | Useful for complex jobs without bloating the global prompt.[cite:1][web:4] | Skill |
| Writing conventions | Good for report agents, but too narrow for a universal prompt.[cite:1][web:4] | Skill or context file |

## Where to inspect Hermes prompt behavior

Hermes does not publicly present a single static “master prompt” page. Its public documentation instead explains prompt assembly and the editable layers that feed the effective prompt seen by the model.[page:1]

The most useful public references are the prompt assembly docs, the Hermes repository, and the repo `AGENTS.md` guidance file.[page:1][page:2][page:3]

## Public links

- Prompt assembly docs: [Hermes Prompt Assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)
- Hermes repository: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- Repo guidance: [AGENTS.md](https://github.com/NousResearch/hermes-agent/blob/main/AGENTS.md)

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[Hermes_Obsidian_Windows_Install_Guide]]
