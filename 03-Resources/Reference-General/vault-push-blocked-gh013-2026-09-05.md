---
title: Vault push blocked — GH013 Google OAuth secret in history (2026-09-05)
created: 2026-09-05
tags: [alert, security, vault, github, oauth, leak]
status: partially-resolved
priority: high
---

# Vault push blocked — GH013 Google OAuth secret in history

> **Action required from Ole.** Cron detected this 2026-09-05 22:31. Push is currently broken until history is rewritten and the credential is revoked.

## What happened

The nightly `git_autocommit.sh` run on **2026-09-04 22:30** (commit `7cf4e6d`) staged and committed a Google OAuth client credential file:

```
_Trash/_Deleted-Dupes-20260902_222529/_Conflicts/client_secret_REDACTED.apps.googleusercontent.com.json
```

Contents:

```json
{"web":{"client_id":"REDACTED.apps.googleusercontent.com",
        "project_id":"modular-sign-507311-p7",
        "client_secret":"GOCSPX-REDACTED", ...}}
```

The file is also still present in `~/Obsidian/_Inbox/` (untracked-by-design). Tonight's cron (2026-09-05 22:31) committed locally (`ec783f7`) and tried to push — **GitHub push-protection (GH013) blocked the entire push** because commit `7cf4e6d` still contains the secret.

The local secret-guard regex in `git_autocommit.sh` (line 10) only checks:
```
api-keys|ORACLE_VPS_CREDENTIALS|debug_token|\.db$|\.env$
```
It does not match `googleusercontent`, `client_secret`, generic `*.json`, or many other common secret patterns. **The local guard is the primary defense and is too narrow.**

## Recommended remediation (in order)

1. **Revoke the leaked OAuth credential immediately** in Google Cloud Console:
   - Project `modular-sign-507311-p7`
   - APIs & Services → Credentials → OAuth 2.0 Client IDs → `...201026737817...`
   - Click **Reset secret** (or delete the client and create a new one)
   - This is mandatory regardless of history cleanup — once pushed to a Git remote it is considered leaked even if no one cloned it.
2. **Remove the file from working tree** (it's been promoted by the dedupe process but the cron keeps re-adding it):
   - `rm ~/Obsidian/_Inbox/client_secret_201026737817-...apps.googleusercontent.com.json`
   - `rm ~/Obsidian/_Trash/_Deleted-Dupes-20260902_222529/_Conflicts/client_secret_201026737817-...apps.googleusercontent.com.json`
3. **Strip the file from git history** with `git filter-repo`:
   ```bash
   cd ~/Obsidian
   git filter-repo --invert-paths \
     --path-glob '*googleusercontent*' \
     --path-glob '*client_secret*'
   git push origin main --force
   ```
   (Alternative: BFG Repo Cleaner — `bfg --delete-files '*googleusercontent*'`)
4. **Patch `git_autocommit.sh` secret-guard** (line 10) to add patterns:
   ```bash
   'api-keys|ORACLE_VPS_CREDENTIALS|debug_token|googleusercontent|client_secret|\boauth\b|credentials|\.env$|\.db$|\.pem$|\.key$|\.p12$|service-account'
   ```
   Also add a `gitleaks` or `trufflehog` pre-commit scan if available.
5. **Audit other recent auto-commits** for similar leaks:
   ```bash
   cd ~/Obsidian && git log --all -p --name-only | grep -iE 'secret|token|api[-_]?key|credential'
   ```
6. **Add the pattern to `.gitignore`** so future dedupe runs can't surface it into the working tree:
   ```
   *_googleusercontent*.json
   *_client_secret*
   *_credentials*.json
   *_oauth*.json
   *.pem
   *.key
   ```

## Why this matters

- The vault repo is **private**, so exposure window is limited to anyone with repo access + GitHub staff.
- However, the OAuth `client_secret` is **a long-lived bearer credential** — it does not expire and can be used to mint Google API tokens for the `modular-sign-507311-p7` project until revoked.
- If the project `modular-sign-507311-p7` is in active use (any production app relying on Google sign-in / APIs), the credential must be revoked NOW.

## Status

- [ ] **Ole: revoke OAuth credential — STILL OPEN, mandatory.** Google Cloud Console → project `modular-sign-507311-p7` → APIs & Services → Credentials → OAuth 2.0 Client IDs → `...201026737817...` → **Reset secret**.
- [x] ~~Ole: delete local copies of the file~~ — done 2026-09-16 by the history rewrite (both copies removed from disk and from git history).
- [x] ~~run `git filter-repo` + force-push~~ — **done 2026-09-16 22:45 without needing a force-push**: all 6 offending commits were local-only, so `git filter-branch --tree-filter` rewrote only local commits and the plain `git push` succeeded (`7d0eb02..3b4c053`).
- [ ] Ole: approve patch to `git_autocommit.sh` regex + exit-code check — **proposed 2026-09-16, not wired** (waiting on Ole's "share here first before wiring" rule).
- [x] ~~Re-run nightly cron to verify clean push~~ — done 2026-09-16 22:45, clean push verified.

## Resolution (2026-09-16 22:45, memory-curator cron)

Root cause of the 11-day outage: `git_autocommit.sh` never checked the exit code of `git push`. From 2026-09-04 onward it printed `[git-autocommit] pushed at …` on every run while GitHub rejected every push with GH013, so the vault silently accumulated 6 unpushed commits.

- Safety ref before the rewrite: `backup/pre-gh013-20260916` → `849c9de` (local-only; **contains the live secret — delete after the credential is revoked, never push it**).
- Rewrite: `git filter-branch --tree-filter` over `origin/main..main` — deleted both `client_secret_….json` copies and redacted this note via `~/.hermes/profiles/memory-curator/scripts/redact_gh013.py`.
- Verification: zero residual matches for the client_id/client_secret across every rewritten commit before pushing.
- Note: this alert note had itself been re-committing the credential in plain text (lines 24–26). Incident notes must show `GOCSPX-REDACTED`, never the real value.

## Links

- Parent: [[05-Daily/2026-09-05]]
- Related: [[AGENT_RULES]] § Git & Deployment Boundary
- Related: [[vault-security-baseline]]