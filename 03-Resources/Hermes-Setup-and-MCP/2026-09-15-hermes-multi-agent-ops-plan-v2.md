---
type: decision
project:
  - LexFlow
  - AVibe Agency
status: verified
owner: Olesia
created: 2026-09-15
updated: 2026-09-15
review_date: 2026-09-29
tags:
  - hermes
  - cloud
  - agents
  - software-factory
  - multi-provider
  - risk-register
  - ops
  - auth-fix
  - obsidian-architecture
supersedes: 2026-09-15-hermes-multi-agent-ops-plan
---

# Hermes multi-agent ops plan v2: Cloud, Software Factory, multi-provider, auth fix

This is the iterated reference doc. New content this revision: folder-numbering rationale, memory-curator audit prompt, the enforced worktree pre-flight rule, the Nous auth repair sequence, and the profile-distribution setup path.

## 1. Hermes Cloud — verdict (unchanged)

Confirmed pay-as-you-go, billed from Nous credit balance. Do not deploy Cloud yet. Revisit only after LexFlow and AVibe deployments are stable and a specific scheduled/asynchronous job is identified.

## 2. Software Factory — verdict (unchanged) + enforced rule (new)

Confirmed with one correction: Git refuses to check out the same branch in two worktrees at once (`fatal: '<branch>' is already used by worktree at '<path>'`). This is now enforced with a pre-flight script, not just documented as a caution.

### Pre-flight script: `safe-worktree-add.sh`

Save this on ASUS at `~/projects/lexflow/scripts/safe-worktree-add.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$HOME/projects/lexflow/lexflow-main"
WORKTREE_ROOT="$HOME/projects/lexflow/worktrees"
BRANCH_NAME="$1"      # e.g. feat/LF-030-fix-nav
TASK_SLUG="$2"         # e.g. LF-030-fix-nav

cd "$REPO_DIR"
git fetch origin --prune

if git worktree list | grep -q "\[$BRANCH_NAME\]"; then
  echo "BLOCKED: branch '$BRANCH_NAME' is already checked out in a worktree."
  git worktree list
  exit 1
fi

if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
  echo "BLOCKED: local branch '$BRANCH_NAME' already exists. Choose a unique task ID."
  exit 1
fi

TARGET_PATH="$WORKTREE_ROOT/$TASK_SLUG"
if [ -d "$TARGET_PATH" ]; then
  echo "BLOCKED: worktree path '$TARGET_PATH' already exists."
  exit 1
fi

git worktree add -b "$BRANCH_NAME" "$TARGET_PATH" origin/main
echo "OK: worktree created at $TARGET_PATH on branch $BRANCH_NAME"
```

Make it executable once:

```bash
chmod +x ~/projects/lexflow/scripts/safe-worktree-add.sh
```

**Orchestrator rule (mandatory)**: the orchestrator profile must call this script for every new task instead of running `git worktree add` directly. Never bypass it, even for "quick" tasks.

```bash
~/projects/lexflow/scripts/safe-worktree-add.sh feat/LF-030-fix-nav LF-030-fix-nav
```

Cleanup after merge:

```bash
git worktree remove ~/projects/lexflow/worktrees/LF-030-fix-nav
git branch -d feat/LF-030-fix-nav
git worktree prune
```

## 3. Multi-provider Hermes profiles — verdict (unchanged)

Confirmed possible: Nous Portal and OpenRouter can run on different profiles simultaneously. Risk confirmed to have materialized this session (see section 5).

## 4. Nous Portal auth — broken and fixed this session

**Symptom**: only frontend-dev work was still running; other profiles lost Nous access after an auth reset. Root cause is a known Hermes bug — refresh-token rotation isn't always persisted, so after roughly 4–10 days of runtime the pool returns `invalid_grant: Refresh token reuse detected`. Because profiles can share the same Nous OAuth session, one profile's failed refresh can lock out others relying on that same login.

### Fix sequence (run in this order)

```bash
hermes auth list nous
hermes auth reset nous
hermes auth add nous --type oauth
hermes portal info
```

Then confirm each affected profile individually — do not assume a global fix propagated:

```bash
hermes -p orchestrator auth status nous
hermes -p lexflow-reviewer auth status nous
```

If a specific profile still shows logged out after the above, re-run OAuth scoped to that profile:

```bash
hermes -p <profile-name> auth add nous --type oauth
```

**Prevention going forward**: if isolation between profiles matters more than convenience, use separate Nous logins per profile instead of one shared session — trades a repeated OAuth step for immunity to this shared-token failure mode.

## 5. Profile distributions — package once, clone to ASUS

Official docs: `https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions`

Open that page, then:
1. Read the "Distribution manifest" section for the exact `distribution.yaml` schema.
2. Click through to the linked example repo if you want a working reference before writing your own.

### Setup commands (run on MacBook, current working profile)

```bash
cd ~/.hermes/profiles/<your-profile-name>
cat > distribution.yaml <<'EOF'
name: lexflow-agent-distro
version: 0.1.0
EOF

git init
git add -A
git commit -m "Initial LexFlow agent distribution"
git remote add origin <YOUR-NEW-GITHUB-REPO-URL>
git push -u origin main
```

### Install on ASUS

```bash
hermes profile install <YOUR-NEW-GITHUB-REPO-URL> --alias
```

### Faster alternative if you don't need a shareable repo yet

```bash
hermes profile create lexflow-builder --clone
```

This copies `config.yaml`, `.env`, `SOUL.md`, skills, and curated memory only — it deliberately excludes sessions, `state.db`, and cron jobs, so a clone never double-fires the source profile's scheduled jobs.

