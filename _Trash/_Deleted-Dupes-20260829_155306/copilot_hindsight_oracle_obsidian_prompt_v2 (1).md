# Copilot Prompt v2 — Phased Deploy of Self-Hosted Hindsight on Oracle Free Tier

## Context
Oracle Cloud Always Free Ampere A1 instance (4 OCPU / 24GB RAM / Ubuntu), for self-hosted Hindsight (vectorize-io/hindsight, MIT) as shared memory for Hermes Agent + Obsidian across up to 4 devices, initially used by me and possibly one colleague. Later this server will also back a CRM used by real legal-firm clients, so security must escalate in phases.

Shared memory bank name to use everywhere, exactly as written, case-sensitive: `avibe-hq`
(Later, for client data: a second bank `avibe-clients` — do not mix the two.)

## Phase 1 — Personal/colleague use, low stakes, get running fast

1. On the Oracle Console, add a Security List ingress rule for TCP port 8888, but restrict the Source CIDR to only my current public IP and my colleague's public IP (not 0.0.0.0/0). Tell me the exact syntax for a single-IP CIDR (e.g. `x.x.x.x/32`).
2. SSH in, install Docker: `sudo apt update && sudo apt install docker.io docker-compose-plugin -y`.
3. Install Hindsight: `pip install hindsight-all`.
4. Set env vars before starting:
   - `HINDSIGHT_API_LLM_API_KEY=<my-llm-key-or-local-ollama-endpoint>`
   - `HINDSIGHT_API_KEY=<a-strong-random-key-I-generate>` — this protects the bare-HTTP endpoint with a required header even before TLS is added.
5. Run `hindsight-api` as a systemd service (not a raw terminal session) so it survives reboot/disconnect. Give me the full unit file.
6. Verify from my laptop: `curl -H "Authorization: Bearer <key>" http://<oracle-ip>:8888/health`.
7. Configure Hermes on each device: `hermes memory setup` → Hindsight → Local External → API URL `http://<oracle-ip>:8888` → API key from step 4 → bank id `avibe-hq`.
8. Configure Obsidian on each device: install Hindsight plugin via BRAT (`vectorize-io/hindsight-obsidian`) → Settings → Hindsight → API URL `http://<oracle-ip>:8888` → API key from step 4 → Bank name `avibe-hq`. Do not rename the vault or any Hermes agent — this bank field is independent config, not an identity change.
9. Test: store a note/fact on device A, recall it in a fresh session on device B, confirm it works before trusting the setup.

## Phase 2 — Before onboarding real legal-firm clients (do this before any client data touches the server)

1. Harden `iptables`/`ufw` on the instance itself to only allow inbound traffic on the reverse-proxy port (443), closing the direct 8888 access from Phase 1.
2. Install Nginx or Caddy as a reverse proxy in front of Hindsight, with Let's Encrypt TLS on a real domain/subdomain I own.
3. Move the `HINDSIGHT_API_KEY` check to the proxy layer as well (defense in depth), and reissue a new key (don't reuse the Phase 1 one).
4. Update the Security List ingress rule to allow 443 from anywhere (0.0.0.0/0) since TLS + auth now protect it, and remove the old port-8888 rule entirely.
5. Update every device's Hermes and Obsidian config to use the new HTTPS domain URL instead of the raw IP:8888.
6. Create the second bank `avibe-clients` and set up a clear rule (in Hermes config or a wrapper script) so any session tagged as client/CRM work writes to `avibe-clients`, never `avibe-hq`.
7. Document data-retention and access-control basics for the client bank (who can query it, how long data is kept) since this now involves third-party client confidentiality.

## Output I need from Copilot
- Exact commands for every numbered step, in order, for both phases.
- The systemd unit file for Hindsight.
- The Nginx/Caddy config with TLS for Phase 2.
- Explicitly tell me if Phase 1's bare-HTTP + IP-allowlist + API-key setup is not safe enough for any specific action I describe, before I take that action.
- Do not let me put real client data into `avibe-hq` — warn me if a step looks like it would.

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[copilot_hindsight_oracle_obsidian_prompt]]
