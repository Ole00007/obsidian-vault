# LexFlow Eliza Cross-Test — 2026-10-25

Independent QA of the in-app Eliza agent on the wave2-agent worktree.

Result: NO-GO.

What was verified
- Auth and flag-off gating behaved as expected for the tested routes.
- Tenancy checks blocked cross-user approvals.
- No tool execution happened before approval.
- Prompt-injection text stayed inert in chat output.
- SSRF header was ignored on /api/agent/chat.
- Rate limiting and message-length guards worked.

Findings
- MAJOR: malformed and past dates are accepted instead of being rejected or clarified.
- MINOR: malformed bearer tokens return a raw 422 JWT parser error.

Report file
- /Users/olesiarasing/.hermes/profiles/backend-dev/cache/scratch/report_tester_eliza.md

## Links
- Parent: [[LexFlow-CRM-Architecture]]
- Related: [[AGENT_RULES]]
- Related: [[LexFlow-Eliza-InApp-Agent-2026-10-25]]
