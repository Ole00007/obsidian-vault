# Railway vs Cloudflare: Real Cost of Running Hermes Agent

**Research date: 22 September 2026.** For the standard, continuously available Hermes deployment, **Railway is the simpler and safer fit** and a realistic hosting budget is **about $6–12/month**, excluding the model/API bill. Cloudflare Workers can make an event-driven agent backend very cheap—often $0–5/month—but the full Hermes runtime is not a natural Worker; a continuously running Cloudflare Container is more likely to cost roughly **$20–25/month** and currently has weaker persistence guarantees.

## What “agent cost” includes

There are three separate bills:

- **Runtime hosting:** Railway or Cloudflare compute, memory, storage, and network.
- **Model usage:** OpenRouter, Anthropic, OpenAI, Google, or another LLM provider. Railway’s “Agent spend limit” controls Railway’s own platform agent—not Hermes and not the external LLM API.[^1][^2]
- **Connected services:** databases, browser automation, search APIs, Google APIs, email, or observability tools.

The Hermes project says it can run on a $5 VPS, while a Railway-specific community template estimates $5–10/month for hosting plus separate LLM API charges. A Hermes community report describes approximately 300–600 MB RAM and very low CPU use, but this is anecdotal rather than a guaranteed sizing specification.[^3][^4][^5]

## Railway pricing reality

Railway Hobby is a **$5 monthly minimum commitment**, not a $5 ceiling. That payment covers the first $5 of measured resource use; if resources cost $8, the bill is approximately $8 rather than $13. Current rates are about $10 per continuously used GB of RAM per month, $20 per continuously used vCPU per month, $0.15 per GB-month of volume storage, and $0.05 per GB of outbound traffic.[^6][^7][^8]

Railway’s important cost characteristic is persistent memory use: an online service occupies RAM even with little traffic, so a quiet agent is not free merely because nobody is chatting with it. CPU can remain inexpensive when Hermes mostly waits for messages and external model responses, but memory generally forms the cost floor.[^7][^9]

### Estimated Hermes bill

| Deployment pattern | Assumptions | Railway hosting estimate |
|---|---|---:|
| Light personal agent | Around 0.5 GB average RAM, very low CPU, small volume and egress | **$5–7/month** |
| Comfortable always-on agent | Around 1 GB average RAM, low CPU, 1–5 GB persistent volume | **$10–13/month** |
| Agent plus local database or browser-heavy tools | 1–2 GB RAM, more CPU, larger volume | **$15–35+/month** |

These are planning estimates derived from Railway’s unit rates, not quoted fixed plans. A community Railway template explicitly recommends mounting `/root/.hermes` as a persistent volume so sessions, memories, API keys, configuration, logs, and cron jobs survive redeployment.[^10]

## Track Railway correctly

Use **Workspace → Usage** as the primary cost view. Railway’s CLI can show the current and estimated bill, rank projects by cost, break a project down by service and resource, and export JSON for a monthly script:[^1]

```bash
railway usage
railway usage projects
railway usage --period current --json
railway usage limit status
```

Set both an email warning and a hard stop. For a first personal Hermes deployment, a practical starting policy is **$8 soft / $12 hard** if occasional downtime is acceptable, or **$10 soft / $15 hard** for more headroom:

```bash
railway usage limit set --target workspace --soft 8 --hard 12
```

Railway can pause workloads at the hard limit, so it is a real cost guardrail but can make Hermes unavailable until the next billing period or until the limit is increased. Also cap the unrelated Railway Agent at zero if it is not needed:[^11][^12]

```bash
railway usage limit set --target agent --hard 0
```

Check usage after 24 hours, 72 hours, and 7 days. Identify the service with the largest memory charge; unused deployed services still consume resources, and one community support case traced an unexpected alert to eleven services left active.[^9]

## Cloudflare pricing reality

A normal Cloudflare Worker is billed for active CPU rather than time spent waiting for a model or database. The Free tier allows 100,000 requests per day but only 10 ms CPU per invocation; Workers Paid costs at least $5/month and includes 10 million monthly requests and 30 million CPU-ms, followed by $0.30 per additional million requests and $0.02 per additional million CPU-ms. This is excellent for a thin webhook/API layer because external-network waiting time does not add CPU charges.[^13][^14][^15]

However, a standard Worker has only 128 MB memory and is not equivalent to an ordinary persistent Linux host. The full Hermes runtime uses Python/Node tooling, a web UI, local files, sessions, cron jobs, and often terminal execution; the established Railway deployment uses a Docker service and persistent volume. Therefore, “put Hermes on Cloudflare Workers” normally means **redesigning it into Workers, Queues, Durable Objects, D1/R2, and external execution**, not simply redeploying the Railway container.[^14][^10][^3]

### Cloudflare cost paths

