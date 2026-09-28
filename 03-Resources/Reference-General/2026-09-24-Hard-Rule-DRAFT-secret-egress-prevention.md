---
title: Hard Rule DRAFT — Secret Egress Prevention (all profiles)
created: 2026-09-24
tags: [agent-rules, security, secrets, draft]
status: DRAFT — awaiting Ole approval
author: memory-curator
---

# Hard Rule DRAFT — Secret Egress Prevention

> **DRAFT for Ole's review.** Nothing has been propagated to the roster yet. Once approved this
> becomes a numbered hard rule in `_Meta/AGENT_RULES.md` (version bump) and a block in every
> profile's `SOUL.md` / `profile.yaml` description.

## Why this rule exists (evidence, 2026-09-24)

1. `Ole00007/obsidian-vault` is **PUBLIC** while holding client folders, 28 daily notes and `_Trash/`.
2. A **live Google Gemini API key** (`AIzaSyDR-i…`) is hardcoded in 2 tracked files
   (`01-Projects/AVibe-CRM/LexFlow/test_gemini.py`, `01-Projects/AVibe-CRM/aLEXy/test_gemini.py`),
   committed 2026-08-27 and present in `origin/main` → public for ~26 days, key not rotated.
3. The Downloads stager had **regressed**: the live script lost its `EXCLUDE_PATTERNS` credential
   guard that the vault backup still had, so a `client_secret_…googleusercontent.com.json` sitting
   in `~/Downloads` was a staging candidate. The vault auto-commits and pushes, so the next step
   would have been publishing an OAuth client secret.

## §S1 — Nothing enters the vault until it is scanned

- No agent may copy a file into `~/Obsidian/` without a filename **and** content scan for
  credential shapes first. Filename-only checks are insufficient.
- Excluded names (case-insensitive substring): `credential`, `secret`, `password`, `passwd`,
  `token`, `apikey`, `api_key`, `api-key`, `.env`, `.pem`, `.key`, `.ssh`, `client_secret`,
  `google_token`, `oauth`, `service_account`, `id_rsa`, `id_ed25519`, `.p12`, `.pfx`,
  `.keystore`, `.sqlite`, `.db`.
- Excluded content shapes (regex): `AIza[0-9A-Za-z_\-]{30,}` (Google),
  `sk-or-v1-…`/`sk-…` (LLM providers), `ghp_`/`gho_`/`github_pat_` (GitHub),
  `xox[baprs]-…` (Slack), `-----BEGIN [A-Z ]*PRIVATE KEY-----`,
  `postgres(ql)?://[^:]+:[^@]+@`, `eyJ[A-Za-z0-9_\-]{20,}\.` (JWT).

## §S2 — The vault is a publishing surface, not a folder

- Treat every write to `~/Obsidian/` as a **publication** until the vault repo is private.
- Never write a credential value into any vault note, not even "temporarily". Store a
  **reference** ("key in Railway var X", "key in 1Password") and the value goes nowhere else.
- `_Trash/`, `_Inbox/_Conflicts/` and `_Meta/` are inside the same repo — they are published too.
  "It's only in trash" is not a mitigation.

## §S3 — Secrets never travel through chat, notes, or manifests

- Never print, echo, log or summarise a secret value — not in chat, not in a manifest JSON,
  not in a daily note, not in a commit message. Report the **location**, never the value.
- Redact with `<REDACTED>`; include at most a 6-character prefix for identification.
- This applies to agent-to-agent reports, cron output and weekly digests.

## §S4 — Pre-push gate (every push, every repo)

- Before any `git push`, run a secret scan on the **staged diff and the commit range**, not just
  the working tree. A scan that only looks at the current files misses secrets already committed.
- A push whose scan hits is **aborted**, never "forced through" or retried after the guard fails.
- Treat a provider's secret-scan rejection (e.g. GitHub GH013) as a **success signal of the gate**,
  not a nuisance to work around: fix the finding, then push.

## §S5 — Retention beats deletion (history is forever)

- Deleting a file does not unpublish it: it stays in git history and in every clone.
- Therefore the only correct response to a leaked credential is **rotate/revoke it at the provider
  first**, then clean history. Cleaning history first is theatre.
- Never rewrite history on a branch that has been pushed without Ole's explicit approval, and
  never force-push a deploy-triggering branch.

## §S6 — Scripts that write to the vault must carry the guard

- Any script that ingests into the vault (`downloads_stager.py`, `organize_inbox.py`,
  `repo_sync.py`, `dedupe_vault.py`, …) MUST implement §S1 exclusions in code.
- A script edit that **removes** a credential guard is a regression: after every edit, re-verify
  the guard is present and byte-sync the vault backup copy.
- Verification line for any stager change: the run output must report a non-zero
  `excluded_sensitive` count when a known credential file is present in `~/Downloads`.

## §S7 — Prove it, don't assume it

- "It's in `.gitignore`" is not a control unless verified with `git check-ignore -v <path>` and a
  `git ls-files` check showing the file is untracked.
- Any claim that a secret is "not committed" must be backed by a scan of **`origin/main`**, not the
  local working tree.

## Enforcement / roles

| Who | Owns |
|---|---|
| operator-installer | pre-push gate in every repo + history-rewrite coordination |
| memory-curator | vault ingestion guards, .gitignore, weekly secret scan of the vault tree |
| each profile | §S3 in its own reports and cron output |
| Ole | key rotation, visibility changes, history-rewrite approval |

## Links
- Parent: [[AVibe-CRM-INDEX]]
- Related: [[2026-09-21-avibe-hindsight-network-egress-audit]]
- Related: [[2026-09-23-AVIBE-Ecosystem-Master-Table]]
- Related: [[Hindsight-Read-Auth-Runbook]]
