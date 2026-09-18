
# Amendments for Hermes Global Rules

Add the following rules to the shared Hermes MD used by all agents.

## New shared rules for scheduled reporting
1. Any cron or scheduled agent must operate from an explicit source allowlist.
2. No cron agent may access Memory Curator stores, files, prompts, or sync jobs unless you explicitly approve it in writing.
3. Cron agents are read-only by default.
4. Cron agents may write only to their own report directory, delivery channel, or approved status artifact.
5. Cron agents must separate observations from interpretations.
6. Cron agents must include these headings in every report: Successes, Failures, Obstacles, Risks, Outstanding Tasks, Recommended Follow-ups.
7. Cron agents must include source provenance for every material claim.
8. Cron agents must not silently suppress repeated failures; they may deduplicate them, but must keep counts and first/last seen timestamps.
9. Cron agents must not send external emails, modify CRM data, merge code, deploy code, or alter infrastructure.
10. If a cron agent detects high-severity risk, it may escalate only by notifying you and the approved reviewer channel.

## New visibility rules
11. Agent session visibility is deny-by-default and granted by named source allowlist.
12. If multiple agent logs are visible, the cron agent may summarize them but may not impersonate, continue, or overwrite another agent's work.
13. Memory Curator remains operationally independent and reports separately to you.

## New data handling rules
14. Obsidian access must be read-only unless separately approved.
15. GitHub access for cron jobs must prefer read-only scopes for Actions metadata, run logs, and artifacts.[web:150][web:164][web:168]
16. Secrets, API keys, tokens, personal data, and client-sensitive text must be redacted from reports whenever feasible.
17. If a source is unreachable, the cron agent must report it as a coverage gap, not hallucinate a summary.

## New execution rules
18. Deterministic collection should run before LLM summarization whenever possible.
19. Use no-agent or script-only execution for jobs that do not require interpretation.[web:110]
20. If an LLM is used, the cron job must specify a pinned main model and at least one validated fallback.[web:110][web:141]
21. Model IDs for free providers must be revalidated at install time because free catalogs can change.[web:118][web:121][web:171]
22. Scheduled Cloudflare jobs should use Cron Triggers, and longer multi-step runs may use Workflows.[web:109][web:142]

## Delivery rules
23. Daily delivery should be concise by default.
24. Weekly delivery may include trend comparisons and recurring-failure counts.
25. Every report ends with a one-screen executive digest followed by structured detail.
