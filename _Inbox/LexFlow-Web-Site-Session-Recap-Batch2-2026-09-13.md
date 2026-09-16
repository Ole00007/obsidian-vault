---
title: LexFlow Web-Site — session recap batch 2 (humanizer, EN leakage fixes, WhatsApp Option C, Kanban artefact)
created: 2026-09-16
tags: [lexflow, web-site, session-recap, i18n, humanizer, whatsapp, build-script, vault-logging]
status: active
repo: /Users/olesiarasing/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site
commit: 63f46d4
source_card: t_76668155
session_date: 2026-09-13
---

# LexFlow Web-Site — session recap, batch 2 (2026-09-13)

Vault logging for kanban card `t_76668155` (source profile
`frontend-developer-lovable_react`). Repo `LEXFLOW Web-Site`, branch `main`, HEAD after
that session `63f46d4`.

## 1. Humanizer pass across EN / IT / RU

- **259 replacements in 34 distinct strings.**
- Em-dash overuse (pattern 14) fixed in prose; accent-accordion titles now use a colon;
  the final dash was inconsistent (plain hyphen vs em dash) and is now normalised.
- Ole's example applied: Russian "Напишите нам." → "Свяжитесь с нами." (0 left,
  18 occurrences of the new phrasing).

## 2. Two real bugs found and fixed (they were live on the site)

a) The i18n runtime only cleared an element's **direct** text nodes when swapping language,
   so `<em>disordine</em>` survived and the English home page rendered
   "Every legal firm loses time to chaosdisordine" and
   "Gli studi che usano LexFlow chiudono di più.più."
   `setText` now walks **all descendant text nodes (TreeWalker)**, matching the build script.

b) **13 English dictionary values and 16 static elements held ITALIAN**, so English visitors
   read Italian: `why_results_title/sub`, `problem_label/title/sub`, `problem1_h/p`,
   `problem3_h/p`, `contact_intro`, `contact_consent1/2`, `contact_privacy`,
   `contact_submit`, `contact_name`, `contact_message`, `chatbot_greeting/note/status_new`,
   `contact_title`.

## 3. WhatsApp Option C shipped

- `whatsapp` + `whatsappDisplay` in `assets/site-config.js` are the **single source**;
  the generator stamps both into all 27 pages.
- Proven: changing both rewrote **98 wa.me links and 38 displayed numbers**, leaving zero
  of the old number. Idempotent across runs.

## 4. Kanban artefact replaced

- The schematic PNG is now a rendered board mirroring the REAL `/kanban` columns
  (Intake, Conflict Check, Review, In Progress, Waiting Docs, To Verify, Engaged, Closed)
  in the site's own palette. Placeholder matters only; board is login-gated so no card
  data was read. Source kept at `templates/kanban-artefact.html`.

## 5. FAQ "notifications" image replaced

- Swapped for the approved `romanelli-sala-riunioni.png`.

## Near-miss worth remembering

A patch to the build script reused a **stale loop variable** and overwrote ALL TEN English
pages with the last localised page — the site briefly served a Russian article at English
URLs. Caught and restored from git in the same session. The build now snapshots every English
page title up front and **ABORTS** if a page comes out with different content, and aborts on
any malformed `wa.me` link.

**Lesson:** in `templates/build-lang-sites.py` the English-page loop must read its own page;
never reuse a variable from the localised-pages loop above it.

## Tooling lesson (reusable)

Patterns in `build-lang-sites.py` must be built from **character classes with no backslash
escapes**. That file is written by tooling that escapes source twice: two patterns silently
degraded into "matches nothing", and one display pattern matched the digits inside a `wa.me`
URL and would have published `wa.me/+39 345 023 4084`. Use `[+]` for a literal plus, `[.]`
for a literal dot.

## Pending (owner input, still open 2026-09-16)

- **Domain:** Ole supplies from Cloudflare after he approves a version to deploy. `ORIGIN` in
  `build-lang-sites.py` is still `https://lexflow.example.com`, baked into 26 sitemap URLs,
  4 hreflang tags × 24 pages and every canonical — must be set before any deploy.
- 27 webhook URLs (all null, fail loudly).
- Article IT/RU bodies (owner sending in batches; not blocking).
- **NOTHING is deployed yet.**

## Blocked handoffs at the time

Cards `t_d6065167` (operator-installer) and `t_6c2c8c07` (memory-curator) both failed with
"No access token found for Nous Portal login. Run `hermes model` to re-authenticate." —
resolved later: operator-installer now runs on OpenRouter `deepseek/deepseek-v4.1-flash`.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Enrichment-Elisa-2026-09-13]]
- Related: [[LexFlow-Web-Site-Agent-Surface-2026-09-15]]
- Related: [[LexFlow-Public-Intake-Contract-2026-09-15]]
