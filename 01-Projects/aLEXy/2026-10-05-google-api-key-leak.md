---
title: "aLEXy — Google API Key Leak (public repo)"
created: 2026-10-05
tags: [security, secrets, alexy, github, incident]
status: active
---

# aLEXy — Google API Key Leak

## Verdict: 🔴 CONFIRMED LEAK (independently verified)

A Google API key is hardcoded in a **PUBLIC** GitHub repository and has been exposed for
~2.5 months.

| Field | Value |
|-------|-------|
| Repo | `Ole00007/aLEXy` — **public** |
| File | `test_gemini.py` — **line 3** |
| Blob SHA (HEAD) | `14fdc4b7b21eba4b290c9ff1ba80bc28fcd072f7` |
| Introduced in | `aa94491e3356431bbf530bd29a7f5dcf73baedbc` — "Initial commit" |
| Commit date | 2026-07-21 16:14:48 +0200 |
| Author | olesia rasing |
| Key type | `google_api_key` (Google AI / Gemini) |
| In HEAD? | **Yes** — never removed |
| In history? | **Yes** — initial commit onward |
| GitHub alert | #1, `state: open`, opened 2026-07-21T14:14:53Z |

Code shape (redacted):

```python
from google import genai
client = genai.Client(api_key="AIzaSyDR***REDACTED***")
```

No other credentials found: no `GOCSPX-` OAuth secrets, no service-account JSON, no
`private_key` fields. `.env` is **not** tracked (only `.env.example` with placeholders).

## Verified facts

- Confirmed independently via `gh api repos/Ole00007/aLEXy/contents/test_gemini.py`
  (file present, 335 bytes) — not taken on a subagent's word.
- GitHub's own secret scanner flagged it the same day it was pushed; the alert is **still open**.
- `secret_scanning_push_protection` is **enabled** on the repo, so future leaks of this pattern
  are blocked — but the existing one is not auto-removed.

## Blast radius in the Hermes estate — CLEAR

Checked every `.env` in `~/.hermes/` and all 24 profiles: **no `GOOGLE_*` / `GEMINI_*` key
exists anywhere.** Profiles using the `google` provider authenticate through OAuth
(`auth.json → providers.google-gemini-cli`), not a static key.

**Conclusion: rotating this key breaks nothing in the estate.** No config edits, no redeploys.

## Remediation

### (a) Ole must do — credential work, never automated

1. **Revoke the key now** → [Google Cloud Console → Credentials](https://console.cloud.google.com/apis/credentials).
   This is the step that actually ends the exposure.
2. Create a replacement key, **API-restricted to Gemini only**, and store it as an env var.

### (b) Can be automated safely (needs Ole's yes)

- Rewrite `test_gemini.py` to read `os.environ["GEMINI_API_KEY"]`, or delete the file if it was
  a scratch test.
- Add `.env` to `.gitignore` (currently missing — a real risk).
- Optionally add a `gitleaks` / `detect-secrets` pre-commit hook.

### (c) History rewrite — Ole's explicit decision only

`git filter-repo` + force-push is a **destructive rewrite of a public repo**. It is *cosmetic
hygiene*, not the fix: once public, the key may already be scraped. **Rotation is the fix;
history rewriting is cleanup.** Not to be done without explicit approval.

## Verification after remediation

```bash
gh api repos/Ole00007/aLEXy/contents/test_gemini.py        # expect 404 after removal
gh api repos/Ole00007/aLEXy/secret-scanning/alerts \
  --jq '.[] | {state, secret_type}'                        # expect resolved/empty
```

## Sequencing note

Ole decided (2026-10-05) to **fix this leak before registering on Canva** — a live key in a
public repo is actively exploitable, so it outranks a new integration.

## Links

- Parent: [[aLEXy-INDEX]]
- Related: [[2026-10-05]]
- See also: [[2026-10-05-canva-fronty-intake-and-d1-15-fix]]
