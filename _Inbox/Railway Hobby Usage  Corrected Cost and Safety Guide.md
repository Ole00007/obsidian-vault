# Railway Hobby Usage: Corrected Cost and Safety Guide

## Direct assessment

The original note is **mostly correct on prices and the main risk**, but it needs three corrections:

1. **Storage and network egress also count toward usage.** RAM and CPU are usually the largest charges, but Railway bills RAM, CPU, persistent volume storage, and outbound network traffic.[^1][^2]
2. **The $5 included usage applies at workspace billing level.** The Railway CLI reports workspace usage and can rank projects by cost, so describe the credit as shared by projects in the same billed workspace—not automatically every workspace under an account.[^3]
3. **A Railway project token is not read-only.** It is environment-scoped but supports deployments, redeployments, logs, variables, and other project actions. Do not share one merely to inspect billing.[^4][^5]

## Verified pricing

| Resource | Railway rate | Practical meaning |
|---|---:|---|
| RAM | $10 per GB-month | An average 1 GB held for the full billing month costs about $10 before CPU, storage, or egress.[^1] |
| CPU | $20 per vCPU-month | Charged from actual CPU consumption over time; an idle service can still use CPU and RAM.[^1][^2] |
| Persistent volume | $0.15 per GB-month | 5 GB continuously used costs about $0.75 per month; Railway charges the amount actually used.[^6][^1] |
| Network egress | $0.05 per GB | 20 GB outbound costs about $1; inbound traffic is not the item listed in resource pricing.[^1] |

The Hobby subscription is $5 per month and includes $5 of resource usage. If total metered usage is $7, the effective bill is $7: the $5 subscription plus $2 above the included usage.[^7][^1]

## Storage interpretation

Hobby provides a default 5 GB persistent-volume size and up to 100 GB of ephemeral deployment storage. Ephemeral storage is not suitable for databases or uploads that must survive deployments; persistent data belongs on a volume, database volume, or object-storage bucket.[^6][^8]

Calling 5 GB “safe” is reasonable **only for cost estimation**: a fully used 5 GB volume is inexpensive, but capacity, filesystem metadata, backups, database growth, and operational recovery remain separate concerns. Railway notes that each volume uses approximately 2–3% for filesystem metadata.[^6]

## Main cost risk

The note correctly identifies always-on memory as the most likely source of overage. At current rates, the entire $5 included usage corresponds to roughly 0.5 GB-month of RAM if there were no CPU, volume, or egress charges; in practice, the available RAM budget is lower because all metered resources draw from the same included usage.[^1]

Do not assume CPU is negligible without checking. Railway states that running services consume RAM and CPU even when they are not handling requests, and common causes of unexpected usage include memory leaks, traffic spikes, resource-heavy templates, public database connections, and duplicate pull-request environments.[^2][^9]

## Recommended check

Complete this audit in **10–15 minutes**:

