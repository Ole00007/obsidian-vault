---
title: avibe-hindsight (graceful-presence) — Network Egress & Internal Networking Audit
created: 2026-09-21
tags: [railway, network, egress, avibe-hindsight, audit, graceful-presence]
status: proposal-pending-approval
---

# avibe-hindsight (graceful-presence) — Network Egress & Internal Networking Audit — 2026-09-21

- **Project:** graceful-presence — https://railway.app/project/9b08be93-b288-4772-8ccc-29b724851bf0
- **Services:** `avibe-hindsight` (415d2f9a-8e64-46f9-a943-3f4d79831d54), `Postgres` (7434336d-74b5-434d-899a-a54237eea392). **No Hermes service exists in this project.**
- **Environment:** `production` only (9d75ea4a-b853-442d-a363-25a181446f91), `isEphemeral: false`
- **Method:** Railway CLI 5.45.10 + GraphQL via `railway api`, deploy/build/network/DNS logs, `railway metrics --network --json --raw`, `railway usage --json`. **Read-only — no changes made.** Secrets redacted.
- **Status of this note:** findings + proposals only. Nothing executed (§15 convention: share first, wire after approval).

---

## Checklist

### 1. Every URL / connection string across all services — host class flagged

**avibe-hindsight**

| Variable | Value | Host class | Verdict |
|---|---|---|---|
| `HINDSIGHT_API_DATABASE_URL` | `postgresql://postgres:<redacted>@postgres.railway.internal:5432/railway` | `*.railway.internal` | ✅ private |
| `HINDSIGHT_API_LLM_BASE_URL` | `https://openrouter.ai/api/v1` | public, 3rd-party | ✅ required — cannot be internal |
| `RAILWAY_PRIVATE_DOMAIN` | `avibe-hindsight.railway.internal` | `*.railway.internal` | ✅ private |
| `RAILWAY_PUBLIC_DOMAIN` | `avibe-hindsight-production.up.railway.app` | `*.up.railway.app` | ⚠️ Railway-injected metadata, not a connection string |
| `RAILWAY_STATIC_URL` | `avibe-hindsight-production.up.railway.app` | `*.up.railway.app` | ⚠️ Railway-injected metadata |
| `RAILWAY_SERVICE_AVIBE_HINDSIGHT_URL` | `avibe-hindsight-production.up.railway.app` | `*.up.railway.app` | ⚠️ **user-created, NOT Railway-reserved** — see §5 |

**Postgres**

| Variable | Value | Host class | Verdict |
|---|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:<redacted>@postgres.railway.internal:5432/railway` | `*.railway.internal` | ✅ private |
| `PGHOST` | `postgres.railway.internal` | `*.railway.internal` | ✅ private |
| `RAILWAY_SERVICE_AVIBE_HINDSIGHT_URL` | `avibe-hindsight-production.up.railway.app` | `*.up.railway.app` | ⚠️ same user var duplicated into this service |

**Result: zero public IPs anywhere. Zero inter-service URLs pointing at `*.up.railway.app`.** The only public hostnames present are (a) Railway's own injected `RAILWAY_PUBLIC_DOMAIN` / `RAILWAY_STATIC_URL` metadata strings and (b) one user-made variable (`RAILWAY_SERVICE_AVIBE_HINDSIGHT_URL`) that nothing reads.

### 2. Where `HINDSIGHT_API_DATABASE_URL` points — shared Postgres or embedded volume?

**→ Shared Postgres service, over private networking. Not the embedded volume.**

| Evidence | Source |
|---|---|
| Startup: `Database: postgresql://***:***@postgres.railway.internal:5432/railway (schema: public)` @ 2026-09-20 06:15:26 | deploy log |
| `hindsight_api.migrations - Database migrations completed successfully for schema 'public'` → `Using vector extension: pgvector` | deploy log |
| **Zero** `pg0` / `embedded` log lines, despite the image shipping `pg0-embedded==0.15.1` and creating `/home/hindsight/.pg0` | deploy log |
| DNS: only `postgres.railway.internal` resolved (A `10.239.68.52`, AAAA `fd12:7651:4d44:1:d000:da:4aef:4434`), zone `internal`, RCODE NOERROR | `--dns` logs |
| Egress flows: TCP → peer kind **`Service`**, port **5432**, private IPv6 dest, 0 ms, status OK | `--network` logs |
| `railway private-network status`: both services on network `railway` (83ed7964-d656-42a1-aa71-3bcf34530c15), DNS suffix `railway.internal`, **Status: ready** | CLI |

