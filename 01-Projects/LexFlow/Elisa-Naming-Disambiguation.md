---
title: Elisa naming collision — CRM vs website chatbot
created: 2026-10-29
tags: [lexflow, naming, agents, disambiguation]
status: active
---

# Elisa naming collision — CRM vs website chatbot

**Problem:** "Elisa" is both (A) the LexFlow CRM internal agent and (B) the public-facing chatbot on the LexFlow website lead-gen intake form. Mixing their data, prompts, or training artifacts causes profile and data leakage.

## Agent definitions (revised per backy review)

| Alias (vault) | Alias (Hermes profile) | Scope | Data it touches | Correct home |
|---|---|---|---|---|
| `elisa-crm` | `lexflow-crm-elisa` | Internal CRM agent for lawyers/staff | Matters, deadlines, documents, tasks, client contacts, internal notes | `01-Projects/LexFlow/Elisa-CRM/` |
| `elisa-intake` | `lexflow-intake-elisa` | Public website chatbot (script + AI hybrid) | Prospect contacts, service requests, marketing leads, intake form fields | `01-Projects/LexFlow/Elisa-Website/` |

### Canonical file naming

Use one prefix per agent; never mix:

- CRM artifacts: `elisa-crm-<topic>.md`
- Website artifacts: `elisa-intake-<topic>.md`

No `elisa-chatbot-*` variant. If a file touches both sides, it belongs in neither folder and must be split first.

## Hard rules

1. **Data-plane isolation.** CRM data (client matters, privileged docs) and website data (marketing leads, intake forms) require different retention/legal handling. Do not mix retention policies.
2. **Secrets/env separation.** Each agent has distinct API keys, OAuth tokens, and `.env` files. Never share CRM keys with website infrastructure.
3. **Network egress restriction.** The website agent must be sandboxed and prohibited from calling internal CRM APIs or touching CRM database schemas. CRM private networking must not be reachable from the intake path.
4. **Hermes memory isolation.** Profile memories, embeddings, and session histories must not be shared or searchable across `lexflow-crm-elisa` and `lexflow-intake-elisa`.
5. **Cross-link prohibition.** Forbid hyperlinks, wikilinks, or file references between `Elisa-CRM/` and `Elisa-Website/` artifact trees.
6. **Prompt-injection guardrail.** The website agent must never ingest CRM prompt templates or training data. Its model config, system prompt, and allowed tools must be independently auditable.
7. **Routing rule (deterministic, no per-ambiguity ask).** Use explicit namespace/tag-based routing:
   - Files tagged `#elisa-crm` → `Elisa-CRM/`
   - Files tagged `#elisa-intake` → `Elisa-Website/`
   - Files without a tag → default to CRM with a flag in the filename (`elisa-crm-<topic>-needs-review.md`) so they are visible and can be reclassified.
8. **Repo alignment.** Vault folder structure mirrors actual codebase homes:
   - CRM code → `Projects/lexflow/lexflow-crm`
   - Website code → `Projects/lexflow/lexflow-website`
   Vault notes reference these repos directly so infra changes map to real code.

## Links

- Parent: [[LexFlow-Platform-Plan-2026-10-24]]
- Related: [[Elisa-Improvement-Plan-2026-10-27]], [[LexFlow-Session-Summary-and-Operating-Blueprint-2026-10-27]]
