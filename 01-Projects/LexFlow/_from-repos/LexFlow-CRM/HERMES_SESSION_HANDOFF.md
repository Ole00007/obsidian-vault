# Hermes Session Handoff Summary
*Generated: 19 June 2026 — Pass this to the new model before closing the old session*

---

## Project identity

- **Project name:** LexFlow CRM Phase 2
- **Workspace path:** `/Users/olesiarasing/Desktop/LexFlow/LexFlow Review Build/`
- **Platform:** MacBook Pro, macOS, VS Code + Hermes Agent (ACP mode)
- **User:** Olesia Raising

---

## What was being built

LexFlow is a CRM application (Flask / Python) being built in phases. This session covered **Phase 2** which involves schema decisions, database relationships, deploy setup, and local testing before any push to GitHub or Railway.

---

## What Hermes already did this session

1. Reviewed and produced a decision table covering:
   - Profile strategy (fork/separate from main app for CRM)
   - Foreign key fixes: `tasks.caseid` (ON DELETE CASCADE), `cases.assignedto` (→ users.id)
   - Soft vs hard delete policy (soft for GDPR compliance, Phase 6)
   - Deadline status options: "pending", "completed", "overdue", "waived"
   - Deadline search/filter (by case, status, date range)
2. Generated a **PLAN READY FOR APPROVAL** summary with:
   - Estimated build time ~1 hour
   - Risk level: Medium (Procfile change touches production setup)
   - Rollback plan: revert Procfile to `web: gunicorn app:app` if Railway breaks
3. Prepared local build and testing environment setup
4. Reviewed launch config, migration env, and dependency state
5. Checked Python availability, installed packages, migration files
6. Began inspecting current CRM files (1/4 — 15 files changed +801 -11)

---

## What is NOT done yet (pending)

- Full local build has not been completed
- Local test run has not been confirmed as passing
- `FINAL_PREBUILD_CHECK.md` has NOT yet been saved
- `LOCAL_TEST_REPORT.md` has NOT yet been saved
- No push to GitHub has been made (correct — intentional)
- No deploy to Railway has been triggered (correct)

---

## Known blockers / risks

| Risk | Details |
|------|---------|
| Broken `.venv` | The local Python environment shows errors in VS Code status bar. This may affect build/test validity. Must be fixed or confirmed before trusting test results. |
| Procfile change | Changing the Procfile touches Railway deploy setup. Medium risk. Rollback: revert to `web: gunicorn app:app`. |
| Foreign key migrations | Any schema change to `tasks.caseid` or `cases.assignedto` requires clean migration. Must check if existing migrations already assume the current schema. |
| Profile strategy | "Fork/separate for CRM" is still ambiguous — it could mean a separate entrypoint, separate Procfile process, or separate repo. This must be clarified before build. |
| Python env / interpreter mismatch | VS Code shows `.venv (broken)` — this must be separated from a real app logic problem before trusting any diagnosis. |

---

## Commands the new model must know

```bash
# Navigate to project
cd '/Users/olesiarasing/Desktop/LexFlow/LexFlow Review Build'

# Check Python environment
python3 --version
ls -la .venv 2>/dev/null || true

# Check installed packages
python3 -m pip show Flask flask-cors Flask-Migrate Flask-SQLAlchemy flask-jwt-extended gunicorn psycopg2-binary 2>/dev/null || true

# Check migrations
echo '---migrations---' && ls -1 migrations/versions

# Run locally
source .venv/bin/activate && flask run

# Run migrations
flask db upgrade
```

---

## Standing permissions for the new model

- Work only inside the workspace path above
- Read/write files, run local zsh commands, inspect, build, test
- Do NOT push to GitHub
- Do NOT deploy to Railway
- Do NOT run destructive database operations without confirmation
- Pause and ask only for: GitHub push, deploy, network actions, destructive deletes, irreversible DB operations

---

## Required deliverables before any push

Create these two files in the project root before continuing to build:

1. `FINAL_PREBUILD_CHECK.md` — confirmed blockers, schema risks, deploy risks, rollback steps
2. `LOCAL_TEST_REPORT.md` — what passed, what failed, what is still risky, whether safe to push

---

## Files to read first

The new model should prioritise reading:

1. `LexFlow_Hermes_Context.md` — main project context (source of truth)
2. `Procfile` — current deploy entrypoint
3. `app.py` or main app file — app object path
4. `crm/models/` — all CRM model files
5. `migrations/versions/` — all migration scripts
6. `.env` or `.env.example` — config and secrets reference
7. `requirements.txt` — installed dependencies

---

## Paste-ready first prompt for the new model

```text
Read this fully before doing anything:
@file:LexFlow_Hermes_Context.md

This is your single source of truth for the entire project.

After reading, confirm:
1. What you see in crm/models/ right now
2. Whether Procfile exists
3. Then produce FINAL_PREBUILD_CHECK.md — do not build yet

Work locally only. Do not push to GitHub.
Do not ask me for routine local approvals.
Only pause for: GitHub push, deploy, destructive deletes, irreversible DB operations, or secrets changes.
```

---

## Session tool context

- Hermes was running inside VS Code via ACP (Agent Client Protocol)
- Model used: Claude Haiku 4.5 (visible in screenshot, 22.7 credits shown)
- Credits exhausted — reason for switching to new model
- Hermes approval mode: default approvals (some commands still require Allow/Skip)

---

## Credit and model notes

- GitHub Copilot credits: exhausted, reset 1 July 2026 at 02:00
- To switch Hermes model: run `hermes model` in Terminal, pick new provider/model, start new VS Code session
- To check Nous Portal usage: https://portal.nousresearch.com/
- To monitor Copilot usage: https://github.com/settings/billing
