# UX Fix Plan — 2026-09-04 (Pagliano-first, tenant-neutral, CRM stays English)

**Source:** `docs/UX-Test-Report-2026-09-04.md` (human-like walkthrough, read-only)
**Branch:** `lexflow_hermes_v1` · **Baseline archive:** `archive/ux-baseline-2026-09-04` (5182bf8)
**Scope:** CRM templates only (`templates/*.html` + client-side JS). Landings NOT touched
(`LexFlow-landing` is a separate repo; `templates/pagliano.html` is a landing — per directive).
**Language:** all fixes keep the CRM English (i18n is roadmap T-020, next week).
**Tenant-neutral rule:** no Pagliano/`ws9` hardcoding — fixes are safe for Lexflow + Romanelli too.
**Effort:** S = minutes, M = focused task, L = multi-session feature.

---

## 1. Contrast gap (report §5 verdict: calendar/tasks missed by 3aaea16)

| Item | File:line | Change | Effort | Priority |
|---|---|---|---|---|
| C1 | `templates/calendar.html:18` `.cal-viewbtn.active` | `color:#fff` → `color:var(--bg)` (mirrors kanban `btn-primary` fix 3aaea16) | S | P1 |
| C2 | `templates/calendar.html:35` `.cal-today .cal-mnum` | same swap | S | P1 |
| C3 | `templates/calendar.html:47` `.cal-dayhead.cal-today .cal-dh-num` | same swap | S | P1 |
| C4 | `templates/tasks.html:25` `.btn-submit` (+ hover 26) | `color:#fff` → `color:var(--bg)` | S | P1 |

Dark theme math: `--accent #3B7DD8` vs `#fff` = **4.09:1** (AA fail, <4.5) → vs `--bg #0E1117` = **4.61:1** (pass).
Light theme: vs `#fff` 6.3:1 (pass) → vs `--bg #F8FAFC` **6.30:1** (pass). Both themes AA-pass after swap.
`--bg` is defined in base.html (`calendar/tasks` extend base) and kanban.html root block.

## 2. A11y quick wins (report §3 bonus-6 + findings 3.2/5.3/5.5/8.4)

