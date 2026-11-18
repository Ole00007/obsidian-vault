# LexFlow-Elisa Worker | Inspect, reinforce, test, install

**Pilot objective:** from one authorised LexFlow CRM matter, produce one source-linked draft for a human reviewer. The baseline is the assistant’s current manual process, including any copy/paste into ChatGPT. Do not replace that process unless the new one reduces total work, including review.

This is an execution guide, not a report that the existing worker passed. Build ID, source location, launch commands, model and installer are unverified here. The architecture to check is the existing LexFlow CRM and Elisa worker; Flask/PostgreSQL with row-level security is a project target, not evidence about the installed build.

## Responsibilities and effort ceiling

| Owner | Deliverable | Boundary |
|---|---|---|
| You, **AI engineering assistance** | Choose one workflow; approve scope and cost; witness release rehearsal; make install decision with office IT | No secrets or client records in chat. No installation implied by the visit. |
| **ADMY**, Hermes orchestrator | Inventory, issue one bounded task to backy, independently rerun acceptance tests, report evidence | No new agent, cloud provider, migration, customer contact or production deployment. |
| **backy**, builder | Reproduce baseline, make smallest approved patch, run regressions, document release/rollback | Work on isolated branch or copy and test CRM only. Cannot approve own release. |
| **Office assistant / lawyer** | Assistant repeats task unaided; lawyer validates facts, permissions and time saved | Use invented records first. Neither needs to debug the installation. |

Planning allowance, not a quote: 45–90 minutes to locate and trace a working build; 1–3 hours for one narrow fix and regression tests; 45–90 minutes for a clean-PC rehearsal. If the first trace reveals a missing worker, missing tenant isolation or no supported installer, stop and re-estimate. Use ADMY’s approved low-cost model for inventory, backy’s approved coding model only for an actual defect, and deterministic checks for permissions/arithmetic. Default new external spend: zero; get a cap before any paid test. No Grok purchase, model training, new vector database, swarm or scheduled job.

## Step 1 | Identify what actually runs

1. You provide ADMY the authorised source/release location, candidate version, intended OS, non-production CRM and named approver. Do not hand over a production database dump or credentials in a prompt.
2. ADMY identifies the version/commit, release recipe, dependency lockfiles, entry points, service definitions, migrations, tests, model adapter and documented uninstall procedure. A screen mock-up, standalone model response or old README is not evidence of a working CRM worker.
3. Read-only examples, inside an authorised source checkout: `git status --short`, `git rev-parse --short HEAD`, `rg --files`, then `rg -n -l 'enqueue|register_handler|worker|matter_id|workspace_id|row.level.security'` restricted to application and tests directories. Inspect configuration names, never secret values. Do not guess a queue, endpoint or installer.
4. Return one row per component: **component | actual path/symbol | command or test | expected | observed | verified / missing / unknown**. Identify app, CRM, database, model and worker hosts individually. A local UI connected to a hosted CRM is not an offline deployment.

## Step 2 | Trace one real code path using fictional records

1. Seed a disposable test workspace with matter A; create a second matter and a separate workspace for isolation tests. Use normal CRM permissions, not an administrator session. Retain fixture IDs only.
2. Start the services using the repo’s documented, pinned commands. Record the actual commands, runtime versions, test DB and model destination in a release record with secrets omitted. Never point a worker at the production queue.
3. From the **CRM UI**, sign in as the assistant, select matter A and request one draft. Trace: authorised user → matter lookup → task creation → handler actually invoked → approved model or fixture adapter → draft attached to A → lawyer review. Capture a job/request ID and draft ID; log IDs, status and timing, not prompt bodies.
4. If asynchronous, prove the handler is registered in the **running worker**, not merely importable in a test. If synchronous already works, retain it; don't introduce a queue for a one-click draft. If the worker completes but the draft cannot be opened from A after restarting, the end-to-end test failed.
5. Compare the output with the current workflow. Pick one friction point to fix: e.g. returning the draft to the right CRM matter instead of manual re-entry. Choose **reuse unchanged / configure / patch / block**. Build only for the third outcome and only after approval.

## Step 3 | Minimum acceptable patch, only if needed

1. Add the failing regression first. Reuse the existing CRM login, service, model adapter and draft store. Do not implement another CRM, identity store or bot profile.
2. On the server derive workspace and user from authenticated context. Check that the user may read this matter and these source documents; reject mismatched matter/contact/workspace before creating a job. Recheck permission and matter scope before reading or writing in the worker, including after permissions change.
3. Pass the minimum input: selected source IDs and versions, task type, matter scope, request ID and approved destination. Treat document text as evidence, not authority to invoke tools. Apply destination policy **before** sending content to a model. No external fallback, mail, filing, shared memory or autonomous external action.
4. Produce a reviewable draft with document/page anchors. On retries use a stable request key tied to the input version; double-click must not create two drafts. If a source changes, make an explicitly new version. On failure leave a visible error and an intact original.
5. Preserve the existing review mechanism: assistant may prepare; lawyer may accept, correct or reject. Keep only approved local operational metadata. Submit a small diff, test output and reversal procedure. If a schema migration is unavoidable, require a tested backup/restore in the disposable environment before release.

