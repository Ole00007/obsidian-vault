## Prompt to paste into Hermes (v5 — free-tier-only Gemini + task rerouting)

```
Task: Prepare (do NOT install/implement yet) the tools and skills needed for the
current learning scope: Resend (transactional email only), Railway (deploy CRM),
Cloudflare (DNS + CDN only), Penpot, Flask-SQLAlchemy/Alembic (database), the
named skill source below, and any GitHub-sourced skill referenced in
skill-gap-and-acquisition.json.

Named skill source to evaluate (human-identified, not auto-discovered):
- Author: Michael Shimeles (YouTube: @rasmic / Ras Mic)
- GitHub profile: https://github.com/michaelshimeles
- Skills repo: https://github.com/michaelshimeles/skills
- Also for reference: https://github.com/michaelshimeles/nextjs-starter-kit
No exemption from Step 4's safety scan.

Step 0 — Substitution rule (mandatory, before shortlisting anything):
- For each candidate skill/tool, check if it links to a PAID product.
- If it does, search for a free/open-source equivalent OR check if the same
  job can be done with something already in use: Canva (Pro), Penpot, Railway,
  Resend, Cloudflare, Gemini API (Free tier), Nous Hermes, OpenRouter (free
  models), Ollama, Obsidian, GitHub, VS Code, Hindsight.
- Priority order: (1) already in use > (2) free/open-source > (3) new paid —
  only propose (3) with explicit justification.

Step 1 — Model/task routing rule (mandatory — apply to EVERY task Hermes runs,
not just installs):
- Nightly cron digest (LexFlow/AVibe) and long legal-document summarization:
  route to Nous Hermes (self-hosted/free). Do NOT route these to Gemini.
- Swarm / multi-agent orchestration: route to OpenRouter free tier, model
  nvidia/nemotron-3-ultra-550b-a55b:free (built for long-horizon
  agents/orchestration, 1M context, free).
- Agentic coding / multi-file autonomous edits: route to OpenRouter free tier,
  model poolside/laguna-m.1:free (agentic coding, 262K context); use
  poolside/laguna-xs-2.1:free for lighter/faster tasks.
- Private/sensitive CRM code review: route to local Ollama (e.g. qwen3:8b),
  never send this code to any cloud API.
- Design copy, copywriting, SEO/GEO content, and light single-function code
  review ONLY: route to the Gemini API, and ONLY on the Free usage tier — do
  NOT enable Cloud Billing for this project. Confirm the project shows usage
  tier "Free" before making any Gemini call.
- Never route high-volume, repetitive, or unattended jobs through the Gemini
  Free-tier key — it has daily request limits that reset once per day and
  will be exhausted quickly by loops or batch jobs.

Step 2 — Google AI Studio prototyping (human-only step, not something Hermes
executes): I will manually draft and test prompts/function-calling schemas in
the AI Studio Playground using my Pro subscription quota — this never touches
API billing. Once I hand you a finalized prompt from that process, treat it as
final text to embed in your Free-tier Gemini API call; do not redesign it.

Step 3 — Check rules first (mandatory, before anything else):
Locate and read the general rules file that applies to the whole agent roster
(e.g. HERMES.md, CLAUDE.md, or equivalent root-level rules file in this repo).
Summarize any rule that restricts installs, network calls, credential handling,
or unattended writes. If no such file exists, tell me explicitly.

Step 4 — Kanban board separation (mandatory, before touching any code):
Create a NEW, separate project/board named "Learning & Skill Acquisition" in
the CRM's Kanban tool, with columns: Backlog, Researching (GitHub search),
Safety scan pending, Approved - implementing, Done - logged in Obsidian.
Do NOT add its cards to the existing LexFlow CRM build board. Cross-link only
via a text tag (e.g. "blocks: CRM-upgrade"). Confirm the exact board/columns.

Step 5 — Hard safety rule (non-negotiable, every dependency/skill, including
everything inside michaelshimeles/skills):
- Never download or run third-party code before it has been scanned.
- Required scanner: Microsoft Application Inspector
  (https://github.com/microsoft/ApplicationInspector).
- Install if missing: dotnet tool install --global Microsoft.CST.ApplicationInspector.CLI
- Run before cloning into a real folder: appinspector analyze -s <path> -f json
- If it flags unexplained network calls, shell/OS execution, or obfuscated
  code, STOP and report — do not proceed automatically.

Step 6 — Do not auto-implement. For each tool/skill, give me:
1. Exact GitHub repo URL (+ sub-path if inside a bigger repo).
2. Exact local path it WOULD be cloned to (don't create it yet).
3. Application Inspector scan summary from a throwaway temp clone only.
4. Which Kanban card it's tracked under.
5. Step 0 substitution verdict.
6. Which model/provider (per Step 1) this task should run on, and why.

Step 7 — Wait. Present everything to me and my tutor before any real install,
clone into a working folder, billing change, or code change happens.
```

## What changed from v4

- **Step 1 is new**: an explicit, non-negotiable routing table so Hermes never sends nightly digests or long-document summarization to Gemini (those stay on your already-free Nous Hermes), and never runs swarm/agentic-coding loops against the Gemini free key (those go to free OpenRouter models built for exactly that job).
- **Step 2 clarifies the AI Studio handoff**: it's explicitly a human-only manual step, not something Hermes does — Hermes only receives the finished prompt text afterward.
- **Gemini is now scoped to Free-tier only, no billing**, for design/copy/SEO/light code review — matching your instruction to preserve free API calls at the start.