**Private networking confirmed in use.** The Dockerfile's pg0/embedded-Postgres scaffolding is dead weight in production (a fallback that never fires because `HINDSIGHT_API_DATABASE_URL` is set).

### 3. External downloads on every container start

**Build-time (baked into the image layer — NOT repeated per start):**
- `apt-get install libssl3 libgssapi-krb5-2 tzdata libreadline8`
- `pip install --no-cache-dir hindsight-all` → pulls `hindsight-all 0.9.2`, `torch 2.13.0`, `transformers 5.15.1`, `sentence-transformers 6.0.0`, `onnxruntime`, `huggingface-hub 1.29.0`, `flashrank`, `mlx`, nvidia CUDA stack.

**Runtime, at process start (the real repeat egress) — observed 2026-09-20 06:15:32:**

| Log line | Meaning |
|---|---|
| `Embeddings: initializing local provider with model BAAI/bge-small-en-v1.5` | embedding model fetch |
| `Reranker: initializing local provider with model cross-encoder/ms-marco-MiniLM-L-6-v2` | reranker model fetch |
| `huggingface_hub.utils._http - Warning: You are sending unauthenticated requests to the HF Hub` | **proof of live HF Hub egress** |
| `Loading SentenceTransformer model from BAAI/bge-small-en-v1.5.` | weights load |

**File sizes (HuggingFace API, `?blobs=true` — authoritative):**

| Model | Main weight file | Whole repo (all blobs) |
|---|---|---|
| `BAAI/bge-small-en-v1.5` | `model.safetensors` **133.5 MB** (`pytorch_model.bin` 133.5 MB, `onnx/model.onnx` 133.1 MB) | 382.5 MB |
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | `model.safetensors` **90.9 MB** (`pytorch_model.bin` 90.9 MB; 4× ONNX ~91 MB each) | 848.9 MB |

**Minimum per cold start ≈ 224 MB.** Measured actual: **357.9 MB RX burst** in the 2026-08-28 20:00 bucket (matches the 2026-08-28 21:11 deploy).

**Can it be cached? Yes — and it is not, today.**
- avibe-hindsight has **no attached volume** (only Postgres has one) → `HF_HOME` / `~/.cache/huggingface` lives on the ephemeral container layer → wiped on every new deployment.
- Observed: the 2026-09-20 in-place restart re-initialised the models **without** a large RX burst (~20 MB bucket), i.e. the cache survived a process restart but does **not** survive a new deployment. Every redeploy pays the full download again (19 prior deployments in the retained history).

**Fix options (proposal only):**
- **(a) Best — bake into the image.** Add to `Dockerfile` after the `pip install` line:
  `RUN python -c "from sentence_transformers import SentenceTransformer, CrossEncoder; SentenceTransformer('BAAI/bge-small-en-v1.5'); CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"` — ~224 MB into a cached image layer, **zero** runtime fetch, removes a startup dependency and a network failure mode.
- **(b) Persistent volume.** Attach a Railway volume at `/home/hindsight/.cache/huggingface` and set `HF_HOME=/home/hindsight/.cache/huggingface`. Keeps the image small; pays one download per volume lifetime.
- Both are **tier-2 infra changes** → propose, then wait for Ole.

### 4. PR / preview environments (Project Settings → Environments)

| Check | Result |
|---|---|
| `project.prDeploys` (GraphQL) | **`false`** → **"Enable PR Environments" is OFF** |
| Environments in project | **1** — `production` (created 2026-08-14), `isEphemeral: false` |
| Active ephemeral PR environments | **0 — none running** |

