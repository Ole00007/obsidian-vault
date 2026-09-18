# Smoothy Prompt — Free Model Audit for Cron Sentinel

> **Run in terminal first:** `smoothy`
>
> If `smoothy` is not recognized, start the terminal application/command you normally use for Smoothy, then paste the prompt below.

```text
Perform a READ-ONLY audit for a proposed LexFlow Cron Sentinel agent. Do not download models, create an agent, change settings, start persistent services, or alter files/configuration.

Check whether Ollama is installed and usable. Run `ollama ls` to list downloaded local models and `ollama ps` to list loaded models. If no local model is installed, state exactly: “Ollama application installed; no local LLM model currently available.”

For each local model found, report its exact tag, approximate size, suitability for concise daily operational summaries and log/error interpretation, and tool/function-calling support if verifiable.

Then check the live current free Nous Portal / Hermes-compatible model catalog. Free-only is mandatory for now. Recommend one main model and three ranked free fallbacks for: daily summaries, GitHub/Cloudflare log analysis, and English/Italian mixed notes. Do not guess model IDs; validate that the models are currently free.

Cron Sentinel will be read-only. It may later summarize approved agent sessions, GitHub Actions logs, Cloudflare telemetry, approved read-only Obsidian notes, and exported LexFlow CSV/JSON task snapshots. It must never access, inspect, modify, or summarize Memory Curator systems, files, prompts, skills, or sync jobs.

Return only these headings:
- Ollama Status
- Local Models
- Recommended Free-Only Model Policy
- Three Free Fallbacks
- Future Anthropic Migration Note
- No-Change Confirmation

The final line must state every change made. Expected: “No changes made.”
```