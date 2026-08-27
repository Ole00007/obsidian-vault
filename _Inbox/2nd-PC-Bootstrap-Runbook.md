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

> ⚠️ **IMPORTANT — authoritative source found:** the vault file
> `_Inbox/avibe_hindsight_setup_guides.xlsx` (sheet "Guide 1 — Connecting Your Other 3 Devices")
> contains the OFFICIAL device-setup procedure (via `hermes memory setup` selecting Hindsight,
> then Obsidian BRAT plugin). That is the canonical per-device Hindsight connection flow —
> **follow Guide 1 for the Hindsight connection; this runbook covers the vault/profiles layer
> Guide 1 does not.** It also mirrors the private spreadsheet Ole linked (which returns 401; the
> xlsx is the readable copy).

### 1. Get the vault onto the 2nd PC (pick ONE)
- **(a) Git (DONE on this Mac 2026-08-27):** vault is now a local git repo (commit `88e728d`,
  1005 files, secrets excluded via `.gitignore`). **Still needs a remote** to clone from —
  push to a private GitHub repo (requires token/ssh — see below) or copy the `.git` dir.
- **(b) Manual copy:** copy `~/Obsidian` via USB / cloud drive / `scp`. Simple, no merge history.
- **(c) Syncthing / iCloud:** ongoing two-way sync (more setup).

### 1b. Push to a private remote (to finish 1a) — PREPPED 2026-08-27
Status on this Mac:
- ✅ `gh` CLI installed (v2.98)
- ✅ SSH key generated: `~/.ssh/id_ed25519` (pubkey below)
- ✅ git SSH-prefers (`insteadOf`), credential helper = osxkeychain, global identity = Ole <olesyarasing@users.noreply.github.com>
- ✅ vault `origin` set → `git@github.com:olesyarasing/obsidian-vault.git`
- ⏳ **ONE manual step left (Ole):** add the public key to GitHub →
  **Settings → SSH and GPG keys → New SSH key** → paste:
  ```
  ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMI7UMy2QQHIKb8VNzRDYU6OphcXahj2ESk2q31Ijnqx olesiarasing-vault
  ```
- After adding: `ssh -T git@github.com` should say "Hi <user>!"; then `git push -u origin main` (creates the private repo on first push if it doesn't exist via the GitHub "create from push" behavior, or use `gh repo create obsidian-vault --private --source=. --push`).

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
