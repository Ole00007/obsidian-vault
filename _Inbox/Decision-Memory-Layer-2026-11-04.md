---
tags: [decision, memory, rules]
project: agent-ops
home: _Meta
status: active
reversible: true
---

# Decision: Obsidian is the memory, Hindsight is paused (2026-11-04)

**Decided by:** Ole, 2026-11-04. **Reason:** cost saving. **Reversible:** yes, revisit any time.

## Decision
- **Obsidian is the single source of truth** and the only memory every agent reads at session start.
- **Hindsight (`avibe-hq`) is paused as a live memory.** No agent may depend on it. The monthly derived sync in AGENT_RULES §17 stays low priority. Nothing in Hindsight is deleted.

## Every session start (all active agents)
Read, in this order: `~/Obsidian/_Meta/AGENT_RULES.md`, the project-status note (`~/Obsidian/01-Projects/LexFlow/LexFlow-Project-Status.md`), today's Daily note `~/Obsidian/05-Daily/YYYY-MM-DD.md`. Owner of project status: memory-curator (Memy).

## What moves over from Hindsight
Hindsight holds no decision that is not already in the vault, except what Memy's last reconcile finds. Memy exports those as notes into `~/Obsidian/03-Resources/` before the switch.

## To revert
Re-enable the monthly sync (`com.avibe.obsidian-sync`), then run one full reconcile. Review trigger: Obsidian recall quality drops, or Hindsight costs fall.

## Links
- Parent: [[_Meta-INDEX]]
- Related: [[Obsidian-INDEX]]
