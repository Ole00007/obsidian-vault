# Elisa Architecture (preview draft v0.9, 2026-10-30)

Status: DRAFT FOR APPROVAL. After approval the research pack (xlsx, json, brief, implementation plan) gets one surgical update and is re-zipped for Backy.
Scope: Elisa stays the in-house orchestrator inside LexFlow CRM. External pieces are narrow plug-ins behind Elisa's tools. Nothing replaces Elisa.

## 1. Team roster (remember and notify)
| Nickname | Role | Notes |
|---|---|---|
| Backy (also "Bone") | Backend dev, owns this build | Remembers both nicknames. Notifies the roster that this plan exists, selects other collaborators himself, and records them below. |
| Fronty (also "Skin") | Frontend dev | Called "Fronty" or "Skin" by Olesia. |
| Other collaborators | Chosen by Backy | Add name, nickname, lane. |

Backy: when you receive this pack, post a short message to Fronty/Skin and any collaborator you add, with the pack name and your lane assignments.

## 2. Principles (soft rules)
1. Elisa orchestrates; plug-ins only answer narrow questions. No plug-in decides, writes or sends.
2. Every write or outbound action goes through an approval record. Tenant ID comes from Elisa's session, never from a model or a plug-in.
3. Deterministic code for conflicts, deadlines and document assembly. The model reads, drafts and explains.
4. Foreign (US/UK) material gives structure only, never legal content. Italian sources give the content.
5. Anything unverified is labelled unverified. Nothing is installed from a public marketplace without manual review and a pinned hash.
6. Reversible by default: each plug-in can be switched off without breaking Elisa.

## 3. System context
```
 Lawyer / staff (browser)  <--  Fronty/Skin UI: chat, approval inbox, draft viewer, citation viewer
            |
            v
 Elisa API (Flask, assumed)  -- auth, session, tenant context -->  Postgres (RLS on every table)
            |
            v
 Elisa Orchestrator (LangGraph graph, checkpointed per tenant)
    |-- Elisa-crm        (action agent)
    |-- Elisa-researcher (Italian law)
    |-- Elisa-contract   (analysis + drafting)
    |-- Elisa-s&m        (later)
            |
            v
 TOOL GATEWAY  <-- the plug-in seam: manifest, schema check, scope, egress, audit, timeout
    |-- native CRM tools + deterministic engines (in-process)
    |-- Legal Source Index (read-only, shared, tenant-neutral)
    |-- mcp-legal-it container (Streamable HTTP, internal network only)
    |-- OpenContracts (per-tenant instance or extraction pipeline)
            |
 Approval Service --> Approval Executor (the only component that writes to CRM / sends)
```
Stack assumptions (Backy to confirm in the first step): Flask + PostgreSQL with row-level security, containers on the current host, existing auth and approval concept inside Elisa.

