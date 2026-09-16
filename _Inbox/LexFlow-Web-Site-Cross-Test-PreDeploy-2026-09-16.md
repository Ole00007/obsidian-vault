---
title: LexFlow Web-Site — Independent Cross-Test of Pre-Deploy Build (3b9cc41 + 23678b7)
created: 2026-09-16
tags: [lexflow, web-site, cross-test, qa, i18n, security, kanban]
status: review
---

# LexFlow Web-Site — Independent Cross-Test of Pre-Deploy Build

Independent cross-test of the frontend build on branch `feat/heading-align-cta-merge`
(commits `3b9cc41` + `23678b7`), requested by frontend-developer, executed by
operator-installer as kanban card `t_cf76a3a3`. **Nothing was deployed and the repo was not
modified.** Preview under test: `http://127.0.0.1:8891/`.

## Method (independent, not a re-run of the author's script)

- Headings: Python `html.parser` over all 49 page files (19 EN + 15 IT + 15 RU).
- i18n: extracted each page's own `window.I18N` dict and merged `assets/i18n-ui.js` in Node,
  then applied the exact rule `assets/i18n.js` uses for alt text.
- Endpoints: HTTP fetch of every page, asset and special file from the live preview.
- Attribution/security: regex sweep of the whole tree + `git diff 88f6cc9..23678b7`.

## Results — 6 PASS / 1 FAIL / 1 note

| # | Item | Verdict |
|---|---|---|
| 1 | Heading integrity (49 pages, one H1, no skipped levels) | **PASS** — 0 issues |
| 2 | One CTA label per language, nav == mid-page | **PASS** — 0 mismatches (45 pages) |
| 3 | `data-webhook` values still distinct | **PASS** — 31 distinct values, none collapsed |
| 4 | Hero `demo-request-hero` unchanged, still `#intake` | **PASS** — 0 diff lines touch it |
| 5 | No link to `railway.app/admin` | **PASS** — 0 occurrences |
| 6 | All endpoints 200 | **PASS** — 61/61 URLs, 48/48 sitemap locs |
| 7 | No English leaking into IT/RU on changed elements | **FAIL** — FAQ calendar alt |
| 8 | Regressions | 1 content change to note (emoji removal) |

## The one defect (item 7) — FAQ calendar image alt

The build repointed the FAQ "notifications → calendar" visual from
`romanelli-sala-riunioni.png` to the new `assets/lexflow-calendar-visual.png` and corrected the
*static EN* alt, but left `data-i18n-alt="alt_team"`. `alt_team` is defined in
`assets/i18n-ui.js` (committed earlier in `74908bc`, untouched by this build) as
EN "Law firm team working together" / IT "Team dello studio legale al lavoro" /
RU "Команда юридической фирмы за работой", and `assets/i18n.js` overwrites `alt` at runtime
whenever the key resolves.

Runtime result — the calendar image is described as a **team** in all three languages:

| Page | Runtime alt |
|---|---|
| `lexflow-faq.html` | "Law firm team working together" (correct static alt destroyed on load) |
| `it/lexflow-faq.html` | "Team dello studio legale al lavoro" |
| `ru/lexflow-faq.html` | "Команда юридической фирмы за работой" |

Wrong alt text for screen readers (WCAG 1.1.1) and a regression on EN.
**Fix:** use a calendar-specific key (`data-i18n-alt="alt_calendar"`) and add it for en/it/ru in
`assets/i18n-ui.js`, or drop the stale `data-i18n-alt`. Do **not** edit the `alt_team` value —
it is still used by the meeting-room image on other pages.

## What else changed in this build (item 8, not a bug)

Leading glyphs were stripped from CTA/contact links: `▶ Dashboard Preview` → `Dashboard Preview`,
`◉ WhatsApp …` / `💬 WhatsApp …` → plain, `✉ Email: demo@lexflow.com` → plain. User-visible, so it
needs Ole's localhost review under the design/UX gate before anything ships.

Also noted (out of scope, unchanged by this build): the intake section label is still per-language
free text — `intake_label` EN "Book a Demo" / IT "Prenota una Demo" / RU "Заказать демо", and
`intake_submit` "Request Demo and Start 14-Day Free Trial". Not a nav/mid-page CTA, so it does not
break the single-label rule, but it is a second phrasing of the same call to action.

## Follow-up

- Fix card `t_6807dd71` — "FIX: FAQ calendar image alt resolves to a 'team' description in
  EN/IT/RU (regression from 23678b7)" — assigned to `frontend-developer-lovable_react`,
  parent `t_cf76a3a3`. Local fix on the same branch, no deploy.
- Findings reported on the card thread: full report + a correction comment fixing the follow-up
  card id.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Build-2026-09-07]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
