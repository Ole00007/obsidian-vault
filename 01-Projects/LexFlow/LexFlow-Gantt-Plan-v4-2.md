# LexFlow CRM — Frappe Gantt Integration, Hermes Build Plan v4.2

**Status:** final pre-build plan. Execute prerequisite and inspection gates first; do not begin Gantt code immediately.

**Product name:** LexFlow CRM. Do not use the retired MVP-era product name in new code, documents, branches, commits, UI text or reports.

**Repository:** https://github.com/Ole00007/lexflow-crm

**Primary objective:** add a safe internal staff Gantt view (C) by reusing LexFlow CRM task data. Define the client-safe view (D) now and start it automatically when the explicit D activation event in this plan occurs.

## 0. Governing rules

1. Work in this order: **Understand → Explore → Plan → Implement → Verify → Document → Next step**.
2. Reuse existing code and approved documents before creating anything.
3. Work in small reversible iterations.
4. Never edit an existing migration. Create a new migration only after schema approval, backup and a verified rollback path.
5. Never push directly to `main`. Use `staging` for staging and a pull request for production.
6. Never use the production `DATABASE_URL` for local tests.
7. Do not touch auth, payment, production configuration or unrelated files without flagging the change first.
8. At every gate, save work, verify locally, commit, push the working branch and record the evidence.
9. All database access must follow the active architecture confirmed at P1. If the active path is the Node monorepo, queries go through `/packages/db/repositories`. If the approved Flask-first override remains active, use the existing Flask SQLAlchemy model/service pattern and do not mix Flask code into `/apps/api`.
10. Schema fields come only from the latest approved Master Plan and latest approved Starter. Archived CSVs and older fragments are reference-only.

## 1. Sources and reuse

### Frappe Gantt

Do not fork Frappe Gantt. Vendor the built JavaScript, CSS and license from one immutable npm archive.

| Item | Action | Link |
|---|---|---|
| Source repository | Read implementation and issues | https://github.com/frappe/gantt |
| npm registry metadata | Confirm latest version | https://registry.npmjs.org/frappe-gantt |
| Default archive | Use 1.2.2 | https://registry.npmjs.org/frappe-gantt/-/frappe-gantt-1.2.2.tgz |
| Fallback archive | Use 1.0.3 only if 1.2.2 fails an option or smoke test | https://registry.npmjs.org/frappe-gantt/-/frappe-gantt-1.0.3.tgz |
| Official demo | Compare expected behavior | https://frappe.io/gantt |
| Configuration | Verify option names | https://docs.frappe.io/gantt/config |

Copy only:

- `dist/frappe-gantt.umd.js`
- `dist/frappe-gantt.css`
- `license.txt` from the same downloaded package

Do not use a floating content-delivery-network URL in production. Record the archive version and SHA-256 checksum in the gate report.

Previously calculated archive checksums to re-verify locally:

| Version | SHA-256 |
|---|---|
| 1.2.2 | `2e8c82de7b5423466cf28e7e6f52c163f34f2e65dedf2b0e2b5ea217529fc2c5` |
| 1.0.3 | `08027d91532bb0c8b7bba36699edd7b4e8bce08eb1f3fa507fd1723b8a6a26ac` |

### Hermes community plugin

Hermes has a separate community `kanban-gantt` plugin:

- Catalog: https://github.com/NousResearch/hermes-agent/blob/main/plugin-catalog/kanban-gantt.yaml
- Repository: https://github.com/e-is/hermes-kanban-gantt

It visualizes Hermes Desktop Kanban data; it is not LexFlow CRM code and is not Frappe Gantt. Its GPL-3.0 code is reference-only. Do not copy it into LexFlow CRM. Reuse only non-code ideas such as filters, task drawer behavior and test cases.

### LexFlow CRM

Reuse the active CRM authentication, task model, calendar rules, Kanban behavior, base layout, error patterns and test fixtures after P1 confirms where the authoritative implementation lives.

## 2. P0 — Backup and remote/local inventory

### Remote findings already confirmed

GitHub-visible branches reviewed on 2026-10-12:

- `main`
- `lexflow_hermes_v1`
- `railway/code-change-p5yOFx`

GitHub `main` contains:

- Flask CRM under `/crm`
- Partial Node API under `/apps/api`
- Database package under `/packages/db`
- No GitHub-visible `/apps/web`
- No GitHub-indexed Gantt code
- No root `CLAUDE.md` visible on `main`

Do not repeat this remote discovery unless the remote commit has changed.

