# Lexflow + Elisa: workflow comparison, MVP approach and architecture
Version 1 | 17 November 2026 | For you and your lawyers' brainstorm
Diagram: `lexflow_architecture.png` (same folder). Time and effort figures are my estimates unless a source is linked.

## 1. Four lawyer workflows compared with yours
Assumption: "law + ChatGPT" means a legal database or traditional research plus ChatGPT. Correct me if it means something else.

| | Lawyer 1: Claude Cowork + Lexroom | Lawyer 2: legal database + ChatGPT | Lawyer 3: Lexroom only | Lawyer 4: CRM (Lexflow, if adopted) | Your workflow with me |
|---|---|---|---|---|---|
| Role of the AI | Cowork: contract review, drafting, `/review-contract` against a playbook ([plugin](https://claude.com/marketplace/plugins/legal)); Lexroom: Italian sources | General drafting and summaries | Research, document analysis, drafting, private library ([Lexroom](https://www.lexroom.ai/)) | Matter state, deadlines, tasks; Elisa as operator and guide | Research, analysis, ledgers, versioned files |
| Record of the matter | Folders plus Lexroom "fascicolo"; no single record | Folders and email | Lexroom fascicolo | CRM database | Facts ledger and status file |
| Glue between tools | Copy and paste, human | Copy and paste | None needed | MCP and API | You, between threads |
| Data exposure | Two clouds | Text goes to the chat service; pseudonymisation advised ([guide](https://www.qualityandsafety.org/guide/chatgpt-per-avvocati)) | One vendor; no training on your documents; ISO 27001 claimed by vendor | Your infrastructure plus the model provider | Perplexity plus any connected storage |
| Strength | Best drafting and Italian sources | Cheap, flexible | One place for research and drafting | Deadlines, tasks, client status, audit | Source discipline, tags, critique |
| Weak point | Two stores of facts; Art. 13 disclosure covers both | Confidentiality; no case state | No evidence found of deadlines, billing or PA task management (unverified) | Does not replace research or drafting tools | Not a system a firm can run; one person's discipline |

Facts behind the table:
- Lexroom: Italian research with cited sources, document analysis, drafting, private library, Word add-in, GDPR and ISO 27001 stated by the vendor, packages from EUR 99 per month per user excluding VAT with annual contract ([Lexroom](https://www.lexroom.ai/); [Pescara bar presentation](https://www.ordineavvocatipescara.it/wp-content/uploads/2025/10/lexroom-ai.pdf)).
- Claude: Legal plugin for Cowork, playbook-based review with green, yellow and red flags, connectors through MCP, outputs to be reviewed by licensed attorneys ([Claude](https://claude.com/marketplace/plugins/legal)); custom connectors can be added by pasting an MCP address ([Bind guide](https://bindlegal.com/resources/guides/claude-for-legal/)).
- Law: Art. 13 of L. 132/2025, in force since 10 October 2025, requires the lawyer to tell the client which AI systems are used, in clear language, and limits AI to supporting activities ([Ordine degli Avvocati di Firenze](https://www.ordineavvocatifirenze.eu/2025/10/intelligenza-artificiale-legge-23-settembre-2025-n-132/)).

### What the comparison tells you
1. **Do not build what Lexroom already sells.** Research, drafting and a private library exist and cost from EUR 99 per month. Competing there loses.
2. **Lexroom's "fascicolo" overlaps with a CRM's matter record.** Lexflow must differ on what a research tool lacks: deadlines, task ownership for the PA, client status, intake, communications log, billing, and an AI-use register.
3. **The gap in all four workflows is the system of record.** Facts live in folders, chats and heads. That is the opening for Lexflow.
4. **Compliance is a feature.** Art. 13 creates a duty that today sits in each lawyer's letter of engagement. A client-facing AI disclosure and an AI-use log per matter is a concrete, sellable function.

## 2. How to approach the matter
### Step 1: observe before building (2 weeks)
Ask each lawyer for a 45-minute working-session walk-through of one real, closed matter. Capture:
- where the matter starts and what is written down;
- where deadlines live and who updates them;
- every copy-and-paste between tools;
- which tool holds the "truth" about the client;
- what they refuse to put in any cloud;
- who is the PA, and what the PA does that the lawyer would delegate to software;
- how they currently meet the Art. 13 duty.

Record answers in a table: task, tool, frequency, minutes, pain (1-5). The top three pains by frequency × minutes define the MVP.

### Step 2: pick one wedge
Candidate: "matter cockpit" = one screen per matter with parties, state, next deadline, open tasks, document index, AI-use log. Elisa answers "what is open on matter X?" and creates tasks and deadlines on request.

### Step 3: freeze the MVP (decisions that stop rework)
| Decision | Freeze now | Reason |
|---|---|---|
| Where Elisa lives | Separate service next to the app on Railway (section 4) | Long-running work stays out of the web process |
| Tool contract | One tool layer (REST plus MCP) | Any AI system can connect through it |
| Write policy | Elisa proposes, a human confirms | Liability and trust |
| Model access | One abstraction layer, provider switchable | Avoid lock-in; EU-region choice |
| Data | Masked store: no ID scans, no account numbers | Confidentiality |
| Scope | List in section 3 | Prevents drift |
| Pilot | One lawyer, one PA, four weeks | Real feedback |

### Step 4: pilot and kill criteria
Run one real matter in parallel with the old method for four weeks. Stop or re-scope if, after four weeks: the lawyer opens the app fewer than 3 times a week; deadlines are still tracked elsewhere; or Elisa's confirmed actions are fewer than 5 a week.

## 3. What Elisa does at MVP
| Tier | Capability | Policy |
|---|---|---|
| 0 | Guide: explains the app, where to click, what a field means (answers from the product help) | Free |
| 1 | Read: "open tasks for matter X", "deadlines this week", search contacts and notes | Free, logged |
| 2 | Propose: drafts a task, deadline, note, matter summary | Shown to the user |
| 3 | Write: creates or updates records | Only after human confirmation |
| 4 | Scheduled: daily digest of deadlines and overdue tasks | Notification only |
Out of scope for MVP: legal research, drafting of court acts, sending emails on its own, e-filing, anything that decides.

CRM core: clients and parties, matters, deadlines and reminders, tasks with owners (lawyer or PA), document index with links, notes and time log, engagement-letter template with the Art. 13 AI disclosure, audit log.

## 4. Where Elisa lives
| Option | How | Strengths | Weaknesses | Verdict |
|---|---|---|---|---|
| A. Inside Flask | Agent code in the web app | Simplest deploy | Long model calls block web workers; one crash takes both; harder to scale or secure | Reject |
| B. Separate service on Railway | Second service in the same project, same repo, shared Postgres, talks to the app through the tool layer | Python end to end; isolation; Railway supports workers and Postgres in one project ([Railway Flask guide](https://railway.com/deploy/flask-python-starter)); cost for a small stack about $10-30 per month ([Railway guide](https://railway.com/guides/estimate-ai-agent-costs)) | You run and monitor it | Recommended |
| C. Cloudflare Workers | Agent as a Durable Object per user or matter, with its own SQLite, scheduling and MCP client ([Cloudflare Agents](https://developers.cloudflare.com/agents/)); near-zero cost when idle ([repository](https://github.com/cloudflare/agents/blob/main/docs/agents/index.md)) | Per-user isolation; cheap at rest; edge | TypeScript SDK; second platform; Durable Objects need Workers ([session](https://www.cloudflare.com/connect/2026/session/building-durable-agents-with-durable-objects/)); data split between Cloudflare and your Postgres | Later, if per-user agents at scale are needed |

Rule: build Elisa behind the tool layer. If she later moves to Cloudflare, only the host changes; the contract stays.

### Cost sketch (my estimate, check at purchase)
- Railway Hobby: $5 per month with $5 usage included; an always-on worker about $4; a stack with Postgres and bucket $10-30 ([Railway pricing](https://railway.com/pricing); [guide](https://railway.com/guides/estimate-ai-agent-costs)).
- Model tokens: the largest and least predictable line. Railway's own worked example, at $3 and $15 per million input and output tokens, comes to about $0.40 per run, so cap runs per user per day.

## 5. Interoperability with the lawyers' tools
| Their tool | Route | Status |
|---|---|---|
| Claude Cowork | Lexflow tool layer as a custom MCP connector | Feasible; confirm the plan allows custom connectors |
| ChatGPT | Connector if supported; otherwise exported matter summaries | To verify |
| Perplexity | Connectors or exported files | To verify |
| Lexroom | No public API found; file export, Word add-in, copy of matter summary | To ask Lexroom |
| Word, Outlook, Drive | Links and attachments in the document index | Feasible |
Pitfall: a lawyer who has only a "Project" in Cowork or ChatGPT has no PA tool to connect to. For them the MCP connector is the product; the CRM UI is optional.

## 6. Risks and mitigations
| Risk | Consequence | Mitigation |
|---|---|---|
| Building before observing | Wrong product | Step 1 first |
| Scope creep into research and drafting | Competing with Lexroom | Section 3 out-of-scope list in the product brief |
| Elisa writes wrong data | Missed deadline | Approval gate, audit log, undo, digest of changes |
| Client data in prompts | Confidentiality breach | Masked store; provider with data agreement; log what is sent |
| Missing client disclosure | Breach of Art. 13 | AI-use register and disclosure template inside the matter |
| Lawyers mistrust a founder building on their cases | Relationship damage | Keep product research separate from your own matter; say so openly |
| Rework loops | No MVP | Freeze table in section 2; change only after the pilot |
| Cross-platform sprawl | Cost and security gaps | One tool layer; one host for MVP |

## 7. Message to the lawyer (Italian)
Your text: "salve. to follow up our previous meeting mi piacerebbe sapere il tuo workflow sul caso. fammi sapere quando e dove serebbe comodo per te."

Corrections: "serebbe" becomes "sarebbe"; mixed English and Italian becomes Italian; "il tuo workflow" becomes "come intende organizzare il lavoro". Use "Lei" if you are not on first-name terms.

**Formal**
> Buongiorno Avvocato [Cognome],
> facendo seguito al nostro precedente incontro, vorrei capire come intende organizzare il lavoro sul caso: strumenti, fasi, tempi e modalità di condivisione dei documenti. Mi faccia sapere quando e dove le sarebbe comodo incontrarci.
> Cordiali saluti,
> [Nome]

**Informal**
> Ciao [Nome],
> per dare seguito al nostro incontro, mi piacerebbe sapere come organizzi il lavoro sul caso: strumenti, fasi, tempi e condivisione dei documenti. Dimmi quando e dove ti farebbe comodo vederci.
> A presto,
> [Nome]

**Version with the AI duty** (add one sentence)
> Vorrei inoltre sapere quali strumenti di intelligenza artificiale, se presenti, vengono utilizzati nella gestione del mio caso, come previsto dall'art. 13 della L. 132/2025.

Keep your Lexflow questions out of this message. Ask them in a separate message or meeting so the case and the product research stay separate.
