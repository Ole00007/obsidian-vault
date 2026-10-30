# Railway Hobby Usage — Corrected Cost & Safety Guide

**Verdict:** The original note is mostly correct on pricing and the main cost risk, but three points need correction.

## Corrections

1. **RAM and CPU are not the only overage resources.** Railway meters RAM, CPU, persistent volume storage, and outbound network egress.
2. **Treat the $5 allowance as workspace-level.** It is shared by projects inside the same billed workspace—not necessarily every workspace on the account.
3. **A Railway project token is not read-only.** It can deploy, redeploy, inspect logs, and perform other project operations. Do not share one for a billing check.

Sources: [Railway pricing](https://docs.railway.com/pricing/plans), [Understanding your bill](https://docs.railway.com/pricing/understanding-your-bill), [Railway CLI usage](https://docs.railway.com/cli), [CLI authentication](https://docs.railway.com/cli/login).

## Verified pricing

| Resource | Rate | Practical impact |
|---|---:|---|
| RAM | $10 per GB-month | 1 GB held all month costs about $10 before other resources. |
| CPU | $20 per vCPU-month | Actual CPU usage is metered over time. |
| Persistent volume | $0.15 per GB-month | 5 GB used all month costs about $0.75. |
| Network egress | $0.05 per GB | 20 GB outbound costs about $1. |

Hobby costs **$5/month and includes $5 of metered usage**. If metered usage reaches $7, the effective monthly bill is $7: the subscription covers the first $5 and $2 is charged as overage.

## Storage meaning

- Hobby persistent-volume default limit: **5 GB**.
- Paid-plan ephemeral deployment disk: **100 GB**.
- Ephemeral disk is wiped when deployments are replaced; never rely on it for databases or uploads that must persist.
- A 5 GB persistent volume is low-cost, but capacity, backups, database growth, and recovery remain operational concerns.

Sources: [Railway volumes](https://docs.railway.com/volumes/reference), [Deployments reference](https://docs.railway.com/deployments/reference).

## Main risk

Always-on RAM is probably the biggest cost driver. At $10 per GB-month, the full $5 allowance equals roughly **0.5 GB-month of RAM only**; the practical RAM budget is lower because CPU, volumes, and egress consume the same allowance.

Do not assume CPU is negligible. Check actual metrics. Unexpected costs can also come from memory leaks, public database connections, replicas, staging services, workers, and duplicated pull-request environments.

## 10–15 minute audit

1. Open [Railway Dashboard](https://railway.com/dashboard).
2. Select the billed workspace.
3. Open **Workspace Settings → Usage**.
4. Record total estimated usage and the breakdown by project/resource.
5. Rank projects locally if Railway CLI is authenticated:

```bash
railway usage
railway usage projects
railway usage limit status
```

6. Open the highest-cost project and inspect every service's **Memory**, **CPU**, **Replicas**, and **Metrics**.
7. Check each database/stateful service for its attached volume and used storage.
8. Find forgotten workers, staging environments, replicas, and PR deployments.
9. Verify Railway databases use private networking where possible.
10. Configure a cost alert/limit only after establishing the production baseline; preserve shutdown headroom.

## Evidence to share

Use one of these methods:

- Redacted screenshot of **Workspace Settings → Usage**.
- Redacted output from `railway usage` and `railway usage projects`.
- Screen-share session while the account owner remains authenticated.

**Never paste Railway tokens in chat.** Project tokens are scoped but are not read-only.

## Risk matrix

| Finding | Risk | Action |
|---|---:|---|
| Estimated usage up to $4 | Low | Monitor weekly; keep at least $1 headroom. |
| Estimated usage $4–$5 | Medium | Optimize the top memory service and remove duplicates. |
| Estimated usage above $5 | High | Expect overage; inspect and reduce the dominant service. |
| Sudden unexplained increase | High | Check leaks, replicas, PR environments, workers, and public DB traffic. |
| Sharing a project token | High | Do not share; provide redacted screenshots or CLI output. |
| Aggressive hard limit | Medium | Use alerts first; keep enough headroom for production availability. |

## Corrected message

> Railway Hobby costs $5 per month and includes $5 of metered usage. RAM, CPU, persistent volume storage, and outbound network traffic all count; RAM is usually the main overage risk. Current rates are $10 per GB-month of RAM, $20 per vCPU-month, $0.15 per GB-month of volume storage, and $0.05 per GB of egress.
>
> A fully used 5 GB persistent volume costs about $0.75 per month, so storage alone is unlikely to exhaust the credit. However, the 100 GB deployment disk is ephemeral and must not store data that needs to survive redeployments.
>
> Check **Workspace Settings → Usage**, rank projects, and inspect memory first. Treat the $5 credit as shared across projects in the same billed workspace. Do not send a token: Railway project tokens are scoped but not read-only. Share a redacted Usage screenshot or run `railway usage` and `railway usage projects` locally instead.