| Item | File:line | Change | Effort | Priority |
|---|---|---|---|---|
| A1 | `templates/base.html:161` toast container | add `role="status" aria-live="polite"` | S | P1 |
| A2 | `templates/kanban.html:606` toast container | add `role="status" aria-live="polite"` | S | P1 |
| A3 | `templates/login.html:46` `<p class="err">` | add `role="alert"` | S | P1 |
| A4 | `templates/kanban.html` (standalone) | skip-link → `#board` + CSS (kanban does not extend base; base.html:104 has one) | S | P1 |
| A5 | `templates/staff_board.html` (standalone) | skip-link → `#board` + CSS | S | P1 |
| A6 | `templates/roadmap.html` (standalone) | skip-link → `#board` + CSS | S | P1 |
| A7 | `base.html`, `kanban.html`, `staff_board.html`, `roadmap.html` | `@media (prefers-reduced-motion: reduce)` kill-switch (report 1.10: LP has it, CRM chrome doesn't) | S | P2 |
| A8 | `templates/kanban.html:577–578` inline login inputs | add `aria-label` (report 3.4: placeholders only, no labels) | S | P2 |

## 3. TOP-5 human-friction items

| # | Report ref | Change | Effort | Priority | Verdict |
|---|---|---|---|---|---|
| T1 | 1.1 masked phone `tel:+393****9810` (pagliano.html:1568,1831) | Needs the REAL number (data, not code) + it's a landing page | S (once data exists) | P1 | **FAIL/DEFER** — needs real phone from Ole; landing page (out of scope per directive). Flagged for operator. |
| T2 | 5.1 kanban "New Task" raw numeric Contact ID (kanban.html:685–687,1097) | Replace `<input type=number>` with `<select>` populated from `/api/contacts` (mirror tasks.html case picker, report 11.2 "the right pattern"); `handleCreateCase` unchanged (value = id) | M | P1 | **IMPLEMENT** |
| T3 | 7.1 workspace_panel prompt()/confirm() CRUD (workspace_panel.html:88–209) | Full refactor to styled modal(s) — 4 flows (rename, add login ×3 prompts, add team ×4, edit, delete). Needs a reusable modal like tasks/calendar + validation UI | L | P2 | **FAIL/DEFER** — too large for this round's "minimal, additive" rule; scoped for a dedicated iteration. No partial prompts→modal half-fix (risk of inconsistent UX). |
| T4 | 1.2/1.3 debug btn text + P.IVA `[da inserire]` (pagliano.html:1760,1860–1862); 10.1 raw contactid (admin.html:79) | admin.html: fetch `/api/contacts`, render contact NAME (fallback `Contact #id`); landing text items deferred (landing + real data) | S | P1 | **IMPLEMENT** (admin part) / **DEFER** (landing text) |
| T5 | 5.2 kanban nav `display:none!important` <900px, no hamburger (kanban.html:164–166,196–198) | Hamburger toggle + dropdown panel <900px; move nav inline styles to stylesheet; `aria-expanded`; close on link/Escape | M | P1 | **IMPLEMENT** |
| T6 | 6.1 calendar login link hardcodes `?ws=romanelli-studio` (calendar.html:189) | Derive `ws` from current URL search params (tenant-neutral); fallback no-`ws` link (never wrong tenant) | S | P1 | **IMPLEMENT** |

## 4. Secondary confident fixes (small, additive)

| Item | File:line | Change | Effort |
|---|---|---|---|
| S1 | `calendar.html:244,260` `alert()` validation/error | → global `toast(...,'error')` (base.html:166) | S |
| S2 | `staff_board.html:91` cards not clickable (8.1) | wrap card in `<a href="/admin/matter/{{ c.id }}">` + `cursor:pointer` (route exists: views.py:491) | S |
| S3 | `admin.html:45` "Loading…" | keep (legit loading state, not a bug) | — |

## 5. Deferred (explicitly NOT this round — cross-audit note for operator)

| Ref | Item | Why deferred |
|---|---|---|
| 2.1/2b.1 | Intake/status i18n (Italian) | Roadmap T-020 "i18n next week"; CRM stays English per directive |
| 3.1 | Partner password reset | Backend + email flow — backend_dev territory (superadmin reset exists admin_panel.html:16) |
| 5.4 | Kanban keyboard move alternative | Drag-only → needs move-menu UI; M+ |
| 5.6 / 12.2 | Modal focus traps (kanban/tasks/calendar/contacts) | Command-driven a11y, no browser E2E available this round; needs real-device verification |
| 6.3 | Calendar popover aria wiring | needs role=dialog + boundary logic; M |
| 10.3 | Matters table search/pagination | Enhancement, not a defect; M |
| 1.8/1.9 | Chat GDPR consent, cookie "Rifiuta" | Landing widget (separate repo) + legal/consent flow decision |
| 9.1/9.2 | Roadmap content exposure + tooltips | Product decision (internal board vs staff-facing) |
| 12.1/12.3 | Contacts status vocabulary, confirm() delete | Vocabulary = i18n-adjacent; confirm() is acceptable UX |
| 8.2 | Staff board mobile layout (@media) | Board horizontal scroll is a deliberate pattern; revisit with T5 pattern |

## 6. Self-review (regression check, done before implementation)

1. **Shared templates → all tenants:** every edit is additive CSS/JS or a color-var swap; no tenant strings added. `calendar.html` login link becomes URL-derived (currently hardcodes romanelli — no behavior change for Romanelli since `?ws=` absent → falls back gracefully; Pagliano fixed by URL param).
2. **kanban.html nav <900px:** current rule `display:none!important` replaced by toggleable dropdown; `>900px` layout untouched (inline styles moved to stylesheet, same values). Toggle lives inside `#loggedInControls` so it only appears post-login; login-form layout unaffected. Board/columns untouched.
3. **workspace_panel prompt() refactor scope:** correctly NOT attempted — 6 flows, 4 sequential prompts, no shared modal component; partial refactor would double the UX debt. Documented for a dedicated round (T3).
4. **Contrast swap scope:** only the 4 `#fff`-on-`--accent` spots in calendar/tasks (grep-verified); `base.html:65` `.brand-mark` (#fff on accent, 12px icon-ish mark) left as-is — matches kanban `logo` mark style, tiny glyph, not part of the reported gap.
5. **Jinja balance:** staff_board/roadmap edits are pure HTML/attr additions inside existing blocks; no new `{% %}` tags.
6. **API use:** `/api/contacts` + `/api/cases` both `jwt_required(optional=True)` with workspace scoping (routes/contacts.py:24, routes/cases.py:23) — same-origin fetch, no backend change, no cross-tenant leak.

— UX subagent, 2026-09-04 (plan phase; implementation follows)

---

## 7. Implementation results (same day — local working tree, NO commit/push)

| Item | Status | Evidence |
|---|---|---|
| C1–C3 calendar contrast | **PASS** | calendar.html:18,35,47 → `color:var(--bg)`; dark 4.60:1, light 6.41:1 (AA) |
| C4 tasks contrast | **PASS** | tasks.html:25–26 → `var(--bg)` both states; hover dark 6.35 / light 8.34 |
| A1 base toast aria-live | **PASS** | base.html:161 `role="status" aria-live="polite"` |
| A2 kanban toast aria-live | **PASS** | kanban.html:671 |
| A3 login err role=alert | **PASS** | login.html:46 |
| A4–A6 skip-links | **PASS** | kanban.html:633, staff_board.html:92, roadmap.html:144 (+ `.skip-link` CSS in each) |
| A7 reduced-motion | **PASS** | base.html:101–107; kanban.html:~254; staff_board.html:~59; roadmap.html:~88 |
| A8 kanban login aria-labels | **PASS** | kanban.html:641–642 |
| T2 contact picker | **PASS** | kanban.html:750–754 (select), `loadContacts()` ~1009–1031, called from `openModal()` ~1169 |
| T4 admin contact names | **PASS** | admin.html:75–94 (fetch `/api/contacts`, map id→fullname, fallback `Contact #id`) |
| T5 mobile nav | **PASS** | kanban.html:161–172 (.nav-toggle), 214–238 (<900px dropdown), 648 (button), `toggleNav()` + click/Escape close ~1209–1236 |
| T6 calendar login link | **PASS** | calendar.html:184–195 (URL-derived `ws`, no tenant hardcode) |
| S1 calendar alert→toast | **PASS** | calendar.html:248, 264, 597, 630 |
| S2 staff board clickable cards | **PASS** | staff_board.html:120–129 (`<a class="card" href="/admin/matter/{{ c.id }}">`), CSS display:block+cursor |
| T1 masked phone | **FAIL/DEFER** | needs real number (data) + landing page per directive |
| T3 workspace_panel prompts | **FAIL/DEFER** | L-effort refactor; dedicated iteration |
| Landing scaffolding (debug btn text, P.IVA) | **FAIL/DEFER** | pagliano.html is a landing; content/data changes |

**Static verification (passed):** Jinja tag balance on all 8 touched templates · `node --check` on kanban/calendar/tasks/admin inline JS · HTML parser structural check (7 templates, 0 errors) · WCAG contrast matrix (all 10 pairings ≥4.5:1, both themes) · route existence (`/api/contacts`, `/api/cases`, `/admin/matter/<id>`, `/login`, `/calendar`, `/kanban`, `/api/calendar`).

**Note on contrast approach:** the report's suggested swap to `var(--bg)` is correct for BOTH themes (dark accent #3B7DD8 vs bg #0E1117 = 4.60:1; light accent #1D4ED8 vs bg #F8FAFC = 6.41:1) and matches the shipped kanban fix (3aaea16). A `--on-accent` token variant was evaluated and reverted (white-on-accent = 4.11:1 dark, below AA).

