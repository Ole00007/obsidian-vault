# LexFlow Web-Site — FAQ calendar image alt fix (2026-09-16)

Card `t_6807dd71` (frontend-developer-lovable_react), parent `t_cf76a3a3`.
Fix for the single FAIL from the independent pre-deploy cross-test.

## Defect

`lexflow-faq.html`, `it/lexflow-faq.html`, `ru/lexflow-faq.html` line 105 — the second
`premium-visual`: the build swapped the image to `assets/lexflow-calendar-visual.png` and fixed the
static EN `alt`, but left `data-i18n-alt="alt_team"`. `assets/i18n.js` overwrites `alt` at runtime
whenever the key resolves, so all three languages described a **team**, not a calendar
(WCAG 1.1.1). EN was a regression: the correct static calendar alt was destroyed on load.

## Fix

- New key `alt_calendar` added for **en / it / ru** in `assets/i18n-ui.js` (kept `alt_team` untouched).
- EN source `lexflow-faq.html` now points the image at `data-i18n-alt="alt_calendar"`.
- `/it/` and `/ru/` **regenerated** from the EN source with `python3 templates/build-lang-sites.py`
  (not hand-edited) so the baked static `alt` matches the new key:
  - EN: *LexFlow calendar showing deadlines and appointments synced from notifications*
  - IT: *Calendario LexFlow con scadenze e appuntamenti sincronizzati dalle notifiche*
  - RU: *Календарь LexFlow со сроками и встречами, синхронизированными из уведомлений*

## Verification (real output, headless Chrome, local server 127.0.0.1:8901)

- Static attribute after fix, all three pages: `data-i18n-alt="alt_calendar"`, alt = calendar text.
- Post-load DOM (`--headless=new --dump-dom`) equals the static value in EN/IT/RU.
- Runtime resolution proved separately with a throwaway probe page carrying an **empty** static alt:
  JS filled it per language — `alt_calendar` EN/IT/RU all resolved; `alt_team` still resolves to
  "Law firm team working together" (key intact).

## Notes / findings

- `alt_team` is **no longer referenced by any markup** in the repo (the meeting-room image uses
  `alt_sala_riunioni`). The key was left in place per the card's instruction — zero risk either way.
- **Concurrency:** the repo was being edited live during this run (new PNG exports, a blog-layout
  tweak, and untracked probe files). **Ole committed the working tree at 18:11:46 as
  `2110368` "Premium visuals: dark calendar…" which swept in this i18n fix**, so the fix landed
  inside that commit rather than a separate one of mine. The build regeneration of `it/`/`ru/`
  also propagated a blog-layout edit into the localised blog pages, which Ole's commit carries.
- Nothing deployed; branch `feat/heading-align-cta-merge` untouched apart from that commit.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Web-Site-Cross-Test-PreDeploy-2026-09-16]]
- Related: [[LexFlow-Web-Site-SEO-AEO-GEO-Origin-Plan-2026-09-16]]