## 4. Components
| # | Component | Responsibility | Source |
|---|---|---|---|
| C1 | Elisa API + session | Auth, tenant context, rate limits | in-house |
| C2 | Orchestrator | Intent routing, sub-agent graph, state | in-house, LangGraph pattern |
| C3 | Tool Gateway | Registers every tool with a manifest; validates input/output; enforces scope, egress, timeout; writes audit | in-house |
| C4 | CRM read tools | list_tasks, get_matter, list_contacts, get_agenda, get_deadlines | in-house |
| C5 | Conflict engine | Overlaps, double-booking, hearing vs deadline clashes, buffers | in-house (code) |
| C6 | Deadline engine | Procedural terms, August suspension; cross-checked against mcp-legal-it calculations in tests | in-house (code) |
| C7 | Approval Service + Executor | Approval records, pause/resume, idempotent execution | in-house + LangGraph interrupt |
| C8 | Legal Source Index | Statutes (Italia Corpus), optional case-law metadata (HF corpus); BM25 + vectors | USE-DATA |
| C9 | Italian law plug-in | mcp-legal-it, profile `normativa` for research, profile `calcoli` for offline calculations | USE-CODE |
| C10 | Citation Guard | Every cited norm must match a retrieved text; unverified citations are flagged [verify] | in-house (mcp-legal-it's Stop hook is Claude Code-specific) |
| C11 | Document service | Parse, clause extraction, Q&A, per-tenant | OpenContracts (spike first) |
| C12 | Drafting service | Template fill, deterministic DOCX assembly, tracked-change application | in-house + mcp-legal-it templates |
| C13 | Model router | Role-to-model map in env; cheap fast tier by default, stronger model only on QA flag | in-house |
| C14 | Security layer | Injection filters, egress allowlist, secrets, scan results, plug-in pins | in-house |
| C15 | LLMOps | Traces, cost per session, escalation rate, missed intents, Italian golden sets | in-house |
| C16 | Scheduler | Watchers (deadlines, agenda, digest) via Hermes cron | Hermes |

## 5. Agents
### Elisa-crm (action agent)
- Reads: tasks, matters, contacts, agenda, deadlines (C4).
- Finds: conflicts (C5) and deadline risks (C6). It must call `find_conflicts` before proposing any slot.
- Writes: notes to the user are free. Everything else (new task, calendar entry, letter, proposal) is a draft in an approval record.
- Pattern source: claude-for-legal (intake, portfolio status, docket watcher, escalation router, client letter drafter, append-only comms log). Rewrite for Italian practice.
### Elisa-researcher
- Tools: `italian_law_lookup`, `check_currency`, `eu_basis`, `case_law_search` (only where a licensed or open source exists).
- Output: answer + citations with URN/article + currency flag. No citation, no claim.
### Elisa-contract
- Tools: `doc_qa`, `extract_clauses`, `review_against_playbook`, `draft_act`, `draft_letter`.
- Italian playbooks first (arts. 1229, 1341-1342 c.c., penalty clauses, GDPR art. 28 DPA).
- Redlines applied by deterministic code, not by asking the model to rewrite the document (pattern from Microsoft's Word Legal Agent).
### Elisa-s&m
- Not designed. Needs its own research round.

## 6. The plug-in seam (Tool Gateway manifest)
Each tool, native or external, is registered like this:
```yaml
name: italian_law_lookup
agent: Elisa-researcher
class: read            # read | draft | write
tenant_scope: none     # none | tenant (index is shared, read-only)
approval_required: false
transport: mcp-http    # in-process | mcp-http
endpoint: http://legal-it:8000/mcp   # internal network only
egress_allowlist: [normattiva.it, eur-lex.europa.eu]   # per source-terms review
timeout_s: 20
pinned: {repo: capazme/mcp-legal-it, tag: "<release tag>", commit: "<sha>"}
input_schema: {...}
output_schema: {...}
audit: ids_counts_only   # never log content
```
Rules: writes are never exposed to a model directly; the model proposes, the Approval Service decides, the Executor writes.

## 7. Data and tenant isolation
- Every tenant table has `tenant_id` and an RLS policy; the app role cannot bypass RLS.
- LangGraph checkpoints use a durable Postgres checkpointer; `thread_id = tenant:matter:approval`.
- Approval record: id, tenant_id, matter_id, agent, action_type, payload, payload_hash, status, requested_by, decided_by, decided_at, expires_at, idempotency_key. An approval is bound to tool + argument hash + user identity + expiry, so changed arguments invalidate it.
- Audit log stores ids, counts and dates only. Lesson: clio-mcp 2.0.1 wrote client content into its audit log and had to fix it in 2.2.0.
- Shared Legal Source Index holds public law only. No tenant text enters it.
- Plug-in containers: no volume mounts of tenant data except the one tenant they serve; one instance per tenant where they touch documents.

## 8. Approval flow
1. Agent proposes an action. 2. Gateway stores a draft approval record. 3. Orchestrator calls `interrupt()` with a JSON-serialisable summary. 4. UI shows draft, diff, sources, risks. 5. User approves / edits / rejects. 6. Executor runs the write once, with an idempotency key. 7. Audit entry (ids only).
LangGraph rules to respect: durable checkpointer; the node restarts from its beginning on resume, so side effects before `interrupt()` must be idempotent; never wrap `interrupt()` in a bare try/except; do not loop `interrupt()` calls non-deterministically.

## 9. Security and supply chain
- Document text and web content are data, never instructions. Wrap in delimited blocks; strip hidden Unicode/HTML comments before the model sees it.
- Prompt-injection test set: hostile text inside a matter note must not trigger any tool.
- Plug-ins: fork to private org, pin commit, scan with `uvx mcp-scan@latest --skills` and a manual read of prompts, install scripts and network calls. Scanners are one input only: researchers bypassed ClawHub, Cisco and skills.sh detectors, and the advice is not to outsource trust to a scanner.
- mcp-legal-it: bind to the internal network (its default host is 0.0.0.0), pin a release tag (not `@main`), use profile `calcoli` where no network is needed.
- OpenContracts: change default admin credentials, disable anonymous telemetry, review MCP endpoints that can write (it can propose annotations and post thread messages).
- Secrets in a secret store, per tenant keys, no secrets in prompts or logs.
- Re-scan on every update; update only after review.

## 10. Jurisdiction and licensing
- Primary law: Italy and EU. Statutes are free of copyright under art. 5 L. 633/1941, but court judgments are outside that carve-out and Normattiva's site terms restrict bulk reuse of its database structure. Normattiva is also reported to declare CC-BY-4.0 since 2026-01-01 (reported by the Ansvar notes; verify at the source).
- Case law needs a separate basis per source (PSI rules or the court's own terms). Counsel to confirm before any commercial case-law retrieval.
- US/UK material (claude-for-legal, Vaquill, Ally) is structure only: playbook pattern, approval gates, redline UX. Their legal content (FRE 408, FMLA, Bluebook, CourtListener) must not reach Italian users.
- Common-law boilerplate transplants badly into Italian contracts (liability caps, indemnities, onerous clauses). Italian playbooks are mandatory; a lawyer reviews all drafts.
- AI-use disclosure to clients and professional secrecy: confirm current Italian requirements with counsel.
- Licence register: Apache-2.0 (mcp-legal-it, claude-for-legal, Vaquill), MIT (OpenContracts, clio-mcp, google-calendar-mcp, italia-corpus script), CC-BY-4.0 (HF corpus, attribution required), public domain (statutory text), AGPL-3.0 (Lexia, AVOID). LangGraph licence: read the LICENSE file in the repo (not shown on the page I fetched).

## 11. Models and cost
Role-to-model map lives in env and can be hot-swapped. Default: cheap fast tier for routing and reporting, mid tier for drafting, a stronger model only on an auditor flag. The project's current template names Haiku 3.5, Gemini Flash 2.0, GPT-4o-mini and Sonnet 4; Backy re-checks current availability and prices at build time. Provider terms for tenant data (no training, retention, EU region) are decided per tenant before go-live.

## 12. LLMOps and evals
- Metrics: cost per conversation, escalation rate, approval acceptance/edit/reject rates, unverified-citation rate, top unhandled intents, skill hit rate.
- Golden sets in Italian: 50 research questions with verified citations; 30 agenda scenarios (0 missed conflicts); 20 contract clauses per playbook; injection tests; cross-tenant leak tests.
- Gate tests run before any plug-in version bump.

## 13. Source register (live check 2026-10-30)
Classes: USE-CODE = fork, pin, integrate. USE-DATA = ingest. PATTERN = read and copy ideas only. INFO = context only. AVOID = do not use.
| Class | Source | Live | Key facts |
|---|---|---|---|
| USE-CODE | github.com/capazme/mcp-legal-it | OK | Apache-2.0; 228 tools, 23 skills, 5 agents; 28 stars, 507 commits; Docker serves Streamable HTTP on :8000/mcp; profiles incl. `normativa`, `calcoli`; not supported in Cowork cloud |
| USE-CODE | github.com/Open-Source-Legal/OpenContracts | OK | MIT; 1.5k stars, 13,089 commits; GraphQL/REST + MCP; Docling parser; US examples; change default admin password; telemetry on by default |
| USE-CODE | github.com/langchain-ai/langgraph and docs.langchain.com/oss/python/langgraph/interrupts | OK | 44.1k stars; interrupt/resume rules as in section 8 |
| USE-DATA | github.com/ahmeabd/italia-corpus | OK | Script MIT; data public domain (art. 5); >280,000 acts; daily updates; 450 stars |
| USE-DATA | huggingface.co/datasets/dossier-legal/italian-legal-corpus | OK | CC-BY-4.0 (attribution); 366k rows: Normattiva, Corte Costituzionale ~18K, OpenGA metadata ~100K, EUR-Lex ~50K; OpenGA rows are short metadata, not full judgments |
| PATTERN | github.com/anthropics/claude-for-legal | OK | Apache-2.0; 9.8k stars; agents for intake, docket watcher, escalation, client letters; legal-builder-hub trust layer; US law content |
| PATTERN | github.com/oktopeak/clio-mcp | OK | MIT; 37 tools; per-call audit log; AES-256-GCM tokens; READ_ONLY mode; 26 stars |
| PATTERN | techcommunity.microsoft.com ... word-legal-agent-in-frontier | OK | Microsoft Legal Agent, Frontier program, Word for Windows; deterministic redline layer; closed |
| PATTERN | github.com/Vaquill-AI/ms-word-addin | OK | Apache-2.0; 77 stars; sign-off gate, playbook fallbacks, grounding check; US research |
| CONDITIONAL | github.com/nspady/google-calendar-mcp | OK | MIT; 1.2k stars; free/busy and cross-account conflicts; only if a tenant syncs Google Calendar; use read-only tool filter |
| INFO | github.com/openlegaldata/awesome-legal-data | OK | 324 stars; dataset directory incl. Italian sources; Hermes discovery aid |
| INFO | github.com/topics/normattiva | OK | Other small Italian projects: ondata/normattiva_2_md (22 stars), SimonBerg255/gov-it-legal-mcp (11), casungo/italia-corpus (verified pipeline) |
| INFO | snyk.io ToxicSkills; CSA scanner-bypass note | OK | 3,984 skills: 13.4% critical, 36.82% any issue, 76 malicious; scanners bypassed in June 2026 |
| INFO | github.com/Azure-Samples/ally-legal-assistant | OK | 82 stars; no licence file seen, README says free to use; node_modules.7z committed; Azure-coupled |
| INFO | microsoft.github.io/copilot-studio-gallery ... contract-review-assistant | OK | Labelled "demo submission", community, as-is; contains almost no logic |
| INFO | github.com/Ansvar-Systems/italian-law-mcp | OK | Archived 7 Jul 2026; Apache-2.0; its source-terms table is useful reading; hosted gateway is a data-egress risk |
| INFO | github.com/zavora-ai/mcp-scheduling | OK | Apache-2.0; 1 star; holiday list excludes Italy; sealed approval-state idea is worth reading |
| INFO | harvey.ai | OK | Commercial benchmark only |
| INFO | reddit.com/r/legaltech/comments/1t71ev5 | OK | 14 votes, 20 comments; includes vendor promotion; weak evidence |
| INFO | legalagent.github.io/Legal-Agent-for-Word | OK | Third-party Word add-in with its own billing; unrelated to Microsoft's Legal Agent |
| AVOID | github.com/GoryNickel9/Lexia-Italian-Law-LLM | OK | AGPL-3.0; 1 star |
| AVOID | github.com/yellenlegal/clio-mcp | OK | MIT; 3 stars, 3 commits; single-user by its own notes; exposes direct writes |
| AVOID | Unvetted ClawHub / skills.sh skills; Ansvar hosted gateway | n/a | Supply-chain and data-egress risk |
Not re-fetched this round (verify on first touch): normattiva.it terms, Brocardi, Italgiure, EUIPO eSearch plus / TMview, Trail of Bits post, NVIDIA SkillSpector, snyk mcp-scan repo, "Mike" project (no repo URL found).

## 14. Build order and parallel lanes (priorities, no dates)
Priority labels: P0 first, P1 next, P2 after, P3 last. Items in the same lane run in order; lanes run in parallel.

### P0 - prerequisites (all parallel)
- A. Backy: write down Elisa's actual stack, tables, auth and approval model; correct section 3 assumptions.
- B. Backy (+ collaborator): fork and pin mcp-legal-it, OpenContracts, claude-for-legal; run mcp-scan and manual review; record results.
- C. Olesia + counsel: source-terms review (Normattiva, Brocardi, Italgiure, CeRDEF, TAR/CdS), Italia Corpus and HF corpus attribution, AI-disclosure rules.
- D. Olesia: EUIPO / TMview / UIBM trademark search (mcp-legal-it also has TMview-based `cerca_marchi` tools).

### P1 - spine (order matters)
1. Tenant context and RLS audit (Backy).
2. Tool Gateway with manifest, audit log, egress rules (Backy).
3. Approval Service, Executor and durable checkpointer (Backy). Can start once the approval record schema is frozen.
4. In parallel after the schema freeze: approval inbox, draft/diff viewer, citation viewer (Fronty/Skin, against mocks).

### P2 - capabilities (parallel lanes after P1 steps 1-3)
- Lane crm: read tools, conflict engine, deadline engine, note writer, draft letters/proposals (Backy).
- Lane research: ingest Italia Corpus into the index, run mcp-legal-it in sandbox, Citation Guard (Backy or collaborator).
- Lane contract: OpenContracts spike (keep, trim, or drop), Italian playbooks (lawyer-reviewed), template drafting, deterministic redline (collaborator).
- Lane quality: golden sets, injection tests, cross-tenant tests (collaborator; starts as soon as the first tool exists).
- Lane UI: chat panel, agent status, settings per tenant (Fronty/Skin).

### P3 - hardening
- LLMOps dashboard, cron watchers, cost caps, red-team pass, plug-in update procedure.
- Elisa-s&m research round, then design.

## 15. Soft guardrails for Backy
- Ask before touching billing, auth or RLS policies.
- Do not enable a write-capable plug-in tool; wrap it.
- Prefer small reversible PRs; one plug-in per PR.
- No content in logs. No tenant data in plug-in containers beyond their tenant.
- If a source's licence or terms are unclear, stop and ask Olesia.
- Record every deviation from this document in a short decision log.

## 16. Open questions for Olesia
1. Is the assumed stack (Flask, PostgreSQL with RLS, current host) right, and what does Elisa already have for approvals?
2. Do tenants use Google Calendar or Outlook sync, or only Elisa's native agenda?
3. Is case-law retrieval required at launch, or statutes only until counsel clears the sources?
4. Which Italian practice areas come first for playbooks?
5. Who are the other collaborators Backy will select, and should I add them to the roster section?
