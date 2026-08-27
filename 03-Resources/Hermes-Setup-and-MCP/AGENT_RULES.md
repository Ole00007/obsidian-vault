# Obsidian Vault — Agent Rules of Engagement

> **Version:** 2.0  
> **Scope:** All Hermes agents operating on Ole's workspace  
> **Location of this document:** `~/Obsidian/AGENT_RULES.md`  
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
- **Evening Cron Job Staging:** A scheduled Hermes background stager runs every evening at **18:00 (6:00 PM)** to copy daily document downloads into `_Inbox/`.
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

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[Agent-Profiles]]
