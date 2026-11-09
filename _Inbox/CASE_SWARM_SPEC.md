# CASE SWARM - Specification v0.1 (private use only)
Scope: private case analysis. No statutory retention, PDF/A or evidentiary-format rules applied.
Oversight and control: Admy (CEO) for the test run. Archive only after analysis is complete.

## 1. Principles
1. Originals are never modified. Hash first (SHA-256), then work on copies.
2. Everything is treated as human-made and real unless a clear sign inside says otherwise; then ask the user.
3. Counting is done by script, not by the LLM. The LLM only labels (literal / synonym / ambiguous).
4. Every statement in every deliverable cites source_id + msg_id. No citation = not released.
5. Two independent transcriptions per image/scan; disagreements are listed, never silently resolved.
6. Subagents start with zero context: pass file paths, schemas and constraints explicitly in every task.
7. Privacy: image/chat content goes to cloud models only if the provider's data policy allows it.
   Free endpoints may log prompts. Prefer local OCR/Whisper; use a zero-retention provider for cloud steps.

## 2. Folder layout
case_<name>_<date>/
  00_originals/        (read-only copies + manifest.csv with SHA-256)
  01_sources/          (normalised: png/webp, pdf, txt, audio)
  02_transcripts_A/  02_transcripts_B/  03_merged/
  04_analysis/         (messages.csv, timeline.csv, participants.csv, phrase_counts.csv, emotion_report.md, authenticity_flags.csv)
  05_summary/          (case_summary_vN.md, questions.md)
  06_deliverables/     (negotiation_strategy.md, preliminary_procedure_draft.md, case_structure.md, grill_questions.md, grill_answers.md, evidence_index.csv)
  07_audit/            (audit_report.md, run_log.md)
  08_archive/          (created by Memy only after ANALYSIS COMPLETE)

## 3. Data schema (messages.csv)
msg_id, source_id, source_type (whatsapp|email|scan|photo|audio|other), timestamp, sender, recipient, text_original,
language, translation, transcription_confidence, transcriber_diff (y/n), authenticity_flag, notes

## 4. Workflow (gates in capitals)
P0 INTAKE - Intake Clerk copies files, hashes, assigns source_id, converts to working formats. Prefer WhatsApp "Export chat" over screenshots when available.
P1 TRANSCRIBE - Transcriber A and B read independently (local OCR first; vision model only if needed). Output JSON per source.
P2 STRUCTURE - Structurer merges, lists disagreements, builds messages/timeline/participants.
P3 ANALYSE - Authenticity Checker; Phrase & Emotion Analyst (see section 5).
P4 SUMMARISE + ASK - Summariser drafts; Interviewer asks the user; summary is edited until user says DONE.
   GATE 1 (user): summary approved.
P5 PULL MORE - Scout proposes extra documents seen earlier (Drive/OneDrive/SharePoint, read-only). GATE 2 (user): approve list.
   Approved items go through P0-P4, then Case Builder merges everything into ONE Case and re-runs counts.
P6 DELIVERABLES - Strategist, Drafter produce md files (section 6).
P7 GRILLS - Opponent Red Team writes cross-questions; Defender writes answers; Strategist updates.
P8 AUDIT - Auditor re-checks quotes, recomputes counts, verifies citations. GATE 3 (Admy): release.
P9 ANALYSIS COMPLETE (user types it) -> Memy archives (section 7).

## 5. Phrase and emotion counting (explicit method)
- Unit: per participant, per file, and overall.
- LITERAL: identical normalised phrase (lowercase, punctuation stripped), n-grams 1-5, minimum 2 occurrences. Counted by script.
- SYNONYM: phrases grouped into a named cluster (e.g. "apology: sorry / my bad / forgive me"). Cluster members are listed in the report; counted by script from the listed members.
- AMBIGUOUS: phrases that could mean two things (sarcasm, irony, cultural idiom, emoji-only). NOT counted in totals; listed with possible readings and a question to the user.
- Report columns: participant, file, cluster, type (literal|synonym|ambiguous), count, msg_ids.
- Emotions are reported as "expressed wording", never as a diagnosis of what a person felt.

## 6. Deliverables
1. negotiation_strategy.md - one section per opponent representative (A, B, C, D): interests, likely positions, leverage, concessions, sequence, red lines, phrasing to use/avoid. Each point cites evidence.
2. preliminary_procedure_draft.md - draft of the preliminary procedure.
3. case_structure.md - facts, timeline, parties, claims, evidence map, gaps.
4. grill_questions.md + grill_answers.md - opponent cross-questions with prepared answers and the evidence backing each.
5. Supporting: messages.csv, timeline.csv, phrase_counts.csv, evidence_index.csv; optional DOCX/PDF exported from md.
Note: drafts for a real legal procedure should be reviewed by a qualified lawyer before use.

## 7. Memy as Archivist (only after ANALYSIS COMPLETE)
1. Verify 00_originals hashes still match manifest.csv.
2. Store originals losslessly (restic repo or tar.zst --ultra -22) + par2 if > 100 MB.
3. Create derivatives: WebP (lossy q60-80, ~80-89% smaller) for images, optimised PDF, Opus audio.
4. Never delete originals without the typed phrase CONFIRM DELETE.
5. Write archive_index.md (what, where, hash, restore command). Report space saved.
Tool: memy_archiver.py (scan / preview / commit gates apply).

## 8. Hermes configuration sketch
delegation:
  max_concurrent_children: 4
  max_spawn_depth: 2          # Orchestrator -> workers
  model: ""                   # set a cheaper model for workers if desired
Use one Hermes profile per role that needs different credentials/tools (profile_routes). Kanban card per task; assignee = profile.
Default model chain: z-ai/glm-5.2:free -> nvidia/nemotron-3.5-lightning:free -> minimax/minimax-m3:free.
Vision-capable model or local OCR is required for Transcribers (the free text-only chain cannot read images).

## 9. Tests before using the real case
T1 Synthetic case: 5 invented chat screenshots with a known number of repeated phrases. Pass = counts match exactly.
T2 Disagreement test: one deliberately blurred image. Pass = flagged, not guessed.
T3 AI-sign test: one file containing an obvious AI disclaimer. Pass = agent asks the user.
T4 Citation test: Auditor must reject a summary sentence with no msg_id.
T5 Archive test: restore one file from the archive; SHA-256 equals manifest.
T6 Pull-more gate: Scout must not pull anything before approval.
Then run on the real case with Admy supervising.
