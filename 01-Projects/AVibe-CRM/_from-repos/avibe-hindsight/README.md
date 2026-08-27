# avibe-hq — Hindsight on Railway (PoC)

Lightweight project to deploy Hindsight on Railway and connect Hermes + Obsidian.

Prerequisites
- Railway account and optional `railway` CLI (`npm i -g @railway/cli`).
- `docker` installed locally (for local image build / Railway deploy-from-dockerfile flows).
- `python3.11` and `pip` for helper scripts.

Quick steps
1. Create Railway project (dashboard or `railway init avibe-hq`).
2. Add PostgreSQL plugin in Railway dashboard; note `DATABASE_URL` provided.
3. Deploy the service from this repo (use `railway up` or Deploy from GitHub). The service exposes port `8000` by default.
4. In Railway Service Variables, set:
   - `HINDSIGHT_API_KEY` (generate locally: `openssl rand -hex 32`).
   - `HINDSIGHT_API_LLM_API_KEY` (optional — your LLM provider key).
   - Leave `DATABASE_URL` as provided by Railway.
5. Verify:
   ```bash
   curl -H "Authorization: Bearer <HINDSIGHT_API_KEY>" https://<your-railway-domain>/health
   ```
6. Configure Hermes on each device with API URL `https://<your-railway-domain>`, API key, and bank `avibe-hq`.
7. Configure Obsidian Hindsight plugin with the same URL/key/bank.
8. Backup Postgres for migration later:
   ```bash
   pg_dump "$DATABASE_URL" > avibe-hq-hindsight.sql
   ```

Files in this repo
- `Dockerfile` — minimal runtime to run `hindsight-api` from `hindsight-all` Python package.
- `railway.json` — optional Railway service metadata.
- `env.example` — environment variables template.
- `deploy.sh` — helper script (edit before running).
- `scripts/hindsight_client.py` — small Python client examples.
- `scripts/snapshot_to_obsidian.py` — convert a newline-delimited JSON snapshot to an Obsidian vault structure.
- `obsidian/templates/hindsight-convo-template.md` — Obsidian note template for conversations.

Security notes
- Railway domains are public by default. Enforce `HINDSIGHT_API_KEY` and do not share it.
- Do not store secrets in checked-in files. Use Railway Service Variables.

If you want, I can: (A) create a Git repository and push these files to GitHub (I will provide commands you run), or (B) prepare a CI pipeline for automatic builds. Which do you want next?