### Local-only inspection

Hermes must inspect only state unavailable remotely:

```text
git status --short --branch
git branch -vv
git branch -a
git worktree list
git stash list
git log --all --decorate --oneline -30
git diff --stat
git diff --cached --stat
```

Search tracked and untracked project files for:

```text
gantt
frappe-gantt
apps/web
CLAUDE.md
startdate
start_date
Kanban
calendar
GANTT_WRITE_ENABLED
Admy
Smothy
```

Do not change branches, apply a stash, reset, delete, migrate or write implementation code during this inspection.

Output:

```text
location | branch/worktree | commit | relevant files | reusable | conflict | recommended action
```

### Backup checkpoint

Before any later change:

1. Back up every file that may change.
2. Create and verify an application snapshot.
3. Confirm the backup can be read.
4. Create a clean git checkpoint.
5. Record the rollback command.

**P0 stop condition:** dirty or ambiguous working state, unverified backup, local-only architecture conflict, or existing Gantt work that has not been reviewed.

## 3. P1 — Architecture reconciliation

The current evidence conflicts:

- Current LexFlow project rules describe `/apps/web`, `/apps/api` and `/packages/db/repositories` as the stable architecture.
- The latest approved Master Plan contains an active Flask-first override and says to evaluate Node migration only after the Flask CRM ships and is tested.
- GitHub `main` has `/apps/api` and `/packages/db`, but no visible `/apps/web`; the most complete visible CRM feature set is under `/crm`.

Hermes must read, in priority order:

1. Local `CLAUDE.md`, if present.
2. Latest approved Master Plan workbook.
3. Latest approved Flask/backend Starter.
4. `LexFlow_Hermes_Context.md`.
5. Current app entry points, deploy configuration and tests.
6. Local-only branches/worktrees discovered at P0.

Then output one decision table:

```text
candidate architecture | complete locally | deployed | tests pass | approved source | missing pieces | recommendation
```

Decision rule:

- If a complete and approved local `/apps/web` exists and `CLAUDE.md` makes it active, use the Next.js/Node/repository architecture.
- Otherwise, if the latest approved Plan’s Flask-first override remains active, use the Flask CRM for this Gantt sprint.
- Do not create `/apps/web` only to host Gantt.
- Do not put Flask code in `/apps/api`.
- Do not create a third frontend.
- If the documents still conflict, stop and report the conflict to Olesia before code.

**P1 output:** `docs/gantt_architecture_decision.md`, including active frontend, backend, database-access pattern, auth pattern, deploy target, test command and rollback path.

## 4. P2 — Required data capability

### Current visible gap

The GitHub-visible Flask `Task` model has `duedate` but no approved task start date, progress field, dependency field, visibility field or version field. A Gantt duration cannot safely use `createdat` as its start.

### Start-date prerequisite

Before implementing C, Hermes must compare the latest approved Plan and Starter and locate an approved task start field.

- If it exists locally, map and test it.
- If it does not exist, prepare a minimal proposal for a nullable task start date, including exact name, type, validation, API impact, form impact, Kanban/calendar impact, existing-record behavior, migration and rollback.
- Do not infer start from task creation, case opening or another unrelated date.
- Do not create or apply the migration until Olesia approves the field and the backup rules are complete.

A possible field such as `tasks.startdate DATE NULL` is only a proposal, not an approved schema decision.

### Status prerequisite

Inspect the real Kanban statuses and staging data. Do not assume `To do`, `In progress` and `Done`. Create one explicit status-to-progress map in `docs/gantt_bar_semantics.md`.

Unknown status behavior:

- Add class `gantt-status-unknown`.
- Log only task ID and unknown value; never log client data.
- Fail the semantics cross-test until the value is mapped or deliberately excluded.

### Other fields

- Dependencies: omit unless an approved relationship exists.
- Milestone: render as a one-day bar only if an approved milestone type exists; otherwise omit milestone behavior.
- Progress: derive from approved statuses for read-only C unless a real approved progress field exists.

**P2 stop condition:** missing or unapproved start date, conflicting status definitions, or a proposed schema field not approved by Olesia.

## 5. P3 — Authorization prerequisite

Authentication means confirming who the user is. Authorization means confirming which records that user may access.

The visible Flask task-list route requires login but uses an unscoped `Task.query...all()`. Do not reuse that query.

Hermes must map:

