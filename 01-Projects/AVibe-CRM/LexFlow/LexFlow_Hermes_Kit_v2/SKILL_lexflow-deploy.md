---
name: lexflow-deploy
description: >
  Activate for: Railway deploy failures, "not available" errors, missing Procfile,
  gunicorn startup crash, code recovery after laptop loss, regenerating missing files
  from GitHub history, or deploying a new module (LexBillFlow, LexTaskFlow).
version: 1.1.0
---

# LexFlow Deploy & Recovery Skill

## Quick Reference

| Task | Command |
|---|---|
| Check Railway logs | railway logs --tail 100 |
| Run MVP locally | gunicorn app:app --bind 0.0.0.0:5000 |
| Run Chatbot locally | gunicorn server:app --bind 0.0.0.0:5000 |
| Check Procfile | cat Procfile |
| Install deps | pip install -r requirements.txt |
| Run migrations | flask db upgrade |
| Check DB tables | sqlite3 data/app.db ".tables" |
| Check git history | git log --oneline -20 |

## Known Current Issue — LexFlow-MVP (as of 2026-06-18)

**app.py has 3 bugs that prevent Railway boot:**
1. `load_demo` route defined twice — Flask throws AssertionError on startup
2. `resend` package missing from requirements.txt — ImportError on startup
3. `# PASTE CRM BLOCK HERE` comment + duplicate `if __name__` block — unfinished edit in prod

**Fix sequence:**
1. Add `resend==2.4.0` to requirements.txt
2. Remove duplicate `load_demo` route from app.py
3. Remove second `if __name__ == "__main__"` block
4. Remove placeholder comment
5. Push to main

## Procfile Standard

LexFlow-MVP:     web: gunicorn app:app
LexFlow-Chatbot: web: gunicorn server:app --bind 0.0.0.0:$PORT

## Diagnosing a Failed Deploy

1. Read logs: railway logs --tail 100
2. Check for: missing Procfile, wrong entry point, missing env var, ImportError, migration failure
3. Fix the specific error — do not guess

## Recovering Lost Code

1. Clone: git clone https://github.com/Ole00007/LexFlow-MVP
2. Check history: git log --oneline -20
3. Check all branches: git branch -a
4. Checkout old commit: git checkout <sha>
5. Rebuild missing files from existing code structure (see AGENTS.md)
6. Use pipreqs to regenerate requirements.txt from imports if missing

## New Module Deploy (LexBillFlow)

1. Create app structure: app.py, templates/, static/
2. Write Procfile: `web: gunicorn app:app`
3. Write requirements.txt and .env.example
4. Push to github.com/Ole00007/LexBillFlow
5. Connect to Railway → set env vars → deploy

## Lovable.dev Frontend Integration

1. Lovable project → Settings → GitHub → connect to target repo
2. Push from Lovable to GitHub
3. Flask integration: copy React build to static/ or serve via send_from_directory
4. Standalone: deploy via Netlify (connect GitHub repo)

## Verification Checklist

- curl https://<railway-domain>/ returns 200
- /intake loads matter submission form
- /admin loads without 500 errors
- /health returns {"status": "ok"}
- Email notification fires on status change

## Links
- Parent: [[LexFlow_Hermes_Kit_v2-INDEX]]
- Related: [[LEXFLOW_REBUILD_PLAN]]
