# Memory Policy v1 (goes to governance/memory/memory-policy.md)
## 1. System of record vs memory
- SoR = Postgres (via API). Memory (Obsidian, Hindsight later) = derived, rebuildable, may be stale.
- Memory suggests; Postgres decides. Before acting on any deadline, amount, party, status, conflict check: re-fetch by source_id.
- Agents write facts to the DB via API first; memory is refreshed after. Never the reverse.
- Example: note says hearing 3 Nov, DB says 10 Nov -> use 10 Nov, mark note stale.
## 2. Source IDs
`lf:<workspace_id>:<entity>:<uuid4>`; opaque only (see gdpr-opaque-uuid-rule.md). Stored in Obsidian frontmatter (+ Postgres memory_index at M1).
## 3. What goes where
| Content | Obsidian | GitHub |
|---|---|---|
| Rules, schemas, ADRs, templates | copy | YES |
| Matter summaries | YES (encrypted disk) | NEVER |
| PII, case text, secrets | avoid | NEVER |
## 4. Retention + deletion
Rules: config/retention.yaml, config/deletion-propagation.yaml. Periods TBD until lawyer/DPO confirms. Legal hold exempts purge. Erasure request overrides period.
## 5. Deferred (event-triggered, see triggers.yaml)
Hindsight bank per workspace (2nd tenant live), MCP/OAuth2 (tenant wants own agent), adapters (legacy CRM confirmed).