| Cloudflare approach | Realistic cost | Fit for Hermes |
|---|---:|---|
| Worker webhook/orchestrator on Free | **$0/month** while within hard free quotas | Good for a small custom agent endpoint; not the full stock Hermes runtime |
| Worker webhook/orchestrator on Paid | Usually **$5/month** at low-to-moderate traffic | Good when most time is spent waiting for external LLM APIs |
| Cloudflare Container that sleeps when idle | Approximately **$5–15/month**, highly activity-dependent | Possible adaptation, but requires persistence redesign |
| Cloudflare basic Container kept active all month | Approximately **$24/month** before external storage/model costs | Technically closer to Hermes, but usually worse value than Railway |

The always-on Container estimate uses Cloudflare’s current “basic” allocation of 0.25 vCPU, 1 GiB memory, and 4 GB disk against its published CPU, memory, and disk rates, after the Workers Paid included amounts. Containers bill only while active and normally sleep after inactivity, but their disk is ephemeral, Cloudflare does not guarantee an instance will run for any fixed period, and durable state must be moved to R2 or another external store.[^16][^17][^18]

Cloudflare D1 can remain inexpensive for normal small-agent use because Paid includes 25 billion rows read, 50 million rows written, and 5 GB storage per month; above that, writes cost $1 per million and storage $0.75 per GB-month. The danger is faulty automation rather than ordinary chat volume: one published incident attributes a $4,868 bill to an infinite loop that wrote 4.83 billion D1 rows, and reported no hard D1 write-spend cap.[^19][^20]

## Track Cloudflare correctly

Cloudflare requires more manual cost control than Railway. In **Workers & Pages → Worker → Analytics**, monitor requests, errors, wall time, and CPU time; then inspect D1, Durable Objects, R2, Queues, and Containers separately because each product has its own meter. Account billing notifications are informational, and Cloudflare documentation says the invoice remains the most reliable billing record.[^21][^22]

Community reports consistently flag that notifications are not a universal hard spending cap. The safest configuration is:[^23][^24][^25]

- Remain on **Workers Free** during development, where request and CPU quotas stop workloads instead of creating overage charges.[^14]
- On Paid, set a low per-invocation `limits.cpu_ms` value so a runaway request cannot burn arbitrary CPU; Cloudflare itself recommends this against denial-of-wallet incidents.[^26]
- Add application rate limits by authenticated user and IP; cap concurrent jobs, tool calls, loop iterations, retry count, output size, and daily LLM tokens.
- Put explicit counters and circuit breakers around D1 writes, Durable Object alarms, Queues, and browser/container launches.
- Send daily usage metrics through the GraphQL Analytics API or an external monitor; do not rely on a month-end invoice.
- Use a restricted Cloudflare API token. Never give Hermes unrestricted account, billing, DNS, or deletion rights.

## Recommended setup

For the current full Hermes agent, use **Railway Hobby**, one Hermes service, one small persistent volume, and no unnecessary database service. Start with an **$8 warning and $12 hard limit**, review seven days of actual memory/CPU consumption, then move the cap only after seeing the trend. Keep a separate hard budget at the LLM provider—initially perhaps $5–10/month—because model calls may exceed the infrastructure bill.

Use Cloudflare alongside Railway for DNS, caching, access protection, or a low-cost public webhook, but not as the first host for the complete Hermes process. Choose a Cloudflare-native agent only if redesigning the workflow around short event-driven invocations is acceptable; in that architecture, $0–5/month infrastructure is credible, but model/API consumption remains separate.

---

## References

