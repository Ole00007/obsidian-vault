# HERMES PROMPT — Compare LexFlow-crm vs Twenty CRM, Propose Clone, Delegate Build

**Purpose:** Paste this into Hermes as-is. It runs in strict stages with a hard approval gate before any code is written, and splits execution into independent frontend/backend sub-tasks that Hermes stitches together at the end.

**Source of truth repos (do not guess paths — use these):**
- LexFlow (system of record, reuse-first target): https://github.com/Ole00007/lexflow-crm
- Twenty CRM (comparison/clone source): https://github.com/twentyhq/twenty
- Twenty live demo (for feature inspection): https://demo.twenty.com — login `tim@apple.dev` / `Applecar2025`

---

## STAGE 0 — CONTEXT (read-only, no writes)

You are Hermes, the build agent for LexFlow MVP. Perplexity plans and reviews; the founder gives final approval. You do not write, commit, or deploy anything until explicitly told to in a later stage.

Repo structure you must respect: `/apps/web` (Next.js frontend), `/apps/api` (Node.js backend), `/packages/db` (schema + migrations), `/scripts` (seed, migrate), `CLAUDE.md` at root.

Protected — never touch without stopping and flagging first: existing migrations (never edit old ones, only add new), the `main` branch (PRs only, no direct push), production `DATABASE_URL`, auth files, payment flow.

Reuse-first rule already decided: `lexflow-crm` is the mature skeleton (migrations/, packages/db, apps/api) and stays the single system of record. Do not create a third parallel CRM implementation.

---

## STAGE 1 — COMPARE (read-only, no writes)

Clone or read (read-only) both repos:
- https://github.com/Ole00007/lexflow-crm
- https://github.com/twentyhq/twenty

Also inspect the live Twenty demo for UX/feature behavior: https://demo.twenty.com (`tim@apple.dev` / `Applecar2025`).

Produce a comparison table with these exact columns:

| Feature/Module | LexFlow-crm has it? (Y/N/Partial) | Twenty has it? (Y/N) | Twenty's implementation approach (1 line) | Clone candidate? (Y/N) | Est. effort (S/M/L) | Collision risk with existing LexFlow code (Low/Med/High) |

Cover at minimum: contacts/companies data model, kanban/pipeline view, calendar/events, task management, notes/activity timeline, custom fields, filtering/sorting/views, notifications, file attachments, workflow automation, REST/GraphQL API layer, role/permission model.

Do not propose cloning anything yet. Output only the table plus a 3-5 line summary of where Twenty is architecturally ahead of LexFlow-crm.

---

## STAGE 2 — PROPOSE (read-only, no writes) — HARD STOP FOR APPROVAL

From the Stage 1 table, propose a shortlist of items to clone or adapt from Twenty into LexFlow-crm. For each proposed item state:
1. What exactly gets cloned (component, pattern, or concept — not necessarily raw code)
2. Which LexFlow-crm file/module it would touch or extend
3. Why it doesn't collide with or duplicate existing LexFlow logic
4. One assumption you are making that could be wrong (technical) — flag it explicitly so it can be corrected before build

**STOP HERE.** Do not write any code. Wait for a reply from the founder in the exact form:
`APPROVED: [item1, item2, ...]` (items not listed are rejected for this round)

If the founder or Perplexity sends corrections instead of approval, revise the proposal and re-stop. Do not proceed to Stage 3 without an explicit `APPROVED:` line.

---

## STAGE 3 — CLONE (writes begin, staging only)

For only the approved items:
1. Confirm you are on the `staging` branch, not `main`.
2. Apply LexFlow backup rules first: back up affected files, snapshot the app state, verify the backup, then create a git checkpoint (commit) before touching anything.
3. Port the approved Twenty pattern/component into the correct LexFlow-crm path (`/apps/web`, `/apps/api`, or `/packages/db`). New migrations only — never edit existing ones.
4. Do not rename or restructure anything outside the approved scope.

---

## STAGE 4 — DELEGATE (split into two independent sub-agent jobs)

Split the approved work into two self-contained prompts, each following this exact template, and hand one to a frontend-dev sub-agent and one to a backend-dev sub-agent. They must be independently buildable and testable — no shared assumptions beyond a written API contract you define first.

**API contract (write this before delegating):** for each approved feature, list the exact route, method, request payload shape, and response shape that frontend will call and backend will serve. This is the single source of truth both sub-agents build against — it is what prevents mismatched pieces later.

**Frontend-dev sub-prompt (scope: `/apps/web` only):**
```
CONTEXT
[Relevant Twenty UI pattern being cloned, relevant LexFlow-crm files, the API contract from above]

TASK
[Exact component/page to build or modify — one atomic unit]

ACCEPTANCE CRITERIA
[Testable: renders correctly, calls the exact contracted endpoint, mobile-first breakpoints, keyboard/ARIA accessible]

CONSTRAINTS
Do not touch /apps/api or /packages/db. Do not invent endpoints not in the API contract. Surgical only.

FILES TO EDIT / CREATE
[Exact paths in /apps/web]

VERIFICATION
[How to confirm it worked locally before staging push]
```

**Backend-dev sub-prompt (scope: `/apps/api` and `/packages/db` only):**
```
CONTEXT
[Relevant Twenty data model/logic being cloned, relevant LexFlow-crm files, the API contract from above]

TASK
[Exact route/migration/repository function to build — one atomic unit]

ACCEPTANCE CRITERIA
[Testable: endpoint returns the exact contracted shape, migration is additive only, repository pattern followed]

CONSTRAINTS
All DB queries via /packages/db/repositories. Never edit existing migrations. Do not touch /apps/web. Do not touch auth files or payment flow without flagging first.

FILES TO EDIT / CREATE
[Exact paths in /apps/api and /packages/db]

VERIFICATION
[How to confirm it worked locally before staging push]
```

---

## STAGE 5 — STITCH (integration check, still staging)

After both sub-agent jobs complete:
1. Verify frontend calls match backend routes exactly (method, path, payload, response shape) against the API contract from Stage 4.
2. Verify CORS origin whitelist includes the correct frontend domain.
3. Verify env vars (`DATABASE_URL`, `RESEND_API_KEY`, `NODE_ENV`, `RAILWAY_PRIVATE_DOMAIN`) are present in staging `.env`, not hardcoded, and `.env.example` is updated with placeholder keys only.
4. Run `npm run db:migrate` and `npm test` on staging. Fix only what's broken — do not refactor unrelated code.

---

## STAGE 6 — SELF-AUDIT (before reporting done)

Check and report explicitly on: correctness, accessibility, responsiveness, performance, security, clarity, edge cases, deploy impact. Any "No" or "Unsure" answer must be listed as an open risk, not silently skipped.

---

## STAGE 7 — REPORT

End your report in exactly this format:

`Done | Next | Risks`

then one concrete next step (e.g., "push staging branch and request PR review for main"). Do not merge to `main` yourself — that requires a PR and founder approval.

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[Hermes_Prompt_Compare_Clone_Twenty_v1]]
