# LexFlow Multi-Tenancy Rollout — Phases 2–4 Design Plan

> **Status:** Phase 1 complete (committed + pushed)  
> **Phase 1 deliverable:** `tenants` table exists; `tenant_id INTEGER DEFAULT NULL` columns added to `contacts`, `cases`, `tasks`, `events`.  
> **No code queries `tenant_id` yet.**  
> **Repo root:** `/Users/olesiarasing/Desktop/projects/services/LexFlow-MVP/`  
> **Date:** August 2026

---

## Table of Contents

1. [Tenant Model & Terminology](#1-tenant-model--terminology)
2. [Phase 2 — Tenant Context Middleware](#2-phase-2--tenant-context-middleware)
3. [Phase 3 — Query Filters (Opt-In, Route-by-Route)](#3-phase-3--query-filters-opt-in-route-by-route)
4. [Phase 4 — Tenant Onboarding + Auth](#4-phase-4--tenant-onboarding--auth)
5. [Capacity & Scaling Notes](#5-capacity--scaling-notes)
6. [Migration Sequence — Deploy Order](#6-migration-sequence--deploy-order)
7. [Potential Pitfalls](#7-potential-pitfalls)

---

## 1. Tenant Model & Terminology

### Tenant types

| Type | Description | Examples | Isolation |
|------|-------------|----------|-----------|
| **Internal (shared workspace)** | Your own LexFlow CRM instance — used by LexFlow team, aLEXy, Avibe Agency. All share one tenant. | `slug = "lexflow"`, `id = 1` | No isolation needed internally; RBAC views control what each brand sees |
| **Isolated (studio/avvocato)** | Each studio or independent lawyer gets their own tenant with data isolation, separate login, separate subdomain. | Pagliano, Romanelli, etc. | Full row-level isolation via `tenant_id` |

### The `tenants` table (Phase 1 — already deployed)

```sql
CREATE TABLE tenants (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(255) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    plan        VARCHAR(50) DEFAULT 'free',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Proposed additions to `tenants` (future migration, end of Phase 2)

```sql
ALTER TABLE tenants ADD COLUMN subdomain      VARCHAR(100) UNIQUE;       -- pagliano → pagliano.lexflow.app
ALTER TABLE tenants ADD COLUMN custom_domain  VARCHAR(255) UNIQUE;       -- pagliano.studio (optional)
ALTER TABLE tenants ADD COLUMN is_active      BOOLEAN DEFAULT TRUE;
ALTER TABLE tenants ADD COLUMN deleted_at     TIMESTAMP;                 -- soft-delete
ALTER TABLE tenants ADD COLUMN settings       JSONB DEFAULT '{}';        -- per-tenant config
```

### The "internal" tenant convention

- **ID = 1**, slug = `"lexflow"`, name = `"LexFlow — Internal Workspace"`
- Seeded as a data migration in Phase 2.
- All existing rows with `tenant_id IS NULL` are implicitly owned by this tenant.
- Code treats `tenant_id = 1` as the "internal/shared" workspace.
- When no tenant is resolved (e.g., legacy paths), default to tenant 1.

### Membership model (new table)

```sql
CREATE TABLE tenant_memberships (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tenant_id   INTEGER NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    role        VARCHAR(50) NOT NULL DEFAULT 'member',  -- 'admin', 'member', 'viewer'
    invited_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    joined_at   TIMESTAMP,
    UNIQUE(user_id, tenant_id)
);
```

**Design rationale:** Users are global (one `users` table); membership links a user to one or more tenants. A user can belong to multiple tenants (e.g., Diego is admin of all tenants). The internal tenant (id=1) has all existing users auto-enrolled.

---

## 2. Phase 2 — Tenant Context Middleware

### 2.1 Tenant resolution strategy (ordered by precedence)

The tenant must be resolved **before** the request reaches any route handler. Use a `before_request` handler on the Flask app.

```
┌─────────────────────────────────────────┐
│  Request arrives                        │
├─────────────────────────────────────────┤
│  1. JWT claim (tenant_id in token)      │  ← Highest priority (API clients)
│  2. Subdomain (pagliano.lexflow.app)    │  ← Browser users
│  3. Custom domain (pagliano.studio)     │  ← Premium users
│  4. Path prefix (/api/tenant/{slug}/…)  │  ← Explicit routing
│  5. Header (X-Tenant-Id or X-Tenant-Slug)│ ← Explicit override
│  6. Default to tenant 1 (internal)      │  ← Fallback (legacy safety)
└─────────────────────────────────────────┘
```

**Middleware location:** New file `crm/middleware/tenant.py`

```python
# crm/middleware/tenant.py
from flask import g, request, current_app
import re

INTERNAL_TENANT_ID = 1

def resolve_tenant():
    """Resolve tenant context for the current request and store in g."""
    tenant_id = None

    # 1. JWT claim
    try:
        from flask_jwt_extended import get_jwt
        jwt_data = get_jwt()
        tenant_id = jwt_data.get("tenant_id")
    except Exception:
        pass

    # 2. Subdomain
    if not tenant_id:
        host = request.host.split(":")[0]  # strip port
        # Match *.lexflow.app subdomains
        match = re.match(r'^([\w-]+)\.lexflow\.app$', host)
        if match:
            slug = match.group(1)
            tenant_id = _lookup_tenant_id_by_slug(slug)

    # 3. Custom domain
    if not tenant_id:
        tenant_id = _lookup_tenant_id_by_domain(request.host)

    # 4. Path prefix
    if not tenant_id:
        match = re.match(r'^/api/tenant/([\w-]+)/', request.path)
        if match:
            tenant_id = _lookup_tenant_id_by_slug(match.group(1))

    # 5. Header
    if not tenant_id:
        slug_or_id = request.headers.get("X-Tenant-Id") or request.headers.get("X-Tenant-Slug")
        if slug_or_id:
            if slug_or_id.isdigit():
                tenant_id = int(slug_or_id)
            else:
                tenant_id = _lookup_tenant_id_by_slug(slug_or_id)

    # 6. Default
    if not tenant_id:
        tenant_id = INTERNAL_TENANT_ID

    g.tenant_id = tenant_id

    # Attach the tenant record (lazy-loaded, cached per request)
    from crm.models.tenant import Tenant
    g.tenant = Tenant.query.get(tenant_id)


def _lookup_tenant_id_by_slug(slug):
    """Memoized lookup; cache in a module-level dict or request context."""
    from crm.models.tenant import Tenant
    tenant = Tenant.query.filter_by(slug=slug, is_active=True).first()
    return tenant.id if tenant else None


def _lookup_tenant_id_by_domain(host):
    """Resolve tenant by custom domain."""
    from crm.models.tenant import Tenant
    tenant = Tenant.query.filter_by(custom_domain=host, is_active=True).first()
    return tenant.id if tenant else None
```

### 2.2 Registration in app factory

In `crm/__init__.py`, `create_app()`:

```python
from .middleware.tenant import resolve_tenant

def create_app():
    app = Flask(__name__)
    # ... existing setup ...

    # Register tenant middleware (runs before every request)
    app.before_request(resolve_tenant)

    # ... register blueprints ...
```

### 2.3 JWT identity claim

When creating access tokens (in auth routes), include `tenant_id` in the additional claims:

```python
from flask_jwt_extended import create_access_token

access_token = create_access_token(
    identity=str(user.id),
    additional_claims={
        "tenant_id": current_tenant_id,   # from g.tenant_id or membership lookup
        "tenant_slug": current_tenant_slug,
    }
)
```

### 2.4 The "internal" tenant seed

Add a data migration to seed the internal tenant:

```python
# migration: seed_internal_tenant.py
def upgrade():
    op.execute("""
        INSERT INTO tenants (id, name, slug, plan)
        VALUES (1, 'LexFlow — Internal Workspace', 'lexflow', 'internal')
        ON CONFLICT (id) DO NOTHING;
    """)
```

### 2.5 Backfill existing NULL tenant_id rows

Same migration: assign all rows with `tenant_id IS NULL` to tenant 1:

```python
for tbl in ('contacts', 'cases', 'tasks', 'events'):
    op.execute(f"UPDATE {tbl} SET tenant_id = 1 WHERE tenant_id IS NULL;")
    # Make tenant_id NOT NULL going forward (new rows must have it)
    op.execute(f"ALTER TABLE {tbl} ALTER COLUMN tenant_id SET NOT NULL;")
```

> **Note on SQLite:** `ALTER COLUMN SET NOT NULL` is not supported in SQLite. For SQLite dev, the NOT NULL constraint must be enforced at the application layer (model `__init__`). For Postgres (production), a full `ALTER COLUMN` works.

### 2.6 Adding `tenant_id` to the User model

The `users` table itself does NOT get a `tenant_id` — users are global. Instead, membership is tracked via `tenant_memberships`.

However, for convenience in querying, `User` gets a relationship:

```python
# crm/models/user.py (add)
memberships = db.relationship("TenantMembership", backref="user", lazy=True)
```

### 2.7 Routes that stay global (no tenant scope)

These routes bypass tenant resolution or always use tenant 1:

| Route | Reason |
|-------|--------|
| `GET /api/health` | Infrastructure health check |
| `POST /api/auth/login` | Must work before tenant is known |
| `GET /api/auth/me` | Returns user info regardless of tenant |
| `POST /api/intake/` | Public intake — gets tenant from form field, header, or defaults to 1 |

---

## 3. Phase 3 — Query Filters (Opt-In, Route-by-Route)

### 3.1 Strategy: explicit `.filter_by(tenant_id=...)` everywhere

Do NOT add a global SQLAlchemy event listener that auto-appends `tenant_id`. That approach makes it too easy to accidentally omit the filter in the admin panel and hides intent. Instead, **every route handler** that touches tenant-scoped data must explicitly include `.filter_by(tenant_id=g.tenant_id)`.

**Why explicit:** Debuggability, intent visibility, admin override.

### 3.2 Helper mixin for models

To reduce boilerplate and prevent oversights:

```python
# crm/models/mixins.py
from flask import g

class TenantScopedMixin:
    """Add to any model that is tenant-isolated."""

    @classmethod
    def query_by_tenant(cls, tenant_id=None):
        """Return a base query filtered to the current tenant."""
        tenant_id = tenant_id or getattr(g, 'tenant_id', 1)
        return cls.query.filter_by(tenant_id=tenant_id)

    @classmethod
    def get_by_tenant(cls, record_id, tenant_id=None):
        """Get a single record scoped to tenant; returns None if cross-tenant."""
        tenant_id = tenant_id or getattr(g, 'tenant_id', 1)
        return cls.query.filter_by(id=record_id, tenant_id=tenant_id).first()
```

Usage in models:

```python
class Contact(db.Model, TenantScopedMixin):
    __tablename__ = "contacts"
    # ... existing fields ... tenant_id = db.Column(...)
```

### 3.3 Route-by-route conversion

#### 3.3.1 Public intake (`POST /api/intake/`)

```python
# crm/routes/intake.py
from flask import g

@intake_bp.post("/")
@intake_bp.post("")
def create_intake():
    # ... parse data ...
    tenant_id = data.get("tenant_id") or getattr(g, "tenant_id", 1)
    contact = Contact(
        tenant_id=tenant_id,
        # ... other fields ...
    )
    # Same for Case
```

**How intake gets its tenant:**
- If the public form includes a hidden `tenant_id` or `tenant_slug` field → use it.
- If request comes through a subdomain → `g.tenant_id` is already set.
- Fallback → tenant 1 (internal).

#### 3.3.2 Contacts CRUD (`GET/POST /api/contacts`)

```python
@contacts_bp.get('/contacts')
def get_contacts():
    contacts = Contact.query_by_tenant().filter_by(is_deleted=False).order_by(Contact.id.desc()).all()
    return jsonify([c.to_dict() for c in contacts]), 200

@contacts_bp.post('/contacts')
def create_contact():
    data = request.get_json()
    # ...
    contact = Contact(
        tenant_id=g.tenant_id,
        # ...
    )
```

#### 3.3.3 Cases CRUD (`GET/POST /api/cases`)

```python
@cases_bp.get("/cases")
@jwt_required()
def get_cases():
    query = Case.query_by_tenant()
    # ... existing status/priority filters ...
    paginated = query.order_by(Case.id.desc()).paginate(...)
```

#### 3.3.4 Kanban API (`GET /api/kanban/cases`)

```python
@kanban_api_bp.get("/cases")
@jwt_required()
def get_kanban_cases():
    cases = Case.query_by_tenant().order_by(Case.id.desc()).all()
```

#### 3.3.5 Tasks

```python
@tasks_bp.get('/tasks')
def get_tasks():
    tasks = Task.query_by_tenant().order_by(Task.id.desc()).all()
```

#### 3.3.6 Events

```python
@events_bp.get('/events')
def get_events():
    events = Event.query_by_tenant().order_by(Event.id.desc()).all()
```

### 3.4 Admin override (global cross-tenant view)

Admin users (role = `"admin"`) can bypass tenant scoping:

```python
# Admin context: skip tenant filter for super-admin roles
from flask_jwt_extended import get_jwt

jwt_data = get_jwt()
is_admin = jwt_data.get("role") == "admin"

if is_admin and request.args.get("all_tenants"):
    query = Case.query  # no filter
else:
    query = Case.query_by_tenant()
```

Add an `all_tenants=true` query parameter to admin API calls.

### 3.5 Safety belt: warning on unscoped queries

Add a simple audit in the middleware or a SQLAlchemy `before_execute` event that logs a warning when tenant-scoped tables are queried without a `tenant_id` filter:

```python
# In crm/middleware/tenant.py or a dedicated audit module
import logging
logger = logging.getLogger(__name__)

# This is aspirational — real implementation needs SQLAlchemy event listening
# on before_execute to inspect compiled query for tenant_id in WHERE clause.
# For now, add a code-review checklist item (see Section 7).
```

**Simpler safety net:** Add it as a code review rule: every new query on `contacts`, `cases`, `tasks`, `events` must include `.filter_by(tenant_id=...)` unless the route is explicitly in the global-whitelist.

### 3.6 Backfill script (run once)

```python
# scripts/backfill_tenant_id.py
from crm import create_app
from crm.extensions import db
from crm.models.contact import Contact
from crm.models.case import Case
from crm.models.task import Task
from crm.models.event import Event

app = create_app()
with app.app_context():
    for model in (Contact, Case, Task, Event):
        count = model.query.filter_by(tenant_id=None).update(
            {model.tenant_id: 1}, synchronize_session=False
        )
        print(f"Backfilled {count} rows in {model.__tablename__}")
    db.session.commit()
```

---

## 4. Phase 4 — Tenant Onboarding + Auth

### 4.1 Tenant onboarding flow (admin creates new studio)

```
Admin (you) fills form → Creates tenant record → Provisions subdomain → Sends invite
```

**New endpoint:** `POST /api/admin/tenants` (admin-only, JWT required)

```json
{
  "name": "Studio Legale Pagliano",
  "slug": "pagliano",
  "plan": "pro",
  "admin_email": "avvocato@pagliano.studio",
  "subdomain": "pagliano"
}
```

**What happens server-side:**

1. Create `tenants` row with the slug, name, plan, subdomain.
2. Create `users` row for `admin_email` (or look up existing user).
3. Create `tenant_memberships` row with `role = "admin"`.
4. If `subdomain` provided, configure DNS/wildcard record (manual or via Railway/Cloudflare API).
5. Send invitation email with onboarding link.
6. Return tenant details + invitation token.

### 4.2 Auto-provision subdomain

**Railway + Cloudflare approach:**

- Wildcard DNS `*.lexflow.app` → Railway.
- Railway routes based on `Host` header.
- Or use a simple path-based routing: `lexflow.app/tenant/pagliano/...`

**Recommended approach for MVP:** **Subdomain-based** via Railway wildcard cert (`*.lexflow.app`) + nginx/Flask host matching.

**Registration** happens when admin creates the tenant. The tenant's slug becomes their subdomain: `{slug}.lexflow.app`.

### 4.3 Tenant-aware login

The login flow changes from "global login" to "tenant-scoped login":

```
User lands on pagliano.lexflow.app/login
  → Middleware resolves tenant_id = 2 (Pagliano)
  → Login page renders with tenant branding
  → User submits email + password
  → Auth checks:
      1. User exists globally
      2. User has membership in this tenant (tenant_memberships)
      3. User's password matches
  → Create JWT with:
      - identity = user.id
      - additional_claims = { tenant_id: 2, tenant_slug: "pagliano", role: "admin" }
```

**Implementation in `auth.py`:**

```python
@auth_bp.post('/login')
def login():
    data = request.get_json()
    tenant_id = getattr(g, 'tenant_id', None)

    if not tenant_id:
        return jsonify({'error': 'Tenant not resolved. Use subdomain or X-Tenant-Id header.'}), 400

    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Check membership in this tenant
    membership = TenantMembership.query.filter_by(
        user_id=user.id, tenant_id=tenant_id
    ).first()
    if not membership:
        return jsonify({'error': 'No access to this workspace'}), 403

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            'tenant_id': tenant_id,
            'tenant_slug': g.tenant.slug,
            'role': membership.role,
        }
    )
    return jsonify({'access_token': access_token, 'user': user.to_dict()}), 200
```

### 4.4 Multi-tenant login (user in multiple tenants)

A user who belongs to multiple tenants needs a tenant picker:

**Endpoint:** `POST /api/auth/tenant-picker`

```python
@auth_bp.post('/tenant-picker')
def tenant_picker():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid credentials'}), 401

    memberships = TenantMembership.query.filter_by(user_id=user.id).all()
    tenants = [{
        'id': m.tenant_id,
        'name': m.tenant.name,
        'slug': m.tenant.slug,
        'role': m.role,
    } for m in memberships]

    return jsonify({'tenants': tenants}), 200
```

Then the user picks a tenant and gets a dedicated JWT scoped to that tenant.

### 4.5 Invitation flow

**Endpoint:** `POST /api/tenants/{tenant_id}/invite`

```json
{
  "email": "colleague@pagliano.studio",
  "role": "member"
}
```

**Server-side:**
1. Check requesting user is admin of this tenant.
2. Look up user by email or create placeholder.
3. Create `tenant_memberships` row with `invited_at`, no `joined_at`.
4. Generate invitation token (JWT with expiry).
5. Send invitation email with link to accept + set password.

**Accept invitation:** `POST /api/auth/accept-invite`

```json
{
  "token": "...",
  "password": "secure-password"
}
```

### 4.6 JWT structure with tenant claims

```json
{
  "sub": "42",
  "tenant_id": 2,
  "tenant_slug": "pagliano",
  "role": "admin",
  "iat": 1719763200,
  "exp": 1719849600
}
```

**Middleware enforcement:** On every `@jwt_required()` route, verify that `g.tenant_id` matches the JWT `tenant_id` claim:

```python
from flask_jwt_extended import verify_jwt_in_request, get_jwt

@jwt_required()
def some_route():
    jwt_data = get_jwt()
    if jwt_data.get("tenant_id") != g.tenant_id:
        return jsonify({"error": "Tenant mismatch"}), 403
```

Or use a decorator:

```python
def tenant_matches_jwt():
    jwt_data = get_jwt()
    if jwt_data.get("tenant_id") != g.tenant_id:
        return jsonify({"error": "Tenant mismatch"}), 403
```

### 4.7 Auth policy per tenant (future)

Each tenant can have different auth requirements stored in `tenants.settings`:

```json
{
  "auth": {
    "method": "sso",         // "password" | "sso" | "mfa" | "saml"
    "sso_provider": "google",
    "mfa_required": true,
    "session_duration_hours": 24
  }
}
```

During login, the auth route reads `g.tenant.settings` and adapts the flow accordingly. (Phase 4++ — not MVP.)

---

## 5. Capacity & Scaling Notes

### Current assessment

- **Tech stack:** Flask + SQLAlchemy + Postgres (prod) / SQLite (dev)
- **Expected tenant count:** Low (5–20 studios initially)
- **Data per tenant:** < 10K rows per table
- **Concurrent users:** < 50

### Scaling implications of multi-tenancy

| Concern | Impact | Mitigation |
|---------|--------|------------|
| Row-level filters | `WHERE tenant_id = ?` is indexed (indexes created in Phase 1) | ✓ Covered |
| Connection pool | More tenants = more queries; but same DB | Pool size of 10–20 is fine |
| `tenants` table lookups | Subdomain → tenant_id lookup on every request | Cache in Redis or in-process dict; TTL 60s |
| Custom domains | DNS resolution; SSL certs | Use Railway wildcard + Let's Encrypt |
| Admin cross-tenant queries | No `tenant_id` filter; full table scan | Add pagination + explicit `all_tenants=true` param |

### Recommended: In-memory tenant cache

```python
# crm/middleware/tenant.py
import time
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_tenant_lookup(slug_or_domain: str, lookup_type: str = "slug") -> int | None:
    """Cache tenant lookups for 60 seconds using TTL via wrapper."""
    from crm.models.tenant import Tenant
    if lookup_type == "slug":
        tenant = Tenant.query.filter_by(slug=slug_or_domain, is_active=True).first()
    else:
        tenant = Tenant.query.filter_by(custom_domain=slug_or_domain, is_active=True).first()
    return tenant.id if tenant else None
```

For production, replace with Redis:

```python
# crm/services/cache.py
import redis, json
cache = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

def get_tenant_id_by_slug(slug: str) -> int | None:
    key = f"tenant:slug:{slug}"
    tid = cache.get(key)
    if tid is not None:
        return int(tid)
    tenant = Tenant.query.filter_by(slug=slug, is_active=True).first()
    if tenant:
        cache.setex(key, 60, tenant.id)  # 60s TTL
        return tenant.id
    return None
```

---

## 6. Migration Sequence — Deploy Order

Each phase is a separate deploy. Do NOT combine phases.

```
Phase 1 ✅ DONE — Schema: tenants table + tenant_id columns (nullable)
     │
     ▼
Phase 2a ─ Seed internal tenant (id=1), backfill NULL → 1, add NOT NULL
     │        File: migrations/versions/phase2a_seed_internal_tenant.py
     │        File: crm/models/tenant.py (NEW)
     │        File: crm/models/tenant_membership.py (NEW)
     │
Phase 2b ─ Middleware: resolve_tenant(), register in create_app()
     │        File: crm/middleware/__init__.py (NEW)
     │        File: crm/middleware/tenant.py (NEW)
     │        Modify: crm/__init__.py
     │
Phase 2c ─ JWT claims: include tenant_id in access tokens
     │        Modify: crm/routes/auth.py
     │
     ▼
Phase 3a ─ Add TenantScopedMixin, convert intake + contacts + cases routes
     │        File: crm/models/mixins.py (NEW)
     │        Modify: crm/models/contact.py, case.py, task.py, event.py
     │        Modify: crm/routes/intake.py, contacts.py, cases.py, kanban_api.py
     │
Phase 3b ─ Convert kanban dashboard, tasks, events routes
     │        Modify: crm/routes/tasks.py, events.py (if exists), kanban.py
     │
     ▼
Phase 4a ─ Tenant onboarding endpoint (admin creates studios)
     │        File: crm/routes/admin_tenants.py (NEW)
     │        Modify: crm/__init__.py (register blueprint)
     │
Phase 4b ─ Tenant-aware login + invitation flow
     │        Modify: crm/routes/auth.py
     │        File: crm/routes/invitations.py (NEW)
     │
Phase 4c ─ Admin cross-tenant view + tenant picker
     │        Modify: crm/routes/auth.py (tenant-picker)
     │        Modify: crm/middleware/tenant.py (admin override)
     │
     ▼
Phase 5+ ─ Capacity improvements, Redis cache, custom domains
```

---

## 7. Potential Pitfalls

### 7.1 NULL tenant_id = internal workspace

**Problem:** Existing rows have `tenant_id = NULL`. If code does `.filter_by(tenant_id=g.tenant_id)` and `g.tenant_id = 1`, those NULL rows are excluded (NULL != 1 in SQL).

**Solution:** Phase 2a backfill sets `tenant_id = 1` on all NULL rows, then adds `NOT NULL` constraint. After that, no NULLs exist.

**Mid-transition safety:** While backfilling, use `db.or_(tenant_id == g.tenant_id, tenant_id.is_(None))` in the query filter.

### 7.2 Subdomain vs custom domain routing

**Problem:** Both `pagliano.lexflow.app` and `pagliano.studio` point to the same app. The middleware must resolve both to the same tenant.

**Solution:** The middleware checks subdomain first (pattern-matched), then custom domain (exact match). Both return the same tenant_id.

**Wildcard cert:** Railway/Cloudflare must have `*.lexflow.app` SSL wildcard cert.

### 7.3 Cache keys must include tenant_id

**Problem:** Flask endpoint caching (if added later) would serve tenant A's data to tenant B.

**Solution:** All cache keys must include `tenant_id` as a prefix or suffix:
- `cache_key = f"tenant:{g.tenant_id}:cases:list"`
- Redis keys: `tenant:{id}:cases:{page}`

### 7.4 Admin panel must see across tenants

**Problem:** If the admin user's JWT has `tenant_id = 1`, they can't see studio data.

**Solution:** Admin override via `all_tenants=true` query param (Section 3.4). Also, the admin's JWT can carry `tenant_id = "global"` or use a special claim like `"sudo": true`.

**Recommended approach:** Admin users get `tenant_id = 1` in their JWT but the middleware checks `jwt_data.get("role") == "admin"` and allows cross-tenant queries when requested.

### 7.5 Tenant deletion/archival

**Problem:** Hard-deleting a tenant would cascade-delete all their contacts, cases, tasks, events.

**Solution:** Soft-delete only:
1. Set `tenants.is_active = False`, `tenants.deleted_at = now`.
2. All routes check `Tenant.query.filter_by(is_active=True)` when resolving.
3. No cascade delete of data — data is orphaned but recoverable.
4. Admin panel shows "deleted tenants" section with restore option.
5. Future: GDPR right-to-erasure can actually hard-delete after 90-day grace period.

### 7.6 Public intake form + tenant assignment

**Problem:** The public intake form (on Pagliano's landing page) doesn't know about tenants. It posts to `/api/intake/` which defaults to tenant 1.

**Solution options (in priority order):**
1. Each studio's LP includes a hidden `tenant_slug` field → middleware sets `g.tenant_id`.
2. Each studio's LP posts to its subdomain → subdomain routing resolves tenant.
3. Intake endpoint accepts `X-Tenant-Slug` header set by the LP.

### 7.7 Race conditions on tenant creation

**Problem:** Two admins create a tenant with the same slug simultaneously.

**Solution:** `slug` has a UNIQUE constraint in the DB. The second `INSERT` fails, app catches `IntegrityError`, returns a friendly error.

### 7.8 Legacy sessions/tokens without tenant_id

**Problem:** Existing JWT tokens (issued before Phase 2c) have no `tenant_id` claim.

**Solution:** 
1. Accept tokens without `tenant_id` for a transition period.
2. In middleware, if JWT has no `tenant_id`, use subdomain/header resolution and log a warning.
3. Set token expiry low during transition (existing users re-login).
4. After transition, reject tokens without `tenant_id`.

### 7.9 Code review checklist for future PRs

Every PR that touches `contacts`, `cases`, `tasks`, or `events` must verify:

- [ ] All new queries include `.filter_by(tenant_id=...)`.
- [ ] If intentionally cross-tenant: wrapped in `if is_admin:` guard.
- [ ] New models that belong to a tenant use `TenantScopedMixin`.
- [ ] Cache keys include `tenant_id`.
- [ ] New endpoints that bypass tenant scoping are documented in the global whitelist.

---

## Summary of files to create/modify

### New files

| File | Phase | Purpose |
|------|-------|---------|
| `crm/models/tenant.py` | 2a | `Tenant` model |
| `crm/models/tenant_membership.py` | 2a | `TenantMembership` model |
| `crm/middleware/__init__.py` | 2b | Package init |
| `crm/middleware/tenant.py` | 2b | `resolve_tenant()` middleware |
| `crm/models/mixins.py` | 3a | `TenantScopedMixin` helper |
| `crm/routes/admin_tenants.py` | 4a | Tenant onboarding endpoints |
| `crm/routes/invitations.py` | 4b | Invitation endpoints |
| `scripts/backfill_tenant_id.py` | 2a | One-time backfill utility |

### Modified files

| File | Change |
|------|--------|
| `crm/__init__.py` | Register `before_request` middleware + new blueprints |
| `crm/models/__init__.py` | Import new models |
| `crm/models/contact.py` | Add `TenantScopedMixin`, `tenant_id` relationship |
| `crm/models/case.py` | Add `TenantScopedMixin`, `tenant_id` relationship |
| `crm/models/task.py` | Add `TenantScopedMixin`, `tenant_id` relationship |
| `crm/models/event.py` | Add `TenantScopedMixin`, `tenant_id` relationship |
| `crm/models/user.py` | Add `memberships` relationship |
| `crm/routes/auth.py` | Tenant-aware login, JWT claims, tenant-picker |
| `crm/routes/intake.py` | Use `g.tenant_id` for new records |
| `crm/routes/contacts.py` | Add `.filter_by(tenant_id=...)` |
| `crm/routes/cases.py` | Add `.filter_by(tenant_id=...)` |
| `crm/routes/kanban_api.py` | Add `.filter_by(tenant_id=...)` |
| `crm/routes/tasks.py` | Add `.filter_by(tenant_id=...)` |
## Links
- Parent: [[documents-INDEX]]
- Related: [[safety_assessment]]
