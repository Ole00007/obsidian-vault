---
title: Kanban cross-card closure — worker scope guards and the 3 closed LexFlow vault-logging cards
created: 2026-09-16
tags: [hermes, kanban, board-hygiene, trust-boundary, lexflow, vault-logging]
status: active
source_card: t_f3c6dee2
---

# Kanban cross-card closure — worker scope guards

Board-keeping note from card `t_f3c6dee2` (operator-installer). Records how three
stuck cards were closed, the runtime guard that blocks agents from doing it, and the
side findings that came with the closure.

## 1. What was closed (verified before closure)

Three vault-logging cards sat in `blocked` although the work itself was finished
(logged 2026-09-16 by memory-curator under `t_a261ac01`). Each artifact was re-read
from disk before any status change, not taken on trust:

- `t_c421f430` — `~/Obsidian/_Inbox/LexFlow-Web-Site-Agent-Surface-2026-09-15.md`
  exists (4755 B; frontmatter `source_card: t_c421f430`, `commit: b9b406a`) and
  carries all six agent-surface items (ai-plugin.json, openapi.yaml, webmcp.js 6
  tools, llms.txt, JSON-LD, 48-URL sitemap).
- `t_6c2c8c07` — cross-check section `2026-09-13 recap cross-check (added 2026-09-16,
  card t_6c2c8c07)` present at line 104 of
  `01-Projects/LexFlow/LexFlow-Web-Site-Enrichment-Elisa-2026-09-13.md`.
- `t_76668155` — `~/Obsidian/_Inbox/LexFlow-Web-Site-Session-Recap-Batch2-2026-09-13.md`
  exists (4601 B, 97 lines; `source_card: t_76668155`, `commit: 63f46d4`).

All three are now `done` with handoff results naming this card as the closer. No
further vault work is outstanding on any of them.

## 2. The guard: agents cannot close a sibling card

Both agent surfaces fail closed on cross-card mutation, and this is by design:

- **Tool layer** — `tools/kanban_tools.py` `_worker_guard`: a worker is scoped to
  `$HERMES_KANBAN_TASK`; passing another `task_id` is rejected ("worker is scoped to
  task X; refusing to mutate Y"). `kanban_comment` on another card IS still allowed —
  that and `kanban_create` are the sanctioned handoff channels.
- **Durable layer** — `hermes_cli/kanban_db.py::_assert_not_delegated_child_mutation`
  rejects every `write_txn` from a delegate-child / worker-descendant context. The
  marker `HERMES_DELEGATED_CHILD_CONTEXT=1` is deliberately propagated into a worker's
  shell, so even shelling out to `hermes kanban complete …` is refused there.

Consequence: a card whose body says "close sibling card X" is **unsatisfiable from a
dispatched worker**. The correct terminal action for such a card is `kanban_block`
with a one-line instruction for the operator, or better, the spawning agent should
route the closure to a human/operator CLI session in the first place. `hermes kanban
edit` exists to backfill a wrong result on an already-done task — the recovery path
used here.

## 3. Crash pattern behind the backlog

All three cards had been stuck by the same failure, also seen on `t_62db7c26`:
worker exits `rc=0` **without** calling `kanban_complete` / `kanban_block` — a
protocol violation, counted twice before the card goes `blocked`. When sweeping
blocked cards, check the diagnostics block first: a card with that error usually
needs its *own* worker re-run (unblock → dispatcher respawns it), not a cross-card
close by someone else.

## 4. Side findings for Ole (unresolved, ownership questions)

- `lexflow.netlify.app` answers **401 behind Netlify password protection** —
  ownership unverified; log into Netlify and confirm whether this is an orphaned
  deploy of ours.
- The new LexFlow Web-Site repo **deploys nowhere**: no git remote, no
  `netlify.toml` / `vercel.json` / `wrangler.toml`.
- The only live LexFlow marketing surface is the legacy LP at
  `poetic-kleicha-28d058.netlify.app`; the live CRM is `web-production-031a6`
  (see [[LexFlow-Ecosystem-Index-v3-2026-09-16]]).
- `lexflow.pages.dev` is **not ours** (different company) — do not treat it as
  a LexFlow surface.

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Ecosystem-Index-v3-2026-09-16]]
- Related: [[LexFlow-Web-Site-Agent-Surface-2026-09-15]]
- Related: [[LexFlow-Web-Site-Session-Recap-Batch2-2026-09-13]]