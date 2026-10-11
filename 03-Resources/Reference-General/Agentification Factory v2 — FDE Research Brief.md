# Agentification Factory v2 — FDE Research Brief
## Direct recommendation
Upgrade the factory from a code-producing swarm into an **FDE-led operating-transformation system**. Its job should be to audit how a company actually works, choose one measurable workflow, integrate bounded agents around the company’s existing systems of record, prove outcomes in shadow mode, release with human gates, and transfer ownership—not merely build another CRM.

The strongest current FDE pattern is end-to-end ownership: discovery, technical scoping, system design, production rollout, adoption, measurement, and codification of reusable playbooks. New FDE programs similarly emphasize governed data, integration into existing workflows, phased production deployment, and customer handover.[^1][^2][^3]
## October upgrade
| Earlier factory emphasis | Upgraded FDE factory |
|---|---|
| Build software from tasks | Audit operations before selecting automation |
| CRM/product delivery | Company-wide workflow agentification |
| Agents around a repository | Agents around systems of record, policies, people, and evidence |
| Code tests and visual proof | Technical, operational, safety, adoption, and unit-economics proof |
| One-off implementation | Repeatable deployment and client ownership |
| Confidence score | Evidence gate plus independent cross-test and human release |

Production-agent practice increasingly favors owned control flow and context, durable state, pause/resume, small focused agents, and structured tool boundaries rather than unconstrained autonomous loops. The GitHub ecosystem also shows strong adoption of worktree isolation, durable workflows, provider-independent orchestration, and cost-aware loops.
## FDE engagement model
The recommended delivery cycle is:

```text
Discover → Audit → Design → Integrate → Shadow → Assist → Bound autonomy
→ Measure → Adopt → Transfer → Expand or stop
```

An FDE should first observe the real workflow, including undocumented exceptions and the systems where authoritative records live. Industry descriptions consistently position FDEs as hybrids of engineer, architect, product thinker, and embedded consultant who own the path from operational discovery to measured production.[^4][^5][^3]

Use the least complex intervention: remove unnecessary work, simplify policy, connect systems, use deterministic automation, add AI assistance, and employ multi-agent execution only when the workflow truly requires role separation or parallel specialization. This avoids replacing a broken process with a more expensive agentic version.[^6][^4]
## Integration doctrine
Agents should sit on top of the applications companies already use, with the existing CRM, practice-management platform, accounting system, DMS, ERP, or database remaining authoritative. Current finance guidance stresses that AI produces more value when embedded into core enterprise systems, where it can access current process context while remaining traceable and auditable. Automotive guidance similarly centers integration across sales, service, parts, finance, and CRM rather than introducing a disconnected assistant.[^7][^8]

Each production action should have an identity, tenant, case ID, policy version, tool schema, evidence trail, cost record, and approval status. Legal-sector guidance specifically recommends permissible-use definitions, observability, audit trails, decision tracing, restricted data access, reversibility, and organizational accountability.[^9]
## Industry priorities
| Sector | First workflows to test | Keep human-controlled |
|---|---|---|
| Legal | Intake completeness, matter routing, document chronology, deadline preparation, due-diligence review, billing/status drafts | Advice, privilege, conflicts clearance, final filing, settlement, client commitments |
| Accounting/audit | Document requests, extraction, anomaly queues, reconciliation preparation, vouching, close monitoring, cited workpapers | Material entries, audit opinions, policy judgments, signing and submission |
| Vehicle repair | Missed-call recovery, appointment preparation, pre-diagnosis questions, parts/technician coordination, reminders and follow-up | Safety diagnosis, repair authorization, warranty representation, roadworthiness |
| Vehicle retail | Lead routing, vehicle matching, trade-in evidence, missing-document monitoring, sales-to-service handoff | Credit decisions, regulated disclosures, valuation, binding price and contracts |

Professional-services platforms are moving toward complete workflows combining extraction, analysis, exception handling, cited documentation, and professional review rather than isolated prompting. Automotive workflows show the same pattern: agents connect calls, diagnosis preparation, real availability, parts, VIN/history, scheduling, and follow-up through DMS integration.[^10][^11][^12][^13]
## Governance model
Classify agent actions into four levels:

- **Green:** read, classify, summarize, test, and prepare internal drafts.
- **Yellow:** create pending records, open pull requests, queue communications, and recommend changes.
- **Red:** merge, deploy, send externally, post financial entries, change permissions, spend money, or delete data—human approval required.
- **Black:** bypass controls, conceal evidence, self-expand permissions, or use client data without authorization—always forbidden.

This follows the reversibility principle: low-impact “two-way door” work can be delegated more freely, while consequential or irreversible actions require stricter review. Human involvement should focus on exceptions, professional judgment, relationships, and release decisions rather than routine supervision of every successful step.[^9]
## Quality gate
The package implements:

```text
INTAKE → AUDIT → ISOLATE → BUILD → PROVE
→ ПЕРЕКРЁСТНЫЙ ТЕСТ → SCORE → HUMAN SHIP → OBSERVE
```

