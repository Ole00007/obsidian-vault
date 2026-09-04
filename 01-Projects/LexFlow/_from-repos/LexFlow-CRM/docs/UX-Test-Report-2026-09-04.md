# LexFlow CRM + Landing — Human-Like UX Walkthrough Report

**Date:** 2026-09-04
**Branch:** `lexflow_hermes_v1` (working tree, post contrast-fix commit `3aaea16`)
**Tester role:** Human evaluator simulating (A) a first-time Italian client and (B) a returning lawyer partner
**Method:** NN/g-style usability walkthrough · WCAG 2.2 AA (ISO 40500:2025) heuristic check · mobile-first evaluation (<900px) · keyboard-only path · screen-reader semantic order
**Scope note:** `LexFlow-landing/index.html` does **not exist** in this repo (the LexFlow landing is deployed at `https://poetic-kleicha-28d058.netlify.app` per `templates/base.html:194`). The in-repo, user-facing landing tested here is the **Pagliano LP** (`templates/pagliano.html`). `static/lexflow_dashboard.html` is a dev/curl harness, not user-facing. All findings cite `file:line`.

---

## 1. Walkthrough Log (Step → Finding → Severity)

Severity: 🔴 High (blocks a human task / kills trust) · 🟠 Medium (friction, slows task) · 🟡 Low (polish/a11y debt)

### Step 1 — Landing: Pagliano LP (`templates/pagliano.html`)

| # | Finding | Severity |
|---|---------|----------|
| 1.1 | **Masked phone in a clickable CTA.** Hero `Chiama ora` links `tel:+393****9810` (1568); footer repeats the masked number (1831). A client who taps it dials a corrupt number — the single most conversion-killing defect on the site. | 🔴 |
| 1.2 | **Debug text on the primary form button:** `Invia Richiesta (workspace: Pagliano)` (1760; re-set at 2122). Looks like internal scaffolding shipped to clients. | 🔴 |
| 1.3 | **Legal-identity placeholders in footer:** `P.IVA: [da inserire]`, `Rea: [da inserire]`, `Iscr. Albo: n° [da inserire]` (1860–1862). For a law firm this reads as "not a real practice yet" — trust killer. | 🔴 |
| 1.4 | **Submit button stays disabled after a successful send.** `showSuccess()` (2109–2120) never calls `resetBtn()`; the button was disabled pre-fetch (2096–2097). Second submission requires a page reload — silent dead end. | 🟠 |
| 1.5 | **Privacy policy rendered via `alert()`** (1754) — browser chrome, unstyled, no scroll, feels unprofessional; the footer modals (1903, 1921) are fine but the form's inline link bypasses them. | 🟠 |
| 1.6 | **Hero avatar is a monogram placeholder** (`DP`, 1572–1575) with an uncommitted video placeholder comment — no real face builds less trust for legal services. | 🟡 |
| 1.7 | **Blog content is stale:** dates Jul/28/Jun/10 2025 (1779, 1791, 1804) — "2025" copy in a 2026 walkthrough. | 🟡 |
| 1.8 | **Chat widget hardcodes a Railway origin** (`https://web-production-ab54f.up.railway.app`, chat-widget.js:304, 472) and collects name/email/phone (chat-widget.js:159–208) **without any GDPR consent step in the chat flow** — the LP's own privacy text says data is only collected with consent (1754). | 🟠 |
| 1.9 | Cookie banner offers only `Accetta` — no "Rifiuta" (1891–1899). Cosmetic for technical cookies, but users accustomed to a choice will look for it. | 🟡 |
| 1.10 | Contrast (light theme): `.btn-primary`/`.submit-btn` `#fff` on `--accent #698269` ≈ 4.5:1 — AA pass at the threshold; hero paragraph `rgba(255,255,255,0.75)` on navy gradient ≈ 6.8:1 — pass. Good: 17 `@media` blocks incl. `prefers-reduced-motion` (419, 1103). | 🟢 |

**Human verdict:** Beautiful, calm, Italian-first design — then a masked phone number, a debug-labeled button, and `[da inserire]` legal IDs make a client doubt they're dealing with a real firm.

