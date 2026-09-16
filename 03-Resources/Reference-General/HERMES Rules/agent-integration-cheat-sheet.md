# Integrating an AI Agent into a Modern Web App / CRM — One-Page Cheat Sheet

## Core idea
An "agent" is a program that can decide what to do, call tools, and act — not just answer a question. Integrating one into a web app means giving it a **door in** (an API endpoint or webhook), **memory** (what it should remember), and **limits** (what it's allowed to do).

## The 5 building blocks

- **Trigger** — what starts the agent: a user action (form submit), a schedule (cron), or another system's webhook.
- **Endpoint** — the specific URL in your Flask app the trigger calls, e.g. `POST /api/agent/handle-lead`.
- **Agent logic** — the code that decides what to do: call Gemini/Hermes, read the request, produce a result.
- **Memory** — where facts persist between calls: your database (SQLAlchemy), or a dedicated tool like Hindsight for agent memory.
- **Output/action** — what happens next: write to the database, send an email, update a CRM record, or just return JSON to the frontend.

## Minimal integration pattern (Flask + agent)

```python
@app.route("/api/agent/handle-lead", methods=["POST"])
def handle_lead():
    data = request.get_json()          # 1. receive trigger data
    result = run_agent(data)           # 2. agent logic decides + acts
    db.session.add(Lead(**result))     # 3. persist to CRM database
    db.session.commit()
    return jsonify({"status": "ok", "result": result})  # 4. respond
```

## Scheduling agent work (cron)

- **Cron** = a scheduler that runs a command automatically at fixed times. [web:81][web:90]
- On Mac/Linux: `crontab -e` opens your schedule file; `crontab -l` lists it. [web:81]
- Syntax: `minute hour day month weekday command`
  Example — run a digest script every night at 22:00:
  ```
  0 22 * * * /usr/bin/python3 /path/to/nightly_digest.py
  ```
- Use [crontab.guru](https://crontab.guru/) to build/verify the schedule expression before deploying it. [web:88]
- Matches your "Nightly LexFlow and AVibe digest" pilot: start the job, let it run, stop it — don't leave it always-on until validated.

## When one agent isn't enough: swarm / multi-agent orchestration

- **Multi-agent orchestration** = coordinating several specialized agents (e.g., a research agent + a writer agent) that hand off tasks to each other. [web:89]
- **OpenAI Swarm** — lightweight, experimental framework using `Agents` + handoffs for coordination. [web:83]
- **Swarms (kyegomez)** — enterprise-grade multi-agent framework with tool integration and orchestration at scale. [web:85]
- Rule of thumb: don't reach for a swarm framework until a single agent + clear tool calls genuinely can't handle the task — added coordination layers add failure points.

## Security rules (non-negotiable)

- Never let an agent get unattended write access to production — require human approval on merges/deploys (matches your own decision rule).
- Keep API keys and secrets in `.env`, never in code pushed to GitHub.
- Give the agent the minimum tool permissions it needs for one task, not blanket access.
- Log every agent action somewhere reviewable (Obsidian notes, database table, or Hindsight memory).

## Your next concrete step

Pick **one** real endpoint in your CRM Flask app (e.g., new lead submitted) and wire it to call Hermes with the pattern above — start read-only (agent suggests, human approves) before granting any write action.
