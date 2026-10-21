# LexFlow CRM: Frappe Gantt Integration, Hermes Build Plan (v3, refine-only, budget models)

Status: refinement of the prompt first written 2026-10-07 (Perplexity session 663e953b) and re-confirmed in session 1cd08049 (project 306aadaa-7479-42b0-9ac3-794b02c3a66d). Do not restart from zero. Reuse everything below that already exists.

Changes in v3 (2026-10-12): models moved one class lower using Nous Portal prices and promos; library source corrected with direct URLs (the earlier "pin v1.0.3 as latest" was stale); explicit risk table; 5 cross-tests plus 1 smoke test before merge; measurable success parameters.

Repo: https://github.com/Ole00007/lexflow-crm (Flask, branch `main`)

---

## 0. Read first, in this order (reuse-first rule)

1. `LexFlow_Hermes_Context.md` and `HERMES_SESSION_HANDOFF.md` (if present).
2. Local git: `git branch -a`, `git log --all --oneline -20`, `git status`, `git stash list`. Look for existing Gantt work: branch `feat/frappe-gantt-crm`, local-only commits, `static/vendor/frappe-gantt`, `crm/gantt`, `templates/gantt.html`.
3. Known GitHub state on 2026-10-12: branches `main`, `lexflow_hermes_v1`, `railway/code-change-p5yOFx` only. No Gantt branch and no Gantt pull request.
4. If Gantt work exists locally: report it, then continue from it. If not: start at M0.

## 1. What to clone, reuse or fork (exact sources)

Decision: do NOT fork the library. Vendor (copy in) the built files and keep the CRM code in our own repo. Fork only if we ever have to patch the library itself (not planned).

| Item | Action | Direct URL |
|---|---|---|
| Library source and docs | Read only. Reference for options and demos (`index.html`, `builder/`, `src/`) | https://github.com/frappe/gantt |
| Library license | Copy `license.txt` (MIT) next to the vendored files | https://github.com/frappe/gantt/blob/master/license.txt |
| Built files (`dist/frappe-gantt.umd.js`, `dist/frappe-gantt.css`) | Vendor these two files plus license into `static/vendor/frappe-gantt/<version>/`. The `dist/` folder is not in the GitHub repo; it ships in the npm package | https://www.npmjs.com/package/frappe-gantt |
| Exact package archive (default version 1.2.2) | Download once, verify, unpack, copy only the files above | https://registry.npmjs.org/frappe-gantt/-/frappe-gantt-1.2.2.tgz |
| Fallback archive (1.0.3, the version in the 2026-10-07 prompt) | Use only if 1.2.2 fails the smoke test | https://registry.npmjs.org/frappe-gantt/-/frappe-gantt-1.0.3.tgz |
| Official live demo | Compare behavior of bars, popups, view modes | https://frappe.io/gantt |
| Official docs | Option names | https://docs.frappe.io/gantt/introduction |
| Example patterns (project timeline, read-only dashboard, combined features) | Copy the pattern, not the code blindly | https://deepwiki.com/frappe/gantt/6.3-examples |
| CRM code to reuse | Existing Kanban task model, calendar date logic, auth decorators, test fixtures, `static/` and `templates/` base layout | https://github.com/Ole00007/lexflow-crm |

Version correction: GitHub tags and "Latest release" stop at v1.0.3 (2025-01-23 on npm). The npm registry lists 1.2.2 as `latest` (2026-02-25), with 1.0.4 (2025-10-10), 1.1.0 and 1.2.0 (Feb 2026) in between. The repo was last pushed 2026-06-18, so it is maintained.

Rule for M0: Hermes compares 1.0.3 and 1.2.2 for the options we use (`readonly`, `readonly_dates`, `readonly_progress`, `custom_class`, `popup`, `show_expected_progress`, `view_mode`, `move_dependencies`, `bar_height`). Default pick is 1.2.2. If any option behaves differently, record it and either adapt or fall back to 1.0.3. Never use a floating CDN in production. No npm or build step inside the CRM (npm is used once, only to download the archive).

## 2. Mission

Add one safe, isolated Gantt page to the existing CRM. Additive only. Nothing existing is deleted, renamed or restyled. Existing Kanban task data and calendar dates stay the single source of truth.

