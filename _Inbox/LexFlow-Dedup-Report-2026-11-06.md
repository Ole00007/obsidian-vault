---
tags: [lexflow, dedup, archive]
project: LexFlow
home: 01-Projects/LexFlow/
---
# LexFlow dedup / archive — dry-run report 2026-11-06 (nothing moved)

Root: /Users/olesiarasing/projects/lexflow  (26 CRM worktrees of one repo, 25 branches; plus mixed-case `~/Projects` paths in git worktree registry)

## Candidate canonical
- lexflow_hermes_v1 @ 9af129c (2026-11-06, wt-merge) — newest, ahead 95 of legacy-recovered
- integration/filters-roi-demo2 @ 52370af (2026-11-05, wt-demo2, serves :5057, 3 dirty files)

## Already merged into lexflow_hermes_v1 (safe to archive): 
wt-agent, wt-context, wt-deadlines, wt-gantt, wt-int, wt-notify, wt-audit (2 dirty files), wt-docs (1 dirty file)
## NOT merged (check before archive): 
t019, wt-blocked, wt-calyear, wt-checklist, wt-demo, wt-demo2 (3 dirty), wt-filters, wt-harden, wt-insights, wt-menu, wt-roi, wt-roi2, wt-t021, wt-t027, wt-t029 (6 dirty)
## Junk: wt-origin (detached HEAD), /private/tmp/lx_admy_origin_wt (prunable), lexflow-crm main dir on stale integration/graph-gantt-local (053265e, Oct 27) with modified DBs
## Backups: _backups/lexflow-crm-ui-bus-2026-10-26.bundle; website dupes `lexflow-index (1).html`, `lexflow-faq (1).html`, `lexflow-pricing (1).html`, `lexflow-practice-areas (1).html`, probe-*/_probe-* files; ~/projects/LEGAL_backup, ~/projects/_archive

## Website
Repo lexflow-website (branch feat/heading-align-cta-merge, deploys to https://lexflow-site.pages.dev). Sign-in link in lexflow-index.html line 122 -> https://web-production-031a6.up.railway.app/login?ws=lexflow

## Links
- Parent: [[LexFlow]]
- Related: [[LexFlow-Agent-Roster-and-Ecosystem-CANONICAL-2026-11-04]]
