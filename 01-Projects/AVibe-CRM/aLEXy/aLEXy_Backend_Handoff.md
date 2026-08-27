# aLEXy Backend — Handoff Package (Corrected)
**Prepared:** July 23, 2026 (v2 — corrected chatbot origin + GDPR status)

---

## 1. Confirmed Understanding Table

| Item | Confirmed | Where it lives & environment | Local path |
|---|---|---|---|
| aLEXy = new Flask **backend** app | Yes | GitHub: `Ole00007/aLEXy` · Deploy: Railway project `9c6f87e9-2d41-438b-b92c-1f62120b4d6a` · DB: PostgreSQL (Railway) | `/Users/olesiarasing/Desktop/aLEXy/` |
| aLEXy **landing page** | Yes | Not yet in git · Future deploy: Netlify (not yet live) | `/Users/olesiarasing/Desktop/aLEXy/landing page/aLexy_Netlify_READY_index.html` |
| LexFlow-MVP (heritage) | Yes | GitHub: `Ole00007/LexFlow-MVP` · Deploy: Railway (separate project) · Read-only reference for merge work | Not yet confirmed — confirm exact local folder before merge work starts |
| **LexFlow-Chatbot ("Alessia")** | Corrected | Custom-built by founder + Perplexity (NOT Flowise — this was a wrong assumption in the prior draft). Repo: `Ole00007/LexFlow-Chatbot` | `Desktop/lexflow/lexflow chatbot` |
| Goal: merge, no destruction | Yes | Work happens in new Space, additive-only commits | N/A |
| This Space (current) scope | Yes | Continues on aLEXy landing page only | `/Users/olesiarasing/Desktop/aLEXy/landing page/` |

**Correction applied:** The chatbot "Alessia" was NOT built with Flowise on LexFlow-MVP — it was custom-built by the founder in this working relationship. Whether Hermes has since built a SEPARATE/NEW bot inside aLEXy is UNKNOWN and must be checked in Phase 1, not assumed either way.

**GDPR consent logging:** NOT YET BUILT anywhere — status is "coming up" (planned, future work), not an existing feature to merge or compare. Do not treat as a gap-analysis item; treat as new work, lower priority than the core merge.

**Confirmed stack for aLEXy (from landing page content):** Flask + PostgreSQL, Kanban case/task board, Google Calendar sync, client intake form, email automation (Resend), WhatsApp notifications (new — not previously scoped), AI chatbot "Alessia" (custom-built, origin confirmed above — verify if Hermes duplicated/rebuilt it), configurable practice areas, cookie consent banner (frontend only, no backend yet). GDPR consent logging: planned, not yet implemented.

---

## 2. Comparison Approach — Perplexity Space vs. Hand to Hermes Directly

| Approach | Where | Risk | Speed | When to use |
|---|---|---|---|---|
| **Option A — Compare here first (recommended)** | New Perplexity Space, read-only analysis, no repo write access | Safest — zero chance of code being deleted/overwritten, since no execution happens here | Slower — requires you to paste/upload repo file listings or key files for me to read | Use for the INITIAL gap analysis: "what exists in LexFlow-MVP vs aLEXy, and does aLEXy already have its own chatbot or not" — get the full picture before anyone touches code |
| **Option B — Hand to Hermes directly** | Hermes has real repo + terminal access | Riskier — same pattern that caused prior destructive edits | Faster — can actually run diffs, greps, and file comparisons live | Use ONLY for the actual merge/port execution, AFTER Option A's gap list is reviewed and approved by you |

**Recommended sequence:** Run Option A first for the comparison/gap list (safe, no risk) — this MUST include checking whether Hermes already built a chatbot inside aLEXy, since that's currently unknown. Once you've reviewed and approved which functions to port, hand ONLY the approved, itemized merge list to Hermes (Option B).

---

## 3. Settings for New Space — "aLEXy Backend"

- **Name:** aLEXy Backend — LexFlow-MVP Merge
- **Repos in scope:** `Ole00007/aLEXy` (active build target), `Ole00007/LexFlow-MVP` (read-only reference only), `Ole00007/LexFlow-Chatbot` (read-only reference — confirm if already ported/duplicated into aLEXy)
- **Railway project:** `9c6f87e9-2d41-438b-b92c-1f62120b4d6a`
- **Stack:** Flask + PostgreSQL, custom chatbot "Alessia" (founder-built, NOT Flowise), Email automation (Resend), WhatsApp notifications, Google Calendar sync, Kanban case/task management — vertical legal SaaS
- **Hard rule carried over:** one commit per function/fix, wait for Railway green before next push
- **New hard rule for this Space:** no deletions or overwrites of existing aLEXy code without an explicit diff shown to founder first
- **Out of scope:** landing page (stays in current Space), ContaFlow/Project B (stays parked)
- **GDPR consent logging:** flagged as planned/future work, not part of this merge pass

---

## 4. Prompt for New Space — aLEXy Backend Build

