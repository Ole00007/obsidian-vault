---
title: LexFlow — legal publishing blockers (P.IVA + entity + contact)
created: 2026-09-16
tags: [lexflow, legal, compliance, website, blocked, reminder, partita-iva]
status: active
source: "kanban card t_051169c7 (queued by frontend-developer)"
project: LexFlow
---

# LexFlow — legal publishing blockers register

**Registry only — nothing here is implemented.** These are the public-facing values that
must come from Ole (real legal entity + fiscality) before the LexFlow marketing site can be
published. Card: `t_051169c7` (blocked-on-legal, not blocked-on-dev).

**Hard dependency:** item 6 and the cookie/privacy pages cannot be finalised until the
**Partita IVA (P.IVA)** exists — the operating entity is still the placeholder
"Studio Legale X". P.IVA acquisition is therefore the *single* gate item below; everything
else is a text substitution once it is settled.

Verified read-only on **2026-09-16** against repo
`~/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site` (HEAD `88f6cc9`,
31 modified files in flight). No page was edited.

---

## Item 1 — Primary contact address (decision, not a value)

Two addresses are presented as "the" contact, side by side in the **same footer block**:

| File | Lines | Present |
|---|---|---|
| `lexflow-faq.html` | 270–271 | `info@lexflow.com` + `demo@lexflow.com` |
| `lexflow-pricing.html` | 179–180 | `info@lexflow.com` + `demo@lexflow.com` |
| `lexflow-practice-areas.html` | 293–294 | `info@lexflow.com` + `demo@lexflow.com` |
| `lexflow-how-it-works.html` | 153–154 | `info@lexflow.com` + `demo@lexflow.com` |
| `llms.txt` | 60 | `Email: info@lexflow.com · demo@lexflow.com` |
| `lexflow-article-*.html` — **9 article pages** in root (`law-firm-workflows`, `ai-assisted-operations`, `matter-tracker`, `adoption-in-small-firm`, `law-firm-automation`, `security-privacy`, `crm-migration`, `client-communication`, `client-intake`) | ~157–188 | **`demo@lexflow.com` only** |
| same 9 article pages mirrored in `it/` and `ru/` | ~157–183 | **`demo@lexflow.com` only** |
| `privacy.html` | 72, 75 | `info@lexflow.com` (GDPR contact) |

**NEW — inconsistency beyond the card:** the article pages carry **only `demo@`**, while
FAQ / pricing / practice-areas / how-it-works carry **both** (`lexflow-how-it-works.html`
lines 153–154 verified). So there are three different contact patterns in production copy
today, not two.

**Decision needed (proposed default, ready to approve as-is):**
1. **`info@lexflow.com` = primary** general/sales/first-contact address (footer, `llms.txt`,
   privacy/GDPR contact). Keep as the single "contact us" address.
2. **`demo@lexflow.com` = secondary, role-labelled** "request a demo" only, shown with an
   explicit label, never as a second generic contact.
3. Article pages: add the labelled contact pair or reduce to `info@` only — pick one so all
   pages match.
4. Role labels become: `info@` → "General enquiries"; `demo@` → "Request a demo".

Rejected alternative: keep both as generic contacts — that is exactly the ambiguity flagged.

## Item 2 — Legal-entity placeholders on public pages (values needed)

| File | Line | Current (placeholder) | Needed real value |
|---|---|---|---|
| `privacy.html` | 75 | `LexFlow · Studio Legale X · Genova, Italia` — **unflagged** | Legal entity name; registered office; (VAT) |
| `cookie-policy.html` | 47 | `[LEGAL COMPANY NAME]`, `[REGISTERED ADDRESS]`, `[NUMBER]` | Legal entity name; registered office; VAT / company number |
| `cookie-policy.html` | 48 | `[privacy@lexflow.example]`, `[PEC / postal address]` | Privacy contact address; PEC (or postal address) |
| `cookie-policy.html` | 49 | self-flagged "Review before launch" note | delete the note once values are in |
| `cookie-policy.html` | 94 | `[privacy@lexflow.example]` | Privacy contact address (same as line 48) |

**Note:** `privacy.html` line 75 is the dangerous one — it is **not** flagged as a
placeholder, so it reads as final copy while still saying "Studio Legale X". It must not
ship as-is.

**Values needed (one block, OA: Ole):**
- legal entity name and legal form (e.g. `LexFlow S.r.l.` / `Studio Legale Y`)
- registered office (full address)
- VAT / P.IVA number (see item 3)
- PEC address (Italian certified mail) — or an explicit decision to use a postal address
- privacy/GDPR contact address (proposal: `privacy@lexflow.com`, not `privacy@lexflow.example`)

## Item 3 — Partita IVA (P.IVA) — the gate

The entity is still "Studio Legale X", so **no VAT number exists yet**. Consequences:

- `cookie-policy.html` line 47 `[NUMBER]` cannot be filled.
- `privacy.html` line 75 cannot name the operating entity.
- Both pages are legally **unpublishable** until P.IVA is established (Italian consumer /
  GDPR controller-identity requirements).
- Any pre-launch cookie scan (already self-flagged on `cookie-policy.html` line 49) has to
  run *after* the entity details are correct, not before.

**Action for Ole:** open the P.IVA request; when the number/issues are issued, hand back the
full value block from item 2 and the legal pages can be closed out in one dev pass.

---

## One reminder — combined (as requested by the card)

> **Ole — two things that gate the LexFlow site launch, and they are the same task:**
> 1. **P.IVA** — start the request; the operating entity is still "Studio Legale X".
> 2. **Entity/contact block** — when P.IVA is issued, give: legal entity name + form,
>    registered office, VAT/P.IVA, PEC (or decision to use postal), privacy contact address,
>    and the `info@` vs `demo@` decision (proposed default in Item 1).
> Until then `privacy.html` and `cookie-policy.html` stay unpublished and `privacy.html`
> line 75 must not ship as "Studio Legale X".

## Do not do

- **Do not edit** `privacy.html` / `cookie-policy.html` / the footers / `llms.txt` until Ole
  supplies the values — this is blocked-on-legal, not blocked-on-dev.
- **Do not invent** a VAT number, entity name, address or PEC.
- **Do not** put the real values in this note if Ole prefers they stay out of the vault —
  they are public-registry data, so this note is safe to hold them; keep any account
  credentials out (AGENT_RULES: no secrets in notes).

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-2026-09-16-Stack-Decision-and-Task-Board]]
- Related: [[LexFlow-Ecosystem-Index-v3-2026-09-16]]
- Related: [[LexFlow-Web-Site-Agent-Surface-2026-09-15]]
