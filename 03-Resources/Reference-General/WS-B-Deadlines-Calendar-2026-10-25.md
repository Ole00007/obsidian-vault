---
title: "WS-B Deadlines + Calendar Reflection - Complete"
date: 2026-10-25
author: sales-crm
status: done
---

# WS-B: Deadlines + Calendar Reflection

## What was built
- `crm/services/deadline_sync.py`: service that converts Task.duedate (open tasks only) and Deadline rows into calendar-compatible dicts, workspace-scoped, deduplicated, with kind/source/id fields
- `crm/routes/calendar.py` (modified): list_events() now accepts ?deadline_events=true/false flag. When CALENDAR_DEADLINES_ENABLED env flag is on (or request explicitly passes deadline_events=true), deadline events are merged into the existing CalendarEvent response
- `crm/models/deadline.py` (modified): added docstring documenting Italian legal deadline_type vocabulary (udienza, termine_perentorio, etc.)
- `tests/test_deadline_calendar.py`: 5 pytest tests (all passing)
- `seed_deadlines_demo.py`: minimal seed script

## Key findings
- BEFORE this change: task duedates and Deadline rows were **NOT** reflected in the Calendar. The calendar API only served CalendarEvent rows.
- AFTER: with `CALENDAR_DEADLINES_ENABLED=true`, both appear with kind=task_due and kind=deadline respectively

## Links
- Parent: [[LexFlow-Context-Graph-and-Gantt-Local-2026-10-24]]
- Related: [[LexFlow-Platform-Plan-2026-10-24]]