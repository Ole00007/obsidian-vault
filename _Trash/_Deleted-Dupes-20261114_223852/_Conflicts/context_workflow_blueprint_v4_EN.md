# Blueprint v4: persistent context across threads, projects, devices and agents
Version 4 | 13 November 2026 | Tools: Perplexity Projects, Claude Cowork, Claude Code, Obsidian, Hindsight, Hermes Agent
Shared for lawyer brainstorm. Contains no client data.

## 1. Rule of precedence
Reliability falls in this order: 1) project instructions you wrote; 2) files you maintain (the facts ledger wins over any memory); 3) automatic memory (Claude, Hindsight); 4) earlier chat text. Put every critical fact in layers 1-2.

## 2. What persists
| Layer | Perplexity Projects | Claude Cowork | Main failure |
|---|---|---|---|
| Instructions | Up to 8,000 characters per project ([Help Center](https://www.perplexity.ai/help-center/en/articles/10352961-what-are-projects)) | Project plus global instructions ([Anthropic Academy](https://academy.claude.com/courses/introduction-to-claude-cowork/giving-cowork-context)) | Too long, contradictory, outdated |
| Files | Persistent project file system ([Perplexity](https://www.perplexity.ai/hub/products/projects)) | Folders on your computer, mounted per session | Stale file, wrong version, never saved to the project |
| Memory | Project memory ("Brain"); personal Memory also applies when on ([Memory](https://www.perplexity.ai/help-center/en/articles/10968016-memory)) | Automatic, scoped to the project; shared with chats outside projects unless "Use account memory" is off | Wrong, stale or leaked detail |
| Thread text | Not carried to new threads | Not carried to new tasks | Lost decisions, repeated questions |

### Claude Cowork: where data lives
- The [support page](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork) (updated 12 November 2026) says new projects are saved to your Claude account: name, description, instructions, Google Drive links, a copy of project memory. Folders and files stay on your computer.
- The [docs page](https://claude.com/docs/cowork/guide/projects) says projects live on your computer and are not synced. Treat it as superseded for Pro, Max and Ultra.
- Team and Enterprise without "Chat and Cowork unified": projects created from an existing folder stay on that computer only.
- Result: instructions and memory follow the account. Files follow only the folder you chose.

## 3. Where to put the project folder
You choose the folder per project; no global default exists in the pages I found. Cowork works with a local path, so any location the computer sees as a folder works.

| Option | Cowork | Second device | Cost | Security | Pitfall |
|---|---|---|---|---|---|
| Plain local folder | Yes | No | 0 | Disk encryption only | Single point of failure |
| Obsidian vault + Obsidian Sync | Yes | Other computer or phone (Obsidian app) | $4/month annual, $5 monthly (Standard) | End-to-end encrypted (AES-256) | Standard: 1 vault, 1 GB, 5 MB per file |
| Vault in iCloud Drive | Yes | Apple devices | Included in iCloud plan | Apple-managed keys | Problems reported on Windows |
| Vault in Google Drive or OneDrive (desktop client) | Yes | Yes | Free tier | Provider-managed keys | Sync conflicts |
| Syncthing | Yes | Computers, Android | Free | Device to device | No official iOS app |
| Drive or Microsoft 365 connector | Read and search only by default | Yes | Plan cost | Provider terms | Cannot be the working folder |

Sources: [Claude Academy](https://academy.claude.com/courses/introduction-to-claude-cowork/getting-set-up); [Obsidian pricing](https://obsidian.md/pricing.html); [Standard plan limits](https://obsidian.md/blog/standard-plan/); [sync comparison](https://ob-lite.app/guide/en/obsidian-sync-alternatives).

Verdict: fastest = vault folder picked at project creation; cheapest = local folder or Syncthing (0), managed = Obsidian Sync Standard; best security = Obsidian Sync (end-to-end) or local-only vault. End-to-end encryption protects files at rest and between devices; text that Claude reads is processed under Anthropic's terms. Prices are USD as published; confirm the euro amount at checkout.

## 4. Second-device scenarios
Principle: Claude Cowork on a phone or the web cannot open a local folder ([Claude Academy](https://academy.claude.com/courses/introduction-to-claude-cowork/getting-set-up)). Files travel only through the sync layer (Obsidian Sync). Instructions and Claude memory travel through the account. A Hermes agent is a different product: it does not read Cowork's project record or Claude memory.

| Scenario | Files | Instructions | Memory | Verdict |
|---|---|---|---|---|
| A. Second PC with Claude Desktop, same account | Obsidian Sync mirrors the vault | Account | Account | Full parity after sync completes |
| B. Phone, Obsidian app only | Read and edit notes | None | None | Reading and capture only |
| C. Phone, Telegram to a Hermes agent | Only if the agent host sees the vault | Hermes config (separate) | Hindsight bank if you connect both | Works; the vault is the only shared record |
| D. Phone, Claude app or web | Not the local folder | Account | Account | Connectors only |
| E. Other chat front end (for example Lexflow) | Same rule as C: depends on what the host behind it can read | Own config | Own | Not researched; I found no documentation for "Elis Lexflow" |

### Test A: second PC
1. PC1: create the vault, enable Obsidian Sync (end-to-end password stored in a password manager), create a Cowork project on that folder, save `test_A.md`.
2. PC2: install Obsidian and Claude Desktop, sign in to both accounts, open the same synced vault.
3. Check in order: `test_A.md` present; project and instructions visible in Cowork; open the project on the vault folder and ask: "Read test_A.md and quote line 1."
4. Pass: all three work. Fail on file: sync not finished or wrong vault. Fail on project: wrong account or plan setting.
5. Edit on one PC at a time; wait for sync to finish before switching.

### Test C: phone via Telegram and Hermes
1. Decide where Hermes runs. Hermes runs on a cloud VM or your own machine, and the gateway serves Telegram, Discord, Slack, WhatsApp, Signal ([Hermes repository](https://github.com/nousresearch/hermes-agent)). It can read the vault only if the host has the vault folder. Unverified options: run Hermes on a PC that holds the synced vault; or give the container a private git clone of the vault.
2. Restrict access: set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_ALLOWED_USERS` to your own ID only ([Hermes Telegram docs](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram)).
3. Send: "Read test_A.md and quote line 1." Pass: correct quote. Fail: the agent cannot see the vault; fix the host, not the prompt.
4. Send a fact the agent should retain, then start a new Telegram chat and ask for it. Pass only if the memory layer works.
5. Keep the vault read-only for the agent until the test passes (risk 20).

## 5. Hindsight: your private deployment
Your setup: backend only, cloned from your private GitHub repo, deployed on Railway, mode local external. Corrections to my earlier text, and what the sources say:
- **"Flags"** means the command-line options `--server self-hosted --api-url ...` of Vectorize's Claude Code installer. The installer's default mode is `cloud`, which sends sessions to Hindsight Cloud, Vectorize's hosted service ([Starry Hope](https://www.starryhope.com/ai/hindsight-memory-for-coding-agents/)). They matter only if you run that installer. Your own Railway server is not Vectorize's service. Your own configuration overrides the default; check `serverMode` and `apiUrl` in `~/.hindsight/coding-agent.json` on each machine.
- **LLM key.** The Hindsight Railway template ships with the LLM provider set to `none`, so Hindsight runs as a semantic store on bundled local models; a provider and key are needed only for fact extraction, reflect and consolidation ([Railway template](https://railway.com/deploy/hindsight--hindsight-memory-api)). My earlier statement that you must supply a key was true only for those features. Your instance may differ; check the Railway variables.
- **MCP.** The same template requires the API key "on every REST and MCP request", and the installer registers an MCP server for Claude Code. If your build removed MCP, say so in the lawyer's notes; otherwise assume it exists.
- **Authentication.** The Starry Hope guide says the API has no login by default and that Hindsight's own `docker run` example publishes ports on every interface. The Railway template enables API-key auth. Confirm yours does.
- **Integration route.** Hindsight attaches to Claude Code through hooks and MCP, and to Hermes through a plugin in `local_external` mode ([Hermes plugin](https://hermes-agent.nousresearch.com/docs/plugins/hindsight)). I found no source stating that Cowork runs Claude Code hooks. Treat the Cowork link as an incremental extension through Claude Code and test it (test D below).

### Why two memories can contradict
Claude memory and Hindsight each extract facts from the same conversations, with different models, rules and timing. Hindsight injects its recall into the first prompt of a session. The model then sees both versions. A changed fact (a date, a decision) updates in one store and stays stale in the other. A Hindsight fact can be edited or invalidated but not deleted (issue #3509, per [Starry Hope](https://www.starryhope.com/ai/hindsight-memory-for-coding-agents/)). Obsidian adds a third version. Mitigation: the facts ledger is the record; instruct "if memory and ledger differ, the ledger wins and the difference is reported."

### Test D: Hindsight bridge
1. Create a bank named for the matter. From Claude Code (or the Hermes plugin), retain a fake fact: "Test fact: project colour is green."
2. From the other agent, ask for the project colour.
3. Change the fact in the ledger to "blue"; ask again. Pass: the answer reports the conflict or follows the ledger. Fail: it states "green" without warning; tighten the instruction.

## 6. Risks, pitfalls, mitigations
| # | Risk | Consequence | Mitigation |
|---|---|---|---|
| 1 | Memory stores a wrong or outdated fact | Errors repeat in every thread | Review memory monthly; delete or invalidate errors; keep each critical fact in the ledger with source and date |
| 2 | User statements and verified facts blend | A lawyer receives an assumption as a finding | Tag every line: `[USER]`, `[VERIFIED + source + date]`, `[ASSUMPTION]`, `[TO VERIFY + who]` |
| 3 | Answered questions get asked again | Time lost; inconsistent answers | "Answered" section in the status file; never re-ask |
| 4 | Instruction bloat | Later rules ignored | Maximum 12 rules; reference text goes into files; re-test after each edit |
| 5 | Conflicting layers (global, project, prompt) | Unpredictable output | State precedence in the instructions |
| 6 | Sensitive data (IDs, bank details, shareholder data) in files, memory or sync | Exposure | Keep originals offline; store masked copies; check sharing and connected sources before uploads |
| 7 | Memory leaks between matters | Facts from matter A shape matter B | One project and one memory bank per matter; switch off account memory for sensitive matters |
| 8 | Unsourced or invented legal propositions | Wrong advice reaches counsel | Provision, date, link, applicability for each; unverified items marked; lawyer signs off |
| 9 | Law changes after verification | Outdated analysis | Date-stamp each verification; recheck before filing |
| 10 | Status file not updated | Next session starts from old facts | Close-session routine (section 8); version suffix; compare files before saving |
| 11 | Generated files stay in the chat | Folder lacks the latest version | Confirm the file appears in the project folder after each session |
| 12 | Confident tone hides weak evidence | Overtrust | Ask: "What would falsify this? Which claim rests on one source?" |
| 13 | Voice drifts | Texts stop sounding like you | Voice file with three sample paragraphs and banned phrases |
| 14 | Long thread degrades quality | Contradictions | One deliverable per thread; summarise into the status file |
| 15 | Single point of failure | Lost project or product change | Copy the folder monthly to a second location; export the Hindsight database |
| 16 | Sync conflicts when an agent writes during sync | Duplicates or overwrites | One active writer; wait for sync; keep version history on |
| 17 | Two or three memory systems (Claude, Hindsight, Obsidian) | Contradicting facts | Ledger is the record; run the section 5 test D after changes |
| 18 | Hindsight API reachable without login | Anyone with the URL reads or writes memory | Use the template's API-key auth or Railway private networking; no public address; rotate keys |
| 19 | Fact extraction sends text to an LLM provider | Client text leaves your server | Keep provider `none` for client matters, or use a provider with a data-processing agreement; document the choice |
| 20 | Hermes can run shell commands in its container, and so can anyone holding its API key ([Railway template](https://railway.com/deploy/hermes-agent-with-hindsight-memory)) | Remote command execution on the host that holds the vault | Allow only your Telegram ID; keep API keys private; mount the vault read-only; no secrets on that host |
| 21 | Telegram as a channel for client content | Messages sit on a third-party platform (confirm Bot API encryption terms) | Send commands and file names, not client facts |
| 22 | No access control by team, agent or memory in Hindsight (open issue #2235, per Starry Hope) | A shared server exposes every bank to every connected agent | One server or key per client; never mix lawyer and your own matters |
| 23 | Cowork may not run Claude Code hooks | The memory bridge silently does nothing | Run test D; read the integration logs in `~/.hindsight/coding-agents-logs/` |
| 24 | Token and hosting costs grow with sessions (first-prompt reflect was the largest share in the guide's test) | Unplanned bills | With provider `none`, cost is hosting only; with a provider, check the LLM Requests tab after a day and cap spend |
| 25 | Wrong lawyer-side assumptions about your setup | Brainstorm built on false premises | Share this file with the "corrections" in section 5 intact |

## 7. Growing the assistant
Every correction becomes a rule or a file entry; otherwise the error returns.
1. **Error log** (`04_ERROR_LOG.md`): what was wrong, correction, new rule.
2. **Promotion:** a correction repeated twice moves into the instructions; rules unused for 60 days leave.
3. **Gold examples:** two approved outputs; instruct "match structure and density."
4. **Regression prompts:** three fixed test prompts (fact check, legal-source check, summary) run after each instruction edit.
5. **Weekly metrics:** re-asked questions, unverified claims, corrections per deliverable; each must fall.
6. **Explicit goals:** goal, deliverable, audience, deadline at every session start.

## 8. Files, prompts, instructions
| File | Content |
|---|---|
| `00_STATUS.md` | State, decisions, answered and open questions, next steps |
| `01_FACTS_LEDGER.md` | One row per fact: statement, tag, source, date |
| `02_SOURCES.md` | Links to provisions and documents, retrieval date |
| `03_VOICE.md` | Tone rules, banned phrases, three sample paragraphs |
| `04_ERROR_LOG.md` | Corrections and rules |
| `05_SESSION_LOG.md` | Date, goal, output, improvements |

**Open session**
```
Read 00_STATUS.md and 01_FACTS_LEDGER.md. Goal today: [x]. Deliverable: [x]. Audience: [x]. List the facts you rely on and the gaps that block the goal. Ask only questions the files do not answer. If recalled memory differs from the ledger, report it and follow the ledger.
```
**Close session**
```
Close session. 1) List new facts and decisions with tags. 2) Output the full updated 00_STATUS.md. 3) Add rows to 01_FACTS_LEDGER.md and 04_ERROR_LOG.md. 4) List three claims that rest on one source or on my statement. 5) Give three improvements to my prompts or instructions, ranked by effect.
```
**Project instructions (about 1,800 characters)**
```
ROLE: Research assistant for [matter]. Audience: [self / lawyer].
VOICE: English. Direct. Short paragraphs. Tables for comparisons. No filler words, no closing summary that repeats the body.
PRECEDENCE: These instructions override global instructions. The facts ledger overrides any memory. An explicit prompt overrides these for that task only.
START: Read 00_STATUS.md and 01_FACTS_LEDGER.md. Never re-ask a question listed as answered.
TAGS: Mark every fact [USER], [VERIFIED + source + date], [ASSUMPTION] or [TO VERIFY + who].
LAW: Each legal proposition states provision, date, source link and applicability. Mark unverified items. State where sources conflict.
CRITIQUE: Name risks, weak evidence and single-source claims. Offer a counter-argument.
PRIVACY: Mask ID numbers, bank details and account numbers in all outputs.
OUTPUT: Provide files as Markdown with a version suffix.
CLOSE: On "close session" run the close-session routine.
```

## 9. Limits
- The assistant acts only inside a session; the review after a session happens only on request.
- It cannot audit its own memory; you must read and prune it.
- Plans, prices and features change; recheck vendor pages quarterly.
- Hermes, Hindsight and Lexflow statements rest on public documentation and your description; your deployment was not inspected.
- Legal output supports a lawyer's work; it does not replace verification by counsel.