1. [railway usage | Railway Docs](https://docs.railway.com/cli/usage) - Usage limits track compute and Railway Agent spend independently. Set a custom email alert, a hard l...

2. [Feature flags, Railway Agent in Slack & Discord, usage limits ...](https://railway.com/changelog/2026-07-10-feature-flags) - Setting an Agent hard limit of 0 blocks Agent usage entirely. Every command supports --workspace, --...

3. [NousResearch/hermes-agent: The agent that grows with you - GitHub](https://github.com/nousresearch/hermes-agent) - The installer handles everything: uv, Python 3.11, Node.js, ripgrep, ffmpeg, and a portable Git Bash...

4. [Deploy & Host Hermes Agent [Updated Sep '26] | Railway](https://railway.com/deploy/hermes-agent-updated-sep-26--hermes) - Instead of running Open WebUI or OpenWebUI with limited agent capabilities, deploy Hermes Agent with...

5. [Minimum Specs to Run Hermes? : r/hermesagent - Reddit](https://www.reddit.com/r/hermesagent/comments/1vgjlee/minimum_specs_to_run_hermes/) - It uses around 1GB RAM and next to no CPU. A Raspberry Pi 3 can run it. RAM usage: ~300-600MB Swap (...

6. [Pricing | Railway](https://railway.com/pricing) - Includes $5 of monthly usage credits. After credits are used, you'll only be charged for extra resou...

7. [Understanding Your Bill | Railway Docs](https://docs.railway.com/pricing/understanding-your-bill) - This guide explains how Railway billing works in practice, helping you understand your charges and a...

8. [Usage-Based vs. Fixed Pricing: Which Is Cheaper in 2026?](https://blog.railway.com/p/usage-based-vs-fixed-pricing-2026) - Railway charges for the CPU, RAM, storage, and public egress the application actually uses, rather t...

9. [railway - need help for unknown usage & downgrade to free tier](https://station.railway.com/questions/new-user-w-railway-need-help-for-unkn-cc4c01b6) - You can set up usage alerts, limits, and view your usage breakdown, including per-service costs, by ...

10. [GitHub - mazshakibaii/hermes-agent-railway: Deploy your own ...](https://github.com/mazshakibaii/hermes-agent-railway) - Deploy Hermes Agent to Railway with one click. Hermes is an open-source AI agent by Nous Research wi...

11. [Usage Limits, DB Templates, Launch Week Announcement | Railway](https://railway.com/changelog/2023-09-15-usage-limits) - We’ve heard loud and clear that you’d like ways to control your costs, limit your liabilities, and p...

12. [Questions about Hard Spending Limits and Official Invoices ...](https://station.railway.com/community/questions-about-hard-spending-limits-and-d7fce2c0) - Is there a "Hard Limit" or "Kill Switch" for spending? To comply with our budget policy, I need to e...

13. [Pricing · Cloudflare Workers docs](https://developers.cloudflare.com/workers/platform/pricing/) - CPU time is only billed when the Worker runs (on a cache miss or bypass). A Worker that serves 15 mi...

14. [Limits · Cloudflare Workers docs](https://developers.cloudflare.com/workers/platform/limits/) - Accounts on the Workers Free plan have a daily request limit of 100,000 requests, resetting at midni...

15. [New Workers pricing — never pay to wait on I/O again](https://blog.cloudflare.com/workers-pricing-scale-to-zero/) - Announcing new pricing for Cloudflare Workers, where you are billed based on CPU time, and never for...

16. [Pricing · Cloudflare Containers docs](https://developers.cloudflare.com/containers/platform/pricing/) - Containers are billed for every 10ms ・ $5 USD per month Workers. Paid 25 GiB-hours/month included +$...

17. [Containers are available in public beta for simple, global, and ...](https://blog.cloudflare.com/containers-are-available-in-public-beta-for-simple-global-and-programmable/) - Copy linkPricing and packaging · North America and Europe: $0.025 per GB with 1 TB included · Austra...

18. [Frequently Asked Questions · Cloudflare Containers docs](https://developers.cloudflare.com/containers/faq/) - Answers to common questions about Containers, including logging, scaling, cold starts, disk persiste...

19. [My $5/month Cloudflare bill hit $4,868 because of an infinite ...](https://dev.to/nathanschram/my-5month-cloudflare-bill-hit-4868-because-of-an-infinite-loop-13g8) - Two bugs in my Cloudflare Workers wrote 4.83 billion rows to D1 in January 2026. The bill hit $4,868...

20. [Pricing · Cloudflare D1 docs](https://developers.cloudflare.com/d1/platform/pricing/) - D1 pricing based on rows read, rows written, and storage with scale-to-zero billing.

21. [Usage-based billing - Cloudflare Developer Docs](https://developers.cloudflare.com/billing/understand/usage-based-billing/) - Cloudflare sends a notification to the billing email address on file when traffic, queries, requests...

22. [Metrics and analytics - Workers - Cloudflare Docs](https://developers.cloudflare.com/workers/observability/metrics-and-analytics/) - The CPU Time per execution chart shows historical CPU time data broken down into relevant quantiles ...

23. [Setting up a spending Limit - Feature Request Submitting & Feedback](https://community.cloudflare.com/t/setting-up-a-spending-limit/382846) - You can setup a billable usage notification. Turning off rate limiting unexpectedly could be catastr...

24. [Implement hard billing limit! : r/CloudFlare - Reddit](https://www.reddit.com/r/CloudFlare/comments/1gdcuwk/implement_hard_billing_limit/) - Cloudflare has built in notifications for it, most cloud providers do, but just notifications, no ha...

25. [Feature Request: Actual billing notification for usage based billing ...](https://community.cloudflare.com/t/feature-request-actual-billing-notification-for-usage-based-billing-combined/654326) - Customers who want to receive a notification when the usage of a product goes above a set level can ...

26. [I would pay for Cloudflare Workers Paid ($5) in a heartbeat and ...](https://news.ycombinator.com/item?id=47795924) - For example 1 million requests to a Worker is only $0.30 and there's no bandwidth charge. their rate...

