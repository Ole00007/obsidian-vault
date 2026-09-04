# HARD RULE: Render-Before-Merge Gate

**Status:** Mandatory. Not a suggestion — do not merge or deploy visual/UX-facing changes without explicit sign-off on a rendered preview.

## Trigger

Applies to ANY change that alters what a human sees or interacts with:
- New or modified pages, templates, layouts, components
- Calendar grids, dashboards, kanban views, forms
- Branding, favicons, color/font/spacing changes
- Anything touching `.html`, `.jinja`, `.css`, or frontend JS render logic

Does **not** apply to backend-only changes with no visual surface (API logic, DB migrations, auth flow internals, cron jobs) — those follow the normal verify → commit → deploy path.

## Procedure

1. Build and syntax-check on an isolated branch/worktree. Never target `main`/production branch directly.
2. **Commit to the feature branch only.** Stop here.
3. Spin up a local preview:
   - Run the dev server against that branch with seeded/representative test data (not empty state).
   - Cover all relevant view states (e.g., Month/Week/Day, empty/populated, different tenants if multi-tenant).
   - Produce a localhost link and/or screenshots — do not describe the render in text as a substitute.
4. **Stop and wait.** Do not merge into the main branch or deploy until the human explicitly approves the rendered result.
5. Only after approval: merge, run full regression on affected areas, deploy.

## Why (precedent)

Landing page redesign was merged/pushed before being visually reviewed → user's reaction: "ugly" → rework required after the fact, wasted a full build cycle. This rule exists specifically to prevent repeating that failure mode.

## One-line version for prompts/SKILL.md

> Never merge or deploy a visual/UX change without first giving the user a rendered local preview (link or screenshots) and getting explicit approval — commit to branch and stop there until approved.
