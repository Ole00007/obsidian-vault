# Memory Architecture 2026-10-29 — Obsidian-first, Hindsight on Standby

**Owner:** admy_ceo · **Reviewer:** memory-curator · **Status: DRAFT (pending review)**
**Directive source:** Ole, 2026-10-29. Hindsight is on standby; feed it only monthly
chunks or vectorized summaries to keep credit/token/RAM load low.

---

## 1. Why this exists

Hermes in-session memory is a **finite 2,200-char budget** — it cannot hold history. It
evicts stale entries by design. The consequence: raw conversation history is *not*
retained by default, and long context in-session is the costly path (see §5 cost model).

New policy: **Obsidian is the live system of record for memory.** Hindsight becomes a
**monthly, vectorized summary channel only** — not a per-session mirror.

## 2. Where each kind of knowledge lives

| Content | Home | Cadence |
|---|---|---|
| Daily work log | `05-Daily/YYYY-MM-DD.md` | every session |
| Decisions, ADRs, status | `01-Projects/<Project>/` | at decision time |
| Shared reference facts | `03-Resources/` | on learn |
| Durable cross-session facts | agent `memory()` target | only when needed to every turn |
| Procedures / pitfalls | `skills/` (skill_manage) | on learn |
| **Searchable long-term memory** | **Obsidian vault** | **live** |
| **Hindsight bank** | **monthly chunk / vector summary** | **1×/month** |

**Hindsight is DERIVED from Obsidian** (per Rule §9.1/§9.3). It is never written to
directly for daily notes. Only the monthly summarizer writes to it.

## 3. The monthly Hindsight feed (cost-lite)

- **Cadence:** 1×/month, ~1st of month, owned by memory-curator.
- **Input:** reconcile the past month's `05-Daily/` + new project/decision notes.
- **Output:** one vectorized summary + monthly chunk written to the `avibe-hq` bank.
- **Purpose:** keep Hindsight searchable for cross-session recall WITHOUT paying
  per-session sync cost or growing the bank every day.
- **Load guard:** skip if the API is unreachable (modify the launchd job to **retry**
  and log loudly — do not silently drop; see known-failure history Sep–Oct 2026).
- **Sync job:** existing `com.avibe.obsidian-sync` (06:00) stays on **standby** — it is
  NOT disabled, but does not run per-session. Confirm go/no-go monthly.

## 4. Roles

| Role | Responsibility |
|---|---|
| **admy_ceo** | Every work session appends a one-line entry to the Daily Note (`§V3`). Writes project/decision notes at decision time, with `## Links`. |
| **memory-curator** | Monthly Hindsight summarizer + reviewer of this policy. Verifies the reconcile line, bank stats, and load. |
| **All profiles** | Same Daily-Note + vault-logging duty (`§V3`). None call Hindsight directly for daily logs. |

## 5. Cost model — keep-full-history vs search-and-recontextualize

**Keeping full history in context** (e.g. a big-context model with no compaction):
- Every subsequent turn re-reads the whole transcript as **input tokens** → input cost
  grows **quadratically** across a long session.
- Latency rises; giant context risks truncation/quality loss.
- Only becomes economical if `prompt_caching` (cache_ttl in config) keeps reads on the
  discounted cached tier — and caches expire, so savings are partial.

**Search-and-recontextualize** (this policy, small in-session memory + Obsidian +
monthly Hindsight):
- Base context stays small & flat → per-turn input cost is low and linear.
- Cost moves to *retrieval* (a few `read_file`/`search_files`/recall calls) only when a
  fact is actually needed — a few tokens uncached, not the whole history every turn.
- **Verdict:** for long-lived work the search/recontextualize path is the cheaper and
  the more RAM/credit-lite choice, given this workspace's current constraints.

## 6. Open questions for memory-curator

1. Do we keep `com.avibe.obsidian-sync` launchd as-is (standby) or gate it monthly?
2. Is the existing `hindsight/config.json` token still valid for the monthly write?
3. Should the monthly job hard-fail loudly or degrade to "skip this month, log"?
4. Partitioning: one summary per month vs one per project per month — which stays light?

## Links

[[Obsidian-INDEX]] → Parent folder hub
[[_Inbox]] → Related sibling (this draft's home)
[[memory-policy]] → Related sibling (existing SoR-vs-memory policy, kept)  
[[Hindsight-Vault-Sync-Fix-2026-09-16]] → Related (known sync failures)
