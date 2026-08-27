# Obsidian Integration Notes (avibe-hq)

This folder contains guidance for connecting Obsidian to the Hindsight service for the `avibe-hq` bank.

Setup summary
1. Install BRAT and the Hindsight Obsidian plugin (`vectorize-io/hindsight-obsidian`).
2. In the plugin settings, set:
   - API URL: `https://<your-railway-domain>`
   - API Key: `<HINDSIGHT_API_KEY>`
   - Bank: `avibe-hq`
3. Place the `obsidian/templates/hindsight-convo-template.md` in your vault's Templates folder and use it for new conversations.

Dataview examples
- Show recent Hermes notes:

```dataview
table title, date, tags, last_synced
from "Hermes"
sort date desc
limit 50
```

Re-ingest workflow (when you edit a note locally and want to push changes back to Hindsight)
1. Use `scripts/obsidian_reingest.py` to send edited notes as new records (adds metadata `source: obsidian-edit` and `original_id`).
2. Run in dry-run first:

```bash
python3 scripts/obsidian_reingest.py --vault /path/to/vault --bank avibe-hq --api-url https://<your-railway-domain> --api-key <key> --dry-run
```

3. If output looks good, run without `--dry-run` to create new records in Hindsight.

Notes
- Edits are appended as new records to preserve an append-only audit trail in Hindsight.
- For high-volume or automated re-ingest, consider batching or adding rate-limiting to avoid hitting service quotas.
