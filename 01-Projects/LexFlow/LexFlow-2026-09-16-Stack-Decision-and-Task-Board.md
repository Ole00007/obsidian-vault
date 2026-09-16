---
title: LexFlow — 2026-09-16 decisions: stack 1.4, hiring board, repo-root rule
created: 2026-09-16
updated: 2026-09-16
tags: [lexflow, hermes, orchestration, decisions]
status: active
---

# LexFlow — 2026-09-16 decisions: stack 1.4, boards, repo-root rule

Session: operator-installer, resuming Ole's 15:31 instruction block (session `20260916_143900_372c3b`).

## 1. Stack decision — RECORDED

**Option 1.4: Nous Plus + OpenRouter overflow.** Nous Plus is the primary operator
workspace (hosted tools, multi-model access); OpenRouter is the pay-as-you-go
overflow for burst coding/automation and model-specific routing. Claude Pro is
**not** taken now (its 2026 Claude Code entitlement is unverifiable from public
sources). Railway spend stays separate from the AI subscription — Nous does not
cover app hosting.

Source of instructions for the stack work: `~/Obsidian/03-Resources/Hermes-Setup-and-MCP/hermes_setup_brief.md`.

## 2. Kanban work created today (2026-09-16)

### New isolated board — Ole's personal learning path
`lexflow-learning` ("LexFlow Learning Path") — separate DB, own queue, never
auto-dispatches dev work. Seed cards:
`t_d673a2e0` M1 Flask multi-tenancy · `t_a033743b` M2 Postgres RLS ·
`t_3bcd618f` M3 Railway · `t_cffefe6a` M4 website→CRM wiring ·
`t_8785bee4` M5 deploy hygiene.

### LexFlow CRM — 3 tasks for today
| Card | Owner | Scope |
|---|---|---|
| `t_16356a2c` #1 dead-button sweep (surgical #1+#4, unblocked) | backend-dev | every button real, local only |
| `t_4637a500` #2 RLS: confirm status + close ticket (18-test gate) | backend-dev | no merge until 18 cross-tenant tests on real Postgres, NOBYPASSRLS |
| `t_4f1a9c3c` #3 cross-feature consistency + `/tasks` attach 500 recheck | backend-dev | intake/task must reflect in Contacts + Calendar + dashboard |

### Delegations out of this block
| Card | Owner | Scope |
|---|---|---|
| `t_a261ac01` vault issue + ecosystem inventory v3 | memory-curator | open vault cards + full inventory with live endpoints |
| `t_62db7c26` 14-day Hermes installation roadmap | librarian | agents, memory, skills, routing, tests; propose only, no profile changes |
| `t_198870bd` website → CRM CTA wiring | frontend-developer-lovable_react | deep-link CTAs, local commit only, no deploy |

## 3. Verified live endpoints (checked 2026-09-16)

| URL | Code |
|---|---|
| `https://web-production-031a6.up.railway.app/` | 200 |
| `https://web-production-031a6.up.railway.app/login?ws=lexflow` | 200 |
| `https://web-production-031a6.up.railway.app/admin/panel` | 200 |
| `https://web-production-031a6.up.railway.app/api/health` | 404 (route does not exist) |
| `https://poetic-kleicha.netlify.app/` | **404** (stale in older docs) |
| `https://lexflow-landing.netlify.app/` | **404** (stale in older docs) |

**Correct CTA target for the website:** `/login?ws=lexflow` — the workspace deep
link, not the bare root URL. Superadmin surface: `/admin/panel`.

## 4. Repo-root rule — my recommendation

**Pick `~/projects` (i.e. `/Users/olesiarasing/projects`).**

Principle differences that matter:

1. **macOS TCC.** `~/Desktop` is a protected folder. Reads/writes under
   `~/Desktop/projects/` are inconsistently allowed — this session saw
   `Operation not permitted` on `~/Desktop/projects` while deeper paths partially
   worked. Agent tooling will keep hitting intermittent permission walls.
2. **Depth and Windows-style nesting.** `~/Desktop/projects/services/<vertical>/<project>`
   is a 4-level convention with no technical meaning; `~/projects/<project>` is flat and portable.
3. **Case-insensitivity trap.** APFS is case-insensitive by default, so
   `~/projects` and `~/Projects` are the *same* directory. Whichever root is
   chosen, the strict rule must fix **one exact casing** and forbid the other.
4. **Desktop is a UI surface.** Anything on the Desktop is Finder clutter and gets
   dragged around (this session observed live renames/moves at 15:43–15:47).

Proposed strict rule text for AGENT_RULES:
> All code repos live under `/Users/olesiarasing/projects/<repo>` (lowercase).
> No new repo may be created under `~/Desktop`. `~/Desktop/projects` is frozen
> read-only legacy and is migrated in the staged move below.

