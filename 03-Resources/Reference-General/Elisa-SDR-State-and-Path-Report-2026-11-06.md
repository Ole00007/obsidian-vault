---
title: Elisa / SDR — state on Elisa, what SDR is, and the path decision
created: 2026-11-06
tags: [lexflow, elisa-crm, sdr, sales, architecture, status, decision]
project: LexFlow
home: 01-Projects/LexFlow/
status: awaiting_ole_decision
---

# Elisa / SDR — state on Elisa, what SDR is, and the path decision (2026-11-06)

*Requested by Ole in the Bot Chat session `20260919_185414_b81acb`, where four messages stacked behind a
dead model (`meituan/longcat-2.5-preview:free`) and never ran. Card: `t_34773a0671ec4c8e`.*

Ole's queued asks, verbatim:

1. "ask backy the state on Elisa before running anything because Elisa should be working with it too"
2. "à native. what is SDR?"
3. "path A or D — stability risks and customisability of templates complexity for users — assess"
4. "Plan seems fine but double-check with backy"

---

## 1. State on Elisa — verified, not relayed

I did not take this from a previous report. Every line below is from a command I ran on
2026-11-06 between 21:30 and 22:05 CET.

| Question | Answer | Evidence |
|---|---|---|
| Where is the code? | `/Users/olesiarasing/projects/lexflow/lexflow-crm` — `crm/agent/{brain,dialog,doctext,drafts,guard,intents,llm,router,runner,tools}.py`, `crm/routes/agent.py`, `templates/_elisa_bubble.html`, `static/js/elisa/elisa.js`, `static/css/elisa/elisa.css` | `git ls-tree -r --name-only lexflow_hermes_v1 \| grep -i -E "agent\|elisa"` → 25 files |
| Is it tested? | `tests/test_agent.py`, 837 lines, 26 tests. **25 pass, 1 fails** — on *both* the deploy branch and the hardening branch | `python3 -m pytest tests/test_agent.py -q` in `lexflow-crm-wt-merge` (@`9af129c`) and `lexflow-crm-wt-harden` (@`0b3d3db`) → identical result |
| Is the failure a bug? | **No.** The test hard-codes `due 2026-11-03`; today is 2026-11-06, so Elisa answers `"2026-11-03 is in the past. Which date should I use instead?"` with `status: completed` instead of `pending_approval`. The product is behaving correctly; the test is a time bomb | Reproduced live: `POST /api/agent/chat` → HTTP 200, `{"status":"completed","reply":"2026-11-03 is in the past. Which date should I use instead?"}` |
| What can Elisa do? | 16 tools, of which 5 are approval-gated (`flag_lawyer`, `update_task_status`, `create_task`, `create_calendar_event`, `draft_notification`); **no delete tool exists** | `TOOL_SPECS` in `crm/agent/guard.py` |
| Is she exposed? | No. Flag `AGENT_ENABLED`, default `false` → route answers 404 | `guard.py:is_agent_enabled()` + prod probe |
| Is the latest Elisa deployed? | **No.** `lexflow_hermes_v1` is **15 commits ahead** of `origin/lexflow_hermes_v1`; 8 of those 15 are Elisa work (`829d235`, `0ad2359`, `603b4d6`, `4a68a77`, `6117bbd`, `8ec7c53`, `7a7976b`, `215bcc2`) | `git rev-list --left-right --count origin/lexflow_hermes_v1...lexflow_hermes_v1` → `0 15` |
| Is hardening in the deploy line? | **No.** `bd21460` (payload hash, expiry 410, atomic single-use claim, tenant tests) and `0b3d3db` (only the proposing user may approve) live on `feat/elisa-hardening` and are not ancestors of `lexflow_hermes_v1` | `git merge-base --is-ancestor` → NO for both |
| Is prod up? | **No.** `https://web-production-031a6.up.railway.app` returns `404 {"message":"Application not found"}` from the Railway edge on `/`, `/login`, `/health`, `/api/agent/chat` — that is the service/domain, not the agent flag. Day 3 of `P0-PROD-DOWN-REGRESSION-2026-11-04` | `curl` on 5 paths; `railway whoami` → Unauthorized, so the service state needs Ole's Railway access (card `t_a885fb80` still blocked) |
| Can it be shown today? | Only locally — the demo on port 5057 holds the `port-5057` lock (backend-dev's) | `~/projects/lexflow/lexflow-crm-wt-demo2` |

### The gate Elisa is sitting behind

Card `t_e4706b73` — "ADMY GATE: cross-test Elisa CRM (`ddec0aa..8ec7c53`), read-only, no push" — has been
**blocked since 2026-10-29**, 8 days. Its own text confirms "remote head is ddec0aa — the Elisa commits are
NOT on remote". So the honest summary is: **Elisa is built, green apart from a stale date in one test, and
blocked behind a cross-test gate plus Ole's push authorization. It is not broken; it is not shipped.**

---

## 2. What SDR is

**SDR = Sales Development Representative.** The person (or agent) who owns the *front* of the sales funnel and
hands qualified work to a closer:

| Stage | SDR owns it |
|---|---|
| Define the ideal client profile (ICP) | yes |
| Build the prospect list (sources, enrichment, dedupe) | yes |
| First touch (email, LinkedIn, WhatsApp) | yes |
| Qualify — budget, authority, need, timing (BANT) or MEDDIC | yes |
| Book the meeting | yes |
| Run the deal, quote, negotiation | no — that is the closer |

An **AI SDR** automates the left column: sourcing, sequencing, personalised first touch, reply triage,
qualification, booking — with a human approving anything that leaves the building.

For a law firm that means: intake lead arrives → qualified against the firm's practice areas → conflict check
→ consultation booked → handed to the avvocato. Note that **this funnel already exists as a spec in our own
tracker** — `reflection_rules` in `docs/LexFlow_Agentic_Roadmap.json` model exactly that: `New Lead` →
`Consult Scheduled` → `Pending Conflict Check` (hard gate, "BLOCK engagement_letter until manual clear") →
`Retainer Out` → `Signed/Active Client`, with 24h/72h/7d follow-up cadences and a `lock_lead_nurture`
suppression on signature. It is a specification, not code.

---

## 3. The template Ole looked at, and why it does not plug in

A standalone B2B SDR agent framework built on OpenClaw. What it brings:

| Component | Contents |
|---|---|
| 7-layer context | Identity, Soul, Agents, User, Heartbeat, Memory, Tools — markdown files re-read every turn |
| 10-stage pipeline | lead capture → BANT → CRM entry → research → quotation → negotiation → reporting → nurture → email outreach → multi-channel |
| 4-layer memory | MemOS + rolling summary + ChromaDB vector store + daily CRM snapshot |
| 8 skills | delivery-queue, supermemory, chroma-memory, telegram-toolkit, sdr-humanizer, lead-discovery, quotation-generator, graphify |
| 14 cron jobs | pipeline checks, lead discovery, follow-ups, stalled alerts |
| Channels | WhatsApp, Telegram, Email |
| **Its own CRM** | Google Sheets, JSON file, Notion **or HubSpot** — **not LexFlow** |

The last row is the whole problem. It is not a library or a plugin. It is a complete agent **with its own
system of record**, its own memory stack, its own scheduler, and no adapter for a Flask CRM.

---

## 4. Path assessment (Ole: "A or D" — the options on the table were A / B / C)

| | **A — install alongside, bridge** | **B — native inside LexFlow** ✅ | **C — hybrid** |
|---|---|---|---|
| What it means | Run the template as its own agent; write an adapter that syncs leads to/from the LexFlow API | Rebuild the SDR capability inside the CRM on Elisa's existing plumbing | Template for conversation/channel layer, custom adapter for CRM |
| **Stability risk** | **High.** Two datastores, two schedulers (14 crons + Hermes), MemOS + ChromaDB + Flask, and a sync that has to survive partial failures both ways. Every schema change on either side is a new failure mode. | **Lowest.** Same DB, same Flask app, same `guard.py` allow-list, same approval cards, same JWT-based tenant isolation, same `agent_audit` trail that already ships with Elisa. | **Highest.** A adds latency and a second memory, plus the adapter. |
| **Customisability** | Customisable *within* the template's assumptions (its pipeline, its prompt layers). Going outside them means forking OpenClaw code you do not own. | Full. It is our Flask code; per-firm stage names, per-workspace ICP, Italian/English copy are ordinary code and config. | Middle — customisable at the seam only. |
| **Complexity for the user** | **High.** Two places to look at a lead, two inboxes, two sets of "why did this not send". | **Lowest.** One CRM, one Elisa bubble, one activity timeline. A lawyer asks Elisa "what happened with the Rossi lead" and gets the answer from the same place as everything else. | High. |
| **Legal / data plane** | Two retention regimes for the same prospect — a GDPR liability, and it breaks the Elisa disambiguation rules 1–2 (separate data planes, no shared secrets) in the wrong direction: the same person now exists twice. | One regime, consent fields already on the model (`gdpr_consent`, `gdpr_consent_ts`). | Two regimes. |
| **Rules check (§9 no duplicate registries)** | **Violates it.** A second CRM/registry for leads that LexFlow already models in `crm/models/contact.py` (`source` manual/intake/booking/web/import, `status` default `lead`, `lifecycle_stage`, `tags`). | Extends the existing registry in place. | Violates it partially. |
| **Indicative effort** (not a Phase-0 estimate — say "estimate" and I do it properly) | Medium to install, then permanent sync tax | Higher upfront, no sync tax | Medium-high, plus the tax |

**Recommendation: B — native.** The decisive arguments are not stylistic:

1. `contact.py` already carries a lead lifecycle (`status='lead'`, `lifecycle_stage`, `source`, GDPR consent
   timestamps). A second CRM would be a duplicate registry — our own §9 rule, and it would drift.
2. Elisa already gives us the three things an SDR agent needs and is expensive to rebuild: a **tool allow-list
   with per-tool approval** (`guard.py`), **tenant isolation carried by the caller's own JWT** (she can never
   see more than the user can), and an **audit trail** (`agent_audit`). The template would bring none of that
   and would need all of it rebuilt to be safe in a law firm.
