---
title: DevOps Platform Audits
created: 2026-10-29
tags: [devops, audit, cron, automation]
status: active
---

# DevOps Platform Audits

**Owner:** memory-curator · **Schedule:** Weekly (Sun 18:30) · **Deliver:** Telegram

Routine audits of all active DevOps platforms to catch stale configs, expired tokens, unused services, and cost spikes before they become incidents.

## Platforms in scope

| Platform | What to audit | Key signals |
|---|---|---|
| **Railway** | Project count, usage, env vars, deploy status | Orphaned projects, 500 errors, bank budget |

### Railway pricing reference (Hobby)

| Resource | Rate | Notes |
|---|---|---|
| RAM | $10 / GB-month | Primary overage risk; idle services still consume |
| CPU | $20 / vCPU-month | Charged on actual consumption over time |
| Persistent volume | $0.15 / GB-month | ~2–3% metadata overhead per volume |
| Network egress | $0.05 / GB | Inbound is free; public DB traffic creates egress |
| Hobby subscription | $5 / month | Includes $5 usage; shared at workspace billing level |

**CLI:** `railway usage` · `railway usage projects` · `railway usage limit status`

**Decision thresholds:** ≤$4 low / $4–$5 medium / >$5 high / sudden rise high.

| **Netlify** | Site count, build minutes, bandwidth | Inactive sites, build failures, domain TLS |
| **Cloudflare Pages** | Project count, build config, branch deploys | Stale branches, failed deploys |
| **GitHub** | Repo count, Actions minutes, Packages storage | Orphaned repos, stale secrets, rate-limit |
| **Vercel** | Deployment count, edge bandwidth, env vars | Inactive deployments, env drift |
| **OpenRouter / LLM providers** | API keys, credit balance, rate limits | Low balance, expired keys, provider fallback history |

## Audit checklist

1. **Inventory** — list all active projects/services; compare against last week's baseline.
2. **Health** — check API/health endpoints; flag non-200 or timeout.
3. **Credentials** — rotate any token older than 90 days or with no expiry set.
4. **Cost** — compare current spend vs last 7-day baseline; flag >20% spike.
5. **Stale** — mark any service/project with no deploy/update in 30 days for review.
6. **Docs** — update the per-platform status line in this note after each run.

## Output format

Append a dated entry to this note:

```markdown
## YYYY-MM-DD

- **Railway:** N projects, $X spend, status
- **Netlify:** N sites, build min, status
- **Cloudflare Pages:** N projects, status
- **GitHub:** N repos, Actions min, status
- **LLM providers:** credit balance, status
- **Summary:** clean / flags / actions needed
```

## Failure handling

If a platform's API is unreachable, do not silently skip — mark it `UNREACHABLE` and retry next run. If the same platform is unreachable 3× in a row, escalate to Ole with a Telegram alert.

## Links

- Parent: [[dev-ops-INDEX]]
- Related: [[self-improvement-log]] (weekly audit pairs with the Sunday self-improvement report)
- Related: [[Memory-Architecture-2026-10-29-Obsidian-first-Hindsight-Standby]] (Hindsight standby policy — audits stay in Obsidian, not Hindsight)
