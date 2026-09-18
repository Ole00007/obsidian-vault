---
title: LexFlow — Index
created: 2026-08-26
tags: [index, hub]
status: active
---

# LexFlow — Index

Hub note for the `LexFlow` folder. Links to every note here.

## Notes

- [[LexFlow-Web-Site-Scope-2026-09-17]] — **current scope/status**: deployed to production (`1cba771c`, source `0a6f5bd`), consent UI + privacy disclosure + `id=hero` live, pushed to public GitHub, content export (3038 blocks), CRM repoint + hard rule + daily cron handed to operator; legal identity + Cloudflare Git integration pending
- [[LexFlow-Web-Site-Quality-Debt-Register-2026-09-17]] — **[OVERRIDE] debt register**: prod deploy `bd4b683` with 14/15 DoD checks failing; all 15 re-verified + 3 new findings (hook.example.com placeholder ×45 pages, repo outside the §8 repo root, committed `dist/`); blocked on Ole's rebuild-vs-patch call (kanban `t_3c7158f8`)
- [[LexFlow-Web-Site-CRM-Repoint-2026-09-17]] — CRM repointed to the new site (`6ef25da`, local, unpushed: ole's direct request). Found the site **root `/` 404s** and clean URLs 308 the `.html`; CRM now targets `/lexflow-index#hero`. Follow-up `t_b92d36cc`
- [[LexFlow-Web-Site-Cross-Test-PreDeploy-2026-09-16]] — independent cross-test of build `3b9cc41`+`23678b7`: 6 PASS / 1 FAIL (FAQ calendar alt regresses to a "team" description in EN/IT/RU), not deployed
- [[LexFlow-Ecosystem-Index-v3-2026-09-16]] — **ecosystem inventory v3**: complete inventory + live-probed endpoints (2026-09-16), correct Netlify/Railway hosts
- [[LexFlow-Web-Site-Agent-Surface-2026-09-15]] — WebMCP tools, ai-plugin.json, openapi.yaml, llms.txt, JSON-LD upgrade, 48-URL sitemap
- [[LexFlow-Web-Site-Session-Recap-Batch2-2026-09-13]] — humanizer pass, EN-leakage bug fixes, WhatsApp Option C single source, build near-miss
- [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]] — stack decision 1.4, new kanban board, live endpoints, repo-root rule
- [[LexFlow-Public-Intake-Contract-2026-09-15]] — /api/public/intake contract review: matches, 4 deltas, 4 decisions for Ole
- [[LexFlow-Legal-Publishing-Blockers]] — **legal gate**: P.IVA + entity placeholders + `info@`/`demo@` decision; pages frozen until Ole supplies values
- [[LexFlow-Web-Site-Enrichment-Elisa-2026-09-13]] — Elisa assistant clone, approved FAQ + glossary, claims register, trust wording (commit `0b67e3f`)
- [[LexFlow-Web-Site-Build-2026-09-07]] — multi-page web-site build session
- [[LexFlow-Audit-Checklist]] — audit checklist
- [[LexFlow-Isolation-Fix-Frontend-Handoff]] — isolation fix handoff
- [[LexFlow-MultiTenant-Test-Setup]] — multi-tenant test setup
- [[LexFlow-Romanelli-Sub-Workspaces]] — Romanelli sub-workspaces
- [[LexFlow-Surgical-Additions-2-3]] — surgical additions 2 and 3
- [[LexFlow-Workspace-2026-08-31-Inventory]] — workspace inventory
- [[LexFlow-Workspace-UX-Overhaul]] — workspace UX overhaul
- [[LexFlow-Architecture-Email-Resend]] — email/Resend architecture
- [[LexFlux-UX-UI-Design-Research-Report-2025]] — UX/UI design research report
- [[avibe-hq-bootstrap-plan]] — AVibe HQ bootstrap plan
- [[aLEXy-INDEX]] — a-Lexy project hub (reference LP + chatbot)

## Links

- Parent: [[01-Projects-INDEX]]
- Related: [[aLEXy-INDEX]]
- Related: [[AGENT_RULES]]
