---
title: Downloads Stager blocked — TCC permission lost (2026-09-17)
type: incident
status: resolved 2026-09-18 18:03 CEST (stager green again; backfill run)
date: 2026-09-17
resolved: 2026-09-18
owner: memory-curator
severity: medium (no data loss; daily staging blind 09-16 → 09-18)
---

# Downloads Stager blocked — TCC permission lost

## What happened
The daily cron job **`downloads_stager.py`** (memory-curator, 18:00) failed today:

```
PermissionError: [Errno 1] Operation not permitted: '/Users/olesiarasing/Downloads'
  File ".../scripts/downloads_stager.py", line 73, in main
    for name in sorted(os.listdir(DOWNLOADS)):
```

No files were staged, no manifest was written. The script exits before it touches
`_Inbox`, so nothing was corrupted — it is a **blind run**, not a bad run.

## Evidence (reproduced this run, 2026-09-17 18:00 CEST)
| Probe | Result |
|---|---|
| `python3 downloads_stager.py --dry-run` | `PermissionError` — same traceback |
| `ls -la ~/Downloads` | `Operation not permitted` (dir itself is `drwx------@ olesiarasing staff`) |
| `mdfind -onlyin ~/Downloads 'kMDItemFSName=*'` | 0 results |
| `osascript … Finder …` | `Not authorised to send Apple events to Finder (-1743)` |
| `~/Obsidian/_Inbox` (vault side) | fully readable — the vault half of the job is fine |

## Root cause (high confidence)
TCC (macOS privacy) grants for `~/Downloads` are bound to the **code signature of the
responsible app**. The agent process tree is:

```
Hermes.app  (/Users/olesiarasing/.hermes/hermes-agent/apps/desktop/release/mac-arm64/Hermes.app)
  └── python -m hermes_cli.main dashboard  (PID 75631)
        └── shell → downloads_stager.py
```

`codesign -dv` on that bundle: **`Signature=adhoc`, `TeamIdentifier=not set`**.
Bundle mtime = **2026-09-15 11:44:05** — exactly **2 minutes after** the last
successful stager run (manifest `downloads_stager_2026-09-15.json`, 11:42:45, which
staged 2 files). Replacing an ad-hoc-signed bundle changes the identity macOS keys the
permission to, so the previously granted Downloads access was **silently revoked**.
Consistent with the missing manifests for 09-16 and 09-17.

## Impact
- Zero data loss: `~/Downloads` still holds everything; the stager is additive/copy-only.
- Loss of service: new Downloads have not reached `_Inbox/_Conflicts` review since 09-15.
- The script's own idempotence means a manual re-run after the fix recovers the backlog
  (window is 24 h by default — a re-run with `--hours 72` will pick up the gap).

## Proposed fix (tier-2 — infra/permission change, awaits Ole's go; not actioned)
1. **System Settings → Privacy & Security → Full Disk Access** → add
   `/Users/olesiarasing/.hermes/hermes-agent/apps/desktop/release/mac-arm64/Hermes.app`
   → toggle ON → quit and relaunch the app.
   (Alternative narrower path: *Files and Folders → Hermes → Downloads folder*, only if
   that entry is actually offered for this bundle.)
2. After relaunch, verify with:
   `python3 ~/.hermes/profiles/memory-curator/scripts/downloads_stager.py --dry-run`
3. Then backfill: same command with `--hours 72` (no `--dry-run`).
4. **Durable fix (recommended):** the app is rebuilt in place at a versioned ad-hoc path,
   so this will recur on every rebuild. Give the shortcut a stable home — symlink
   `~/Applications/Hermes.app` → the release bundle and grant FDA to the symlink target once,
   or move to a signed build. Do not create a second copy of the app (§9).

## Duplicate check (vault side, done in place of the Downloads scan)
`inbox_dup_scan.py` on `_Inbox` top level: **81 files, 1 byte-identical duplicate group**:

- `hermes-cloud-plan.csv` and `hermes-cloud-plan (1).csv` (identical, 1743 B each)

Per **archive-never-delete**, the `(1)` copy should be archived, not deleted — proposed, not
done, pending Ole's confirmation of which name is canonical.

## RESOLUTION (2026-09-18 18:00–18:05 CEST)

The Download TCC grant was re-established (by Ole, out of band). Verified by real runs:

- 18:00:24 daily cron run — `downloads_stager.py --hours 24` **succeeded**, 10 files staged, 0 errors, manifest written.
- 18:02:54 manual backfill — `downloads_stager.py --hours 72` staged **8 gap files** that the blind window (09-16 → 09-18) had missed:
  `-.csv`, `-bestshotever.csv`, `-bestshotever (1).csv`, `CANDIDATE-full-stack-rules-v0.2 (1).md`,
  `LexFlow-Hermes-Final-Execution-Prompt.txt`, `avibe_agency_legal_site_package.zip`,
  `hermes-cloud-plan (1).csv`, `lexflow_crm_cloudflare_plan.csv` — all md5-verified byte-identical to source.
- 18:03:48 vault-side dedupe (`inbox_dedupe_archive_only.py`, archive-only) — 3 byte-identical duplicate
  groups moved to `_Trash/_Deleted-Dupes-20260918_180348/_Inbox/`, canonical names kept.
  `_Inbox`: 93 → 101 → **98** files.

### Correction to the duplicate finding above
The 09-17 note claimed `hermes-cloud-plan.csv` **and** `hermes-cloud-plan (1).csv` were both in `_Inbox`.
Re-checked 2026-09-18: only `hermes-cloud-plan.csv` was in `_Inbox`; the `(1)` twin was still in
`~/Downloads`. The pair is byte-identical (`2634759c8c8968479aceb4d0a2d4473d`), so staging the `(1)`
copy just re-created a duplicate — it was archived again by the dedupe step. The 09-17 count
(81 files / 1 group) was therefore a stale reading of the `(1)`-suffix family, not of `_Inbox` itself.

### Residual risk (unchanged, NOT actioned — tier-2, needs Ole)
The app is still an **ad-hoc-signed** bundle at a versioned release path, so the next in-place rebuild
will silently revoke Downloads access again. Steps 1–4 under "Proposed fix" above are still the
recommendation; only step 1/3 were effectively done for this round.

## Links
- Parent: [[Obsidian-INDEX]]
- Related: [[_Meta-INDEX]]
- Related: [[05-Daily-INDEX]]
- Related: [[AGENT_RULES]]
