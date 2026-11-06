---
title: Railway Hobby plan — how much data/GB can we use, what costs money
date: 2026-10-27
author: backend-dev
status: reference (live usage NOT measured — Railway CLI signed out)
tags: [dev-ops, railway, costs, hobby-plan]
---

# Railway Hobby plan — data allowance and what actually costs money
Source: docs.railway.com/pricing/plans and railway.com/pricing (read 2026-10-27). Corrected 2026-10-29 per direct assessment.

## Plan facts
- Hobby = $5/month subscription that INCLUDES $5 of usage. Over $5 total usage in a billing cycle → the extra is billed. Credit resets each cycle, does not roll over.
- Volume storage on Hobby: up to 5 GB (per service/volume). Ephemeral disk: up to 100 GB (wiped on redeploy). Up to 48 GB RAM / 48 vCPU per service (max, billed by use).

## Price per month

| Resource | Price (Hobby plan) | Meaning |
|---|---|---|
| Persistent volume storage | $0.15 / GB-month | 5 GB continuously used ≈ $0.75/month. Railway charges for actual used amount; each volume reserves ~2–3% for filesystem metadata. |
| Memory (RAM) | $10 / GB-month | 1 GB held for the full billing month ≈ $10 before CPU, storage, or egress. THIS is the primary overage risk. |
| CPU | $20 / vCPU-month | Charged from actual CPU consumption over time; an idle service still consumes RAM and CPU. |
| Network egress | $0.05 / GB | 20 GB outbound ≈ $1/month. Inbound traffic is not metered. |

Builds are free.

## Storage interpretation

Hobby provides a default 5 GB persistent-volume size and up to 100 GB of ephemeral deployment storage. Ephemeral storage is wiped on redeploy and is not suitable for databases or uploads that must survive deployments.

Calling 5 GB "safe" is reasonable only for cost estimation: a fully used 5 GB volume is inexpensive, but capacity, filesystem metadata, backups, database growth, and operational recovery remain separate concerns.

## Cost scope

The $5 Hobby subscription includes $5 of metered usage. The $5 included usage applies at **workspace billing level**, not account level. All projects in the same billed workspace share the same included usage pool — not automatically every workspace under an account.

## Conclusions

- Safe data size from a cost point of view: up to 5 GB (database + uploads), but plan for metadata overhead and growth.
- The overage risk is memory-hungry always-on services (that was Hindsight). Hindsight is a separate project (`graceful-presence`) from the CRM (`perceptive-achievement`); a CRM redeploy cannot touch it. As understood, the $5 credit is shared by projects in the same billed workspace, so any heavy service in that workspace counts.
- Do not assume CPU is negligible without checking. Railway states that running services consume RAM and CPU even when idle, and common causes of unexpected usage include memory leaks, traffic spikes, resource-heavy templates, public database connections, and duplicate pull-request environments.
- Current usage: not measured. Look in the Railway dashboard → Workspace Settings → Usage (memory first) and each service → Volumes (GB). For CLI: `railway usage`, `railway usage projects`, `railway usage limit status`.
- **Do not share a project token for billing inspection.** A Railway project token is environment-scoped but supports deployments, redeployments, logs, variables, and other project actions — it is NOT read-only. Use screenshots or local CLI output instead; redact project names if needed.

## Decision thresholds

| Observed monthly estimate | Risk | Action |
|---|---|---|
| Up to $4 | Low | Monitor weekly; retain at least $1 headroom. |
| $4–$5 | Medium | Identify the top memory service and remove duplicate or unused environments. |
| Above $5 | High | Expect overage; optimize or stop the dominant service and configure a limit/alert. |
| Sudden unexplained rise | High | Check memory leaks, public DB traffic, replicas, PR environments, and newly deployed workers. |

## Links
- Parent: [[dev-ops-INDEX]]
- Related: [[DevOps-Platform-Audits]], [[LexFlow-Session-Summary-and-Operating-Blueprint-2026-10-27]]
