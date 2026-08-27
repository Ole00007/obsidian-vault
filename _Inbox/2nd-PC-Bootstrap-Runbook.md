---
title: 2nd PC Bootstrap Runbook
created: 2026-08-27
tags: [runbook, bootstrap, multi-device, 2nd-pc, hindsight, obsidian, provisioning]
status: active
---

# 2nd PC Bootstrap Runbook — get a new Mac/PC "on the same page"

> Purpose: provision a second device so it can pull the vault, run the Hermes agent roster,
> connect to Hindsight `avibe-hq`, and recall the same long-term memory as this machine.
> Created 2026-08-27 for the scheduled 2nd-PC test (calendar event + reminder).

## What a fresh PC needs (the 4 layers)

| Layer | What | Source (this Mac) | Status |
|---|---|---|---|
| 1. Obsidian vault | All notes/knowledge | `~/Obsidian/` — **NOT yet in git** | ⚠️ needs sync path |
| 2. Hermes profiles | 24 agent configs, skills, cron, SOUL rules | `~/.hermes/profiles/*` | ⚠️ needs copy/export |
| 3. Secrets | API keys, `HINDSIGHT_API_KEY`, bot tokens | `~/.hermes/.env`, password manager | 🔒 manual / password manager |
| 4. Hindsight connection | api_url + bank_id + key | `hindsight/config.json` + `.env` | ⚠️ needs config |

## Step-by-step

### 1. Get the vault onto the 2nd PC (pick ONE)
- **(a) Git (recommended):** `cd ~/Obsidian && git init && git add -A && git commit` on this Mac,
  push to a private repo (or a private GitHub repo), clone on the 2nd PC. Add a `.gitignore`
  for `.DS_Store`, `.obsidian/workspace*`. **Requires: this Mac git init + Ole approves the repo.**
- **(b) Manual copy:** copy `~/Obsidian` via USB / cloud drive / `scp`. Simple but no history/conflict merge.
- **(c) Syncthing / iCloud:** ongoing sync, both directions. More setup, live sync.

### 2. Install Hermes + copy profiles on the 2nd PC
- Install Hermes Agent (docs: hermes-agent.nousresearch.com).
- Copy `~/.hermes/profiles/` from this Mac → 2nd PC `~/.hermes/profiles/` (24 profiles with skills/cron).
- Copy `~/.hermes/skills/` (global skills incl. obsidian + wikilinks).
- Copy `~/.hermes/SOUL.md` + `config.yaml` (default instance).
- **Verify skills present:** `ls ~/.hermes/skills/note-taking/` → `obsidian`, `wikilinks` must exist.

### 3. Secrets (NEVER in git)
- Put API keys in the 2nd PC's `~/.hermes/.env` (same keys from the password manager).
- Critical: `HINDSIGHT_API_KEY`, `OPENROUTER_API_KEY`, any `*_API_KEY` the roster uses.
- Do NOT copy `.env` via git — copy via password manager / secure transfer.

### 4. Connect to Hindsight `avibe-hq`
- Create `~/.hermes/hindsight/config.json` on the 2nd PC:
  `{"mode":"local_external","api_url":"https://avibe-hindsight-production.up.railway.app","bank_id":"avibe-hq"}`
- Ensure `HINDSIGHT_API_KEY` is in the 2nd PC's `.env`.
- Verify: `curl https://avibe-hindsight-production.up.railway.app/health` → healthy.

### 5. The "same page" Hindsight test
1. On the 2nd PC, run a profile: `hermes -p memory-curator chat -q "Recall something from avibe-hq"`
   → it should pull shared memories.
2. Write a test note in the 2nd PC's vault → confirm it syncs to Hindsight (Obsidian → Hindsight).
3. Back on this Mac, recall that note → confirms both machines share the same memory.

### 6. Verify the roster is "on the same page"
- Both PCs should see the same: vault (same notes), skills (obsidian+wikilinks), rules (§V1-V4), Hindsight bank.
- Check: `grep "Vault & Knowledge Logging Rule" ~/.hermes/SOUL.md` on both → present.

## Known gaps to fix BEFORE this works fully
1. **Vault not in git** — the #1 blocker. Do step 1(a) or (c) first.
2. **Read-auth on Hindsight still open** (deferred) — a 2nd PC connecting is *more* reason to lock reads once it's live (multi-device surface = trigger D).
3. **No cross-device conflict merge** for the vault — two machines editing simultaneously can clash; git (1a) mitigates, or designate one machine as writer at a time.

## Safety
- Secrets via password manager, never git/chat.
- This is a **tier-2 setup task** — execute only with Ole present/approving.
- Reversible: nothing destructive; worst case re-copy the vault.