### Step 2 — Intake form (`templates/index.html`)

| # | Finding | Severity |
|---|---------|----------|
| 2.1 | **Whole flow is English** ("Start secure intake", "Submit intake", "Back to admin") — served to Italian clients coming from the Pagliano/Romanelli LPs. Language jump is jarring. | 🔴 |
| 2.2 | **`autocomplete="off"` on name, email, phone** (46, 55, 59) blocks browser autofill — extra typing for the exact users who need speed (intentional per commit `309e33c`, but felt as friction). | 🟠 |
| 2.3 | 8 fields + file upload + select — acceptable length, but "Practice area" options come from DB (77–79); empty DB = empty select with no explanation. | 🟡 |
| 2.4 | `Urgency` silently pre-selected "Medium" (86) — users may submit without noticing the default; no hint why it matters. | 🟡 |
| 2.5 | Document input has no visible label text — only `<small>` formats line (97–99); keyboard/screen-reader label is the input's implicit one. | 🟡 |
| 2.6 | Clear affordance: `Start secure intake` anchors to `#intake-form` (16) — good single-path design. | 🟢 |

**Human verdict:** Simple and fast for an English speaker; for the Italian persona it's "why is your site half-English?"

### Step 2b — Client status page (`templates/status.html`)

| # | Finding | Severity |
|---|---------|----------|
| 2b.1 | Client-facing but **entirely English**: "Your new intake has been successfully submitted." (9), "Client status page" (19), raw status strings ("Conflict Check", "Waiting Docs" — kanban statuses leaked verbatim). | 🔴 |
| 2b.2 | Status progression `<ol>` (33–41) renders all 8 stages with a ✓ on the current one — good mental model, but English stage names again. | 🟡 |

**Human verdict:** A reassuring confirmation — in a language the client may not speak.

### Step 3 — Login (`templates/login.html` + kanban inline login)

| # | Finding | Severity |
|---|---------|----------|
| 3.1 | `login.html` is Italian with proper labels (48–51) — good. But **no password-reset path anywhere** ("forgot password?" absent); reset exists only in Super Admin panel (`admin_panel.html:16`). Locked-out partner = email the superadmin. | 🟠 |
| 3.2 | Error `<p class="err">` (46) has no `role="alert"`/`aria-live` — screen reader users never hear login failures. | 🟡 |
| 3.3 | Hardcoded post-login redirect to `/kanban` (75) — fine for staff, wrong for a client sub-workspace user. | 🟡 |
| 3.4 | **Kanban inline login (kanban.html:553–556) has no `<label>`s** — only placeholders; on mobile the login form collapses to icons-only per `.btn-label` hiding (kanban.html:486) while nav is gone (see 4.4). | 🟠 |

**Human verdict:** The standalone Italian login is dignified; the inline kanban login is a naked form floating in a header.

### Step 4 — Dashboard (`templates/dashboard.html`)

| # | Finding | Severity |
|---|---------|----------|
| 4.1 | Only 4 stat numbers + 2 buttons + an activity list that is usually "No activity yet" (53). Thin — a returning partner gets no "what needs me today" answer. | 🟠 |
| 4.2 | Numbers have no trend/context (percentages, deadlines) — "13 Pending" means nothing alone. | 🟡 |
| 4.3 | `Recent activity` truncates summaries at 60 chars with no tooltip/link (50). | 🟡 |
| 4.4 | Positive: live stat refresh via `/api/stats` (68–80) prevents the stale 0/0/0/0 trap after login. | 🟢 |

**Human verdict:** Clean, trustworthy, but empty-calorie — it tells you counts, not what to do next.

### Step 5 — Kanban (`templates/kanban.html`)

