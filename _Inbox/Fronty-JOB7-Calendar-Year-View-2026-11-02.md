---
tags:
  - lexflow
  - frontend
  - handoff
  - calendar
project: "01-Projects/LexFlow/Elisa-CRM"
home: "01-Projects/LexFlow/Elisa-CRM"
---

# Fronty — JOB 7: Calendar "Year" view — DONE 2026-11-02

Status: complete, committed, full suite green. NOT pushed (Git-Push Gate).

## What shipped
Branch `feat/calendar-year-view` in worktree
`/Users/olesiarasing/projects/lexflow/lexflow-crm-wt-calyear`
(based on `integration/filters-roi-demo2`). Commit `f2afacf`.

- 4th view button `data-view="year"` next to Day / Week / Month in
  `templates/calendar.html`.
- 12 mini-month grids: 3x4 desktop, 2x6 tablet (<=900px), 1x12 phone (<600px);
  Monday-first, today highlighted, prev/next step +-1 year, title = the year.
- Per-day dot coloured by kind (hearing/deadline/task_due/other, same palette as
  month chips); 2+ items -> count badge; title/aria label lists first 3 titles.
- Click a day -> jump to Day view for that date; click a month header -> Month view.
- Single data source: existing `GET /api/calendar`, `_calDayRange` extended to
  `YYYY-01-01T00:00:00` .. `YYYY-12-31T23:59:59` for year.
- Respects the shared Filter dropdown (`window.TaskFilters`) + `calFilterRefresh()`
  exactly like the other views (calRender -> renderGrid -> renderYear).
- View is NOT persisted (no localStorage injected) — same as the other views.
- Vanilla JS/CSS, theme vars, dark+light, buttons + aria-labels, no horizontal
  overflow at 390px.

## Tests
- `tests/test_calendar_year_view.py` + `tests/calendar_year_view.js` (headless node,
  mirrors test_calendar_type_select.py pattern). Covers: year range request, dot vs
  count-badge for a seeded day, click-through to day/month, prev/next year, and the
  filter push-down (filtered subset -> fewer dots). 17 assertions all PASS.
- Full suite: `python3 -m pytest -q` -> 85 passed.
- Jinja compile + node `--check` on the inline script both clean.

## Constraints respected
- Never pushed. Did not touch other worktrees / main checkout.
- Demo server :5057 NOT restarted (it serves a different worktree; tested headless).
- Homepage/Flask templates not in scope — this landed only in `templates/calendar.html`.

## Handoff
Deployment is operator-installer's call (not done). No open follow-ups from Fronty
side for this card.

## Links
- Parent: [[LexFlow-Project-Status]]
- Related: [[Obsidian-INDEX]]
