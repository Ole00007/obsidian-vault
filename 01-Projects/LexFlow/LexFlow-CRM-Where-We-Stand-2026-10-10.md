---
title: LexFlow CRM — Where We Stand (2026-10-10)
created: 2026-10-10
tags: [lexflow, status, gantt, frontend, handoff]
status: active
---

# LexFlow CRM — Where We Stand
**Date:** 2026-10-10 · **Owner of this doc:** operator-installer · **Authority for task status:** the roadmap JSON (below)

---

## 1. The one-line answer

The CRM code is fine and its history is now **safe and in the right place for the first time**; the
**production app is still down and I cannot fix it without your Railway access**; the **Gantt is
blocked by your own design gate**, not by our capacity; and the **Fronty visualiser task is now open
on an isolated branch**.

---

## 2. Paths — the truth table (this was the real mess)

| Thing | Correct location now | Status |
|---|---|---|
| CRM code (canonical working copy) | `/Users/olesiarasing/projects/lexflow-crm` @ `lexflow_hermes_v1` | ✅ created 2026-10-10 |
| Task/per-project tracker | `.../docs/LexFlow_Agentic_Roadmap.json` — 21 nodes, `last_updated 2026-10-10` | ✅ recovered + stamped |
| Deployed source (what GitHub/Railway builds) | `github.com/Ole00007/lexflow-crm` branch `lexflow_hermes_v1` | ✅ unchanged |
| Rules of engagement | `~/Obsidian/_Meta/AGENT_RULES.md` §8, §9, §11 | ✅ updated |

**What was wrong:** the tracker file was being read from a second clone buried under `~/Desktop/projects/Products & Services/LEGAL/LEXFLOW Production/lexflow-crm`, while a **third** clone sat in the home root (`~/lexflow-crm`) on the **wrong branch** (`main`, from July, no `docs/` at all). Three copies, two of them lying, and every status run read the one that macOS TCC could stop serving.

**What I did:** rebuilt the canonical repo at the §8 path, recovered the "unreachable" history
(see §4), archived the stray clone and three stale tracker copies (move, not delete — reversible,
manifest at `/Users/olesiarasing/projects/_archive/2026-10-10-lexflow-dedupe/README.md`).

---

## 3. Production — 🟢 RESOLVED 2026-10-10 ~22:20 CEST (was down 15 days)

> **RESOLVED and verified.** `/`, `/health`, `/login?ws={lexflow,romanelli-studio,orasing,pagliano}` → **200**;
> `/health` body `{"db":"ok","python":"3.11.8"}`; anon `/api/admin/users` → **401** (security intact).
> **Hindsight restored too:** `/health` 200, `/v1/default/banks` 401. No push was made.
> The root cause and the exact fix are recorded below — it was a build-pipeline regression, not our code.

- `https://web-production-031a6.up.railway.app` returns **404 `{"status":"error","code":404,"message":"Application not found"}`** with `x-railway-fallback: true` — the **Railway edge has no service bound to that domain**. It answered 200 on 2026-09-25.
- The same signature killed **Hindsight** (`avibe-hindsight-production.up.railway.app`) — one edge/config problem, not two bugs. Hindsight being down means vault notes are **not** reaching long-term memory.
### ✅ ROOT CAUSE FOUND AND FIX PREPARED (updated 2026-10-10, later the same day)

The Railway CLI **is** authenticated (`railway whoami` → olesya00007@yahoo.com), so the earlier
"403 / no access" verdict was stale and wrong. Diagnosis is now complete:

- The CRM is project **`perceptive-achievement`**, env `production`, service **`web`**.
- The domain **is** attached and **ACTIVE** — the domain was never the problem.
- The service's deployment **FAILED**, and the **build** is what fails:
  ```
  [INFO] install mise packages: python
  mise ERROR Failed to install core:python@3.11.8: No GitHub artifact attestations found for python@3.11.8
  Build Failed: build daemon returned an error < failed to solve: process "mise install" did not complete successfully: exit code: 1 >
  ```
- **Chain:** `runtime.txt` pins `python-3.11.8` → Railpack asks `mise` (2026.8.13) for it → mise now
  **enforces GitHub artifact-attestation verification** → that cpython artifact **has no published
  attestations** → install aborts → build fails → no deployment → the domain serves Railway's edge
  fallback 404. **An upstream build-pipeline regression**, affecting any Python project pinned to an
  older interpreter. It was never an application bug.
