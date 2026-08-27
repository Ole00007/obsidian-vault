# Obsidian Vault — Agent Rules of Engagement

> **Version:** 2.2  
> **Scope:** All Hermes agents operating on Ole's workspace  
> **Location of this document:** `~/Obsidian/AGENT_RULES.md` (symlink → `~/Obsidian/_Meta/AGENT_RULES.md`)  
> **Sanction:** Any agent that bypasses these rules is operating outside its authority.

---

## 1. Territorial Boundaries (Hard Limits)

### 1.1 Authorised Territory
All agents have **unrestricted read/write access** to:
- `~/Obsidian/` — the vault root
- All subdirectories and files inside `~/Obsidian/`
- Any folder created under `~/Obsidian/` — whether by Ole, by an agent, or by Obsidian itself

### 1.2 Forbidden Territory
No agent may **read, write, move, rename, or delete** anything outside `~/Obsidian/`, **including but not limited to**:

| Path | Why |
|------|-----|
| `~/Desktop/` | Personal workspace — off limits |
| `~/Documents/` | Contains personal documents not vetted for agent access |
| `~/Downloads/` | Staging area — agent may only access when explicitly directed, or via designated automated cron stagers into `_Inbox/` |
| `~/.hermes/` | Hermes agent configuration — agent already has access via tools, but must not create/delete files there except through its own tool operations |
| `~/Applications/` | System applications — never touch |
| Any path outside `~/Obsidian/` not explicitly granted in a task | Default: forbidden |

### 1.3 Exception Mechanism
If a task **requires** accessing a path outside `~/Obsidian/`:
1. The agent must state *which* path and *why* in its response.
2. The human (Ole) must explicitly approve.
3. The agent executes the single operation only — no scope creep.
4. After completion, the agent returns to the vault boundary.

---

## 2. Vault Structure & Conventions

### 2.1 Top-Level Folders (Standard Layout)

```
~/Obsidian/
├── _Inbox/           # Landing zone for every new file/note, human or agent-created (unprocessed)
├── _Templates/       # Note templates
├── _Meta/            # Vault config, plugin settings, backup rules, agent rules
├── 01-Projects/      # Active, logically named projects (e.g., LexFlow, Alena-Krot-Med-Expert)
├── 02-Areas/         # Ongoing responsibilities (SEO, CRM, personal)
├── 03-Resources/     # Reference, research, models, and setup guides
├── 04-Archive/       # Completed / cold storage
├── 05-Daily/         # Daily notes (YYYY-MM-DD format) - where staging logs sit
└── _Assets/          # Images, files attached to notes
```

### 2.2 File Naming & Properties

| Rule | Example |
|------|---------|
| Use kebab-case for multi-word files | `client-notes-onboarding.md` |
| No spaces in filenames (except daily notes) | `2026-08-13.md` ✅ |
| One sentence, no trailing period for titles | `# Competitor Analysis — Alena Krot` |
| Date prefix for time-bound notes | `2026-08-13-meeting-notes.md` |
| Underscore prefix for system/infrastructure | `_Templates/`, `_Inbox/` |

---

## 3. Workflow & Automation Rules

### 3.1 The Inbox Rule (Deduplicated)
- **Every new file entering the vault goes to `_Inbox/` first.** Nothing bypasses the inbox — not imports, not generated notes, not pasted content.
- **Scheduled Staging Cron:** A scheduled Hermes background stager runs **daily** to copy document downloads into `_Inbox/` (2026-08-26: `evening-downloads-stager` at 18:00; Hindsight-side sync runs 05:00 staging / 05:15 dedup / 06:00 launchd sync).
- **Deduplication Check:** If a file has the exact same name as one already inside `01-Projects/` or `02-Areas/`, the cron job is **strictly forbidden** from overwriting it. It must place the duplicate inside `_Inbox/_Conflicts/` and append a prominent warning flag in your **Daily Note** for manual action.

### 3.2 Saving Custom Voice Notes ("Voice note your answer")
- When Ole asks the agent to *"voice note your answer"*, the agent must generate the TTS `.mp3` file, save it directly to the active project folder (e.g., `01-Projects/LexFlow/`), and immediately trigger macOS to play it.
- **Transcription Lyrics:** The agent must automatically copy and paste the complete text of the voice note directly inside the active `.md` note (like song lyrics) or a companion `.md` file beside the audio, ensuring it is searchable and readable inside Obsidian.

