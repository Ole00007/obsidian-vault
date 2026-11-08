---
tags: [workflow, git, lexflow, agent-rules]
project: LexFlow
home: _Meta/
status: proposal (for Ole's approval)
---
# Keep-it-don't-rebuild workflow for demo builds (2026-11-06)

Root cause of the Nov 5-6 rebuild loops: finished work sat **uncommitted** in a worktree (ROI language toggle), and two feature blueprints (`insights`, `checklist`) were **never registered**, so nothing showed even though code existed. Nothing was lost; it was just invisible.

## Rules
1. **One demo branch per port, named in the boot script header.** 5057 = `integration/filters-roi-demo2` in `lexflow-crm-wt-demo2`. Never commit on a side branch inside the live worktree; if you do, fast-forward the demo branch (`git branch -f`) in the same step.
2. **No end-of-task without commit.** A change that Ole has seen on screen is committed and tagged `demo-<port>-YYYY-MM-DD` before the agent reports. Uncommitted files in a served worktree are a red flag (the daily report BRANCH CHECK now shows it).
3. **Registered or it does not exist.** A new blueprint must appear in `crm/__init__.py`; the route battery (`/insights`, `/api/checklist/templates`, ...) runs after every restart. 404 on a flag-gated page = check registration first, then the flag.
4. **Regression test for every restored feature** (e.g. `test_roi_app_shell_has_language_toggle`). "Restore X" must not remove Y: before/after screenshot or DOM assertion on both.
5. **Rollback is a tag, not memory.** `demo-5057-2026-11-06` marks the known-good build.
6. **Read git, not notes.** For "what ran yesterday" use `ps` start time + `git log --all --since` + `git status`. Notes by free-model agents are not evidence.
7. **Restart procedure:** take lock `port-5057` -> kill -> start as tracked background process -> login + route battery -> release lock.

## Links
- Parent: [[_Meta]]
- Related: [[Agent-Lessons-Loops-Branches-Projects-2026-11-06]]
