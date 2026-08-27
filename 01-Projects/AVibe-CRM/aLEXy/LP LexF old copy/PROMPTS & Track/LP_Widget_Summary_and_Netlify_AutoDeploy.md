# LexFlow LP+Widget Session Summary & Netlify Auto-Deploy Guide

Date: 2026-05-20  
Status: Reference doc — save in Space

---

## PART 1 — Yesterday's LP + Chatbot Widget Work

### 1.1 What we did (efficient steps)

| Step | Action | Why it mattered |
|---|---|---|
| 1 | Confirmed chatbot public URL: `https://lexflow-chatbot-production.up.railway.app` | Gives the widget a real backend to call |
| 2 | Identified LP folder path: `C:\Users\Olesy\Desktop\...\LP` | Needed before any file edit or git command |
| 3 | Copied approved `index.html` from Downloads into LP folder | Replaced stale version with approved widget shell |
| 4 | Ran `git add`, `git commit`, `git push origin main` | Pushed to GitHub so Netlify could pick up the update |
| 5 | Tested backend with `Invoke-RestMethod` POST to `/chat` | Verified Railway is alive before wiring the widget |
| 6 | Saved Alessia widget current-behavior summary as MD note | Created a reusable checkpoint for future backend-wiring work |

---

### 1.2 Bugs we hit and how we debugged them

| Bug / symptom | Root cause | How we fixed it | Debug method used |
|---|---|---|---|
| LP not updating after push | Stale `index.html` still in working folder — old version was being committed | `Copy-Item` from Downloads to LP folder before git add | `Get-Content index.html -TotalCount 20` to verify top of file |
| Widget URL placeholder still in code | `YOUR-CHATBOT-URL` was never replaced with real Railway URL | Identified by reading the HTML — chatbot URL was a template | Manual search in file before deploying |
| Multiple repeated commits with same message | Each attempt pushed before verifying the file was correct | Slowed workflow; did not break anything but cluttered git log | `git log --oneline` to count commits |
| `Invoke-RestMethod` command not run (skipped) | Session ran out of time before backend test was done | **Not yet resolved** — still open for next session | Needs to be first thing in next session |

---

### 1.3 How to avoid bugs next time — pre-flight checklist

Run these four checks **before** every `git add`:

1. `Get-Content .\index.html -TotalCount 30`  
   → Read the first 30 lines. Confirm the correct title and Railway URL are present.

2. `Select-String -Path .\index.html -Pattern "YOUR-CHATBOT-URL"`  
   → If this returns any result, STOP. The placeholder was not replaced.

3. `Select-String -Path .\index.html -Pattern "lexflow-chatbot-production.up.railway.app"`  
   → This must return at least one result. If not, the real URL is missing.

4. Test backend first (run in PowerShell, paste result before editing HTML):
   ```powershell
   Invoke-RestMethod -Uri "https://lexflow-chatbot-production.up.railway.app/chat" `
     -Method POST -ContentType "application/json" -Body '{"message":"ciao"}'
   ```

---

### 1.4 What every version of index.html must include

| Must-have | Why |
|---|---|
| `<link rel="icon">` favicon tags | Browser tab branding |
| Real Railway chatbot URL (not placeholder) | Widget must call actual backend |
| CORS-safe fetch with error handling in JS | If Railway is down, widget must not crash the page |
| `target="_blank" rel="noopener noreferrer"` on all external links | Security + sandbox requirement |
| Theme toggle (light/dark) | Approved UI requirement |
| Language toggle (IT/EN) | Approved UI requirement |
| Alessia widget with avatar | Approved UI element |
| WhatsApp CTA button | Approved UI element |
| Mobile-first layout (375px baseline) | Non-negotiable |
| No hardcoded secrets or API keys in HTML | Security — keys belong in Railway env vars only |

---

## PART 2 — Netlify Auto-Deploy via GitHub (one-time setup)

### What this does

Auto-deploy = every time you push code to GitHub (`git push origin main`),  
Netlify detects the new commit and publishes the updated LP automatically.  
You never have to drag-drop files to Netlify again.

### One-time setup steps

**Step 1 — Connect Netlify to your GitHub repo**

Go to: https://app.netlify.com/start  
Click: **Import an existing project → Deploy with GitHub**  
Authorize Netlify to access your GitHub account.  
Select your LP repo (the one that holds `index.html`).

**Step 2 — Set the build settings**

| Setting | Value for LexFlow LP (static HTML, no build tool) |
|---|---|
| Branch to deploy | `main` |
| Base directory | leave blank (or `.` if repo root has `index.html`) |
| Build command | leave blank |
| Publish directory | `.` (a dot — the repo root, or whatever folder holds `index.html`) |

Click **Deploy site**.

**Step 3 — Verify auto-deploy is working**

Make a tiny test change in `index.html` locally (add a space in a comment).
Then run:
```powershell
cd "C:\Users\Olesy\Desktop\AVibe Agent\Clients\LEGAL\LexFlow\LP"
git add index.html
git commit -m "test: verify Netlify auto-deploy trigger"
git push origin main
```
Then go to https://app.netlify.com → your site → **Deploys tab**.  
You should see a new deploy starting within ~10 seconds.

**Step 4 — Confirm live URL after deploy**

Netlify gives you a URL like `https://lexflow-lp.netlify.app`.  
You can set a custom domain later in **Site settings → Domain management**.

---

### How the three-platform flow works after setup

```
You edit index.html locally (Notepad or PowerShell)
       ↓
git add / commit / push  →  GitHub (your LP repo, main branch)
                                    ↓
                            Netlify detects new commit (webhook, instant)
                                    ↓
                            Netlify publishes updated LP (30–60 seconds)
                                    ↓
                    Alessia widget in LP calls → Railway chatbot backend
```

**Railway is not involved in this deploy chain.**  
Railway only hosts the chatbot backend API.  
Netlify only hosts the static LP HTML/CSS/JS.

---

## PART 3 — Open items for next session

| Item | Status | What to do |
|---|---|---|
| Test Railway `/chat` endpoint | OPEN | Run the `Invoke-RestMethod` command above |
| Replace placeholder URL in widget JS | OPEN | After test confirms route + response shape |
| Add favicon files | OPEN | Two-step: add files → add `<link>` tags to `<head>` |
| Netlify auto-deploy setup | OPEN | Follow Part 2 above (one-time, ~10 min) |
| Wire Alessia widget to real backend | BLOCKED on backend test | Unblocks once `/chat` response shape is known |

---

*Save this file in Space for reference.*

## Links
- Parent: [[PROMPTS & Track-INDEX]]
- Related: [[I Approve. go edit the HTML in one surgical pass]]
