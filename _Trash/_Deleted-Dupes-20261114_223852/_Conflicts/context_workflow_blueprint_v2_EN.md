# Blueprint: persistent context across threads, projects and sessions
Version 2 | 13 November 2026 | Tools: Perplexity Projects, Claude Cowork

## 1. Rule of precedence
Reliability falls in this order: 1) project instructions you wrote; 2) project files you maintain; 3) automatic memory; 4) earlier chat text. Put every critical fact in layers 1-2. Treat memory as a convenience, never as the record.

## 2. What persists
| Layer | Perplexity Projects | Claude Cowork | Main failure |
|---|---|---|---|
| Instructions | Up to 8,000 characters per project ([Help Center](https://www.perplexity.ai/help-center/en/articles/10352961-what-are-projects)) | Project instructions plus global instructions ([Anthropic Academy](https://academy.claude.com/courses/introduction-to-claude-cowork/giving-cowork-context)) | Too long, contradictory, outdated |
| Files | Persistent project file system ([Perplexity](https://www.perplexity.ai/hub/products/projects)) | Project folders ([Claude docs](https://claude.com/docs/cowork/guide/projects)) | Stale file, wrong version, file never saved to the project |
| Memory | Project memory ("Brain"); personal Memory also applies when on ([Memory](https://www.perplexity.ai/help-center/en/articles/10968016-memory)) | Automatic, scoped to the project; shared with chats outside projects unless account memory is off ([Claude support](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork)) | Wrong, stale or leaked detail |
| Thread text | Not carried to new threads | Not carried to new tasks | Lost decisions, repeated questions |

Source conflict: Claude's support page describes project data saved to your account; the docs page describes folders on your computer. Test before trusting: create a file, open the project from a second device.

## 3. Risks, pitfalls, mitigations
| # | Risk | Consequence | Mitigation |
|---|---|---|---|
| 1 | Memory stores a wrong or outdated fact | Errors repeat silently in every thread | Review memory monthly; delete errors; keep each critical fact in the facts ledger with source and date |
| 2 | User statements and verified facts blend | A lawyer or counterparty receives an assumption as a finding | Tag every line: `[USER]`, `[VERIFIED + source + date]`, `[ASSUMPTION]`, `[TO VERIFY + who]` |
| 3 | Answered questions get asked again in a new thread | Time lost; inconsistent answers | Keep an "Answered" section in the status file; rule: never re-ask what it lists |
| 4 | Instruction bloat | Later rules ignored; limit reached | Maximum 12 rules; move reference text into files; re-test after each edit |
| 5 | Conflicting layers (global vs project vs prompt) | Unpredictable tone or format | State precedence in the instructions: project overrides global; prompt overrides project only when explicit |
| 6 | Sensitive data in project files (IDs, bank details, shareholder data) | Exposure through sharing, connectors or memory | Keep originals offline; store masked copies; check sharing settings and connected sources before each upload |
| 7 | Memory leaks between matters | Facts from matter A shape matter B | One project per matter; for sensitive matters switch account or personal memory off |
| 8 | Unsourced or hallucinated legal propositions | Wrong advice reaches a lawyer | Rule: each proposition carries provision, date, source link, applicability; unverified items marked; lawyer signs off |
| 9 | Law changes after verification | Outdated analysis | Date-stamp each verification; recheck before filing or negotiating |
| 10 | Status file not updated | Next session starts from old facts | Close-session ritual (section 6); version suffix `_v3`; compare the new file with the old before saving |
| 11 | Generated files stay in the chat | Project lacks the latest version | After each session, confirm the file appears in project Files; keep a local backup |
| 12 | Confident tone hides weak evidence | Overtrust | Ask: "What would falsify this? Which claim rests on one source?" |
| 13 | Voice drifts | Texts stop sounding like you | Keep a voice file with three sample paragraphs and a banned-phrase list |
| 14 | Long thread degrades quality | Contradictions, forgotten rules | One deliverable per thread; summarise into the status file; start a new thread |
| 15 | Single point of failure | Lost project or changed product behaviour | Export the files monthly to your own drive |

## 4. Growing the assistant
Method: every correction becomes a rule or a file entry. Otherwise the same error returns.

1. **Error log.** After each session record: what was wrong, the correction, the new rule. File: `04_ERROR_LOG.md`.
2. **Promotion.** A correction repeated twice moves into the instructions. Rules unused for 60 days leave the instructions.
3. **Gold examples.** Store two finished outputs you approved. Instruct: "Match the structure and density of the gold files."
4. **Regression prompts.** Keep three fixed test prompts (for example: a fact check, a legal-source check, a summary). Run them after editing instructions; compare with previous answers.
5. **Weekly metrics.** Count re-asked questions, unverified claims in deliverables, and corrections per deliverable. Target: each falls week on week.
6. **Explicit goals.** Open every session with goal, deliverable, audience, deadline. The assistant cannot infer priorities.

## 5. File structure per project
| File | Content |
|---|---|
| `00_STATUS.md` | Current state, decisions, answered questions, open questions, next steps |
| `01_FACTS_LEDGER.md` | One row per fact: statement, tag, source, date |
| `02_SOURCES.md` | Links to provisions and documents, retrieval date |
| `03_VOICE.md` | Tone rules, banned phrases, three sample paragraphs |
| `04_ERROR_LOG.md` | Corrections and resulting rules |
| `05_SESSION_LOG.md` | Date, goal, output, improvements |

## 6. Prompts
**Open session**
```
Read 00_STATUS.md and 01_FACTS_LEDGER.md. Goal today: [x]. Deliverable: [x]. Audience: [x]. List the facts you rely on and the gaps that block the goal. Ask only questions the files do not answer.
```
**Close session**
```
Close session. 1) List new facts and decisions with tags. 2) Output the full updated 00_STATUS.md. 3) Add rows to 01_FACTS_LEDGER.md and 04_ERROR_LOG.md. 4) List three claims that rest on one source or on my statement. 5) Give three improvements to my prompts or instructions, ranked by effect.
```

## 7. Paste-ready project instructions (about 1,700 characters)
```
ROLE: Research assistant for [matter]. Audience: [self / lawyer].
VOICE: English. Direct. Short paragraphs. Tables for comparisons. No filler words, no closing summary that repeats the body.
PRECEDENCE: These instructions override global instructions. An explicit prompt overrides them for that task only.
START: Read 00_STATUS.md and 01_FACTS_LEDGER.md. Never re-ask a question listed as answered.
TAGS: Mark every fact [USER], [VERIFIED + source + date], [ASSUMPTION] or [TO VERIFY + who].
LAW: Each legal proposition states provision, date, source link and applicability. Mark unverified items. State where sources conflict.
CRITIQUE: Name risks, weak evidence and single-source claims. Offer a counter-argument.
PRIVACY: Mask ID numbers, bank details and account numbers in all outputs.
OUTPUT: Provide files as Markdown. Name files with a version suffix.
CLOSE: On "close session" run the close-session routine from 06 prompts.
```

## 8. Limits
- The assistant acts only inside a session; the review after a session happens only when you request it.
- It cannot audit its own memory. You must read and prune it.
- Memory features and limits change; recheck the vendor pages quarterly.
- Legal output supports a lawyer's work; it does not replace verification by counsel.
