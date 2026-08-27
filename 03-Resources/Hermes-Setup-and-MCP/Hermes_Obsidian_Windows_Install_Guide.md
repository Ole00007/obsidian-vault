# Hermes + Obsidian Installation Guide — Windows PC (Asus Zen, 32GB RAM)

> Save this file and follow top to bottom on the second PC. Primary OS: Windows (Microsoft Office machine, native Windows — no WSL required).

---

## PART 1 — Install BEFORE Hermes (prerequisites, most necessary first)

These are apps/programs Hermes itself needs to even install. Do these first, in this order.

1. **Git for Windows** — required first; Hermes installer needs `git` on PATH.
   - Download: https://git-scm.com/download/win
   - Verify after install: open PowerShell, run `git --version`

2. **Windows Terminal** (recommended over legacy cmd.exe — supports UTF-8, Ctrl+Enter for multi-line prompts).
   - Install from Microsoft Store: https://apps.microsoft.com/detail/9n0dx20hk701
   - Usually pre-installed on Windows 11

3. **PowerShell 7+** (modern PowerShell, not the old Windows PowerShell 5.1).
   - Download: https://github.com/PowerShell/PowerShell/releases/latest
   - Optional but smoother than default PowerShell

That's it — everything else (Python 3.11, Node.js 22, ripgrep, ffmpeg, PortableGit, uv) is auto-installed by the Hermes installer itself. You do NOT need to manually install Python or Node.js first — the installer bootstraps them for you.

Reference: https://hermes-agent.nousresearch.com/docs/getting-started/installation

---

## PART 2 — Install Hermes Agent

1. Open **PowerShell** (new window, after Git install).
2. Run the one-liner installer:
   ```
   iex (irm https://hermes-agent.nousresearch.com/install.ps1)
   ```
   No admin rights required. Installs to `%LOCALAPPDATA%\hermes\`.
3. **Close and reopen PowerShell** (PATH won't update in the same window).
4. Verify:
   ```
   Get-Command hermes
   hermes --version
   ```
5. Run the fast setup (covers model provider + Tool Gateway in one command):
   ```
   hermes setup --portal
   ```
6. Start chatting to confirm it works:
   ```
   hermes
   ```

Alternative: if you'd rather double-click an installer instead of using PowerShell, download **Hermes Desktop** (GUI installer) from the same site — it runs the same script under the hood.

**Video guide:** Hermes Agent: The Ultimate Beginner's Guide — https://www.youtube.com/watch?v=CwPUOVUdApE
**Docs:** https://hermes-agent.nousresearch.com/docs/getting-started/installation
**Windows-specific deep dive:** https://hermes-agent.nousresearch.com/docs/user-guide/windows-native

---

## PART 3 — Install Obsidian + Everything Else VIA Hermes

Once Hermes is confirmed working (`hermes` responds to chat), do NOT manually install Obsidian, BRAT, or the Hermes Obsidian plugin one by one. Instead, hand Hermes the prompt below and let it walk you through it (or do it for you, tool-by-tool, with your confirmation at each step).

### What Hermes will help install next (in this order):
1. Obsidian desktop app (Windows)
2. BRAT plugin (inside Obsidian, community plugins)
3. Hermes Agent Obsidian plugin (via BRAT)
4. Filesystem MCP server config, scoped to your vault folder

---

## PART 4 — Prompt to Give Hermes (paste this into `hermes` chat)

```
I just installed you (Hermes Agent) on my new Windows PC (Asus Zen, 32GB RAM, 
native Windows, no WSL). I want you to help me set up Obsidian integration, 
step by step, asking me to confirm before each action.

1. Tell me the exact download link and steps to install Obsidian for Windows.
2. Once I confirm Obsidian is installed, walk me through installing the BRAT 
   plugin inside Obsidian (Settings > Community plugins).
3. Then walk me through installing the "Hermes Agent" Obsidian plugin via BRAT.
4. Then help me create a scoped Filesystem MCP entry in my config.yaml 
   (%LOCALAPPDATA%\hermes\config.yaml) pointing only at a single Obsidian 
   vault subfolder — do not give yourself access to my whole file system.
5. After each step, run `hermes doctor` (or ask me to run it) and tell me 
   if anything is misconfigured before moving to the next step.
6. Do not install anything without telling me exactly what you're about to 
   do first. Summarize what changed after each step.
```

---

## Quick Reference Table

| Step | What | Link |
|---|---|---|
| 1 | Git for Windows | https://git-scm.com/download/win |
| 2 | Windows Terminal | https://apps.microsoft.com/detail/9n0dx20hk701 |
| 3 | PowerShell 7+ | https://github.com/PowerShell/PowerShell/releases/latest |
| 4 | Hermes Agent installer | https://hermes-agent.nousresearch.com/install.ps1 |
| 5 | Hermes docs | https://hermes-agent.nousresearch.com/docs/getting-started/installation |
| 6 | Hermes Windows guide | https://hermes-agent.nousresearch.com/docs/user-guide/windows-native |
| 7 | Beginner video | https://www.youtube.com/watch?v=CwPUOVUdApE |
| 8 | Obsidian download | https://obsidian.md/ |
| 9 | Hermes Agent Obsidian plugin | https://community.obsidian.md/plugins/hermes-agent |
| 10 | BRAT plugin | https://community.obsidian.md/plugins/obsidian42-brat |

## Links
- Parent: [[Hermes-Setup-and-MCP-INDEX]]
- Related: [[Obsidian_Hermes_Vault_Strategy_AllSheets]]