- Current JWT identity type and role claims.
- `tasks.userid` or equivalent assignee field.
- `tasks.caseid`.
- `cases.ownerid`.
- `cases.assignedto`.
- Administrator-role behavior.
- Tenant/organization scope, if present.

Olesia must approve one explicit staff visibility rule. The protected Gantt query must apply that rule in the database query—not by filtering browser data.

Minimum authorization tests:

- Unauthenticated HTML denied.
- Unauthenticated JSON denied.
- User A cannot see User B’s unauthorized task.
- User A cannot see another client/case outside approved scope.
- Admin behavior matches the approved role policy.
- No sensitive fields appear in the response.

**P3 stop condition:** authorization rule unclear, any cross-user success, or client/tenant scope applied only in JavaScript.

## 6. P4 — Existing UI prerequisite

Confirm locally before Gantt:

- Authenticated CRM base layout exists.
- Kanban/task list exists and identifies the authoritative task source.
- Calendar exists or its date logic is documented.
- Navigation pattern exists.
- Empty, loading, error and access-denied states have an existing pattern.
- Baseline test suite passes.
- CRM runs locally without production secrets.

If the active architecture lacks an authenticated shell, task source or safe authorization layer, create/fix those prerequisites as separate small approved tasks before Gantt. Do not build a disconnected standalone Gantt page.

## 7. C and D semantics

### C — internal staff operations, implement first

```text
INTERNAL TASK: Prepare appeal documents

14 Oct              19 Oct                         25 Oct
  │                    │                              │
  ├████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░┤
  │                    ▲                              ▲
Approved task start  Status-derived progress      Task due date
```

C may show only approved staff-operational fields:

- Task title.
- Start and due dates.
- Approved status/progress representation.
- Priority, if approved.
- Case reference, if needed and authorized.
- Assigned staff, if needed and authorized.

C must not return description, notes, documents, tokens or unnecessary personal information in its default JSON response.

C rules:

| Rule | Required behavior |
|---|---|
| Start | Approved task start field only |
| End | Approved task due date/deadline field only |
| Progress | Single approved status map |
| Overdue | End is past and task is unfinished |
| Missing start or end | Exclude and report aggregate exclusion count |
| End before start | Reject from payload and log a non-sensitive data-quality warning |
| Dependencies | Omit unless an approved dependency relationship exists |
| Milestone | One-day bar only when an approved milestone type exists |

### D — client-safe case progress, explicit future phase

```text
CLIENT PHASE: Appeal preparation

14 Oct                                             25 Oct
  │                                                   │
  ├████████████████████████████░░░░░░░░░░░░░░░░░░░░░┤
  │                                                   ▲
Approved client phase start              Approved client-safe target
```

D is a separate server-generated projection. It is not C with hidden fields in browser JavaScript.

D may show only:

- Approved plain-language client phase.
- General client-safe progress.
- Approved target date or date range.
- Approved client-safe status message.

D must never expose internal task titles, internal priority, staff assignment, legal strategy, internal notes, hidden participants, documents, tokens or unapproved legal deadlines.

## 8. Exact D activation event

D is linked to one named event: **`D_READY`**.

`D_READY` occurs at the first release/gate review where **all six mandatory conditions below are true at the same time**. Condition 2 has two approved alternative mechanisms; one is sufficient.

| ID | Mandatory condition | Objective evidence |
|---|---|---|
| D1 | C is released and safe | C passed M6, all 7 staging smoke steps passed, and no open critical/high Gantt security or data-integrity defect exists |
| D2 | A client identity mechanism exists | Either **(A)** authenticated portal user securely maps to the main client/contact, or **(B)** an approved expiring, revocable, case-scoped tracking token exists; server-side tests pass |
| D3 | Client-to-case authorization exists | Server rejects access to every non-authorized case; cross-client and guessed-ID tests pass with zero unauthorized successes |
| D4 | Client visibility policy is approved | Olesia has approved phase labels, progress wording, which dates may be shown, and the explicit forbidden-field list |
| D5 | Client-safe source mapping exists | Every exposed client phase/status/date maps to approved source data; no value is inferred from notes, descriptions or hidden internal strategy |
| D6 | D test fixtures and rollback are ready | At least two clients, two cases and hidden internal tasks are covered; leakage, authorization, empty/error, mobile and rollback tests are specified |

### Owner behavior when `D_READY` occurs

The elected LexFlow CRM Project Owner must check the six conditions:

- At C’s M6 gate.
- At every later release that changes client auth, client portal, case authorization, status tracking or visibility policy.
- At least once per active build cycle while any D condition is incomplete.

