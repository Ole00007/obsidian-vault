# Repo-Sync Stale Repo Paths — 2026-09-17

**Type:** proposal (not actioned) · **Owner:** memory-curator · **Status:** awaiting Ole / operator-installer confirmation
**Severity:** medium — the nightly repo→vault drift-minimizer is 80 % blind, and has been silently so since at least 2026-09-16.

## What is observed

`~/.hermes/profiles/memory-curator/scripts/repo_sync.py` (nightly 22:4x cron) walks a hard-coded
`ROOTS` map of working code repos and mirrors their doc files (`.md .csv .txt .json .yaml .yml .docx .xlsx .pdf`)
into the vault's `_from-repos/` mirrors. On **2026-09-16** and again on **2026-09-17** the dry-run printed:

```
[DRY]  skip (no repo): lexflow-crm
[DRY]  skip (no repo): LexFlow-landing
[DRY]  skip (no repo): LexFlow-Chatbot
[DRY]  skip (no repo): aLEXy
[DRY]  avibe-hindsight: updated=0 new=0 identical=5
[DRY]  TOTALS: updated=0, new=0, identical(no change)=5
```

4 of the 5 configured repos do not exist at the paths the script expects, so **only `avibe-hindsight` is
mirrored**. Drift is invisible: the run reports "0 updated / 0 new", which reads as "in sync".

## Verified reality (2026-09-17, `git rev-parse --short HEAD`)

| configured path (repo_sync.py) | exists? | real location found | HEAD |
|---|---|---|---|
| `~/Desktop/projects/services/LEGAL/lexflow-crm` | no | `~/Desktop/projects/services/LEGAL/LEXFLOW Production/lexflow-crm` | `6ef25da` |
| `~/LexFlow-landing` | no | `~/projects/LEGAL_backup/LexFlow-landing` (git repo) | `55d5488` |
| `~/LexFlow-Chatbot` | no | `~/projects/LEGAL_backup/LexFlow-Chatbot` (git repo) | `8a0e8a2` |
| `~/aLEXy` | no | `~/Desktop/projects/services/LEGAL/aLEXy` | `8ea18c2` |
| `~/Projects/avibe-hindsight` | yes (case-insensitive FS) | `~/projects/avibe-hindsight` | — works |

Other git repos seen in the LEGAL tree: `LEXFLOW Production/LEXFLOW Web-Site` (`4e526a0`),
`LexFlow-MVP` (`f1ad2d3`), `romanelli-studio SEO Audit LP` (`4a41399`).

Note the landed LexFlow CRM commit `6ef25da` is exactly the commit recorded in
[[LexFlow-Web-Site-CRM-Repoint-2026-09-17]] — the working checkout really is the `LEXFLOW Production/`
one, not the path the script points at.

## Why it was NOT auto-patched

1. **Secret-egress risk.** The mirror directory is inside the vault, and the vault is pushed to
   GitHub (`Ole00007/obsidian-vault`). Re-pointing the sync at `~/Desktop/projects/services/LEGAL/LEXFLOW Production/`
   widens the set of `.json` / `.txt` files copied into a git-pushed tree. Several vault outages
   already stem from exactly this class of leak (GH013 secret-scan rejection left the vault unbacked
   2026-08-24 → 09-04, see [[Incident-Downloads-Stager-TCC-Blocked-2026-09-17]] for the same family of incident notes).
2. **Two repos are genuinely ambiguous.** `LexFlow-landing` and `LexFlow-Chatbot` exist only as git
   repos under `~/projects/LEGAL_backup/` — the name says *backup*, so mirroring from them could
   overwrite newer vault mirrors with older content. That has to be confirmed, not guessed.
3. **Repo Root Rule §8.** The correct fix is repos at `~/projects/<repo>`, not a re-point to the
   frozen `~/Desktop` tree — and §8.2 puts the move itself in `operator-installer`'s hands.

## Proposed change (for approval)

**Option A — minimal, no new exposure (recommended now):**
add only the two unambiguous, verified working repos, and leave the rest untouched:

```python
os.path.expanduser("~/Desktop/projects/services/LEGAL/LEXFLOW Production/lexflow-crm"):
    os.path.expanduser("~/Obsidian/01-Projects/LexFlow/_from-repos/LexFlow-CRM"),
os.path.expanduser("~/Desktop/projects/services/LEGAL/aLEXy"):
    os.path.expanduser("~/Obsidian/01-Projects/aLEXy/_from-repos"),
```

then `--dry-run` to inspect every `UPD`/`NEW` path before any `--live`.

**Option B — correct long-term (§8-aligned):** migrate the four repos to `~/projects/<repo>`
(operator-installer, one vertical at a time, symlink grace week), then point `ROOTS` at `~/projects/`
only. Fixes the path *and* the TCC-protected-zone problem in one move.

**Option C — safety net regardless of A/B:** make the script print a hard WARNING and non-zero exit
when a configured repo is missing, so "0 updated" can never again mean "not looked at".

## Links
- Parent: [[Obsidian-INDEX]]
- Parent: [[LexFlow-INDEX]]
- Related: [[Incident-Downloads-Stager-TCC-Blocked-2026-09-17]]
- Related: [[LexFlow-Web-Site-CRM-Repoint-2026-09-17]]