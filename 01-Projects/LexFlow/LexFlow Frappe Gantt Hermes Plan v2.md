# LexFlow CRM — Frappe Gantt Integration: Hermes Build Plan (v2, refine-only)

Status: REFINEMENT of the prompt first written 2026-10-07 (Perplexity session 663e953b, "Frappe Gantt" thread) and re-confirmed in session 1cd08049 (project 306aadaa-7479-42b0-9ac3-794b02c3a66d). Do not restart from zero. Reuse everything below that already exists.

Repo: https://github.com/Ole00007/lexflow-crm (Flask, branch `main`)
Library: https://github.com/frappe/gantt (MIT, vanilla JS, no build step), pinned v1.0.3 (verify it is still the latest release before vendoring).

---

## 0. Read first, in this order (reuse-first rule)

1. `LexFlow_Hermes_Context.md` and `HERMES_SESSION_HANDOFF.md` (if present).
2. Local git: `git branch -a`, `git log --all --oneline -20`, `git status`. Look for any existing Gantt work (branch `feat/frappe-gantt-crm`, local-only commits, stashes, `static/vendor/frappe-gantt`, `crm/gantt`, `templates/gantt.html`).
3. Known GitHub state on 2026-10-12: only branches `main`, `lexflow_hermes_v1`, `railway/code-change-p5yOFx`. No Gantt branch and no Gantt pull request exist on GitHub.
4. If Gantt work exists locally: report it, then continue from it. If it does not exist: start at M0.

Report this in the M0 note before writing any code.

## 1. Mission

Add one safe, isolated Gantt page to the existing CRM. Additive only. Nothing existing is deleted, renamed or restyled. Existing Kanban task data and calendar dates remain the single source of truth.

## 2. Bar semantics (fix once, apply everywhere)

Decision status: PENDING owner pick (see the 5 options A to E in the chat). Recommended: C, deadline-driven bar.

| Rule | Value (default = option C) |
|---|---|
| Bar start | Task start date |
| Bar end | Hard legal or due deadline |
| Fill (progress) | Status map: To do = 0, In progress = 50, Done = 100 (use the existing Kanban status names; if a status is not in the map, use 0 and log it) |
| Warning style | CSS class `gantt-overdue` when end date is past and status is not Done, or when progress is behind expected progress |
| Priority | `custom_class` from task priority (CSS written by us; the library has no per-task color option) |
| Dependencies | Omit unless a real dependency field exists. Never infer from labels |
| Milestones | Not supported by the library. Show as a 1-day bar with class `gantt-milestone` |

Write this table into `docs/gantt_bar_semantics.md` once. Code, tests and UI must reference that file. Any change to bar meaning needs owner approval and a version note at the top of that file.

## 3. Three layers (separate commits, separate PR sections)

Layer 1, Tracking (read-only): protected HTML route (e.g. `/crm/gantt`) plus protected JSON endpoint. Field whitelist only: `id, name, start, end, progress, dependencies, custom_class`. Gantt option `readonly: true`.

Layer 2, Interaction without saving: view modes (Day, Week, Month), filters, status colors, popups. Bars can move visually; nothing is saved; show a clear notice.

Layer 3, Persistence (OFF by default): PATCH endpoint for start, end, progress. Requires auth, per-record authorization, CSRF token, server-side date validation (end on or after start), optimistic locking (version or `updated_at`, return 409 on conflict), idempotency, audit log (who, when, old, new), feature flag `GANTT_WRITE_ENABLED=false`, and `move_dependencies: false`. Reuse the existing Kanban or calendar date-change service if there is one. Starts only after owner approval at M4.

Database migrations: additive only, reversible, backup first, tested on a copy, documented rollback. No DROP. Stop and ask before creating any migration. Follow LexFlow backup rules: backup files, backup app snapshot, verify backup, git checkpoint.

Protected areas (flag before touching): existing migrations, `main` branch (PR only), production `DATABASE_URL`, auth files, payment flow.

## 4. Agents and file ownership (no overlap)

| Agent | Scope | Files |
|---|---|---|
| Backend-agent | routes, JSON endpoint, authorization, PATCH (Layer 3), audit, feature flag | `crm/gantt/*`, `tests/test_gantt_api.py` |
| Frontend-agent | exactly one new page: Gantt. No other page changes. One nav link only if the current nav pattern allows it | `templates/gantt.html`, `static/js/gantt.js`, `static/css/gantt.css`, vendored lib |
| DB-agent | design only until M4 | `migrations/versions/*_gantt_audit.py` (only after M4) |
| Smothy | UI and UX testing (desktop, narrow mobile, empty, error, loading, screenshots, accessibility). Writes no code | reports only |
| Admy | security, authorization, data leakage, secret scan, regression. Writes no code | reports only |

No other test agents are created. Shared files (`app.py`, base templates) are edited by one agent only. If two agents need one file, stop and flag.

Cross-test rule (Перекрёстный тест), always on: every finished layer goes to both Smothy and Admy with branch, commit, run steps, acceptance criteria and known limits. They review each other's findings. Report format: `test_name | verified | result | evidence | open_risks`. Author is never the reviewer.