When all conditions first become true, the Owner must, in the same working session:

1. Create `reports/D_READY_<YYYY-MM-DD>.md` with evidence for D1–D6.
2. Report to Olesia: **“D_READY is true; Phase D is starting.”**
3. Open a dedicated D branch from the approved base.
4. Start D0 immediately: contract, threat model, allowed-field whitelist and tests-first plan.
5. Do not merge or deploy D without the later D4 explicit owner approval gate.

If any condition is false, the Owner reports:

```text
D_READY = BLOCKED
failed condition | evidence | owner | smallest unblock task | risk | expected next check
```

The Owner must not silently postpone D after `D_READY`, and must not start D implementation before `D_READY`.

## 9. Phase D delivery gates

| Gate | Work | Stop/approval rule |
|---|---|---|
| D0 | API contract, threat model, field whitelist, fixtures, UI states and rollback plan | Owner reports to Olesia; no production code until contract review completes |
| D1 | Server-side client-safe projection and authorization | Cross-client and leakage tests must pass before UI work |
| D2 | Read-only client timeline UI | Smothy accessibility/UX cross-test and Admy security cross-test |
| D3 | Staging smoke test with test clients | 100% D tests and no internal-field leakage |
| D4 | Production merge/deploy | Olesia gives explicit “merge and deploy D” command |

D is read-only for its first release. Client editing, commenting or date changes are out of scope.

## 10. Gantt layers

### Layer 1 — C tracking

- Protected HTML route.
- Protected read-only JSON endpoint.
- Exact response whitelist: `id, name, start, end, progress, dependencies, custom_class`, unless the approved contract removes a field.
- `readonly: true`.

### Layer 2 — C interaction without saving

Allowed:

- Day, Week and Month views.
- Filters.
- Status and priority styling.
- Client-safe/internal-safe popups appropriate to the staff view.
- Keyboard navigation.
- Intentional timeline scrolling.

Forbidden:

- Dragging dates.
- Resizing bars.
- Editing progress.
- POST, PUT or PATCH requests.

Use `readonly`, `readonly_dates` and `readonly_progress` where the selected Frappe Gantt version supports them.

### Layer 3 — optional staff persistence

Layer 3 remains off by default and begins only after M4 approval.

Requirements:

- `GANTT_WRITE_ENABLED=false` by default.
- Per-record authorization.
- Cross-site-request-forgery protection where applicable.
- Server date validation.
- Optimistic locking with version or `updated_at`; stale writes return 409.
- Idempotent repeated updates.
- Audit record of actor, time, old value and new value.
- `move_dependencies: false`.
- Reuse approved Kanban/calendar update service.
- Additive migration only, after backup and rollback rehearsal.

## 11. Project ownership and agents

### Project Owner election

The LexFlow CRM Project Owner/orchestrator must be either **Admy** or **Smothy**. Do not choose by name or assumption. Run the separate `LexFlow-Admy-Smothy-Owner-Audit-Prompt.md` before M0.

Until that audit is accepted, **Admy is acting gate coordinator only**, not permanent Project Owner.

The elected Owner:

- Maintains project state, decisions, gates, costs, risks and next actions.
- Routes work but does not take authorship of every implementation task.
- Prevents two agents from editing the same file.
- Checks `D_READY` at the required events.
- Reports gate evidence to Olesia.
- Stops protected, destructive, unauthorized or over-budget work.
- Keeps local and GitHub state synchronized.
- Updates the Master Plan/project tracking when major decisions change.

The non-selected candidate becomes Deputy Owner and independent cross-reviewer. The Owner must not approve their own implementation work.

### Delivery agents

| Role | Responsibility | Model route |
|---|---|---|
| Backend | Read endpoint, mapping, authorization, tests; optional approved write layer | DeepSeek V4.1 Flash |
| Fronty | One Gantt page/component and isolated styles | Mercury 2.5; fallback DeepSeek V4.1 Flash |
| Smothy | UI, accessibility, responsive and browser-network review | DeepSeek V4.1 Flash unless elected Owner |
| Admy | Security, leakage, regression and gate coordination | GLM 5.3 Flash; low-cost Nous fallback if unavailable |
| Tester | Optional fuzz and negative-test generation | MissingNo or LongCat 2.5 Preview; paid low-cost Nous fallback if unavailable |

No reviewer may approve code authored by the same agent/model context without an independent review.

## 12. Nous Portal provider lock