### 3.3 Success & Template Prototyping
- Upon successfully completing a major milestone or deploying a project, the agent must proactively propose saving your clean, stripped-down workspace notes as skeletons or forms inside `_Templates/` for future reuse.

### 3.4 Inactivity & Silent Archiving (30-Day Threshold)
- **The 30-Day Check:** Hermes will inspect active directories weekly. Any note unchanged or unopened for **30 consecutive days** gets flagged in your Daily Note with a proposal to archive.
- **The 7-Day Silent Buffer:** If a note is proposed for archiving and you do not respond or reject the proposal within **7 days**, Hermes will automatically move it to `04-Archive/` and change its metadata to `status: archived`.
- **Strict No-Deletion Rule:** The agent is **never** allowed to permanently delete any active or archived note from disk without direct human instructions inside the chat.

---

## 4. Frontmatter (YAML) — Required on every note

```yaml
---
title: Note Title
created: 2026-08-13
tags: [tag1, tag2]
status: draft      # draft | active | review | archived
source: ""          # URL or origin, if applicable
project: ""         # Project name if note belongs to one
---
```

Frontmatter **must** be the first 3–6 lines of every note. The `status` field is mandatory so agents and filters can track note states.

---

## 5. Git & Deployment Boundary (hard, v1.0)

### 5.1 General Rule (all agents)
- Agents MAY freely: `git add`, `git commit`, create/switch branches, open pull requests. These are local/reversible.
- Agents MAY **NOT** run `git push` to any branch that triggers CI/CD deployment (main/master on repos with GitHub Actions → Railway/Netlify/Vercel hooks) without Ole's explicit, per-instance, in-session approval.
- Before requesting push approval, the agent must state: **repo name, branch, commit summary**, and **whether that branch has an active deploy hook**.

### 5.2 Exception — operator-installer (autonomous infra automation)
- `operator-installer` retains **autonomous `git push` rights** for infrastructure automation purposes (CI/CD config, deployment pipelines, Railway/Netlify automation, infra tooling).
- **However:** whenever `operator-installer` pushes to a branch that will trigger a deployment, it **must always draw Ole's utmost attention** and explicitly surface the deployment for permission before it proceeds. It must never deploy silently. The push may proceed autonomously, but a deployment that changes production must be flagged to Ole with highest priority so he can give permission / attention.

### 5.3 Scope
- This rule is **git/filesystem-scoped only** — it does **not** cover direct API writes to Railway, Airtable, Netlify, HubSpot, etc. (a separate rule, not yet defined — flag to Ole if a task would require one).

## 7. Wikilinks Rule (MANDATORY — all agents + Ole, 2026-08-26)

Every note created or edited in this vault MUST end with a `## Links` section
containing **at least 2 `[[wikilinks]]`**: one `Parent` (up to the project/area
hub note) and one `Related` (to a sibling/knowledge note). Never leave `[[]]`
empty. Load the `wikilinks` skill (with `obsidian`) for any vault write. The
goal: an emergent, connected knowledge graph — not a flat reference store.

---

## 6. Vault Boundary Rule (hard, v2.2)

### 6.1 General Rule (all agents)
- Work ONLY inside `~/Obsidian/` for all notes, memory, docs, and knowledge tasks, unless Ole explicitly approves otherwise in-session.
- Local code repos (`~/LexFlow-landing`, `~/LexFlow-Chatbot`, `~/aLEXy`, `~/Projects/*`) are a **SEPARATE layer**: agents may read/write code there during active dev tasks — this is normal and does **NOT** require vault-boundary approval.
- `~/Downloads`, `~/Desktop`, `~/Documents`, and any other non-vault, non-project path are forbidden without explicit in-session approval.
- New vault files land in `~/Obsidian/_Inbox/` first; never write directly into Projects/Areas/Resources.

### 6.2 Exception — operator-installer (DevOps paths)
- The vault rule above applies to notes/knowledge tasks.
- Additionally permitted, without per-instance approval: local install/deploy paths needed for DevOps work (package managers, Railway CLI config, `.env` files, infra tooling directories).

## Links
- Parent: [[Obsidian-INDEX]]

## Links
- Parent: [[_Meta-INDEX]]