A 5/5 score requires evidence for scope, technical checks, operational behavior, safety, and delivery readiness. An independent reviewer must reproduce and cross-test the result; the builder cannot approve itself, and 5/5 still does not authorize an autonomous merge or production deployment.
## Deployment sequence
| Phase | Agent authority | Exit condition |
|---|---|---|
| Offline replay | No live action | Historical evaluation passes |
| Shadow mode | Reads live input; suppresses writes | Quality, latency, cost, and safety pass |
| Assisted pilot | Prepares work; humans approve actions | Stable outcome and adoption evidence |
| Bounded autonomy | Executes proven reversible actions | Low incident/override rate and positive economics |
| Scale | Adds workflows or locations gradually | Client can operate, audit, pause, and extend system |

A narrow initial workflow is safer than a broad transformation program. FDE deployment guidance commonly recommends establishing a baseline, validating connectors and policies, releasing on a limited slice, comparing cycle time and rework, then scaling only after production evidence.[^14][^15]
## Package contents
The generated package contains eight Markdown playbooks, a dependency-free JavaScript gatekeeper, a task manifest, install instructions, and an attribution file. It is generic across clients and industries, preserves the required isolated-branch and 5/5 evidence model, and expands the scope from CRM construction to audited operational agentification.

The JavaScript gatekeeper validates branch isolation, budgets, permissions, cross-test results, five evidence gates, and human approval. The included test deliberately returns `AWAIT_HUMAN_APPROVAL` at 5/5, demonstrating that agent evidence can make work merge-ready but cannot authorize shipping.

---

## References

1. [CTERA Introduces Forward Deployed Engineering to Close the AI Skills Gap and Accelerate Enterprise Deployments](https://www.globenewswire.com/news-release/2026/10/06/3375457/0/en/ctera-introduces-forward-deployed-engineering-to-close-the-ai-skills-gap-and-accelerate-enterprise-deployments.html) - New service embeds CTERA engineers inside customer environments to prepare governed data, build AI w...

2. [Forward Deployed Engineering for Enterprise AI | Atlassian](https://www.atlassian.com/enterprise/success/fde) - Atlassian FDEs embed with your teams to build, deploy, and scale AI, taking enterprise projects from...

3. [Forward Deployed Engineer (FDE) - SF - OpenAI](https://openai.com/careers/forward-deployed-engineer-(fde)-sf-san-francisco/) - You will own discovery, technical scoping, system design, build, and production rollout, partnering ...

4. [AI Workflow Automation with Forward Deployed Engineers](https://fde.academy/blog/ai-workflow-automation-forward-deployed-engineers) - Explore AI workflow automation with Forward Deployed Engineers, including implementation, use cases,...

5. [Forward Deployed Engineering: Why Enterprise AI Needs More ...](https://stermedia.ai/forward-deployed-engineering-why-enterprise-ai-needs-more-than-a-model/) - An FDE combines engineering, product thinking, domain discovery and deployment ownership. In practic...

6. [Varick Agents: Scaling Forward-Deployed Engineering with AI ...](https://www.zenml.io/llmops-database/scaling-forward-deployed-engineering-with-ai-agents-for-enterprise-transformation) - The company embeds forward-deployed engineers (FDEs) within client organizations to map existing wor...

7. [What is Dealer Management Software? - Salesforce](https://www.salesforce.com/automotive/car-dealership-software/dealer-management-software/) - Dealer management software (DMS) connects sales, service, parts, and CRM in one platform. Learn what...

8. [How AI Is Transforming Enterprise Systems](https://www.aicpa-cima.com/professional-insights/article/how-ai-is-transforming-enterprise-systems) - An exploration of how AI-powered enterprise systems are enabling continuous planning, smarter foreca...

9. [Who's leading the flock? Balancing agentic AI automation ...](https://www.thomsonreuters.com/en/institute/articles/iltacon-2026-agentic-ai-automation) - An ILTACON 2026 panel explores how law firms can govern agentic AI teams, which can now plan and act...

10. [Best conversational AI for automotive dealerships in 2026 | GetVocal](https://www.getvocal.ai/blog/best-conversational-ai-for-automotive-dealerships) - Compare the best conversational AI for automotive dealerships in 2026 on DMS integration, EU AI Act ...

11. [myKaarma Offers New AI Lead Management Solutions to Ford and Lincoln Dealerships](https://finance.yahoo.com/technology/ai/articles/mykaarma-offers-ai-lead-management-123900375.html) - myKaarma, the leading customer interaction and payments platform for automotive dealerships, today a...

12. [How to use agentic AI workflows in professional services](https://www.thomsonreuters.com/en/insights/articles/how-to-use-agentic-ai-workflows-in-professional-services) - Discover how agentic AI transforms legal, tax, and risk workflows for professionals — with use cases...

13. [Thomson Reuters Advances AI Market Leadership with ...](https://www.thomsonreuters.com/en/press-releases/2025/november/thomson-reuters-advances-ai-market-leadership-with-new-agentic-ai-solutions) - CoCounsel Document Analysis - Coming January 2026, auditors and accounting professionals will be abl...

14. [Forward Deployed Engineers for Enterprise AI & CX - Pronix Inc](https://pronix.ai/forward-deployed-engineering) - Hire embedded Forward Deployed Engineers for enterprise AI, agentic AI and contact center implementa...

15. [The Forward-Deployed Engineer Model: Why Consulting Is Dead for ...](https://blog.infrahive.ai/forward-deployed-engineer-model-enterprise-ai-delivery) - Enterprise AI delivery now depends on forward-deployed engineers who connect systems, encode policy,...

