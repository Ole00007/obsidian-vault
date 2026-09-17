---
title: Downloads Stager blocked — TCC permission lost (2026-09-17)
type: incident
status: open — needs Ole (GUI)
date: 2026-09-17
owner: memory-curator
severity: medium (no data loss; daily staging blind)
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

## Links
- Parent: [[Obsidian-INDEX]]
- Related: [[_Meta-INDEX]]
- Related: [[05-Daily-INDEX]]
- Related: [[AGENT_RULES]]