3. The funnel Ole wants is already written down as `reflection_rules`. It needs implementing, not importing.

Elisa's role in it: **the same agent, a second lane.** The naming note already reserves the slot —
`elisa-crm` (internal assistant), `elisa-contracts`, **`elisa-sales`**, `elisa-web` — one visible "Elisa" with
a small subtitle, one entry point routing to the right lane. Data-plane separation stays as written: client
matters (privileged) never mix with marketing leads, separate retention, separate secrets, no cross-links.
SDR tools become new entries in `TOOL_SPECS`, and every write stays approval-gated exactly like `create_task`
is today.

### Staged shape, if Ole says go

- **S0 — unblock (small):** backy confirms the state below, the stale-date test is fixed, and the funnel
  stages stop being a JSON spec and become code (constant + column default), so there is one truth.
- **S1 — inbound SDR, no outbound:** lead stages live on contacts; Elisa gains read+propose tools
  (`list_leads`, `update_lead_stage`, `draft_outreach`); qualification captured as BANT fields; follow-ups
  become **existing** tasks and calendar events, not a new board. Conflict check stays a hard gate.
- **S2 — cadence:** 24h/72h/7d sequences from `reflection_rules`, driven by **one Hermes cron job** (the app
  has no scheduler — there is no APScheduler anywhere in `crm/`), each send approval-gated.
