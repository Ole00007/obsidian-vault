---
tags: [lexflow, crm, frontend, filters, roi-calculator]
project: LexFlow
home: 01-Projects/LexFlow/CRM
status: committed-locally
date: 2026-10-30
---

# LexFlow CRM — JOB 2 (task filters + ROI calculator)

Ole's direct request via backend-dev. Two commits, two worktrees, both local
(no push, no deploy, no server touched). Full brief context lived in the task
itself (the referenced landing-page-upgrade-brief.md was a DIFFERENT task —
landing page; JOB 2 is the CRM templates).

## PART A — feat/task-filters (worktree `lexflow-crm-wt-filters`)
Commit `87fc14b`. Tests: 58 passed (was 56; +2 calendar filter tests).

- **A1 kanban Due filter**: no longer blanks the board (0 cards because 1/25
  matters had a duedate). Derives a matter's due from the earliest open linked
  task duedate (GET /api/tasks keyed by caseid) when the matter has no own
  duedate; hides the Due group entirely when nothing has any due info. New
  `hideDue` option in shared `static/js/filters/task_filters.js`. Column counts
  now show “N of M” when filtered; all-hidden columns show “No matches” and hide
  their Blocked lane-head; all-hidden board shows “No matters match — Clear
  filters”.
- **A2 kanban horizontal reach**: always-visible horizontal scrollbar (styled to
  match the Gantt timeline's), click-and-drag background panning (grab cursor,
  only from empty background, never during a card drag), and a subtle right-edge
  fade scroll-hint that clears at the far end. Board wrapped in `.board-bay`.
  Still fits 390px via native touch scroll.
- **A3 calendar filter**: month/week/day grids AND the list now all honour
  event_type + date_from/date_to via one shared client-side predicate. Root bug:
  grid ignored from/to (only sent its own visible-range dates) and
  deadline-merged events bypassed the server type filter. Added
  `tests/test_calendar_filter.py`.
- **A4 persisted-filter visibility**: always-visible “Filters on — N — Showing
  X of Y — Clear” banner appears next to the toolbar on ALL views including
  calendar; stored filter (`lf_task_filter`) reset on login + logout.

## PART B — feat/roi-calculator (worktree `lexflow-crm-wt-roi`)
Commit `ffb8696`. Tests: 61 passed.

- Public route `/roi-calculator` (no auth) guarded by env flag
  `ROI_CALCULATOR_ENABLED` (DEFAULT OFF → 404), in `crm/routes/views.py`.
- One pure client-side JS module `static/js/roi/roi_calculator.js`
  (`window.ROICalculator.computeRoi`) → testable math, whole euros/hours.
- Self-contained bilingual IT/EN template `templates/roi_calculator.html`
  (logged-out safe, dark/gold, 390px, keyboard accessible, contrast ≥ 4.5:1).
  Editable inputs (lawyers default 1 …), outputs (hours regained month+year,
  euro value, 3-yr ROI %, payback month), 3-yr SVG chart, one summary sentence,
  collapsed editable Assumptions panel (hours-per-matter 1.5 flagged ASSUMPTION,
  billable 1500, ramp 100%), formula in plain words, disclaimer “Estimate, not
  a guarantee”. ZERO external requests, no lead collection (Ole's rule).
- Dashboard/sidebar link in `templates/base.html`, gated on the flag; context
  processor exposes `roi_calculator_enabled` in `crm/__init__.py`.
- Tests `tests/test_roi_calculator.py`: 404 off/unset, 200 on, no external URLs,
  no lead form, module wiring, math sanity, flag exposed.

## Verified / not verified
- Verified: both suites green, JS/CSS/HTML static-syntax-clean, inline scripts
  parse (node --check), no external refs in ROI page, no server started, no push.
- NOT verified: real-browser scrollbar visibility / drag pan / 390px rendering
  (no browser here — backend-dev does the visual test on the 5057 server).

## Links
- Parent: [[LexFlow-INDEX]]
- Related: [[2026-10-30]]
