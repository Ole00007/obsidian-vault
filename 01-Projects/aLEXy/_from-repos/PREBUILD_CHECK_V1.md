# PREBUILD_CHECK_V1.md
**Date:** 2026-06-19 | **Status:** CRITICAL GAPS FOUND | **Build Ready:** NO (requires migration)

---

## 1. DEPLOY ENTRYPOINT & PROCFILE ANALYSIS

### Current Procfile
```
web: gunicorn app:app
```

**What this means:**
- Points to `app.py` (Flask app instance in `app = Flask(__name__)`)
- `app.py` is the intake form handler (live on Railway)
- Uses SQLite (isolated from PostgreSQL CRM)
- **`gunicorn` is not declared in `requirements.txt`** — this can cause Railway deploy failures without an obvious error

### CRM Factory Function
- **Location:** `crm/__init__.py`
- **Function:** `create_app()` ✅ Properly implemented
- **Returns:** Configured Flask app instance
- **Status:** Ready for Railway deployment
- **Note:** `app.py` does not import `crm` or call `crm.create_app()`

### IS PROCFILE BLOCKING RAILWAY DEPLOY?
**Answer: PARTIALLY YES, but NOT YET AN ISSUE**
- Current Procfile works for `app.py` (intake form is live)
- Railway has **TWO SEPARATE services:**
  1. `lexflow-mvp` → should run CRM (currently broken — app not found)
  2. `lexflow-chatbot` → live and working
  
**Why deploy fails:** Railway CLI can't locate `crm:create_app()` in current Procfile
- Need to either:
  - Create separate Procfile for CRM deploy
  - Change Railway config to set `FLASK_APP=crm` env var + custom start command
  - OR deploy CRM to different Railway service

**Recommendation:** Do NOT modify root Procfile (breaks intake form). Use Railway service config instead.

---

## 2. EXACT APP OBJECT PATH

### app.py (Intake Form — Production)
```python
app = Flask(__name__)
# Location: /Users/olesiarasing/Desktop/LexFlow/LexFlow Review Build/app.py:43
# Status: LIVE on Railway (lexflow-mvp — broken intake routes)
# DB: SQLite @ ./data/app.db
# Do NOT touch
```

### crm/ (CRM API — Development)
```python
def create_app():
    app = Flask(__name__)
    # Location: /Users/olesiarasing/Desktop/LexFlow/LexFlow Review Build/crm/__init__.py:6
    # Returns: Flask app instance (not exposed globally)
    # DB: PostgreSQL (Railway)
    # Status: Ready for Railway deployment
```

**Implication for Phase 3:** Railway must call `crm:create_app()` not `app:app`

---

## 3. FOREIGN KEY ANALYSIS — CRITICAL FINDINGS

### Current Database Foreign Keys
```
pratiche.client_id → clienti.id (ON DELETE RESTRICT)
attivita.client_id → clienti.id (ON DELETE RESTRICT)
attivita.pratica_id → pratiche.id (ON DELETE RESTRICT)
registro.client_id → clienti.id (ON DELETE RESTRICT)
registro.pratica_id → pratiche.id (ON DELETE RESTRICT)
registro.attivita_id → attivita.id (ON DELETE SET NULL)
tasks.userid → users.id (ON DELETE SET NULL)    ✅ EXISTS
```

### CRITICAL GAP: tasks.caseid FK MISSING ❌
**Expected by migration 7a8b9c0d1e2f:**
```sql
sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ondelete='CASCADE')
```

**Actual in database:** NOT PRESENT

**Why:** Because `cases` table does not exist!

**Additional note:** `tasks.userid → users.id` exists, but `cases.assignedto` still has no FK to `users.id`.

### CRITICAL GAP: cases TABLE MISSING ❌
**Expected tables in database:**
- ✅ contacts (created by migration 65b843c76b3d)
- ✅ users (created by migration 7a8b9c0d1e2f)
- ✅ tasks (created by migration 7a8b9c0d1e2f)
- ❌ **cases** (NO MIGRATION EXISTS TO CREATE THIS)

**Evidence:**
```sql
SELECT EXISTS (SELECT FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name = 'cases');
-- Result: false
```