## 3. Bar semantics (fix once, apply everywhere)

Decision status: PENDING owner pick (options A to E from chat). Recommended: C, deadline-driven bar.

| Rule | Value (default = option C) |
|---|---|
| Bar start | Task start date |
| Bar end | Hard legal or due deadline |
| Fill (progress) | Status map: To do = 0, In progress = 50, Done = 100 (use existing Kanban status names; unknown status = 0 and logged) |
| Warning style | CSS class `gantt-overdue` when end date is past and status is not Done, or progress is behind expected progress |
| Priority | `custom_class` from task priority (CSS written by us; library has no per-task color option) |
| Dependencies | Omit unless a real dependency field exists. Never infer from labels |
| Milestones | No library option. Show as a 1-day bar with class `gantt-milestone` |

Write this table once into `docs/gantt_bar_semantics.md`. Code, tests and UI reference that file. Any change needs owner approval and a version note at the top of the file.

## 4. Three layers (separate commits, separate PR sections)

Layer 1, Tracking (read-only): protected HTML route (e.g. `/crm/gantt`) plus protected JSON endpoint. Field whitelist only: `id, name, start, end, progress, dependencies, custom_class`. Gantt option `readonly: true`.

Layer 2, Interaction without saving: view modes (Day, Week, Month), filters, status colors, popups. Bars can move visually; nothing is saved; show a clear notice.

Layer 3, Persistence (OFF by default): PATCH endpoint for start, end, progress. Requires auth, per-record authorization, CSRF token, server-side date validation (end on or after start), optimistic locking (version or `updated_at`, 409 on conflict), idempotency, audit log (who, when, old, new), feature flag `GANTT_WRITE_ENABLED=false`, `move_dependencies: false`. Reuse the existing Kanban or calendar date-change service if one exists. Starts only after owner approval at M4.

Database: additive only, reversible, backup first, tested on a copy, documented rollback, no DROP. Stop and ask before any migration. Follow LexFlow backup rules: backup files, backup app snapshot, verify backup, git checkpoint.

Protected areas (flag before touching): existing migrations, `main` branch (PR only), production `DATABASE_URL`, auth files, payment flow.

## 5. Agents and file ownership (no overlap)

| Agent | Scope | Files |
|---|---|---|
| Backend-agent | routes, JSON endpoint, authorization, PATCH (Layer 3), audit, feature flag | `crm/gantt/*`, `tests/test_gantt_api.py` |
| Frontend-agent | exactly one new page: Gantt. No other page changes. One nav link only if the nav pattern allows it | `templates/gantt.html`, `static/js/gantt.js`, `static/css/gantt.css`, vendored lib |
| DB-agent | design only until M4 | `migrations/versions/*_gantt_audit.py` (only after M4) |
| Smothy | UI and UX testing. Writes no code | reports only |
| Admy | security, authorization, leakage, secret scan, regression. Writes no code | reports only |

No other test agents are created. Shared files (`app.py`, base templates) are edited by one agent only. If two agents need one file, stop and flag.

Cross-test rule (Перекрёстный тест), always on: every finished layer goes to both Smothy and Admy with branch, commit, run steps, acceptance criteria, known limits. Report format: `test_name | verified | result | evidence | open_risks`. Author is never the reviewer, and the reviewer runs on a different model than the author.

## 6. Model routing (cheaper: one class lower, plus Nous Portal promos)

