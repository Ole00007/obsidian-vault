# How to Change Your Hermes Model for VS Code

## The key idea

VS Code does not own the model setting. Hermes owns it. When you change the model — in Terminal, in the Hermes web dashboard, or in the Nous Portal — Hermes writes the new choice into one file on your Mac: `~/.hermes/config.yaml`. VS Code then reads it automatically when you start a **new session**.[cite:89][cite:77]

---

## Option 1: Change it in Terminal (fastest, most reliable)

1. Open **Terminal** on your Mac.
2. Type this and press Enter:
   ```bash
   hermes model
   ```
3. An interactive menu appears — use ↑↓ arrow keys to pick a provider and model.
4. Press Enter to confirm.
5. Close the old Hermes session in VS Code.
6. Start a **new** Hermes session in VS Code.

That is all. The new model is now active.[cite:89][cite:122]

---

## Option 2: Change it in the Hermes web dashboard

1. Open the Hermes dashboard in your browser. If you do not have the URL, run this in Terminal first to get it:
   ```bash
   hermes dashboard
   ```
2. In the dashboard, open the **Models** section.
3. Click **Change** next to the main model.
4. Pick your provider and model.
5. Click **Switch**.[cite:89]
6. Go back to VS Code and start a **new** Hermes session.

The dashboard and Terminal write to the same config file, so both methods produce the same result.[cite:89]

---

## Option 3: Change it in Nous Portal (your online account)

1. Open your browser and go to: **https://portal.nousresearch.com/**
2. Log in with your OAuth account (Google or GitHub).
3. In the portal, look for the **Models** or **Subscription** section.
4. Pick or change your preferred model.
5. Back in Terminal, run:
   ```bash
   hermes setup --portal
   ```
   This re-syncs your local Hermes with the portal settings.[cite:44][cite:123]
6. Start a new Hermes session in VS Code.

---

## Why VS Code may not recognize the change immediately

This is normal. The Hermes docs confirm that a model change applies to **new sessions only**. Any Hermes session already open in VS Code keeps the old model until you close it and start fresh.[cite:89]

Simple rule to remember:
- Old session open in VS Code → still old model.
- New session opened after config change → new model. ✓[cite:89][cite:77]

---

## Quick check: which model is Hermes using right now?

Run this in Terminal:
```bash
hermes config show
```
This prints the current active model and provider.[cite:89]

---

## Recommended beginner routine

Use these steps any time you need to switch:

| Step | Action | Where |
|------|--------|-------|
| 1 | Run `hermes model` | Terminal |
| 2 | Pick new provider/model | Terminal menu |
| 3 | Close old Hermes chat | VS Code |
| 4 | Open new Hermes session | VS Code |
| 5 | Verify with `hermes config show` if unsure | Terminal |

---

## My recommendation

Use **Option 1** (Terminal) as your daily go-to. It is the fastest, most direct, and is what the Hermes docs recommend as the primary path.[cite:89][cite:122] Use the dashboard or portal only if you prefer a visual interface — both write to the same file, so the result is identical.[cite:89]


## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[Hermes_Obsidian_Windows_Install_Guide]]