1. Open [Railway Dashboard](https://railway.com/dashboard) and select the billed workspace.
2. Open **Workspace Settings → Usage** and record estimated total usage plus the breakdown by project and resource. Railway documents this page as the source for CPU, memory, network, and project-level usage.[^9]
3. Rank projects by cost if the CLI is already authenticated:

```bash
railway usage
railway usage projects
railway usage limit status
```

These commands show workspace usage, project cost ranking, and current usage-limit status.[^3]

4. Open each active service and inspect **Metrics** for memory and CPU. Check every database or stateful service for its attached volume and current disk use.
5. Look for forgotten services, workers, replicas, staging environments, and pull-request deployments. Stop only resources confirmed unnecessary.
6. Verify database connections use Railway private networking where possible; public database traffic may create egress charges.[^2][^9]
7. Set a conservative compute usage limit or alert after confirming the production baseline. Keep enough headroom to avoid an unexpected production shutdown.

## Safe evidence sharing

Preferred evidence is a screenshot or copied usage breakdown with project names redacted if needed. Do **not** paste account, workspace, or project tokens into chat, documents, logs, or screenshots.

For local diagnosis, authenticate the Railway CLI on the owner’s machine and share only command output. A project token reduces scope to one environment, but it is still capable of operational actions and therefore should not be described as read-only.[^10][^5][^4]

## Decision thresholds

| Observed monthly estimate | Risk | Action |
|---:|---|---|
| Up to $4 | Low | Monitor weekly; retain at least $1 headroom. |
| $4–$5 | Medium | Identify the top memory service and remove duplicate or unused environments. |
| Above $5 | High | Expect overage; optimize or stop the dominant service and configure a limit/alert. |
| Sudden unexplained rise | High | Check memory leaks, public DB traffic, replicas, PR environments, and newly deployed workers.[^9] |

## Gains and risks

| Item | Rating | Mitigation or gain |
|---|---:|---|
| Cost visibility | High gain | Workspace usage plus project ranking reveals the actual cost source. |
| Storage-cost exposure | Low risk | 5 GB of used volume storage is about $0.75 per month at the published rate.[^1] |
| Always-on memory | High risk | Track average memory, remove idle workers, and investigate leaks. |
| CPU assumptions | Medium risk | Use service metrics instead of assuming an idle app costs almost nothing. |
| Shared token access | High security risk | Use screenshots or local CLI output; never share a token for billing inspection. |
| Hard limit | Medium availability risk | Set alerts first and keep production headroom before enforcing a shutdown threshold. |

## Corrected short message

> Railway Hobby costs $5 per month and includes $5 of metered usage. RAM, CPU, persistent volume storage, and outbound network traffic all count; RAM is usually the main overage risk. Current rates are $10 per GB-month of RAM, $20 per vCPU-month, $0.15 per GB-month of volume storage, and $0.05 per GB of egress.[^1]
>
> A fully used 5 GB persistent volume is about $0.75 per month, so storage alone is unlikely to exhaust the credit. However, the 100 GB deployment disk is ephemeral and must not hold data that needs to survive redeployments.[^8][^6]
>
> Check **Workspace Settings → Usage**, then rank projects and inspect memory first. Treat the $5 credit as shared across projects in the same billed workspace. Do not send a token: Railway project tokens are scoped, but they are not read-only. Share a redacted Usage screenshot or run `railway usage` and `railway usage projects` locally instead.[^5][^4][^3]

---

## References

1. [Pricing Plans | Railway Docs](https://docs.railway.com/pricing/plans) - The Hobby Plan is $5 a month, and it includes a resource usage credit of $5. Even if you do not use ...

2. [Understanding Your Bill](https://docs.railway.com/pricing/understanding-your-bill) - Your subscription fee ($5 Hobby, $20 Pro) is a minimum usage commitment. It covers your first $5 or ...

3. [CLI | Railway Docs](https://docs.railway.com/cli) - railway usage projects # Rank projects by cost
railway usage limit status # Show compute and agent l...

4. [Deploying with the CLI](https://docs.railway.com/cli/deploying) - For automated deployments, use a Project Token instead of interactive login. Project tokens are scop...

5. [railway login | Railway Docs](https://docs.railway.com/cli/login) - Login to your Railway account to authenticate the CLI. Sign-in and sign-up are the same flow: if you...

6. [Volumes | Railway Docs](https://docs.railway.com/volumes/reference) - - Hobby plans: **5GB**
...
Volumes are billed at a rate per GB / minutely, and invoiced monthly.

7. [Pricing | Railway Docs](https://docs.railway.com/pricing) - Pay only for the CPU, memory, storage, and egress you … if you're on the Hobby plan at $5/month and ...

8. [Deployments reference | Railway Docs](https://docs.railway.com/deployments/reference) - A usage limit has been reached and raised. Upgrading to Hobby when trial credits were previously dep...

9. [Pricing FAQs | Railway Docs](https://docs.railway.com/pricing/faqs) - While the Hobby plan includes $5 of resource usage per month, you are charged for any usage that exc...

10. [Lock Down a Production Railway Project | Railway Guides](https://docs.railway.com/guides/lock-down-production-project) - Harden a production Railway project with Under Attack Mode, private networking, scoped API tokens, s...

