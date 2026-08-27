# LexFlow — Railway Diagnosis & Rebuild Plan
Generated: 2026-06-18 | Deadline: 2026-06-23

## Diagnosis: Why Railway Shows "Not Available"

### Problem 1 — Duplicate route in app.py (CRITICAL)
`load_demo` route is defined twice in app.py.
Flask raises AssertionError: View function mapping is overwriting an existing endpoint.
Gunicorn cannot start. Railway shows "not available."

### Problem 2 — Two Flask apps in one repo, one Procfile
| App | Entry point | DB |
|---|---|---|
| app.py | gunicorn app:app (Procfile) | SQLite |
| crm/__init__.py | gunicorn run_crm:app | PostgreSQL |

run_crm.py says: "DO NOT use app.py for CRM work."
CRM factory is disconnected — not registered in app.py, not in Procfile. Dangling code.

### Problem 3 — `resend` missing from requirements.txt
app.py line 3: `import resend`
requirements.txt: resend NOT listed
Railway: ModuleNotFoundError: No module named 'resend' at startup

### Problem 4 — Unfinished edit committed to main
app.py ends with:
  # PASTE CRM BLOCK HERE
  if __name__ == "__main__": ...   (appears twice)

---

## Rebuild Plan — Option A: Unified App (Recommended for June 23)

One Flask app. One Railway service. One Procfile.
app.py handles intake + CRM (SQLite initially).

| Step | Action | File |
|---|---|---|
| 1 | Add resend==2.4.0 | requirements.txt |
| 2 | Remove duplicate load_demo route | app.py |
| 3 | Remove second if __name__ block | app.py |
| 4 | Remove placeholder comment | app.py |
| 5 | Register CRM blueprints conditionally | app.py |
| 6 | Verify Procfile unchanged | Procfile |
| 7 | Push to main | GitHub |
| 8 | Verify /health, /, /admin return 200 | Railway |

## What Is NOT Touched
- All templates
- CRM models and routes
- .env.example, migrations/, data/app.db

---

## 3 Confirmations Needed

1. Architecture: Option A (unified) or Option B (split Railway services)?
2. CRM DB: SQLite initially OR PostgreSQL from day 1?
3. Railway env vars: Is RESEND_API_KEY set in Railway project?

---

## Post-Fix Checklist

- [ ] Railway deploy green
- [ ] / intake form loads
- [ ] /submit creates matter, redirects to /status/<token>
- [ ] /admin loads matter list
- [ ] /admin/matter/<id> loads + status update works
- [ ] Email fires on status change (if RESEND_API_KEY set)
- [ ] /health returns status ok
- [ ] CRM /contacts responds
- [ ] CRM /cases responds
- [ ] LexBillFlow receives first commit

## Links
- Parent: [[LexFlow_Hermes_Kit_v2-INDEX]]
- Related: [[SKILL_lexflow-deploy]]
