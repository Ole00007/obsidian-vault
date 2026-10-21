---
title: "Smoothy op-dir — Handover: conclusions, open blockers, next steps"
created: 2026-10-21
tags: [handover, hermes, ops, blockers, canva, lexflow, mcp]
status: active
---

# Smoothy op-dir — Handover (2026-10-21)

**Audience:** the next operator-installer session (Ole is switching this profile's model).
**Source:** live read of configs, cron store, kanban DB, gateway logs, repos, and prod health on 2026-10-21. Nothing here is recalled from memory.
**Why this exists:** the session that produced it is ending; this is the state the new session inherits.

---

## TL;DR

Two live breakages are silently killing the automation estate, and neither has been noticed
because the alert channel is itself broken. The Canva automation is stalled on four steps
**only Ole can do**. Nothing is on fire; everything is fixable, and the fixes are small.

| # | Item | Severity |
|---|------|----------|
| 1 | Telegram delivery broken for this profile — 5 reporting crons dead | FAIL |
| 2 | `canva` / `cloudflare` / `railway` MCPs enabled but unauthorized (401 loop) | FAIL |
| 3 | Canva automation 2/25 tasks done, blocked on Ole | WARN |
| 4 | aLEXy Google API key leak still live (public repo, ~2.5 months) | WARN |
| 5 | LexFlow roadmap stale 7 days; dirty working tree | WARN |
| 6 | Profile model = `meituan/longcat-2.5-preview:free` — being replaced | INFO |

---

## 1. FAIL — Telegram delivery is broken for this profile

**Symptom:** every cron job that reports to Ole fails on delivery.

```
blocked_config: delivery platform 'telegram' has no gateway credentials configured
delivery error: Telegram send failed: You must pass the token you received from https://t.me/Botfather!
```

**Evidence:**

- `~/.hermes/.env` contains `TELEGRAM_ALLOWED_USERS=1372207688` but **no `TELEGRAM_BOT_TOKEN`**.
- `~/.hermes/gateway_state.json` shows telegram **connected** for `frontend-developer-lovable_react`
  and `memory-curator` — but **not** for `smoothy_op_dir`, which owns the reporting jobs.
- Dead jobs (all `deliver: telegram:1372207688`):
  - `lexflow-daily-status-crm` (09:00) — failure_streak 4
  - `lexflow-morning-plan` (07:30) — failure_streak 4
  - `lexflow-morning-report` (08:00) — failure_streak 4
  - `lexflow-nightly-watchdog` (23:59) — delivery_failed
  - `hindsight-weekly-sync` (Sun 08:00) — failure_streak 2
- All marked `preflight_alerted: true` — the system tried to raise the alarm and could not.
- **Corroborating proof the daily ritual is dead:** Obsidian daily notes stop at `2026-10-06`.
  Nothing logged since, 15 days.

**Where the jobs live:** `~/.hermes/profiles/smoothy_op_dir/cron/jobs.json`

**Next session's first task.** Until this is fixed, every "daily status" Ole believes he is
receiving is fiction.

---

## 2. FAIL — three MCP servers are enabled but unauthorized

`canva`, `cloudflare`, `railway` return HTTP 401 on every connect attempt:

```
MCP OAuth setup failed for 'canva': non-interactive environment and no cached tokens found.
Run `hermes mcp login canva` interactively first to complete initial authorization.
```

- **144** `invalid_token` entries in `~/.hermes/logs/gateway.error.log` today. The gateway retries in a loop.
- `hermes -p smoothy_op_dir mcp list` shows all three as `✓ enabled` — **enabled ≠ working**. Do not trust that column.
- Fix is one interactive command each, run by a human or an interactive session:
  `hermes mcp login canva` / `hermes mcp login cloudflare` / `hermes mcp login railway`

**MCP inventory, profile `smoothy_op_dir` (`~/.hermes/profiles/smoothy_op_dir/config.yaml`):**

| Server | Transport | Status |
|--------|-----------|--------|
| composio | http | OK — working |
| obsidian-mcp | stdio (`obsidian-mcp@2.0.1`) | OK — working, 12 tools verified |
| canva | oauth | FAIL — 401, not authorized |
| cloudflare | oauth | FAIL — 401, not authorized |
| railway | oauth | FAIL — 401, not authorized |

Gateway itself is healthy: launchd plist `~/Library/LaunchAgents/ai.hermes.gateway.plist`
exists, process running, Hermes v0.22.2. (Note: the 2026-10-05 note claiming "no plist exists"
is now stale.)

---

## 3. WARN — Canva × Hermes automation: actual status

**2 of 25 tasks done.** The blocker is Ole, not the tooling.

**Done:**
- `D1-15` — Hermes config types fixed (obsidian-mcp args → YAML list, vault path → `~/Obsidian`,
  npm cache v1.0.6 → pinned `@2.0.1`). Verified: `Connected (2311ms)`, 12 tools.

**Stalled on four owner-only steps** (`~/Downloads/Canva_Fronty_Package/Canva_Fronty_Tracker.csv`):

| ID | Ole must do |
|----|-------------|
| D1-01 | Sign in at canva.com/developers (Olesya00007@gmail.com) |
| D1-02 | Create private app "Fronty Hermes Canva Connector" |
| D1-03 | Put Client ID + secret into `.env` |
| D1-07 | Click the Canva consent screen |

Everything downstream (`D1-08` … `D2-10`, 21 tasks) depends on these.

**The MCP URL itself is correct.** The 401 means "not authorized yet", not a config error —
both `.well-known` discovery documents return 200. See `2026-10-05-canva-fronty-intake-and-d1-15-fix.md`.

**Sequencing decision (Ole, 2026-10-05), still binding:** fix the aLEXy leak *before*
registering on Canva. That leak is still open — so Canva has been waiting on a 2-minute
credential revoke for ~2.5 weeks.

**Package path:** `~/Downloads/Canva_Fronty_Package/`
(Tracker CSV, Templates CSV, Field Contract CSV, `Fronty_Prompt.md`, `Smoothy_Final_Prompt.md`)

---

## 4. WARN — aLEXy Google API key leak is still live

- Repo `Ole00007/aLEXy` — **public**. File `test_gemini.py` line 3. Introduced in the initial
  commit 2026-07-21. **Never removed.** GitHub secret-scanning alert still open.
- Blast radius in the Hermes estate: **clear** — no `GOOGLE_*` / `GEMINI_*` key in any profile
  `.env`; google-provider profiles authenticate via OAuth. Rotating breaks nothing.
- **The fix is Ole's:** revoke at Google Cloud Console → Credentials. Automatable follow-ups
  (rewrite `test_gemini.py` to read env, add `.env` to `.gitignore`) need his yes.
- Detail: `~/Obsidian/01-Projects/aLEXy/2026-10-05-google-api-key-leak.md`

---

## 5. WARN — LexFlow CRM state

**Repo:** `/Users/olesiarasing/projects/lexflow-crm`

- OK — prod healthy: `curl https://web-production-031a6.up.railway.app/health` →
  `{"status":"ok","db":"ok","environment":"production"}`
- Branch `feat/progress-visualiser`, HEAD `62bf874` "standalone React app — make any project's
  progress visually obvious"
- WARN — canonical roadmap `docs/LexFlow_Agentic_Roadmap.json` has `last_updated: 2026-10-14`
  (**stale 7 days**). Columns: backlog 10, awaiting_confirmation 4, done 3, local_verified 2,
  blocked 1, deployed 1.
- WARN — dirty working tree: modified `apps/progress-visualiser/src/data/lexflow-roadmap.generated.json`;
  **deleted** `crm_local.db` and `data/app.db`; untracked `Frappe-Gantt/` and `backups/`.
  The DB deletions look accidental — check before committing anything.

**Kanban** (`~/.hermes/kanban.db`): 31 done, **18 blocked**, 5 todo, 1 running
(`t_7048b1a6` FRONTY Progress Visualiser), **0 ready**.

**Other repos** under `/Users/olesiarasing/projects/`: `lexflow-crm-t019`, `lexflow-website`,
`Avibe Agency`, `ENNEFEX`, `HOSPITALITY`, `LEGAL_backup`, `avibe-flowershop`, `avibe-hindsight`.

---

## 6. INFO — model on this profile

Current pin (`~/.hermes/profiles/smoothy_op_dir/config.yaml`):

```yaml
model:
  default: meituan/longcat-2.5-preview:free
  provider: nous
```

**Assessment (honest, from inside):** longcat is a free-tier model and was never in the original
profile spec — the spec names `anthropic/claude-opus-4.8` (nous) as the verified working
orchestrator. There is **no evidence of longcat completing a long autonomous multi-step task**:
the crons that would have exercised it have been failing on Telegram config for 2 weeks, so
"it works" is untested, not proven. It handled the multi-tool status pull that produced this
handover correctly — but that is a weak test.

**Recommendation:** pin this profile to `anthropic/claude-opus-4.8` (nous); keep longcat as a
cheap fallback for low-stakes profiles. Ole has said he will configure the change himself.

---

## Ordered next steps

1. **Fix Telegram delivery** — locate where the working profiles get their bot token, apply it
   to `smoothy_op_dir`, then confirm `lexflow-daily-status-crm` runs and lands.
2. **`hermes mcp login canva|cloudflare|railway`** — interactive; stops the 401 loop.
3. **Revoke the aLEXy Google key** — 2 minutes, ends a 2.5-month public exposure.
4. **Confirm the model change took effect** — `hermes -p smoothy_op_dir config get model.default`.
5. **Clean the LexFlow working tree** — restore or confirm the two deleted DBs before any commit.

**Hard rules that still bind:** never push without Ole's explicit per-push authorization;
never deploy without surfacing repo + branch + commit + target; one source of truth, no
duplicate registries or cards; every deliverable names its repo path.

---

## Links

- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[2026-10-05-canva-fronty-intake-and-d1-15-fix]]
- See also: [[2026-10-05-google-api-key-leak]]
- See also: [[LexFlow-INDEX]]