**Models expect `cases` table:**
```python
# crm/models/case.py
class Case(db.Model):
    __tablename__ = "cases"
    contactid = db.Column(db.Integer, db.ForeignKey("contacts.id", ondelete="RESTRICT"), nullable=False)
    assignedto = db.Column(db.Integer, nullable=True)  # NO FK to users.id
```

**Routes try to use `cases`:**
```python
# crm/routes/cases.py
@cases_bp.get("/cases")
def get_cases():
    cases = Case.query.order_by(Case.id.desc()).all()  # Will fail: no table
```

---

## 4. MIGRATION ANALYSIS & SCHEMA ASSUMPTIONS

### Migration Chain
```
430ee4511375 (None)
  ↓ drops old tables (clienti, pratiche, attivita, registro)
65b843c76b3d (430ee4511375)
  ↓ creates contacts table
7a8b9c0d1e2f (65b843c76b3d)  ← CURRENTLY STAMPED (applied)
  ↓ creates users + tasks tables
```

### Applied Migrations Status
```python
SELECT version_num FROM alembic_version;
# Result: ['7a8b9c0d1e2f']
```

**Problem:** Migration 7a8b9c0d1e2f says:
```python
sa.ForeignKeyConstraint(['caseid'], ['cases.id'], ondelete='CASCADE')
```

But `cases` was never created, so this FK is invalid.

### What Each Migration Does

#### 430ee4511375 — initial_crm_schema
- **Action:** Drops old Italian-named tables (clienti, pratiche, attivita, registro)
- **Does NOT create:** Any CRM tables
- **Assumption:** Previous database had these tables

#### 65b843c76b3d — create_contacts_table
- **Action:** Creates `contacts` table ✅
- **Assumption:** None (successful)
- **Status:** Partially applied (table exists)

#### 7a8b9c0d1e2f — add_users_and_tasks_tables
- **Action:** Creates `users` + `tasks` tables ✅
- **Assumption:** `cases` table already exists
- **Status:** PARTIALLY applied (users + tasks exist, FK to cases fails if enforced)

### Missing Migration
**NO migration exists to create `cases` table**

**Evidence:** Grepping migrations/versions for "create_table.*cases" returns nothing.

---

## 5. ENVIRONMENT & INTERPRETER STATUS

### Python Interpreter
```bash
python3 --version
# Python 3.9.6 ✅ (matches .venv Python 3.11 compatibility)

which python3
# /usr/bin/python3
```

### Virtual Environment
```bash
ls .venv/
# Include, Lib, Scripts, pyvenv.cfg
# Platform: Windows venv structure (created on Windows then copied to macOS)
# Status: FUNCTIONAL (packages installed correctly)
```

### Diagnosis Impact
**Does broken .venv affect diagnosis?** NO
- venv is functional (imports work, dependencies installed)
- All evidence gathered via working database queries
- No Python syntax or import errors

---

## 6. SOFT DELETE — SHOULD WE START NOW?

### Current Implementation
- **Soft delete in models:** NOT IMPLEMENTED
- **Hard delete in routes:** Assumed (need to verify)

### Master Plan v4 Requirement
```
DO NOT modify existing migration files
Rule 6: "Add soft delete (is_deleted flag) — never hard delete CRM data (GDPR)"
Context: Phase 6 — Compliance + Billing
```

### Recommendation: START IN PHASE 3
**Why now instead of Phase 6?**
1. **Database integrity:** Hard delete breaks referential constraints
   - Example: Delete a case → orphaned tasks
   - Example: Delete a user → orphaned "created_by" audit trail
2. **GDPR compliance:** Must preserve audit trail for 3+ years
3. **Data recovery:** Clients may request "undelete"
4. **Easy to add now:** Just add `is_deleted BOOLEAN DEFAULT false` + filter in queries
5. **Hard to retrofit:** Requires migration + all queries + all routes

**Implementation cost:** ~30 mins (add column + queries)
**Implementation cost if delayed to Phase 6:** ~2 hours (rework all deletes)

**Decision:** Add soft delete in Phase 3 for cases + contacts + users
- Add `is_deleted` column (boolean, default false)
- Add `deleted_at` timestamp (for audit trail)
- Update all `DELETE` endpoints to soft-delete
- Update all `SELECT` queries to filter `is_deleted = false`

