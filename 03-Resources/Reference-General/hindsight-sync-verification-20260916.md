---
title: Hindsight Vault Sync Verification 2026-09-16
created: 2026-09-16
tags: [hindsight, sync, verification, memory-curator]
status: test
---

# Hindsight Vault Sync — Verification Note (2026-09-16)

Temporary end-to-end verification note used to prove the repaired
Obsidian → Hindsight (`avibe-hq`) nightly sync actually ingests vault content.

Unique marker (search this string to retrieve this note from Hindsight):

    HINDSIGHT-SYNC-MARKER-7f3a91c2-20260916

Context: the launchd job `com.avibe.obsidian-sync` (daily 06:00) invoked
`hindsight-obsidian-sync reconcile` with no API credential, so every run from
2026-08-27 onward returned HTTP 401 and exited before logging — silently. The
credential is now resolved at runtime from the profile Hindsight config and the
reconcile exit code is checked explicitly, so failures are visible.

This note is disposable; it can be deleted once the sync is confirmed working.

## Links
- Parent: [[05-Daily-INDEX]]
- Related: [[Hindsight-Read-Auth-Runbook]]
- Related: [[Hindsight-Vault-Sync-Fix-2026-09-16]]
- See also: [[2026-09-16]]
