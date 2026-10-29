# LexFlow — Harvey-style Statistic Graph: Brainstorm + Estimation

**Date:** 2026-10-26
**Author:** frontend-developer-lovable_react (on Ole's direct request)
**Status:** brainstorm / estimation — NOT started. Awaiting backend-dev (backy) answers on card `t_0e79f5b8`.

---

## 1. What Ole asked

Build **one Harvey-like STATISTIC graph** for LexFlow (a *statistic* chart, **not** the T-021 work-orchestration *diagram* — those are different deliverables).

Reference pages (grounding):
- https://www.harvey.ai/solutions/in-house
- https://www.harvey.ai/roi-calculator/law-firm  ← the relevant one (law-firm, not in-house)

## 2. The Harvey stat-graph pattern (from the law-firm ROI calculator)

- **Multi-series annual chart** — 3 columns (Year 1 / Year 2 / Year 3 + Total) × 4 series:
  Total Time Regained (hrs) → Net Incremental Billable Capacity → Cost of Harvey → Potential Additional Profit.
- **Headline metric** — a big "24x Annual ROI" figure.
- **KPI stat cards** — 93% reduced non-billable time, 80% faster delivery, 83% better client relations, 37 hrs saved/month.

## 3. What already exists in LexFlow (no new backend needed for the core)

`feat/wave2-insights` ships `/api/insights/summary` returning:
- `activity` — **weekly series**: `matters_opened`, `tasks_completed`, `tasks_created`
- `matters_by_status`, `deadline_health`, `workload_by_role`, `flags`, `kpis` (+ `kpis_previous` for deltas)

**Frontend candidate:** weekly multi-series chart of **matters opened + tasks completed** (data already in `activity`).

## 4. Estimation

| Scope | Time | Credit (tokens) |
|---|---|---|
| Full Harvey-like dashboard (all charts + KPIs) | ~1.5–2.5 focused days | ~1.5–2.5M (~$1–3) + ~0.5M review |
| **ONE statistic graph only** (this task) | **~0.5–1 day** | **~0.3–0.6M (~$0.3–0.8)** |

Assumes reusing existing CRM backend (`web-production-031a6`) + current design system — not greenfield.

## 5. Questions sent to backend-dev (backy) — card `t_0e79f5b8`

1. Is `/api/insights/summary` stable/deployable, and which branch should the chart frontend mount against?
2. Which single chart is most valuable for a legal CRM? (candidate: weekly matters opened + tasks completed)
3. Any field needed that is **not** already in the summary (e.g. billable / time-tracked hours)?

## 6. Build approach (once backy confirms)

- **Frontend only**, spec-first: 1-page spec + 2 layout options in the vault, local preview, **no push**.
- Dark + light theme, 390px mobile usable, keyboard accessible, no heavy new dependency (reuse what /graph already vendors).
- Flags default OFF.

## Links
- Parent: [[LexFlow_Ecosystem_Index]]
- Related: [[harvey-lexflow]]
- Related: [[LexFlow-T021-Diagram-View-Spec-2026-10-06]]
- Related: [[LexFlow-Roadmap]]
