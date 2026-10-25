---
title: LexFlow CRM — pre-push audit (local vs GitHub) 2026-10-25
status: audit only — NOTHING pushed
---
# Which repo, which branch (evidence)
Right target: **github.com/Ole00007/lexflow-crm**, branch **lexflow_hermes_v1** (public repo). Method (3 independent sources):
1. GitHub deployments API (`gh api repos/Ole00007/lexflow-crm/deployments`): environment `perceptive-achievement / production`, latest deploy = commit 8c17456 (2026-09-17) from lexflow_hermes_v1 → **a push to this branch auto-deploys to production** (`web-production-031a6`, /health 200 today).
2. Vault: `01-Projects/AVibe-CRM/LexFlow/LexFlow-Dev-Handoff.md` ("Push to GitHub (lexflow_hermes_v1 branch)") and `2026-09-23-AVIBE-Ecosystem-Master-Table.md` (Railway project perceptive-achievement = LexFlow CRM production). The Master Table calls the repo "stale (Jul 20)" — that is the GitHub `updated_at`; `pushed_at` is 2026-09-17, so the label is misleading.
3. Local git: `origin` = that repo; local branch tracks `legacy-recovered` (a local-path remote), NOT origin — "ahead 55" in `git branch -vv` is against the wrong remote.
Other repos (LexFlow-MVP, lexflow-website, LexFlow-landing, LexFlow-Chatbot, aLEXy…) were NOT audited.

# Local vs GitHub
- origin/lexflow_hermes_v1 = 8c17456. Local lexflow_hermes_v1 (30b6f93) is **ahead 70 / behind 1**. The 1 missing commit is 8c17456 (marketing link repoint; touches crm/__init__.py, config.py CORS, views.py, base/kanban templates). Merging it conflicts once in `crm/__init__.py` (trivial; resolved in `audit/push-candidate`).
- Candidate = local + origin 8c17456 + feat/eliza-docs: branch `audit/push-candidate` (worktree ~/projects/lexflow-crm-wt-audit). 61 non-merge commits would go out.
- Content delta vs origin (excluding node_modules): 104 files added, 27 modified, 2 deleted (uploads/*.txt). Plus **1768 tracked files under apps/api/node_modules removed** (the Node API sources stay).

# Audit results (candidate)
| Check | Result |
|---|---|
| pytest | 38 passed |
| 5 plain-script suites (pytest ignores them via collect_ignore) | all exit 0 (gantt deps 12, context notes 24, gantt team 27, notify 51, deadline isolation 12 pass-lines) |
| Alembic | single head k2f3a4b5c6d7; origin head e2f3a4b5c6d7 is its ancestor (linear) |
| Prod-upgrade simulation on **real PostgreSQL** (pgserver throwaway): origin code builds schema+data, candidate boots on that DB | boots clean, 0 errors |
| Flags-OFF parity vs origin, 33 routes | identical statuses; only differences: additive fields (cases: contact_email/contact_name; tasks: depends_on/startdate), `/api/gantt/tasks` returns 200 [] (JWT-protected) instead of 404 because the API is not flag-gated (page is), POST-less `/api/agent/chat` GET 405 vs 404 |
| Flags ON (SQLite + PG) | gantt/graph/agent/context pages+APIs 200; Eliza bubble only present when AGENT_ENABLED |
| Eliza on PG | chat → pending → approve creates task; doc + draft flows OK |
| Anonymous data | `/api/cases/`, `/api/contacts/` answer 200 to anonymous callers but return `[]` even with data present (pre-existing, same on origin) |
| compileall | OK |

# BLOCKERS / gates before any push
1. **SECRET_KEY and JWT_SECRET_KEY must exist as Railway variables.** Local config.py has no fallback (`os.environ[...]`); origin's has `dev-secret-key-change-in-production` fallback. If either is missing on Railway the new build crash-loops = production outage. I could NOT verify: `railway` CLI login expired ("grant request is invalid"). Needs `railway login` or a dashboard check. (Roadmap T-024 says the same.)
2. **Secrets already PUBLIC in origin history since 2026-07-15** (repo is public): `backups/.env..bak` (Resend API key, WEBHOOK_SECRET, postgres DATABASE_URL, ADMIN_EMAIL), `api-keys-1778573403906 (1).csv` (a Resend key), `test_gemini.py` (hard-coded Google API key). Values were never printed. They stay public even after deleting the files → **rotate: Resend key(s), WEBHOOK_SECRET, Railway Postgres password, Google/Gemini key.**
3. Tracked data/privacy artefacts (all already public except ROLLBACK.md): `crm_local.db` (6 users with password hashes, 3 contacts, 3 cases), `data/app.db`, `sqlite_mcp_server.db`, backups/, 2 zips, 4 CSVs, duplicated "… 2.py" / BACKUP files. `.gitignore` covers `*.db` only — add `node_modules/`, `uploads/`, `.env*`, `backups/`.
4. Pushing deploys immediately (Railway GitHub integration). Recommended: push to a NEW branch first (no deploy hook), review diff on GitHub, then fast-forward lexflow_hermes_v1 after gates 1–2.

# Not covered / honest limits
- Railway env vars and Railway build logs (no CLI access); production data/state not touched.
- Python 3.9 locally vs 3.11.8 on Railway (no 3.11 with deps installed) — syntax-compatible, not executed on 3.11.
- `pymupdf` added to requirements.txt (new build dependency; PDF reading degrades gracefully if absent).
- No full SAST (bandit/gitleaks not installed): regex secret scan + targeted greps only; no new secrets introduced by the 61 commits (pattern scan of every commit in range = 0 hits).

## Links
- Parent: [[LexFlow-Reusable-Build-Protocol-2026-10-25]]
- Related: [[LexFlow-Eliza-InApp-Agent-2026-10-25]]
