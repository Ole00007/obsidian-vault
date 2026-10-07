# Smoothy: Google API key leak fix

## GOAL (fixed)
A Google API key may be exposed in GitHub code. End state, all true:
1. The exposed key is deleted or disabled in Google Cloud.
2. Every app that used it works on a new, restricted key stored only in env vars / secret manager.
3. No key remains in current code or git history.
4. No unexpected Google usage or charges.
The goal is fixed. The steps below are a SUGGESTION. If a step fails or something safer, simpler or cheaper exists, use it and note why. Do not wait for me.

## SUGGESTED PATH (not mandatory)
1. Find: search repos, .env files, deploy settings (Railway, Netlify, Cloudflare) for Google keys (pattern AIza...). Check which repos are public. Record file path + repo + line only.
2. Map usage: which APIs and apps use the key (Google Cloud Console > Credentials, usage/"last used"). Check usage for unexpected calls.
3. Create a new key with the SAME API + referrer/IP restrictions (or tighter). Console "Rotate key" does this.
4. Put the new key in env vars of each app. Redeploy. Test each app.
5. When tests pass, delete the old key (it stays undeletable-recoverable 30 days). Watch usage for 30 min; deleted keys can work briefly.
6. Remove the key from code and git history (git filter-repo or equivalent), on a branch. Push only with my YES.
7. Add protection: .gitignore for .env, secret scanning / push protection on GitHub.

## AUTONOMOUS (do without asking)
Read-only searches and audits; creating a new restricted key when it is free and does not touch the old one; updating env vars of non-production or already-staged apps; running tests; writing notes.

## ASK ME FIRST (only these)
- Deleting/disabling the old key while any app still fails tests or unused-ness is unproven.
- Rewriting or force-pushing git history; changing any public repo.
- Anything with cost (enabling billing, paid APIs, paid tools) or any quota increase.
- Production deploys that cause downtime.
If risk is zero and cost is zero, proceed alone.

## NEVER
- Print, paste, log or commit any key value. Show only the last 4 characters.
- Delete other credentials, projects or APIs.
- Disable billing, delete a project, or touch non-Google keys.
- Use paid tools. Models: OpenRouter :free; name provider.

## EMERGENCY RULE
If a key is in a PUBLIC repo and is unrestricted: disable it immediately (reversible 30 days), then fix the apps. Short outage is cheaper than abuse. Tell me right after.

## REPORT (max 10 lines, at end)
Found (repo/file), apps affected, new key restrictions, old key status, history cleaned yes/no, usage anomalies yes/no, what I still must do.