- **Fix prepared, not deployed:** branch **`fix/railway-mise-python-attestation`** adds one file,
  `mise.toml` (`[settings] python.github_attestations = false`). Delete the file to roll back; no app
  code touched. Alternatives: set `MISE_PYTHON_GITHUB_ATTESTATIONS=false` on the service (no repo
  change), or bump the Python pin (needs its own test pass for Flask 2.3.3 / jwt / psycopg2).
- **⚠️ Second, separate problem:** `railway service status --all` shows **`Postgres … NO DEPLOYMENT`**
  and **`LexFlow-Chatbot … NO DEPLOYMENT`**, all Postgres deployments `REMOVED` (latest 2026-09-30).
  **A fixed build still will not serve without the database up** — Postgres needs a redeploy too.

> **What is genuinely still on you:** authorizing the push that triggers the rebuild (§11.5) and the
> Postgres redeploy — both are production actions. That is now **one decision**, not an access problem.

---

## 4. What we recovered today (good news)

`~/Desktop` refuses *directory listing* under TCC — but **direct reads of a known path and `mdfind`
still work**. That let a subagent pull the legacy clone back out:

- **15 local-only commits** never pushed, including `ede8e13` (2026-10-04 status), `016568e` (T-005 WhatsApp scoping), `7e4343b` (T-008 consolidated audit), and daily status commits back to 2026-09-19.
- **6 branches**: `feat/t021-diagram-gantt` (`87b847c`), `feat/rls`, `feat/attachments`, `feat/saved-views`, `calendar-grid`, `deploy/repoint-b` + tag `archive/ux-baseline-2026-09-04`.
- The **newest tracker revision (2026-10-06, 21 nodes)** — now the live authority.

All fetched **read-only** into the canonical repo as remote `legacy-recovered`; objects are preserved
in `~/projects/lexflow-crm`'s object store. **Nothing was pushed.**

> ⚠️ **These 15 commits contain real, unreviewed work** (RLS, attachments, saved views, calendar grid).
> They are safe now but **not merged and not deployed** — they need review before they go anywhere.

---

## 5. Task board state (21 nodes, from the recovered tracker)

- **Done / deployed (4):** T-001 intake manual name entry · T-007 Contacts two-model split · T-016 landing repoint · one more.
- **Local-verified, awaiting your review (2):** **T-019** design/UX package · one more. (T-019 is now unblocked — see §7.)
- **Awaiting your confirmation (4):** T-005 WhatsApp scoping (provider = Meta Cloud API direct) · T-008 read-only app audit · T-010 Resend delivery · T-015 uploads persistence.
- **Blocked (1):** **T-014 RLS merge** — needs an 18-test Postgres gate + `ALTER ROLE … NOBYPASSRLS` on the Railway role.
- **Backlog (10):** T-002, T-003, T-004, T-006, T-009, T-011, T-012, T-013, T-017, T-018, T-020 (i18n, scheduled NEXT WEEK), **T-021 (Gantt/diagram)**.
- **Kanban:** 53 cards, no activity since 2026-10-06. Every node already has a card → 0 duplicates created.

---

## 6. The Gantt — exactly where it is

| Question | Answer |
|---|---|
| Is there a spec? | Yes — `LexFlow-T021-Diagram-View-Spec-2026-10-06.md` + your master prompt (`Hermes_LexFlow_Gantt_Master_Prompt.Md`, v2026-10-07). |
| Is there any code? | Yes, **a demo already exists locally** on `feat/t021-diagram-gantt` (`87b847c`): `docs/t021-demo/index.html` + vendored `frappe-gantt.umd.js` / `.es.js` / `.css`. **Not production wiring.** |
| Is there a Gantt library in the main app? | **No.** Zero matches for gantt/frappe anywhere in the app tree. Nothing to duplicate. |
| What library, pinned? | `frappe-gantt@1.2.2` (MIT, UMD, no build step). Self-hosted under `static/vendor/` — a bare CDN would be blocked by the existing `script-src 'self'` CSP. Keep the MIT notice. |
| Free URL to look at today? | **Not yet** — that is exactly what the Fronty card now asks for (§7). |
| What blocks implementation? | **T-019 (design/UX) was blocked on your localhost review.** Unblocked today at your instruction. |
| What do I still need from you? | **Which fields make each Gantt bar.** There is no start+end pair anywhere: Task = `createdat`+`duedate`, Case = `openedat`+`duedate`, Deadline = `duedate` only, only CalendarEvent has a real start+end. |