## 6. Memory-curator prompt — Obsidian architecture audit

Run this as a task brief for the `memory-curator` profile. Deliverable is an **audit and recommendation**, not an automatic restructure.

```md
---
task_id: MC-001
profile: memory-curator
type: audit
status: ready
production_access: false
---

## Task

Audit the current Obsidian vault architecture end to end:
- Folder structure and numbering (PARA / Johnny-Decimal-style areas)
- Separation between personal PARA/Zettelkasten notes and agent-generated
  content (80 Agent Ops area)
- Existing Dataview queries and Templater templates
- How Hindsight (Railway) content currently surfaces into Obsidian, if at all
- Any orphaned, duplicated, or stale notes from prior Hermes sessions

## Purpose of the audit

We are running a multi-agent "software factory" (isolate -> build -> prove ->
review -> ship) across two devices (MacBook orchestrator, ASUS builder/tester/
reviewer), with a growing set of Hermes profiles. Determine whether the
current vault structure can cleanly support:

1. Per-task evidence storage (screenshots, test logs, before/after proof)
   without cluttering personal notes
2. Traceability from a task ID to its branch, PR, evidence, and final decision
3. A clear boundary so agents never write into personal PARA/Zettelkasten
   areas
4. My own (non-agent) research and business-planning workflow remaining
   fast and uncluttered as agent volume increases

## Deliverable

Write a single audit note to:
`80 Agent Ops/Hermes/Decisions/MC-001-obsidian-architecture-audit.md`

Structure the note as:
1. Current state (what exists today, with folder tree)
2. Gaps against the 4 purposes above
3. Specific, minimal proposed changes (naming, new sub-folders, Dataview
   query additions) — no change should require renaming existing notes
   unless clearly justified
4. Risks of each proposed change
5. A single recommendation, ranked if there are multiple options

## Constraints

- Do NOT create, move, delete, or rename any existing file or folder
- Do NOT modify Dataview/Templater configuration
- Only write the one audit note listed above
- If something is ambiguous, list it as an open question rather than guessing
```

## Hardware allocation rule (unchanged, non-negotiable)

| Device | RAM | Role | Max concurrent Hermes profiles |
|---|---|---|---|
| MacBook Pro M2 | 8 GB | Orchestration, review, Obsidian, browser checks only | 1 (2 briefly, never sustained) |
| ASUS Zenbook | 64 GB | Building, testing, parallel worktrees | 3 to start, max 6 after 2 stable cycles |
| Railway (Hindsight) | N/A | Shared cross-device memory bus | Not a workstation |

## Profile roster and provider assignment (unchanged)

| Profile | Provider | Write access | Device | Never do |
|---|---|---|---|---|
| `orchestrator` | Nous Portal | Read-only + create branches/task briefs via safe-worktree-add.sh | MacBook | Never writes code directly |
| `lexflow-builder` | OpenRouter | Write only in its assigned worktree | ASUS | Never touches `main`; never reviews own PR |
| `lexflow-tester` | OpenRouter, `:free` model first | Write test artifacts only | ASUS | Never approves merges |
| `lexflow-reviewer` | Nous Portal or a stronger OpenRouter model | PR comments only, no code writes | ASUS or Mac | Never is the same session as the builder |
| `memory-curator` | OpenRouter, `:free` model | Writes only to Agent Ops Inbox + Hindsight | ASUS | Never has Git write access or production access; pending task MC-001 this session |

## GitHub branch protection (apply once ASUS factory is stable)

1. Repository → Settings → Branches → add rule for `main`
2. Require pull request before merging
3. Require at least one approval
4. Require status checks to pass before merge
5. Require branch to be up to date before merge
6. Disable force pushes and branch deletion on `main`
7. Do not allow bots/agents to bypass this rule

## Consolidated risk register

| Risk | Mitigation | Status |
|---|---|---|
| Two worktrees on same branch | `safe-worktree-add.sh` blocks before creation | Mitigated — script added this revision |
| Nous OAuth refresh token reuse detected, locks profiles | `auth reset` + `auth add nous` sequence per affected profile | Fixed this session — monitor for recurrence |
| Builder reviews own PR | Reviewer must be a separate profile/session, enforced by task brief | Open — enforce every time |
| Agent self-declares 5/5 and expects auto-merge | Human approval required on every merge; add GitHub branch protection | Open — configure GitHub rule |
| Unused MCPs consuming RAM via retry loops | Disable unused MCPs in `config.yaml` per profile | Recurring — recheck monthly |
| Client/legal data in test fixtures | Use scrubbed sample data only | Open |
| Cloud instance left running unintentionally | Stop instance after each scheduled run; track hosting cost separately | Open — only relevant once Cloud pilot starts |

## Rollout timeline (unchanged)

| Phase | Days | Gate to proceed |
|---|---|---|
| Stabilise | 1-2 | Clean ASUS clone builds; Hindsight sync confirmed both devices; Nous auth confirmed on all profiles |
| Single worktree test | 3-4 | One PR with evidence produced via safe-worktree-add.sh; no crashes |
| Three-station run | 5-7 | One clean 5/5 PR manually merged |
| Controlled scaling | 8-14 | Two clean 5/5 PRs merged before considering Cloud or CI automation |

## Next actions (in order)

1. Run the Nous auth fix sequence (section 4) and confirm every profile shows logged in.
2. Give `memory-curator` the MC-001 audit task (section 6) and review its output before approving any vault changes.
3. Install `safe-worktree-add.sh` on ASUS before creating any new worktree.
4. Package the current working profile as a distribution and install it on ASUS (section 5).