For this build, every primary and fallback model must come from the live Nous Portal catalog:

https://portal.nousresearch.com/models

Do not use OpenRouter, direct Anthropic, direct Google, direct OpenAI, direct Moonshot, direct DeepSeek or an unapproved local provider.

At M0:

1. Re-read the live catalog.
2. Record the exact route identifier for every model.
3. Send one minimal probe to every paid model.
4. Record displayed price, actual charge, input tokens and output tokens.
5. Stop a route if actual billing exceeds the displayed rate by more than 25%.
6. Replace an unavailable model only with another current Nous Portal model.
7. Do not let a free/promotional model approve a gate.

This provider lock remains until Olesia explicitly changes it.

Planning prices to verify live:

| Model | Planned price, input/output per 1M tokens | Use |
|---|---:|---|
| Mercury 2.5 | $0.04 / $0.15 | Fronty |
| DeepSeek V4.1 Flash | $0.11 / $0.51 | Backend and Smothy |
| GLM 5.3 Flash | $0.12 / $0.40 | Admy/orchestration |
| LongCat 2.5 Preview | Free route when available | Fuzz generation only |
| MissingNo | Free route when available | Fuzz generation only |

Do not use Hermes-4-70B or Hermes-4-405B for the multi-step Hermes Agent loop. A chat model may be used outside the agent loop only if separately approved.

## 13. Budget

Planning estimate: $8–15 total. This is not a measured promise.

- Warning at $8.
- Stop and report to Olesia at $10 before further paid work.
- Absolute cap: $20.
- Record cost and hours at every gate.
- Stop any stage exceeding twice its estimate.

## 14. C milestone gates

| Gate | Content | Required action |
|---|---|---|
| P0 | Backup and remote/local inventory | Stop after report if state is ambiguous |
| P1 | Architecture decision | Olesia approves if conflict remains |
| P2 | Start date/status capability | Olesia approves any schema field/migration |
| P3 | Staff authorization rule and tests | Olesia approves policy |
| P4 | Existing UI/base readiness | Baseline tests pass |
| M0 | Existing-work report, schema map, owner election, library comparison and model probes | Approve scope |
| M1 | API contract, semantics file, vendored library/license | Quick approval |
| M2 | C Layer 1 locally, read-only | First visual inspection |
| M3 | C Layer 2 locally, still read-only | Optional visual inspection |
| M4 | Persistence/migration design | Explicit approval before Layer 3 code |
| M5 | Layer 3 on staging, if approved | Second visual inspection |
| M6 | Seven-step staging smoke test | Explicit “merge and deploy” command |

No auto-merge and no auto-deploy.

## 15. Risks and stop events

| Risk | Mitigation | Stop/report trigger |
|---|---|---|
| Architecture conflict | P1 evidence-based decision | Active target still unclear |
| Missing task start date | P2 approved proposal | Field absent or unapproved |
| Unscoped task query | P3 database-level authorization | Any unauthorized record returned |
| Client data leakage | Exact whitelist and negative tests | Any extra/sensitive key |
| Library behavior drift | Compare 1.2.2 with 1.0.3 | Required option missing/different |
| Promo billing mismatch | Probe and charge log | Actual price > displayed price by 25% |
| Free model disappears | Named current Nous fallback | Two failed calls |
| Two sources of truth | Gantt reads approved task/calendar source | New duplicate task/date table proposed |
| Unsafe migration | Backup, additive change, rollback | DROP, destructive ALTER or old migration edit |
| Existing page regression | Allowed-files list and full suite | Previously passing test fails |
| Secrets committed | Secret scan and `.env.example` only | Secret in repo/logs/output |
| Accidental deadline write | Read-only defaults and feature flag | Any write before M4 |
| Mobile overflow | Contained timeline scroller | Whole document overflows at 375 px |
| D started too soon | `D_READY` matrix | Any D implementation before all D1–D6 |
| D silently delayed | Owner event check | `D_READY` true but no report/D0 start |
| Owner conflict or absence | Owner audit and deputy | No accountable owner at M0 |

## 16. Cross-tests

Tester never equals author. Each report uses:

```text
test_name | verified | result | evidence | open_risks
```