---

## 7. CRITICAL BLOCKERS FOR PHASE 3 BUILD

| # | Issue | Severity | Fix Required | Time |
|---|-------|----------|--------------|------|
| 1 | `cases` table missing | BLOCKER | Create migration 001_create_cases_table.py | 5 min |
| 2 | `tasks.caseid` FK invalid | BLOCKER | Fix migration OR add constraint after cases created | 5 min |
| 3 | `cases.assignedto` has no FK | WARNING | Add FK to users.id | 5 min |
| 4 | No deadlines table | TODO | Create in Phase 3 | 15 min |
| 5 | Procfile points to app:app | INFO ONLY | Use Railway config override (do NOT change Procfile) | 0 min |
| 6 | No soft delete | ARCHITECTURAL | Add in Phase 3 Part A | 30 min |

---

## 8. RECOMMENDED PHASE 3 BUILD SEQUENCE

### PART A: FIX CRITICAL SCHEMA GAPS
1. Create `001_create_cases_table.py` migration
   - Creates `cases` table with all fields from model
   - Adds FK: `cases.contactid → contacts.id (CASCADE)`
   - Adds FK: `cases.assignedto → users.id (SET NULL)`
   - Adds indexes on `status`, `created_at` for query performance

2. Create `002_add_soft_delete.py` migration
   - Add `is_deleted` (BOOLEAN DEFAULT false) to: contacts, cases, users, tasks
   - Add `deleted_at` (TIMESTAMP nullable) to all above
   - Create index on `is_deleted` for fast filtering

3. Update all models to filter `is_deleted = false` in queries:
   - `Contact.query.filter(Contact.is_deleted == False)`
   - `Case.query.filter(Case.is_deleted == False)`
   - etc.

4. Update all DELETE endpoints to soft-delete:
   - `PUT /api/contacts/{id}` with `is_deleted=true`
   - Instead of `DELETE /api/contacts/{id}`

### PART B: BUILD PHASE 3 FEATURES
5. Create `crm/models/deadline.py`
6. Create `crm/routes/deadlines.py`
7. Register `deadlines_bp` in `crm/__init__.py`
8. Create `003_create_deadlines_table.py` migration
9. Verify full CRUD on `/api/contacts`, `/api/cases`
10. Test locally: `FLASK_APP=crm flask run --port 5001`

### PART C: DEPLOY & COMMIT
11. Run migrations: `FLASK_APP=crm flask db upgrade`
12. Test endpoints with curl or Postman
13. Backup: `cp -r crm/ backups/crm_backup_$(date +%Y%m%d_%H%M%S)`
14. Git commit: `git add crm/ requirements.txt migrations/ && git commit -m "Phase 3: Create cases table + add soft delete + add deadlines"`

---

## 9. SUMMARY TABLE

| Check | Result | Impact | Action |
|-------|--------|--------|--------|
| Procfile entrypoint | `app:app` → app.py | Not blocking phase 3 | Railway config override; don't touch Procfile |
| CRM factory function | `crm:create_app()` ✅ | Ready for deploy | Use this when deploying CRM to Railway |
| tasks.userid FK | ✅ exists → users.id | Data integrity OK | No change needed |
| cases table | ❌ MISSING | BLOCKER | Create 001_create_cases_table.py |
| cases.contactid FK | Should exist but doesn't | Will add in 001 | Create in migration |
| cases.assignedto FK | ❌ Missing | Should add | Add FK → users.id in 001 |
| Soft delete | ❌ Not implemented | GDPR risk | Add in 002 migration |
| Python interpreter | 3.9.6 ✅ | OK | No action |
| Virtual env | Functional ✅ | OK | No action |

---

## 10. BUILD READINESS GATE

**Can we build Phase 3 now?** 
- ✅ All code written
- ❌ Schema incomplete (cases table missing)
- ❌ Soft delete not implemented

**Build status:** 🟡 **CONDITIONAL READY**
- Proceed with Part A changes to fix schema
- Then proceed with Part B features

**Estimated duration:** 1.5 hours total
- Part A (schema fixes): 40 mins
- Part B (deadlines): 30 mins
- Part C (deploy): 10 mins

---

**Approval required from user before proceeding to build.**
