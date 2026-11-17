---
tags: [hermes-infra, memory, decision]
project: Hermes
home: 03-Resources/Reference-General
---
# Hindsight OFF in all profile configs — 2026-11-17 (Ole, via backy)

Implements [[Decision-Memory-Layer-2026-11-04]] (Obsidian = memory, Hindsight paused) in config, not just in prose.

- Root `~/.hermes/config.yaml` + 20 profiles: `memory.provider: ''`, `hindsight` removed from `plugins.enabled`. Backups: `config.yaml.bak-hs-off-<ts>` next to each file.
- Not touched: `cron-sentinel`, `testy_tester` (no hindsight entries).
- Model provider: **nous** everywhere (verified); no OpenRouter, no fallbacks.
- Hindsight server/data untouched (nothing deleted). Re-enable = restore the .bak.
- Rule: no config edits while a chat is live on that profile; running chats keep Hindsight until restarted.

## For memy (memory-curator)
Treat vault as sole memory. Monthly derived sync (§17) stays low priority; do not rely on Hindsight recall.

## For admy (admy_ceo)
Coordinate: "taller" (Smoothy/ops) to propose ONE incremental architecture change (vault-only memory, nous-only models). No big-bang redesign.

## Links
- Parent: [[05-Daily-INDEX]]
- Related: [[Decision-Memory-Layer-2026-11-04]], [[Hermes-Fleet-Stability-Repair-2026-11-16]]