| ID | Tester | Test | Pass condition |
|---|---|---|---|
| CT1 | Admy/security reviewer | Authentication and record authorization | 0 unauthorized successes; 0 server 500s |
| CT2 | Admy plus Smothy browser confirmation | JSON field leakage | Exact whitelist; 0 extra/sensitive keys |
| CT3 | Smothy plus Backend | C semantics fixture: not started, active, done, overdue, missing date, invalid dates | Every expected inclusion, exclusion, fill and class matches semantics file |
| CT4 | Smothy | Empty/loading/error, 1 task, 200 tasks, 375 px and 1440 px, keyboard/focus/popup | No accidental document overflow; all states visible; controls keyboard accessible |
| CT5 | Admy | Regression and integrity | Existing tests pass; changed files allowed; Kanban/calendar dates match; 0 writes while flag off |

Layer 2 manipulation check:

- Drag/resize controls are absent or inert.
- Pointer and keyboard attempts cause zero client-state date changes.
- Zero write requests are sent.
- Zero database writes occur.

## 17. C staging smoke test

Run on staging before any merge to `main`:

1. `/health` returns 200.
2. Test staff user logs in and opens C; at least one authorized task renders.
3. Page loads under 3 seconds and JSON under 500 ms for about 200 tasks.
4. Zero browser console errors; Frappe Gantt loads from the LexFlow domain, not a CDN.
5. Logged-out access is denied or redirected correctly.
6. Kanban/calendar still open and show the same authoritative dates.
7. Rollback is rehearsed and documented.

Any failure blocks merge.

## 18. Mobile requirement

At 375 px:

- The overall page has no accidental horizontal overflow.
- The timeline has one intentional, labelled, keyboard-accessible horizontal scroll region.
- Navigation, filters and status messages remain inside the viewport.
- Focus indicators remain visible.
- Bars are not compressed into unreadable widths.

## 19. Success criteria

| Parameter | Required target |
|---|---|
| Existing tests | 100% passing; count not lower than baseline |
| New tests | All planned prerequisite, C and approved Layer 3 tests pass |
| Cross-tests | CT1–CT5 pass; reviewer differs from author |
| Smoke test | 7/7 on staging |
| Authorization | 0 unauthorized records |
| Data exposure | Exact whitelist; 0 secrets; 0 internal fields in D |
| Database | No Layers 1–2 schema change except separately approved P2 prerequisite; any migration additive and reversible |
| Performance | Page <3 s; JSON <500 ms for ~200 tasks |
| Mobile | Only intentional timeline scrolling at 375 px |
| Cost | At or below $20; stop review at $10 |
| Rollback | Rehearsed; target restoration under 5 minutes |
| Ownership | Project Owner elected and Deputy named |
| D activation | Owner checks D1–D6 at required events and starts D0 when `D_READY` becomes true |
| Approvals | Required owner/Olesia approvals recorded |

## 20. Gate deliverables

Every gate report includes:

- Branch and commit SHA.
- Changed-file list.
- Test output.
- Architecture/schema decisions.
- Risks and stop events.
- Rollback steps.
- Actual hours and model cost.
- Exact model route identifiers.
- One verification command.
- Exact `git add`, `git commit` and `git push` commands.
- Request to save important changes.

M2/M5 add desktop and narrow-mobile screenshots. M4 adds migration/rollback scripts and backup evidence. M6 adds pull-request text, staging URL, smoke log and rollback command.

## 21. Allowed implementation shape

After P0–P4 and M0 pass:

```text
Approved task source
        ↓ server-side staff authorization
Read-only C adapter/repository/service
        ↓ exact field whitelist
Protected Gantt endpoint
        ↓
Isolated Frappe Gantt page/component
```

D later uses a separate client-safe projection:

```text
Approved client identity or case token
        ↓ server-side client-to-case authorization
Approved client phase/date mapping
        ↓ stricter D whitelist
Client-safe read-only endpoint
        ↓
Client timeline UI
```

Do not add a duplicate Gantt table. Do not copy the Hermes plugin. Do not infer missing schema. Do not expose C’s response to clients.

## 22. Immediate execution instruction

Run the separate owner-audit prompt first, then execute P0 only. Stop with:

1. Owner audit recommendation.
2. Local-state inventory.
3. Existing Gantt evidence.
4. Architecture evidence gaps.
5. Backup readiness.
6. Smallest next action.

Do not write Gantt production code during this first run.

**Done | Next | Risks**

- **Done:** final C/D semantics, exact `D_READY` activation event, owner duties, provider lock, prerequisites, gates, tests, budget and rollback rules.
- **Next:** elect Admy or Smothy, then run P0 inspection only.
- **Risks:** architecture conflict, missing approved task start date, unscoped task query, local-only work, client authorization not yet ready and accidental D data leakage.