- **S3 — outbound:** only after a verified sending domain exists (see blocker 3).

---

## 5. Blockers that matter more than the path choice

1. **Prod is down, day 3.** Railway edge says "Application not found" on every path. Nothing Elisa or SDR can
   be demoed live until this is fixed, and I cannot inspect the service — `railway whoami` is Unauthorized.
   Needs Ole's Railway access (card `t_a885fb80`).
2. **15 unpushed commits, 8 of them Elisa**, and the ADMY cross-test gate blocked since 2026-10-29. Elisa
   cannot reach prod without: cross-test → Admy gate → Ole's explicit per-push authorization (PUSH GATE).
3. **Email cannot reach clients.** `crm/email_service.py` sends via Resend with `EMAIL_FROM` defaulting to
   `onboarding@resend.dev`; that sender only delivers to the account owner. Any SDR outreach to a prospect will
   fail until a domain is verified. **This is the hard ceiling on outbound SDR** — S1 (inbound) is unaffected.
4. **No scheduler in the app.** Cadence must live on Hermes cron (one job, `--no-agent` style) or Railway cron.
   T-013 "AI adaptive/reflective email agent" is a blocked roadmap node for the same reason.
5. **GDPR for prospects.** Lawful basis, retention and consent tracking must be settled before any outbound
   sequence — the consent columns exist, the policy does not.

---

## 6. Double-check with backy

Ole asked to double-check with backy before running anything, and I am not going to claim his sign-off I do
not have. I verified the state myself (section 1) instead of quoting it second-hand, and I filed card
**`t_be72f3fb`** to `backend-dev`:

- **A** confirm or correct the five facts in section 1, citing the branch/commit he checked;
- **B** fix the stale-date test (date-relative, past-date-refusal kept as its own assertion) — local commit, no push;
- **C** review the native-SDR substrate question: is `contact.py` + `reflection_rules` the right place, and
  where does cadence live (Hermes cron vs Railway cron vs in-app)?

Until that comment lands, treat section 1 as "verified by operator-installer, pending backy's confirmation"
and section 4 as a recommendation, not a decision.

---

## 7. What I need from Ole

One decision, one answer:

1. **Path: B (native) — confirm or pick A/C.** My recommendation is B, for the three reasons in section 4.
2. **S1 scope: inbound-only first (qualification + follow-ups, no outbound)?** That version needs no email
   domain and no new scheduler, and it is the piece that actually touches Elisa.

Say "go" and I will run a Phase-0 estimate in the §14 format before any build starts — estimate only, no
branches, no cards until you approve the number.

---

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[Elisa-CRM-Status-and-Architecture-2026-10-29]]
- Related: [[Elisa-Naming-Disambiguation]]
- Related: [[LexFlow-Platform-Plan-2026-10-24]]
