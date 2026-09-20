---
title: Hindsight Vault Sync — Fix Report 2026-09-16
created: 2026-09-16
author: memory-curator
tags: [hindsight, sync, launchd, incident, avibe-hq, memory-curator]
status: fixed
---

# Hindsight Vault Sync — Fix Report (2026-09-16)

Repair of the silently-broken Obsidian → Hindsight nightly sync
(launchd `com.avibe.obsidian-sync`, daily 06:00, bank `avibe-hq`).
No secret values are recorded here — references and file locations only.

## Root cause (one sentence)

Since 2026-08-27 the nightly `hindsight-obsidian-sync reconcile` call sent no
API credential (the bank returns HTTP 401 without one) **and** aborted on a
single vault file whose frontmatter carries the unresolved Obsidian placeholder
`date: {{date}}` (rejected by the API as HTTP 422) — and because the script used
`set -euo pipefail` with `OUTPUT=$(...)`, both errors exited the script before
anything was logged, so every run left only the 58-byte "Starting vault sync"
line.

### Failure mechanics, precisely

| Layer | Fact |
|---|---|
| Credential | Script passed no `--api-token`; `HINDSIGHT_API_TOKEN` was absent from every profile `.env`. Unauthenticated `POST /v1/.../memories` → `401 Invalid API key`. |
| Data | `01-Projects/AVibe-CRM/_from-repos/avibe-hindsight/obsidian/templates/hindsight-convo-template.md` (mirrored from the repo on 2026-08-26 18:47, i.e. **after** the last good run at 06:00) has `date: {{date}}`; the API answers `422 Invalid timestamp/event_date format: '{{date}}'`. The CLI aborts the **whole** reconcile on that error. |
| Logging | `exec > "$LOG" 2>&1` captured output, but `set -e` killed the script at the failing command substitution — the captured stderr was never echoed. Consequence: a silent failure with no error line. |
| Timeline | Last good run 2026-08-26 06:00 (index `lastSyncAt = 2026-08-26T04:00:36Z`). First silent failure 2026-08-27 06:00 — the day after the template mirror landed, one day **before** read-auth was enabled (2026-08-28), so the 422 was the original trigger and the missing token took over afterwards. |

## Fix applied (all reversible; originals backed up)

Files changed:

- `~/.hermes/profiles/operator-installer/scripts/obsidian-sync.sh`
  - backups: `obsidian-sync.sh.bak-20260916-144541` (original, pre-fix),
    `obsidian-sync.sh.bak-20260916-145554` (token fix, pre-exclude)
  - token resolved at runtime from `~/.hermes/profiles/operator-installer/hindsight/config.json`
    (the documented credential location) and passed as both `--api-token` and
    `HINDSIGHT_API_TOKEN`; no secret literal in the script
  - `set +e` around reconcile + explicit exit-code check → failures are now
    logged instead of swallowed
  - `--exclude "01-Projects/AVibe-CRM/_from-repos/avibe-hindsight/obsidian/templates/hindsight-convo-template.md"`
    — one placeholder skeleton, the only uninjestible file in the vault; the
    file itself is untouched
  - rolling status log `~/.hermes/profiles/operator-installer/logs/obsidian-sync-rolling.log`
    (one OK/FAILED line per run)

Not changed: the vault path, the bank name, the 06:00 schedule, and the plist
(backed up as `com.avibe.obsidian-sync.plist.bak-20260916-144541`, unmodified).

## Evidence

- Manual run (fixed script, main index): `+185 added, ~174 updated, -76 deleted,
  =22 unchanged` → exit 0, success line present.
- Index advanced: `~/.hindsight/obsidian/avibe-hq-avibe-hq-431cb7ef157b.json`
  `lastSyncAt` 2026-08-26T04:00:36Z → **2026-09-16T12:57:22Z**, 270 → 379 entries.
- Clean-environment run (`env -i HOME=$HOME /bin/bash obsidian-sync.sh`) and a
  `launchctl start com.avibe.obsidian-sync` run both exited 0 with `=381
  unchanged` — the token resolves without an interactive shell, and `launchctl
  list` shows exit status 0 (was 1).
- Historical gap closed: the main sync index now contains
  `01-Projects/LexFlow/LexFlow-Public-Intake-Contract-2026-09-15.md`,
  `01-Projects/LexFlow/LexFlow-Web-Site-Enrichment-Elisa-2026-09-13.md`,
  `05-Daily/2026-09-13.md`, `05-Daily/2026-09-15.md`, `05-Daily/2026-09-16.md`.

## Verification note

`_Inbox/hindsight-sync-verification-20260916.md` (marker
`HINDSIGHT-SYNC-MARKER-7f3a91c2-20260916`) was ingested and **retrieved from the
bank** the same day: `POST /v1/default/banks/avibe-hq/memories/recall` returns a
`world` fact for document `_Inbox/hindsight-sync-verification-20260916.md`
carrying the exact marker string (`memory_unit_count: 6`), and the same recall
path returns facts for `05-Daily/2026-09-15.md` and
`01-Projects/LexFlow/LexFlow-Public-Intake-Contract-2026-09-15.md` — the notes
from the historical gap. The note is disposable; it can be deleted once you no
longer need it.

## Open items

- The bank materialises retained documents asynchronously (LLM extraction, free
  model): ~370 vault documents queued at the fix took ~1 h to become retrievable
  and `pending_operations` peaked near 1300. Correctness is unaffected; only
  retrieval latency. Watch `pending_operations` if the bank ever looks "empty"
  right after a sync.
- Decision to ratify: skipping that one template file via `--exclude` (the file
  is a placeholder skeleton with no knowledge content; it stays untouched in the
  vault). Alternatives: fix the placeholder in the vault mirror + source repo, or
  exclude the whole `_from-repos` mirror tree from the sync. Revert = drop the
  `--exclude` line from the script.
- Standing rule: an unresolvable vault file must never be able to kill the whole
  reconcile silently — the rolling log + exit-code check now surface it.

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[Hindsight-Read-Auth-Runbook]]
- Related: [[hindsight-sync-verification-20260916]]
- See also: [[2026-09-16]]