Source: [Nous Portal models and promos](https://portal.nousresearch.com/models) (prices in USD per 1M tokens, input / output, live catalog; checked 2026-10-12). Promos change; free models rotate monthly.

| Work | Was (v2) | Now (v3) | Portal price in / out | Why |
|---|---|---|---|---|
| Backend Layer 1 and 2 (read API, tests) | Claude Sonnet 4.6 | DeepSeek V4.1 Flash (`DeepSeek V4.1 Flash` entry at the lower price) | $0.11 / $0.51 | Cheap, strong coding; low risk because read-only |
| Backend Layer 3 (auth, PATCH, audit) and DB design | Claude Sonnet 4.6 | Claude Haiku 4.5 | check live price (batch variant listed at $0.50 / $2.50) | One class lower, reliable tool use; reviewed by a different family |
| Frontend (vanilla JS, CSS) | GPT-5.4 | GPT-5.4 Mini (fallback: Qwen3.8 27B) | Mini: check live price. Qwen3.8 27B: $0.04 / $1.35 (91% off promo, `qwen/qwen3.8-27b`) | One class lower |
| Smothy (UI/UX, screenshots) | Gemini 3.1 | Gemini 3.8 Flash (fallback: Gemini 3.1 Flash Lite Preview) | $0.75 / $3.75 (50% off promo, `google/gemini-3.8-flash`) | Cheaper, image-capable family. Verify image input works before relying on it |
| Admy (security, regression) | Claude Sonnet 4.6, Opus 4.7 at gates | Kimi K2.6 (escalate to Claude Sonnet 4.6 at M4 and M6 only) | Kimi $0.43 / $2.45 (54% off promo, `moonshotai/kimi-k2.6`). Sonnet 4.6: check live price (Sonnet 4.5 list is $3 / $15) | Different family from the backend author; Sonnet instead of Opus 4.7 at gates |
| Fuzz and negative tests | Kimi K2.6 or DeepSeek | LongCat 2.5 Preview or MissingNo (free) | $0 | Free tier, limited-time. Only for non-gate work |
| Hermes orchestration | Hermes | GLM 5.3 Flash | $0.12 / $0.40 | Cheap and agent-capable |

Rules:
- Do NOT use Hermes-4-70B or Hermes-4-405B as the agent model. [Nous docs](https://hermes-agent.nousresearch.com/docs/integrations/nous-portal) say they are tuned for chat and reasoning, not the tool-calling loop.
- Free models are not used for gated steps (M0 to M6 evidence). In one reported test only 6 of 10 listed free models actually responded ([note.com report](https://note.com/hash_13/n/n4fe7799c48af?hl=en)).
- Before the first real run, send one tiny probe request per model and compare the charged cost with the listed price. A GitHub issue reports some routes billed near list price while a promo was shown ([NousResearch/hermes-agent #110912](https://github.com/NousResearch/hermes-agent/issues/110912)).
- Model names and prices must be re-read from the live catalog on the day of the run. Do not invent model IDs.

## 7. Time and cost (planning estimates, not measured)

Basis: the earlier 22 to 33 agent-hour estimate stays; only the price per token changes. Assumption: about 20M input and 2.5M output tokens in total, blended at the new prices, plus about 1M in and 0.2M out of Claude Sonnet 4.6 for the M4 and M6 reviews.

| Stage | Agent-hours | Est. API cost USD | Calendar |
|---|---|---|---|
| Audit and M0 | 2 to 3 | 0.5 to 1 | 0.5 day |
| Layer 1 | 6 to 8 | 1.5 to 3 | 1 to 1.5 days |
| Layer 2 | 4 to 6 | 1 to 2 | 1 day |
| Layer 3 (after M4) | 8 to 12 | 2 to 5 | 1.5 to 2 days |
| Cross-tests and smoke | 3 to 5 | 1 to 2 | overlaps |
| Staging and M6 | 2 to 3 | 1 to 2 | 0.5 day |
| Total, layers 1 to 3 | 22 to 33 | 8 to 15 (v2 estimate was 30 to 50) | 4 to 5 working days |

Hard budget cap: USD 20. Hermes records actual hours and cost per stage in each gate report. If actual cost passes 2x the stage estimate, stop and flag.

## 8. Milestone gates (stop and wait at each)

| Gate | Content | Owner action |
|---|---|---|
| M0 | Audit, existing-work report, schema map, library version comparison, probe-cost check | Approve scope |
| M1 | `docs/gantt_api_contract.md`, `docs/gantt_bar_semantics.md`, vendored library with license | Quick OK |
| M2 | Layer 1 local, read-only | Visual inspection (first look) |
| M3 | Layer 2 interaction | Optional look |
| M4 | Persistence and migration design | Must approve before any Layer 3 code |
| M5 | Layer 3 on staging | Second visual inspection |
| M6 | Smoke test passed, then merge and Railway deploy | Explicit "merge and deploy" command |

No auto-merge, no auto-deploy. Staging is a push to `staging`; production is a PR merged to `main`.

## 9. Risks, mitigation, and what to flag

| # | Risk | Likelihood / impact | Mitigation | Flag to owner when |
|---|---|---|---|---|
| R1 | Library version differs from the earlier plan (1.0.3 vs npm 1.2.2); option behavior changes | Medium / Medium | M0 comparison, pinned vendored files, smoke test, fallback archive | Any option we use behaves differently or is missing |
| R2 | Promo prices not honored (billed near list) or promo ends mid-project | Medium / Low to Medium | Probe request per model, cost log per gate, cap USD 20, re-read live catalog | Charged cost above 2x listed or stage estimate |
| R3 | Cheaper models write weaker auth or PATCH code | Medium / High | Layer 3 written by Haiku 4.5, reviewed by Kimi K2.6, escalated to Sonnet 4.6 at M4 and M6; 10 Layer 3 tests; read-only until M4 | Any test written by the same model as the code; any authorization test failing |
| R4 | Free or limited-time models vanish or do not respond | High / Low | Free models only for non-gate work; named paid fallbacks | A free model fails twice in a row |
| R5 | A legal deadline is moved by accident | Low / Very high | `readonly: true`, write flag off, audit log, M4 gate | Any write path active without M4 |
| R6 | Client data leaks in JSON | Low / Very high | Field whitelist, CT2 test, no notes, documents, tokens, PII | Any key outside the whitelist |
| R7 | Two sources of truth (Gantt vs Kanban) | Medium / High | Gantt reads Kanban tables only; CT5 date-equality test | Any new task or date table in a PR |
| R8 | Destructive or unsafe migration | Low / Very high | Additive only, backup, copy test, rollback script, M4 | Any DROP or data-loss ALTER; any migration before M4 |
| R9 | Bar meaning drifts between sessions | High / Medium | Single `docs/gantt_bar_semantics.md`, CT3 fixture test | Any code or UI that contradicts the file |
| R10 | Hermes already built part of this locally and we duplicate it | Medium / Medium | Step 0 audit | Local Gantt work found |
| R11 | Wrong agent model for tool-calling (Hermes-4 chat models) | Low / Medium | Rule in section 6 | Hermes-4 selected as agent model |
| R12 | Secrets committed (API keys, `DATABASE_URL`) | Low / Very high | Secret scan by Admy, `.env.example` only | Any secret found in files, logs or CI output |
| R13 | Existing pages change by accident | Medium / High | Allowed-files list, CT5 diff check | Any file outside the allowed list changed |
| R14 | Production deploy breaks the CRM | Low / High | Smoke test on staging, rollback command tested before merge | Smoke test fails or rollback untested |

Standing stop-and-flag events: missing or unclear date or ownership fields; destructive migration; JSON field outside whitelist; secrets found; a previously passing test fails; two agents editing one file; write layer enabled without M4; merge or deploy attempt without owner command; change to a protected area; cost above 2x estimate.

## 10. Cross-tests (5) and smoke test (1) before anything reaches `main`

Tester never equals author. Each cross-test produces a report line in the standard format.

| ID | Tester, target | What is tested | Pass condition |
|---|---|---|---|
| CT1 | Admy tests Backend | Authorization: unauthenticated HTML and JSON denied; user A cannot see user B or other client records; PATCH and POST absent or disabled while flag is off | 0 unauthorized successes, 0 server errors (500) |
| CT2 | Admy tests Backend, Smothy confirms in the browser network tab | Data leakage: JSON keys equal the whitelist exactly; no notes, documents, tokens, personal data | Keys match whitelist 100%, 0 extra keys |
| CT3 | Smothy tests Frontend plus Backend | Bar semantics: a fixed fixture of 6 tasks (not started, in progress, done, overdue, no date, milestone) renders as the bar-semantics file says | 6 of 6 match expected fill, class and exclusion |
| CT4 | Smothy tests Frontend | UI states and accessibility: empty, loading, error, 1 task, 200 tasks; widths 375 px and 1440 px; keyboard focus and popup open and close; text contrast | No horizontal scroll at 375 px, no console errors, all states show a message, keyboard reaches all controls |
| CT5 | Admy tests the whole branch | Regression and integrity: full existing test suite; changed files are only the allowed list; Gantt dates equal Kanban and calendar dates for the same tasks; dragging a bar changes nothing in the database | 0 failing tests, 0 files outside list, 100% date equality, 0 database writes |

Smoke test (one test, on staging, before any PR merge to `main`). Run by Smothy, logs confirmed by Admy.

1. Staging deploy is up and `/health` returns 200.
2. Log in as a test user; open the Gantt page; at least one real task renders.
3. Page load under 3 seconds and JSON response under 500 ms for about 200 tasks.
4. 0 browser console errors; the vendored library file loads from our own domain, not a CDN.
5. Log out; opening the Gantt page redirects to login.
6. Kanban and calendar pages still open and show the same dates.
7. Rollback is rehearsed: the revert command for the PR is dry-run and documented.

Any failed step blocks the merge.

## 11. Success parameters (all must be true to merge)

| Parameter | Target |
|---|---|
| Existing tests | 100% still passing, count not lower than before |
| New tests | Layer 1 (12) and bar semantics (3) pass; Layer 3 tests (10) pass if Layer 3 is shipped |
| Cross-tests | CT1 to CT5 all PASS, each report written by someone other than the author |
| Smoke test | 7 of 7 steps pass on staging |
| Files changed | Only the allowed list; 0 changes to Kanban, calendar, dashboard, client pages (except one nav link) |
| Data exposure | JSON keys equal the whitelist; 0 secrets in repo, logs, CI |
| Database | 0 schema changes in Layers 1 and 2; any Layer 3 migration additive with tested rollback |
| Performance | Page load under 3 s; JSON under 500 ms for about 200 tasks |
| Mobile | No horizontal scroll at 375 px |
| Bar semantics | 6 of 6 fixture cases match `docs/gantt_bar_semantics.md` |
| Cost | At or under USD 20 total; stage costs recorded |
| Rollback | Documented and rehearsed; restore time under 5 minutes |
| Approvals | M0, M2, M4 (if Layer 3), M5 (if Layer 3), M6 recorded from the owner |

## 12. Tests (detail)

Layer 1 (minimum 12): unauthenticated HTML denied; unauthenticated JSON denied; authenticated page 200; authenticated JSON 200; correct content type and shape; valid dates map to id, name, start, end, progress; dates are YYYY-MM-DD; records without dates excluded (no invented dates); end before start handled safely with no 500; user cannot see another user's or client's records; no sensitive fields; empty dataset returns a valid empty response and clear UI.

Bar semantics (3): status map gives 0, 50, 100; overdue class applied only by the rule; unknown status falls back to 0 and is logged.

Layer 3 (10, only if approved): unauthorized PATCH rejected; missing CSRF rejected; other-user record rejected; invalid dates rejected; stale version returns 409; repeated identical PATCH idempotent; audit row written; flag off disables writes; rollback restores dates; Kanban and calendar show the same dates after a Gantt save.

All tests use the existing pytest setup. No new toolchain.

## 13. Deliverables at every gate

Branch, commit SHAs, changed files, test output, risk notes, rollback steps, actual hours and cost. M2 and M5 add screenshots including narrow mobile. M4 adds migration script, rollback script and backup verification log. M6 adds PR text, staging URL, smoke-test log, rollback command. After each gate Hermes posts the exact `git add`, `git commit`, `git push` commands and one verification command, and asks the owner to save.

## 14. Learning leaders (separate task, not part of the Gantt build)

The 12-name list generated on 2026-10-07 was not verified and some handles look unreliable. Do not insert it into agent context. After M2, Hermes proposes 10 to 15 verified practitioners (real accounts with public shipped products) with source links for owner approval. Only then add a weekly Sunday and Monday reminder (CRM event and Telegram). No cron or scheduled job without explicit owner approval.

## 15. Final reminders

Additive only, delete nothing. Do not invent routes, secrets, users, model names or deployment settings. The owner sees the UI locally at M2 and on staging at M5; everything else runs autonomously behind the gates.