**Staged migration (needs Ole's go — moving repos is not reversible casually):**
1. Snapshot: verify every repo under `~/Desktop/projects/services/*` is either
   pushed to GitHub or has no uncommitted work.
2. Create `~/projects/<repo>` moves one vertical at a time (`LEGAL` first), using
   `git status` + `git log` before/after to prove nothing was lost.
3. Leave a symlink `~/Desktop/projects/services/LEGAL → ~/projects/LEGAL` for a
   grace period so scripts/crons keep working.
4. Only after a clean week: remove the symlinks, update AGENT_RULES, and have every
   profile's memory point at the new root.

## 5. Rollout order (UX and any multi-tenant change) — what it means

Order: **Avv. Pagliano → LexFlow → Romanelli**, and archive a baseline git tag
*before* the first step. It is a risk ladder, not a priority list:

- **Pagliano (ws9)** goes first — a single-workspace tenant with one admin, so the
  blast radius is smallest and a bad change is cheap to spot and revert. It is the canary.
- **LexFlow (ws7)** second — internal, we control the users and the data, so
  problems cannot reach a paying client.
- **Romanelli (ws10 + cl1/cl2 sub-workspaces)** last — the most complex tenant
  (parent + client sub-workspaces, most users, real client brand), so it should only
  ever receive a change that has already survived two cheaper environments.

The baseline tag matters because "feature X made Romanelli look wrong" is
unanswerable without a diffable before-state. Same order applies to any UX token,
colour-contrast or layout work — not just this one.

## 6. Roster change — librarian merged into memory-curator (done 2026-09-16)

Ole's decision: `librarian` is retired and merged into `memory-curator`.

- Its roadmap card `t_62db7c26` crashed twice under librarian (worker exited rc=0 without calling
  `kanban_complete`/`kanban_block` — protocol violation, dispatcher gave up after 2), so the card was
  reclaimed and reassigned to `memory-curator`. **librarian was not viable as a worker.**
- Merged: knowledge-management duties (file/folder taxonomy, SOP registry with version+date,
  archive-never-delete, findability-first) + its character text → `memory-curator/SOUL.md`;
  its stale taxonomy and SOP register → `memory-curator/memories/MEMORY.md` (paths flagged as stale,
  not reused).
- Retired: profile exported first to
  `~/.hermes/profile-exports/librarian-20260916-161325.tar.gz` (restorable), then deleted.
  Roster: 23 → 22 profiles.

## 7. Hard rule set — Repo Root Rule (§8)

Written into `~/Obsidian/_Meta/AGENT_RULES.md` as **§8 (hard, v1.0)** and injected into the
`SOUL.md` of every profile, so every agent sees it on boot:

> All code repos live at `/Users/olesiarasing/projects/<repo>` (lowercase `projects`).
> `~/Desktop/projects` is frozen read-only legacy. Never create a repo under `~/Desktop`;
> never use the casing `~/Projects` (APFS is case-insensitive — same directory, breaks path matching).
> Staged migration (LEGAL first, git-checked before/after, temporary symlink for a grace week) is run
> by `operator-installer` only, with Ole's go per batch.

## 8. Open items awaiting Ole

1. Repo-root rule: confirm `~/projects` + approve the staged migration.
2. Roster consolidation: proposal already written —
   [[Agent-Roster-Consolidation-Proposal-2026-09-16]] — 3 orphans
   (`chatbot_builder`, `email-digest-agent`, `tester`) merged into
   `frontend-developer-lovable_react`, `personal-assistant`, `backend-dev`. Awaiting approval; nothing merged, nothing deleted.
3. Whether today's CRM cards should be dispatched now or held.

## 7. Pencilled — blocked-on-legal (NOT dev) — card `t_051169c7`

Registered 2026-09-16 by operator-installer from a frontend-developer handoff. Nothing
implemented; **pages must not be edited** until Ole supplies real legal values.

Two publish gates on the LexFlow web-site, both the same underlying task:

1. **Contact decision** — `info@lexflow.com` and `demo@lexflow.com` are both shown as "the"
   contact in the same footer block (`faq` 270–271, `pricing` 179–180, `practice-areas`
   293–294, `how-it-works` 153–154) and both listed in `llms.txt` line 60; the 9 article
   pages (× EN/IT/RU) carry **`demo@` only** — three patterns, not two. Proposed default
   awaiting Ole: `info@` = primary general contact, `demo@` = role-labelled "request a demo".
2. **Legal entity placeholders** — `privacy.html` line 75 still says "Studio Legale X"
   (**unflagged**, reads as final) and `cookie-policy.html` lines 47, 48, 94 hold
   `[LEGAL COMPANY NAME]`, `[REGISTERED ADDRESS]`, `[NUMBER]`, `[privacy@lexflow.example]`,
   `[PEC / postal address]`, with a self-flagged "Review before launch" at line 49.

**Gate:** both are blocked until the **Partita IVA (P.IVA)** exists — the entity is still
"Studio Legale X", so the VAT number cannot be filled and the legal pages are legally
unpublishable. One combined reminder to Ole. Full registry:
[[LexFlow-Legal-Publishing-Blockers]].

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Surgical-Additions-2-3]]
- Related: [[Agent-Roster-Consolidation-Proposal-2026-09-16]]
- Related: [[LexFlow-Public-Intake-Contract-2026-09-15]]