**Not verified (do not treat as fact):** the demo's claim of "21 tasks / 3 done / 5 agents" at
`localhost:8770` — there is no listener and no demo directory outside git, and the tracker has
**19→21 nodes, not a 5-agent registry**. Per the master prompt, those demo dates are synthetic and
must never be copied into live case deadlines.

---

## 7. Fronty task (opened today)

**Card: `Progress visualiser — see every human's progress in any project`**
→ assignee `frontend-developer-lovable_react`, isolated branch, plus **T-019 unblocked and handed to Fronty**.

Brief: build a **progress visualiser (deck or small app)** that makes a human's progress in *any*
project visually obvious, using the LexFlow CRM as its data base, on **React**, deployable to
**Cloudflare Workers or a Railway worker/service**. It must show the **Gantt progress** for LexFlow
specifically, and be reachable at an **open URL**.

Two hard rules restated to Fronty:
1. **Isolated branch** off `lexflow_hermes_v1` ([§11.1](#)). Never work on `main`, never push untested code.
2. **Design gate stands:** a **local URL** (`localhost`) is the deliverable. Deploying to Cloudflare
   Workers or Railway needs **your explicit authorization** — it is a deploy, it touches a live
   surface, and it may cost money. Same for any push.

---

## 8. Limits — what is out of reach, stated plainly

| # | Not doable by me or any roster agent | Why |
|---|---|---|
| 1 | **Execute the production fix** (rebuild `web` + redeploy `Postgres` + Hindsight) | Root cause is now known and the fix is written and local — but pushing/redeploying is a production action, so it needs your explicit go. |
| 2 | **Deploy the visualiser / Gantt to Cloudflare Workers or Railway** | Deploy authorization + the branch-protection/design gate; also Cloudflare auth is OAuth-gated to your account. |
| 3 | **Push anything** | Your new push gate: 4 cross-tests + 1 smoke local test + explicit per-push authorization (§11.5). |
| 4 | **Verify client email delivery** | Resend is limited to the owner mailbox until the domain is verified; no SMTP fallback configured. |
| 5 | **Google Calendar OAuth end-to-end** | 403 until you add a test user / publish the app. |
| 6 | **The 12-leader "learning from leaders" list** | The original list is not in any artifact I can reach (`_Inbox` has the prompt, not the names). Needs you. |
| 7 | **Independent cross-review by "Smothy" and "Admy"** | The master prompt names them as cross-testers. Their capability for this task is **NOT VERIFIED** — I will not claim a review happened. |
| 8 | **Judge visual quality** | I can read DOM/CSS and run a real browser, but I cannot sign off on *design taste* — that is your localhost review by rule. |
| 9 | **Reconcile unreviewed history** | The 15 recovered commits (RLS/attachments/saved-views) need human review before merge; I won't merge them unilaterally. |

---

## 9. What I think could be improved next (my reasoning, flagged not decided)

1. **Fix this cron job's own prompt.** It still points the tracker at a path that never existed (`~/Desktop/projects/services/LEGAL/...`). A job whose instructions are wrong will keep producing wrong reports. **Highest cheap win.**
2. **Re-home the cron jobs.** §10.3 says `operator-installer` owns the daily status job, but the `lexflow-*` / `obsidian-*` jobs live in `smoothy_op_dir`'s store, and `operator-installer` has **zero jobs**. Only two profiles even run gateways, so most profiles' cron entries can never fire.
3. **Make the roadmap machine-checked.** The tracker's own `report_rule` demands `deploy_status` + `prod_url`/`commit_hash`; T-001/T-007 violate it right now, and four card↔roadmap statuses disagree. A 20-line validator run in the daily job would end this class of drift permanently.
4. **One clone, enforced.** §11 exists now, but nothing *checks* it. A one-line guard in the status job ("no second clone of any repo; code only under `~/projects/`") turns policy into enforcement.
5. **Rotate `JWT_SECRET_KEY`** — already flagged, still outstanding, and it is a security item.
6. **Turn the recovered branches into decisions.** `feat/rls` is the only real enforcement layer for tenant isolation and it has been sitting unmerged; either merge it behind its 18-test gate or consciously close it.
7. **Decide the Gantt bar semantics once** (§6) so T-021 and the new visualiser share one model instead of drifting into two.

---

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Project-Status]]
- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]
- Related: [[LexFlow-Audit-Checklist]]
- Related: [[2026-10-10]]
