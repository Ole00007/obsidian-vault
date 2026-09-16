# Operator Installer Prompt — RLS Hardening + Backend Dev Delegation

Do NOT deploy, push, or touch production. Sprint-scoped work, not a launch blocker.

## Context
RLS (Row-Level Security) is confirmed NOT built (D12 finding). Current tenant isolation is
app-level `workspace_filter()` only. Decision: ship now, add RLS as belt-and-suspenders within
1–2 sprints — this is a hardening ticket, not a blocker.

## Step 1 — Clone as reference only (~1hr), do not install as a dependency
```bash
git clone https://github.com/kdpisda/flask-rls.git ~/refs/flask-rls-pattern
git clone https://github.com/dikshantrajput/supabase-multi-tenancy.git ~/refs/rls-sql-pattern
```
Read both. `flask-rls` is Flask+SQLAlchemy native — closer to our stack. The Supabase repo's SQL
policies (`ENABLE ROW LEVEL SECURITY` / `FORCE ROW LEVEL SECURITY` / `CREATE POLICY`) are portable
even though its JWT-claim lookups (`auth.jwt()`, `auth.uid()`) are not — swap those for our own
`current_setting('app.current_tenant')` pattern.

## Step 2 — List every table currently filtered by `workspace_filter()`
So the delegation ticket scope (N tables) is exact, not estimated. Output as a plain list.

## Step 3 — Confirm Alembic migration compatibility risk
RLS policies via `ALTER TABLE` inside Alembic migrations have known community-reported friction
(policy versioning, upgrade/downgrade symmetry). Flag any specific risk found in our migration
setup before the ticket goes out.

## Step 4 — Draft the backend-dev delegation ticket (do not file it yet)
Write the full ticket text using this scope, substituting the real table count from Step 2:

> **Title:** Add PostgreSQL Row-Level Security (RLS) as second-layer tenant isolation
>
> **Scope:** Add RLS policies to [N] tables using the `tenant_id`/`workspace_id` column, mirroring
> existing `workspace_filter()` logic as a second enforcement layer (not a replacement). Add
> `SET LOCAL app.current_tenant` per request in Flask middleware — must be `SET LOCAL` inside a
> transaction, never plain `SET`, to avoid leaking tenant context across pooled connections.
> Write cross-tenant isolation regression tests (Tenant A cannot read/write Tenant B rows) for
> every table touched. Add a composite index on `(tenant_id, ...)` per table.
>
> **Reference:** `~/refs/flask-rls-pattern` (Flask/SQLAlchemy pattern) and
> `~/refs/rls-sql-pattern` (SQL policy syntax reference only).
>
> **Budget:** 1–2 days RLS implementation + 0.5 day dedicated test suite.
>
> **Out of scope:** schema-per-tenant, physical DB-per-customer, RBAC-within-tenant (revisit
> `point-source/supabase-tenant-rbac` separately if per-role permissions are needed later).

## Step 5 — Present the drafted ticket to me for approval
Show me the full ticket text (Step 4 output) plus the table list (Step 2) and any Alembic risk
flags (Step 3). I will tell you explicitly whether to:
(a) file it as a Linear issue,
(b) file it as a GitHub Issue in the repo, or
(c) hand it directly to a named backend dev via [Slack/email/other channel — confirm which].

## Hard stop
Do not create any Issue, ticket, or PR in Linear or GitHub. Do not message or assign any backend
dev. Do not touch code beyond the two read-only reference clones. Report findings and the drafted
ticket only, then wait for my explicit go-ahead on filing + assignment.