## 5. Model routing (from project stack; verify availability in OpenRouter before use)

| Work | Model | Reason |
|---|---|---|
| Backend API, PATCH, audit, pytest | Claude Sonnet 4.6 | Flask and security patterns, cheaper than Opus |
| Authorization and migration review, final gate review | Claude Opus 4.7 | Only for M4, M5, M6 reviews (highest cost, use sparingly) |
| Frontend vanilla JS and CSS | GPT-5.4 | DOM and CSS work |
| Smothy (UI/UX with screenshots) | Gemini 3.1 | Vision and layout checks |
| Admy (security and regression) | Claude Sonnet 4.6, escalate to Opus 4.7 at M4 and M6 | Independent from the model that wrote the code |
| Negative and fuzz tests | Kimi K2.6 or DeepSeek | Different model family, cheap, good at adversarial cases |
| Orchestration | Hermes | Gates and stop flags |

Rule: the reviewer model must differ from the author model for the same layer.

## 6. Time and cost (planning estimates carried over from the 2026-10-07 plan; not measured)

| Stage | Agent-hours | API cost USD | Calendar |
|---|---|---|---|
| Audit and M0 (shorter if local work exists) | 2 to 3 | 3 to 5 | 0.5 day |
| Layer 1 | 6 to 8 | 8 to 12 | 1 to 1.5 days |
| Layer 2 | 4 to 6 | 5 to 8 | 1 day |
| Layer 3 (after M4) | 8 to 12 | 10 to 18 | 1.5 to 2 days |
| Cross-tests | 3 to 4 | 3 to 5 | overlaps |
| Staging and M6 | 2 to 3 | 2 to 4 | 0.5 day |
| Total, layers 1 to 3 | 22 to 33 | 30 to 50 | 4 to 5 working days |

Hermes must record actual hours and cost per stage in each gate report so the next estimate is real.

## 7. Milestone gates (stop and wait at each)

| Gate | Content | Owner action |
|---|---|---|
| M0 | Audit, existing-work report, schema map, plan | Approve scope |
| M1 | API contract in `docs/gantt_api_contract.md`, bar semantics file, vendoring v1.0.3 with LICENSE | Quick OK |
| M2 | Layer 1 local, read-only | Visual inspection (first look) |
| M3 | Layer 2 interaction | Optional look |
| M4 | Persistence and migration design | Must approve before any Layer 3 code |
| M5 | Layer 3 on staging | Second visual inspection |
| M6 | Merge and Railway deploy | Explicit "merge and deploy" command |

No auto-merge. No auto-deploy. Staging deploy is a push to `staging`; production is a PR merged to `main`.

## 8. Tests

Layer 1 (minimum 12): unauthenticated HTML denied; unauthenticated JSON denied; authenticated page 200; authenticated JSON 200; correct content type and shape; valid dates map to id, name, start, end, progress; dates are YYYY-MM-DD; records without dates excluded (no invented dates); end before start handled safely with no 500; user cannot see another user's or client's records; no sensitive fields (notes, documents, tokens, client personal data); empty dataset returns a valid empty response and a clear UI.

Bar semantics tests: status map gives 0, 50, 100; overdue class applied only when rule says so; unknown status falls back to 0 and is logged.

Layer 3 additions: unauthorized PATCH rejected; missing CSRF rejected; other-user record rejected; invalid dates rejected; stale version returns 409; repeated identical PATCH is idempotent; audit row written; flag off disables writes; rollback restores dates; Kanban and calendar show the same dates after a Gantt save.

All tests use the existing pytest setup. No new toolchain. All previously passing tests stay green.

## 9. Stop-and-flag events

Missing or unclear date or ownership fields; any destructive migration; any JSON field outside the whitelist; secrets in repo, logs or CI output; any previously passing test failing; two agents editing one file; write layer enabled without M4; any merge or deploy attempt without owner command; any change to a protected area.

## 10. Deliverables at every gate

Branch, commit SHAs, changed files, test output, risk notes, rollback steps, actual hours and cost. M2 and M5 add screenshots including narrow mobile. M4 adds migration script, rollback script and backup verification log. M6 adds PR text, staging URL, smoke-test log, rollback command.

After each gate, Hermes also posts: "Save and push now" with the exact `git add`, `git commit`, `git push` commands, and one verification command.

## 11. Learning leaders (separate, optional task, not part of the Gantt build)

The 12-name list generated on 2026-10-07 was not verified and some handles look unreliable. Do not insert it into agent context. Separate task, after M2: Hermes proposes 10 to 15 verified practitioners (confirmed real accounts with public shipped products) with source links, for owner approval. Only then add a weekly Sunday and Monday reminder (CRM event and Telegram). No cron or scheduled job is created without explicit owner approval.

## 12. Final reminders

Additive only, delete nothing. Do not invent routes, secrets, users, model names or deployment settings. Owner sees the UI locally at M2 and on staging at M5; everything else runs autonomously behind the gates.
