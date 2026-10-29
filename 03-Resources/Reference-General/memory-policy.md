# memory-policy.md

**Source:** `/Users/olesiarasing/Downloads/memory-policy.md`  
**Vault location:** `/Users/olesiarasing/Obsidian/_Inbox/`

---

## System of Record vs Memory

- **SoR** = Postgres (via API). Memory (Obsidian, Hindsight later) = derived, rebuildable, may be stale.
- Memory suggests; Postgres decides. Before acting on any deadline, amount, party, status, conflict check: re-fetch by source_id.

## Source IDs

`lf:<workspace_id>:<entity>:<uuid4>`; opaque only. Stored in Obsidian frontmatter (+ Postgres memory_index at M1).

## What Goes Where

| Content | Obsidian | GitHub |
|---|---|---|
| Rules, schemas, ADRs, templates | copy | YES |
| Matter summaries | YES (encrypted disk) | NEVER |
| PII, case text, secrets | avoid | NEVER |

## Retention + Deletion

Rules: config/retention.yaml, config/deletion-propagation.yaml. Periods TBD until lawyer/DPO confirms. Legal hold exempts purge. Erasure request overrides period.

## Deferred

Hindsight bank per workspace (2nd tenant live), MCP/OAuth2 (tenant wants own agent), adapters (legacy CRM confirmed).

---

## Links

[[01-Projects]] → Parent folder hub  
[[03-Resources]] → Related sibling (resources category)