## Step 4 | Acceptance matrix: backy runs, ADMY independently repeats

| Test | Action | Pass evidence |
|---|---|---|
| CRM round trip | Trigger from matter A with a normal assistant account, reopen draft as lawyer | Same matter, source version and draft ID; usable after restart; original untouched |
| Facts and sources | D1 p.1 estimate €1,200 on 3 Nov; D2 p.1 note on 9 Nov reports €400 paid on 6 Nov; D3 p.1 email on 10 Nov requests receipt | Three correct references; estimate not invoice, payment unverified, receipt missing; no inferred debt or deadline |
| Independent variation | Assistant changes fictional €400 to €450 in a new test input and repeats unaided | New draft cites €450 as reported; old draft stays identifiable; no stale value |
| Matter and tenant boundaries | Test accounts restricted to A cannot retrieve B or another workspace’s synthetic marker through normal CRM search, draft lookup, worker or export | Access denied or no results; no job/draft for unauthorised target. If PostgreSQL/RLS is intended, run project policy tests against real test PostgreSQL with a non-owner, `NOBYPASSRLS` app role; SQLite or an admin pass is insufficient |
| Failure and retry | In test environment interrupt selected model/service, retry same request and restart worker | Visible failure, no cloud retry, no duplicate draft or silent loss |
| Local means local | Use downloaded test model and synthetic text; disconnect external network for on-device route, run again, inspect pending work and logs after reconnect | Draft still works, no unexpected destination or deferred upload. For an office server keep private LAN, block external egress; label it LAN, not on-device |
| Human review | Lawyer rejects a draft, then corrects a second one | No sending, filing or original overwrite; only permitted user can accept; decisions visible |
| Recovery | Stop worker, roll back build/config and restore a disposable snapshot if needed | Prior CRM starts and fixture records intact; rollback evidence retained |

For each row record tester, build ID, expected/actual, result and redacted evidence. **Not run ≠ passed.** A model-only smoke test does not pass the CRM row. Block office installation for wrong-matter access, unapproved egress, changed originals, untested rollback or missing release provenance. Block a live-matter pilot for fabricated facts or citations. Do not “fix” a failed check by weakening its assertion.

## Step 5 | Package once, install once

1. backy produces an install card for the **actual** release: artifact/version, trusted checksum or signature, supported OS/architecture, disk/RAM, prerequisites, exact install/start/stop/uninstall commands, local paths, listeners and dependencies. If any required command is unknown, flag it; do not improvise on the lawyer’s PC.
2. ADMY rehearses on a clean comparable PC or VM as a standard user. Verify provenance, install, launch, sign in to test CRM, exercise the real worker, close/reopen, uninstall/restore. Record elapsed time and attach redacted results. If release requires permanent admin rights or disabling office controls, stop and consult IT.
3. You obtain explicit office/IT permission for the chosen build, folders, model, network boundary and acceptance test. Keep the ten-minute lawyer conversation separate from installation time. Record initial settings. No remote-support account, telemetry or background startup without approval.
4. Install the rehearsed artifact using the install card. Keep the test database separate; use the office’s credential store for necessary secrets. Pin the approved endpoint/model. If a local Ollama model is used, follow its [official Windows guide](https://docs.ollama.com/windows) and [local-only configuration guidance](https://docs.ollama.com/faq); these apply to the model server, not to Elisa’s other components.
5. Run the end-to-end and failure checks again on the office PC with fictional data. Have the assistant run the variation and the lawyer inspect it. Measure total time including review against their current method. Do not connect a real file until the office separately approves that scope.
6. Leave a one-page operator card: how to start, request one draft, review/reject, stop and reach you. Record **GO: supervised pilot / REWORK / STOP**, defect owner, next test date and retention decision. On failure stop the worker, restore prior config, verify CRM access; remove only approved test artifacts. Never delete original matter records.

## Copy to ADMY | First instruction

> ADMY, inspect the existing LexFlow CRM + Elisa worker, read-only. Use backy as the existing builder, not a new agent. Identify the candidate build, real handler, model destination and installation/rollback path. Report the evidence matrix in Step 1. In an authorised disposable environment trace one synthetic request from CRM click to a persisted, reviewable draft. List what is verified, missing and untested. Recommend reuse/configure/patch/block; estimate the smallest intervention and any paid usage. Stop before editing, spending, installing or connecting to live data. After an approved patch independently rerun Step 4 on the exact candidate build; do not merely copy backy’s results.

## Copy to backy | After scope approval

> backy, fix only defect [ID] in approved build [version] on isolated test branch/copy [location]. Acceptance condition: [one observable result]. First reproduce it with fictional data; preserve the failing test. Patch the existing path, then show the passing test and relevant regressions. Supply changed files, exact repeatable commands, redacted results, runtime/usage, rollback steps and unresolved risks. No production writes, provider changes, new profiles, broader permissions, deployments or sends. Return the candidate to ADMY for independent verification; stop if the defect requires a larger redesign.