Nothing to clean up: with `prDeploys: false` this project cannot spawn ephemeral PR environments, and none are currently attached to any open PR.

### 5. Total estimated egress reduction if all public inter-service URLs are switched to `*.railway.internal`

**Honest headline: 0 MB — there is nothing to switch.** Every inter-service connection string in this project already uses `*.railway.internal`. The premise of the question does not hold here; this project is already fully private east-west. Confirmed three independent ways (env values, DNS zone `internal`, egress flows all to peer kind `Service`).

**Measured network reality (30-day window 2026-08-22 → 2026-09-21, `railway metrics --network --raw`, 4-hour buckets):**

| Direction | Total | Largest burst | Burst cause |
|---|---|---|---|
| Egress (TX) | **1,160.8 MB** | 337.9 MB (2026-09-16 16:00) | vault ingestion → LLM calls (09-16→09-17 ≈ 1,032 MB total) |
| Ingress (RX) | **518.5 MB** | **357.9 MB** (2026-08-28 20:00) | HF cold-start model download |

Billed period (Sep 15 – Oct 15): avibe-hindsight **egress $0.0511** (~1 GB @ ~$0.05/GB) · project total **$9.46**.

**Exact before/after variable values:**

| # | Service | Variable | Before | After | Net effect |
|---|---|---|---|---|---|
| 1 | avibe-hindsight | `HINDSIGHT_API_DATABASE_URL` | `postgresql://postgres:<redacted>@postgres.railway.internal:5432/railway` | **unchanged** | already private — 0 MB |
| 2 | Postgres | `DATABASE_URL` | `postgresql://postgres:<redacted>@postgres.railway.internal:5432/railway` | **unchanged** | already private — 0 MB |
| 3 | Postgres | `PGHOST` | `postgres.railway.internal` | **unchanged** | already private — 0 MB |
| 4 | avibe-hindsight **and** Postgres | `RAILWAY_SERVICE_AVIBE_HINDSIGHT_URL` | `avibe-hindsight-production.up.railway.app` | **delete it**, or `avibe-hindsight.railway.internal` | a user-created variable (not Railway-reserved), read by no code in the repo → **0 MB either way**; deleting it just removes a public hostname from the variable surface |
| 5 | avibe-hindsight | `HINDSIGHT_API_LLM_BASE_URL` | `https://openrouter.ai/api/v1` | **unchanged** | external LLM API — cannot be internal |

**Therefore the reducible network item is the HF model fetch (~224 MB minimum / 358 MB measured per cold container start), not any URL.** Note honestly: that fetch is **ingress**, and Railway bills **egress**, so fixing it cuts ~224 MB of network per deploy and removes a startup failure mode — it will **not** move the bill.

---

## Cost reality-check (out of scope, but material)

| Line | Cost | Share |
|---|---|---|
| avibe-hindsight **memory** | **$8.76** | 93% of service cost |
| avibe-hindsight CPU | $0.0708 | <1% |
| avibe-hindsight **egress** | **$0.0511** | 0.5% |
| Postgres total | $0.5725 | 6% |
| Project total | **$9.46** | — |

Optimising egress here is chasing 5 cents. The lever is **memory** (worker stats: `rss_mb=1976 peak_rss_mb=2655`), which is a separate, larger conversation.

## Incidental findings

- **Orphaned volume:** `postgres-volume` is detached, 134 MB / 5000 MB, still accruing charge (visible as the `deleted service` line, $0.0038). Candidate for review.
- **Status oddity:** `railway status` reports avibe-hindsight as `● Completed` while its worker logs stream live — cosmetic; the service is healthy.
- **Single shared DB secret:** the same password appears in `DATABASE_URL`, `PGPASSWORD` and `POSTGRES_PASSWORD`; the DB is only reachable over the private network, so blast radius is contained.

## Links
- Parent: [[AVibe-CRM-INDEX]]
- Related: [[Hindsight-Read-Auth-Runbook]]
- Related: [[hermes_rules_avibe_hindsight]]
- Related: [[Hindsight-Vault-Sync-Fix-2026-09-16]]
- Related: [[2026-09-21]]