| # | Finding | Severity |
|---|---------|----------|
| 5.1 | **"New Task" modal demands a raw numeric `Contact ID`** (685–687) with hint "Create a contact first in Contacts" (687) — a classic dead-end: leave modal → find ID in another screen → come back. `handleCreateCase` rejects without it (1097). | 🔴 |
| 5.2 | **Nav disappears below 900px** (kanban.html:164–166 `display:none!important`) with **no hamburger/replacement** — on a phone, once logged in you cannot reach Calendar/Tasks/Contacts/Workspace from the board. | 🔴 |
| 5.3 | Standalone page: **no skip-link** (base.html:104 has one; kanban doesn't extend base) — keyboard users tab through the whole login/board chrome. | 🟡 |
| 5.4 | Board is drag-only for moves — **no keyboard alternative** to move a card between columns. | 🟠 |
| 5.5 | Toast container has no `aria-live` (kanban.html:509) — status feedback invisible to screen readers. | 🟡 |
| 5.6 | Modal lacks focus trap; focus stays on trigger (openModal focuses title, but Tab can escape the overlay). | 🟡 |
| 5.7 | Positive: skeletons (744–758), optimistic counts, escape-to-close, Enter-to-login (1146–1154), contrast fix applied (`.btn-primary` uses `var(--bg)`, commit `3aaea16`). | 🟢 |

**Human verdict:** The heart of the product — but it asks staff to memorize database IDs and strands mobile users with no navigation.

### Step 6 — Calendar (`templates/calendar.html`)

| # | Finding | Severity |
|---|---------|----------|
| 6.1 | **Login prompt hardcodes `?ws=romanelli-studio`** (189) — a Pagliano or LexFlow staff member gets bounced toward the wrong tenant's workspace. | 🟠 |
| 6.2 | `.cal-viewbtn.active` is `#fff` on `var(--accent)` (18) — in dark theme ≈ 4.1:1, **AA fail** for 14px text; same pattern at 35, 47 (`#fff` day numbers). Contrast fix did not touch this template. | 🟠 |
| 6.3 | Month cells and day columns are `cursor:pointer` (29, 52) but clickable surface is the whole cell — good; however popovers are `position:fixed` (63) with no boundary/`aria-` wiring — screen readers get no announcement. | 🟡 |
| 6.4 | `alert()` for validation errors (244, 260). | 🟡 |
| 6.5 | Positive: real Google-calendar-style month/week/day grid, Monday start (274), DnD in month view, filters, "now" line. | 🟢 |

**Human verdict:** Impressive grid that a lawyer would trust — undermined by a wrong-tenant login link and white-on-blue buttons that fail AA.

### Step 7 — Workspace panel (`templates/workspace_panel.html`)

| # | Finding | Severity |
|---|---------|----------|
| 7.1 | **All CRUD via browser `prompt()`/`confirm()`** — rename (88), add login (105–109, three sequential prompts!), add team (164–169, four prompts), edit (187–192), delete (203–206). Feels like a dev tool, not a product; no validation UI, no styling, one typo = start over. | 🔴 |
| 7.2 | "Add staff member" from Matters (admin.html:15) lands here, but the panel's button says "+ Add team member" (25) and adds a directory entry, not a login — naming mismatch confuses. | 🟠 |
| 7.3 | Raw emails/roles rendered in tables (60–63) — fine internally, but this screen is where clients can wander if they log in. | 🟡 |
| 7.4 | Positive: workspace badge, case list with clickable rows, `R-01` ID guidance (13). | 🟢 |

**Human verdict:** The least "designed" screen in the app — every action is a grey browser dialog.

### Step 8 — Staff board (`templates/staff_board.html`)

| # | Finding | Severity |
|---|---------|----------|
| 8.1 | **Cards are not clickable** — no affordance to open the matter; hovering lifts the card (50) implying an action that doesn't exist. | 🟠 |
| 8.2 | **Zero `@media` queries** — on mobile the 250px columns (43) scroll horizontally; header nav wraps into three rows; user badge + logout squeeze. | 🟠 |
| 8.3 | 10px `.pill` text (54) with `--text-muted`/`--text-faint` — legibility at the edge of AA (faint ≈ 4.2:1 on surface). | 🟡 |
| 8.4 | No skip-link; no `aria-label` on the board region. | 🟡 |
| 8.5 | Positive: per-person workload with counts (87), clear footer explanation (113–115). | 🟢 |

**Human verdict:** A nice "who's overloaded" glance — then you realize you can't click into anything.

### Step 9 — Roadmap (`templates/roadmap.html`)

| # | Finding | Severity |
|---|---------|----------|
| 9.1 | Internal agentic roadmap (P1–P4, agent assignments, `deployed/blocked/local`) shown to any logged-in staff — if partners see "blocked" items, that's a trust risk on a client demo. | 🟡 |
| 9.2 | Cards are `cursor:default` (85) with notes only in `title` tooltip (141) — hidden info, no click affordance. | 🟡 |
| 9.3 | Legend exists (161–166) — good; only one `@media` (110–113). | 🟡 |
| 9.4 | Positive: same design language as kanban, contrast fix applied. | 🟢 |

**Human verdict:** It's an internal whiteboard wearing a suit — fine for Ole, odd for staff.

### Step 10 — Matters (`templates/admin.html`)

| # | Finding | Severity |
|---|---------|----------|
| 10.1 | **Contact column shows raw numeric `contactid`** (79) — a human sees "12" instead of "Mario Rossi". Classic DB-field-leak. | 🔴 |
| 10.2 | Three primary-looking buttons in a row: `New intake`, `+ Add staff member`, `Staff Board` (14–16) — no hierarchy; "Add staff member" doesn't add a staff member (see 7.2). | 🟠 |
| 10.3 | Table renders `Loading…` (45) then populates client-side; no count, no search, no pagination — with many matters, hunting rows gets slow. | 🟠 |
| 10.4 | Positive: badge for status, "Open →" link, flashed-message support. | 🟢 |

**Human verdict:** A workable admin table that leaks IDs and mislabels its own buttons.

### Step 11 — Tasks (`templates/tasks.html`)

| # | Finding | Severity |
|---|---------|----------|
| 11.1 | `.btn-submit` is `#fff` on `var(--accent)` (25) — same AA fail in dark theme as calendar. | 🟠 |
| 11.2 | Positive: excellent case picker (`R-01 · title`, 153–156) — this is how kanban's Contact ID should work; drag-drop upload zone (101–104), Escape closes modal (270), toasts. | 🟢 |

**Human verdict:** The best-implemented modal in the app — proof the team knows how to do it right.

### Step 12 — Contacts (`templates/contacts.html`)

| # | Finding | Severity |
|---|---------|----------|
| 12.1 | **Status dropdown uses raw English `lead/active/passive`** (74–76) with no explanations; the "suggest" hint chips (65–66) add cognitive load — staff must parse "active (suggest lead)". | 🟠 |
| 12.2 | Docs modal: no focus trap, no Escape handler (only ✕ / overlay), no `role="dialog"`/`aria-modal`. | 🟡 |
| 12.3 | Delete confirmation via `confirm()` (161). | 🟡 |
| 12.4 | Positive: upload + download + delete with toasts, per-contact docs. | 🟢 |

**Human verdict:** Functional but jargon-y — the status vocabulary feels like developer shorthand, not law-office language.

---

## 2. Screen Score Table (1–5, 5 = excellent)

| Screen | Clarity | Trust | Mobile | A11y | Emotion | **Avg** |
|---|---|---|---|---|---|---|
| Landing (Pagliano LP) | 4 | 2 | 4 | 3 | 3 | **3.2** |
| Intake (`index.html`) | 3.5 | 3 | 3 | 3 | 2.5 | **3.0** |
| Client status (`status.html`) | 3.5 | 3 | 3 | 3 | 2.5 | **3.0** |
| Login (`login.html`) | 4 | 3 | 4 | 3 | 3 | **3.4** |
| Dashboard | 3.5 | 3.5 | 3.5 | 3.5 | 3 | **3.4** |
| Kanban | 4 | 3.5 | **2** | 2.5 | 3.5 | **3.1** |
| Calendar | 4 | 3.5 | 3.5 | 2.5 | 3.5 | **3.4** |
| Workspace panel | 2 | 2.5 | 2.5 | 2 | 2 | **2.2** |
| Staff board | 3.5 | 3 | 3 | 2.5 | 3 | **3.0** |
| Roadmap | 3.5 | 3.5 | 3 | 3 | 3 | **3.2** |
| Matters (`admin.html`) | 3 | 3 | 3 | 3 | 2.5 | **2.9** |
| Tasks | 4 | 3.5 | 3.5 | 3 | 3.5 | **3.5** |
| Contacts | 3.5 | 3 | 3 | 2.5 | 3 | **3.0** |

**Worst:** Workspace panel (2.2). **Best:** Tasks (3.5).

---

## 3. TOP-5 Human-Friction Items (the technical audit's lens missed)

1. **A clickable phone number that dials `3****9810`** — `pagliano.html:1568,1831`. Any human who taps "Chiama ora" gets a broken call. No code test flags a masked string inside a `tel:` URI; only a human walkthrough catches the conversion killer.
2. **"New Task" requires a memorized numeric Contact ID** — `kanban.html:685–687,1097`. Staff must stop working, open Contacts, note a number, return. Tasks (11.2) already shows the right pattern (a picker); kanban should reuse it.
3. **The entire workspace/team management runs on `prompt()`/`confirm()`** — `workspace_panel.html:88–209`. Adding one login = three sequential grey dialogs. It *works*, but it feels like the app is still in a terminal — partners notice this instantly in demos.
4. **End-user-visible scaffolding**: "(workspace: Pagliano)" button text (`pagliano.html:1760,2122`), `[da inserire]` P.IVA/REA/Albo (`pagliano.html:1860–1862`), raw `contactid` column (`admin.html:79`), `Loading…` rows (`admin.html:45`). Each is a small trust cut that compounds into "this was built by a developer, not for us."
5. **Mobile navigation amputated**: kanban's nav is `display:none` <900px with no menu (`kanban.html:164–166`) and the standalone staff/roadmap boards have no mobile layout. A lawyer checking cases from their phone literally cannot reach Calendar or Tasks after login.

Bonus 6th (cross-cutting): **toasts everywhere are silent for screen readers** — no `aria-live` on kanban.html:509 or base.html:161; every async action's feedback is invisible to assistive tech.

---

## 4. What a Real Italian Client Would Struggle With

- **Language whiplash:** Pagliano LP is fluent Italian; the intake form (`index.html:9–16`), client status page (`status.html:9,19`), and every "Login to view…" placeholder (`contacts.html:169`, `tasks.html:123`) are English. The client journey starts in Italian and degrades into English exactly at the moment they're sharing personal data.
- **Legal jargon as UI labels:** "Conflict Check", "Waiting Docs", "To Verify", "Engaged" (`kanban.html:563–590`, status.html progress list) — meaningful internally, cryptic to a client tracking their *separazione*.
- **Form length & defaults:** 8 fields + file upload is manageable, but `autocomplete="off"` (`index.html:46,55,59`) forces retyping on mobile, and the silent "Medium" urgency default (`index.html:86`) means urgent matters can arrive labeled medium.
- **Trust signals that backfire:** masked phone, `[da inserire]` legal IDs, stale 2025 blog dates, monogram avatar instead of a lawyer's face.
- **No self-service recovery:** no password reset for partners (only superadmin reset, `admin_panel.html:16`); no "Rifiuta" on the cookie banner.
- **GDPR inconsistency:** the LP promises consent-based processing (`pagliano.html:1754`) while the chat widget collects name/email/phone without a consent step (chat-widget.js:159–208).

---

## 5. Verdict

The design system (colors, typography, kanban, calendar grid) is genuinely strong and the contrast fix landed in 5 templates — but it **missed calendar/tasks button text** (`#fff` on accent, ~4.1:1 in dark mode, `calendar.html:18,35,47`, `tasks.html:25`) and the human layer still has **production-unready scaffolding** (masked phone, prompt()-driven admin, debug button text, raw IDs). Prioritize the five friction items above before any further design polish — they are what a client or partner actually feels in the first 90 seconds.

— Human-like UX walkthrough, 2026-09-04 (read-only; no code changes, no deploy).
