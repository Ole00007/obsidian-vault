# LexFlow — Project Mind Roadmap (v2, surgical update)

**Generated:** 2026-09-03 | **Owner:** Olesia Rasing | **Scope:** Multi-tenant CRM rollout, agent onboarding, contact model, Elisa access controls

---

## 1. Process Gate

```
Backend-dev report
   ├─ Clean → request local preview link → proceed
   └─ Bugs found → audit those weak spots FIRST → only then request local link
```

**Global rule (permanent):** every "fixed"/"done" report must state LOCAL (preview link) or DEPLOYED (URL + commit hash). Applies to every future deploy.

---

## 2. Tenant Rollout Order & Inventory Status

1. **Romanelli (ws10 + cl1, cl2)** — reference tenant, test first.
2. **Pagliano (ws9)** — replicate after Romanelli passes.
3. **Ferro / AVIBE / aLEXy** — workspace IDs reportedly exist. **Open question for Hermes:** confirm whether each is already built/provisioned or still a TODO/planned task — websites unlinked and workspaces untested regardless.

Internal LexFlow (ws7) access: Dima (backend) and Kirill (design/content, Kanban action-titles only) get separate access.

---

## 3. Contact Model (approved structure)

Two separate models — Internal (staff directory, workspace-filtered) and Client-Facing (marketing-ready, lifecycle stage, consent, tags). **Gate:** backend-dev submits implementation plan for sign-off before any code.

---

## 4. Limits & Congestion Tracking

| Item | Decision | Still Needed |
|---|---|---|
| Matters per tenant | Unlimited | Tracking mechanism + threshold |
| Memory/storage per tenant | Unlimited | Same |
| Seat limit per tenant | **5 seats/tenant** (decided) | Reconfigure later via `SEAT_LIMIT_DEFAULT` config value — DB-configurable, no redeploy needed |

---

## 5. Missing Backlog Item

**Agentic AI-personalized email automation** — confirmed missing, needs its own spec.

---

## 6. QA/Test-Debug Agent — APPROVED, install now

QASkills.sh verified safe (only installs `.md` skill files, no runtime dependency impact). Install: `npx @qaskills/cli add <skill>`. Complementary "debug" skill also approved.

---

## 7. Parallel Tracking Board

**Safe in parallel:** QASkills.sh install, Dima's reads/audits, Kirill's isolated design work, user testing (read/click-through only), Elisa Phase 1 sandbox, backend-dev RLS test runs (test only).

**NOT safe in parallel:** fixes touching intake/contact/Kanban shared code, the RLS merge itself, testers triggering writes during active deploy windows.

---

## 8. Elisa (LexFlow PA) — 4-Phase Gated Access Plan

**⚠ Provenance flag:** Could not verify a distinct pretrained "Elisa" legal-PA repo on GitHub — only ElizaOS/Eliza (a general agent framework) is publicly documented. Confirm with Stefano before Phase 1 sign-off.

```
Phase 1: Isolated sandbox, synthetic data only, zero shared imports
Phase 2: Read-only, ONE workspace, time-boxed key, Postgres GRANT SELECT only
Phase 3: Staging — BLOCKED until feat/rls merged + 18 tests pass
Phase 4: Production — read and write/trigger access are SEPARATE approval gates
```

**Standing rules:** isolated module, scoped time-bound keys via secrets manager, Telegram status-only (never PII), hard key expiration, all actions logged with agent-identity tag, immediate revocation on engagement end.

---

## 9. Memory-Curator Agent

Delegate to save the tester-debugger profile + QASkills.sh links into BOTH the Obsidian vault and local working folders. Confirm exact paths before writing.

---

*Full detail and tables live in the companion Excel workbook: LexFlow_Rollout_Tracker.xlsx*