```
CONTEXT:
- Two+ repos exist:
  1. LexFlow-MVP (github.com/Ole00007/LexFlow-MVP) — HERITAGE app.
     Contains tested, customer-approved functions. READ-ONLY reference
     — do not modify this repo in this workstream. Local path: confirm
     with founder before starting (not yet verified).
  2. aLEXy (github.com/Ole00007/aLEXy) — NEW app, built by Hermes.
     Railway project: 9c6f87e9-2d41-438b-b92c-1f62120b4d6a.
     Local path: /Users/olesiarasing/Desktop/aLEXy/
     This is the ACTIVE build target going forward.
  3. LexFlow-Chatbot (github.com/Ole00007/LexFlow-Chatbot) — the
     ORIGINAL "Alessia" bot, custom-built by founder (NOT Flowise —
     correct this assumption if you see it anywhere in old docs).
     Local path: Desktop/lexflow/lexflow chatbot. READ-ONLY reference.
- Goal: aLEXy should end up with EVERYTHING LexFlow-MVP (and the
  original chatbot, if not already present) has, PLUS everything
  already newly built in aLEXy — a merge, not a replacement. Nothing
  already working in either app should be lost or overwritten.
- UNKNOWN TO RESOLVE FIRST: it is NOT confirmed whether Hermes has
  already built a separate/duplicate chatbot inside aLEXy, or left this
  feature out entirely. This must be checked in Phase 1 — do not
  assume either way.
- STACK: Flask + PostgreSQL, vertical legal SaaS. Confirmed feature set
  from landing page copy: Kanban case/task pipeline, Google Calendar
  sync, structured client intake (conflict checks, engagement terms),
  automatic client updates via email (Resend) AND WhatsApp, AI chatbot
  "Alessia" (custom-built — verify origin/duplication status),
  configurable practice areas (civil, corporate, employment, real
  estate, criminal, custom).
- GDPR CONSENT LOGGING: NOT YET BUILT anywhere. This is planned future
  work, NOT part of the gap-comparison — treat as new-build backlog,
  lower priority than the merge itself.
- KNOWN RISK: In past sessions, rebuilding/refactoring has repeatedly
  destroyed existing working functionality. This must not happen again.

PHASE 1 — COMPARE, DO NOT CHANGE ANYTHING YET:
1. List all routes/functions/models in LexFlow-MVP (grep for
   @app.route, @blueprint.route, class definitions in models/).
2. List all routes/functions/models currently in aLEXy the same way.
3. SPECIFICALLY CHECK: does aLEXy contain any chatbot/bot-related code
   (routes, webhook handlers, AI client calls)? If yes, compare it
   against LexFlow-Chatbot's original code — is it the same bot ported,
   a rebuilt duplicate, or something different? Report clearly.
4. Produce a side-by-side gap table:
   Function/Route | In LexFlow-MVP? | In aLEXy? | Action needed
5. Flag specifically which LexFlow-MVP functions were customer-tested/
   approved and are MISSING from aLEXy — priority merge targets.
6. Also flag any of the confirmed stack features above (WhatsApp,
   chatbot, Google Calendar) that exist in NEITHER app — these need to
   be built fresh, not ported.
7. STOP HERE. Report the gap table back to founder before writing or
   changing any code. Do not proceed to Phase 2 without explicit
   go-ahead.

PHASE 2 — MERGE, ONE FUNCTION AT A TIME (only after founder reviews
Phase 1 gap table):
1. For each missing function, port it from LexFlow-MVP (or
   LexFlow-Chatbot, for bot logic) into aLEXy as its OWN isolated
   commit — one function per commit, never batched.
2. Before each port, confirm: does aLEXy already have a differently-
   named or differently-built version of this function? If yes, STOP
   and ask founder which to keep — do not silently overwrite either
   version. This applies especially to the chatbot, given the unknown
   duplication status.
3. After each commit, push, wait for Railway Deployments tab fully
   green before starting the next function.
4. Never delete or modify existing aLEXy code as a side effect of
   adding a ported function — additive only.

HARD RULES:
- Do not modify the LexFlow-MVP or LexFlow-Chatbot repos at all in this
  workstream — read-only reference only.
- Do not touch aLEXy's landing page work — tracked in a separate Space.
- Do not touch ContaFlow/lexflow-crm.
- Do not build GDPR consent logging in this pass — flagged as separate
  future work, out of scope for now.
- One commit per function/fix. Wait for Railway green before next push.
- No deletions/overwrites without showing founder a diff first.
- If in doubt about whether two functions (especially chatbot logic)
  conflict or duplicate, ASK — do not guess and merge.

DELIVERABLE FOR PHASE 1:
A markdown or table gap-comparison report: function name, purpose,
present in LexFlow-MVP (yes/no), present in aLEXy (yes/no), customer-
approved status if known, recommended action (port as-is / merge logic
/ build fresh / skip — already superseded). Include an explicit,
separate line item resolving the chatbot duplication question.

Do not proceed past Phase 1 without founder review.
```

## Links
- Parent: [[aLEXy-INDEX]]
- Related: [[aLEXy_Backend_Handoff_v2]]
