# Copilot Prompt — Deploy Self-Hosted Hindsight on Oracle Cloud Free Tier + Connect to Obsidian & Hermes

## Context
I have an Oracle Cloud Always Free Ampere A1 instance (4 OCPU / 24GB RAM / Ubuntu) that I can SSH into. I want to self-host Hindsight (vectorize-io/hindsight, MIT licensed, https://github.com/vectorize-io/hindsight) on it as a persistent, always-on memory backend for Hermes Agent and Obsidian across 4 devices (2 laptops, 2 phones/tablets).

## Task 1 — Provision the server
1. SSH into the Oracle instance and update the system: `sudo apt update && sudo apt upgrade -y`.
2. Open the required ports:
   - In the Oracle Cloud Console, add an Ingress Rule on the instance's subnet security list allowing TCP on the port Hindsight will use (e.g. 8888) and 443/80 if I add HTTPS.
   - On the instance itself, update `iptables`/`ufw` to allow the same ports (Oracle images block inbound traffic by default even after the console rule is added).
3. Install Docker and Docker Compose: `sudo apt install docker.io docker-compose-plugin -y`, then enable Docker on boot.

## Task 2 — Install and run Hindsight
1. Install Hindsight with all features: `pip install hindsight-all` (or use the official Docker image if one exists in the repo — check `github.com/vectorize-io/hindsight` for a `docker-compose.yml`).
2. Set the LLM key for fact extraction/synthesis as an environment variable: `export HINDSIGHT_API_LLM_API_KEY=<my-key>`. If I want zero API cost, help me configure it to point at a local Ollama instance running on the same VPS instead of a paid provider.
3. Run the API server as a persistent background service (systemd unit, not just a terminal session) so it survives reboots and SSH disconnects: `hindsight-api` wrapped in a systemd service file.
4. Verify it's reachable: `curl http://<oracle-public-ip>:8888/health` (or the correct health endpoint) from my local machine.
5. Set up a reverse proxy (Caddy or Nginx) in front of it with a free domain/subdomain and Let's Encrypt TLS, so I'm not exposing raw HTTP with an unauthenticated port to the internet. Add basic auth or an API key requirement at the proxy layer as a safety net.

## Task 3 — Connect Hermes (on each of my 4 devices)
1. Run `hermes memory setup`, select Hindsight, choose the "Local External" mode.
2. Configure the API URL to point at my Oracle server's domain (from the reverse proxy step), not the raw IP.
3. Use the same bank ID on every device configuration — call it `avibe-personal` — so all devices share one memory graph.
4. Confirm recall works by storing a fact on one device and recalling it in a fresh session on another.

## Task 4 — Connect Obsidian (on each device's vault)
1. Install the Hindsight community plugin via BRAT, pointing at `vectorize-io/hindsight-obsidian`.
2. In Settings → Hindsight, set API URL to the same Oracle server domain and bank name to `avibe-personal` (same bank as Hermes, so both tools share the exact same memory).
3. Run "Sync vault now" and confirm the chat panel returns grounded answers with citations back to specific notes.

## Output I need from you
- The exact shell commands for each step above, in order.
- The systemd unit file content for keeping Hindsight running.
- The Nginx or Caddy config for the reverse proxy + TLS.
- Flag anywhere I need to substitute my own values (IP, domain, API keys) with a clear placeholder.
- Warn me if any step risks exposing the memory server insecurely to the public internet, and propose the safer alternative before I execute it.

## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[copilot_hindsight_oracle_obsidian_prompt_v2 (1)]]
