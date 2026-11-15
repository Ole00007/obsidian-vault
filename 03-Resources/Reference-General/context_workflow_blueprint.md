# Blueprint: keeping context across threads, projects and sessions
Perplexity Projects and Claude Cowork | 13 November 2026

## 1. Short answer
Saying "remember this in the project" helps only partly. Durable context lives in three places: project instructions, project files, and project memory. Instructions and files are reliable because you control them. Memory is automatic and cannot be fully trusted.

## 2. What each tool actually keeps
| Layer | Perplexity Projects | Claude Cowork |
|---|---|---|
| Standing instructions | Up to 8,000 characters, applied to every query in the project | Per-project instructions; plus global instructions for every session |
| Files | Persistent files and folders, shared across tasks | Project folders mounted for each session |
| Memory | "Brain" builds ongoing memory for the project; personal Memory is also drawn on when on | Project memory is automatic; stays inside the project; shares with chats outside projects unless "Use account memory" is switched off |
| Conversation history | Not carried between threads | Not carried between tasks except via memory |
| Scope | Per project | Per project; global instructions apply everywhere |
Caveat: Claude's help pages disagree on whether Cowork projects sync to the cloud or live on your computer. Check in your own app.

## 3. The workflow that works
1. **Instructions say how to work.** Voice, structure, language, verification rules, what to avoid.
2. **Files say what is known.** Keep one `00_MATTER_STATUS.md` per project: facts, decisions, open questions, next steps. Update it at the end of each session.
3. **Threads are disposable.** Start a new thread when one gets long or confused; the project carries over.
4. **Close every session.** Type "close session". The assistant writes a handoff and a short improvement review.

## 4. Paste-ready project instructions (under 8,000 characters)
```
ROLE: Research assistant for [matter]. Audience: [lawyer/self].
VOICE: Plain, direct, English; short paragraphs; tables for comparisons.
RULES:
- Separate facts you provided from facts verified by sources. Never mix them.
- Do not re-ask questions answered in the status file.
- Cite a source for every legal proposition: provision, date, applicability.
- Mark unverified items "To be verified" and say who can verify them.
- Mask personal identifiers and bank details in outputs.
FILES: Read 00_MATTER_STATUS.md first in every session.
CLOSE-SESSION: When I type "close session":
 1. List what changed today (facts, decisions).
 2. Update 00_MATTER_STATUS.md (output the full new file).
 3. List open questions and next steps.
 4. Give three improvements to my workflow or prompts.
```

## 5. Status file template
```
# 00_MATTER_STATUS
Last updated:
## Settled facts (with source)
## Assumptions
## Decisions taken
## Open questions / to be verified
## Next steps
## Files in this project
```

## 6. Using it across projects
- Put your personal voice and habits in the global layer: Perplexity personal Memory and personalization; Claude global instructions.
- Put matter-specific facts only in the project. Projects do not share memory with each other, which is useful for confidentiality.
- Keep a short `ME_VOICE_AND_METHOD.md` that you paste or upload into each new project.

## 7. Limits to expect
- The assistant cannot watch your sessions on its own; the end-of-session review happens only when you ask for it.
- Automatic memory may store wrong or stale details. Review it regularly and delete errors.
- Sensitive documents (IDs, bank data) should not live in shared projects.
