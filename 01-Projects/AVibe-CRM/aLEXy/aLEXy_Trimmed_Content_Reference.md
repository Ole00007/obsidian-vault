# aLEXy — Trimmed / Consolidated Content (Removed from Main Space Description)

This file captures everything that was cut, merged, or summarized out of `MP_aLEXy_FullStack_V5` to fit the 6,950-character Space description limit. Nothing here is lost — it's preserved as reference/backup context.

---

## 1. Local File Paths (dropped from main doc — too granular for the settings field)

- **aLEXy backend (Flask app):** `/Users/olesiarasing/Desktop/aLEXy/`
- **aLEXy landing page (not yet in git):** `/Users/olesiarasing/Desktop/aLEXy/landing page/aLexy_Netlify_READY_index.html`
  - Future deploy target: Netlify
  - Not yet committed to any repo
- **LexFlow-MVP local folder:** NOT YET CONFIRMED — must confirm exact local path before starting any merge/port work in Phase 2.

---

## 2. Original "Confirmed Understanding Table" (raw source, before consolidation)

| Item | Confirmed | Where it lives & environment | Local path |
|---|---|---|---|
| aLEXy = new Flask backend app | Yes | GitHub: Ole00007/aLEXy · Deploy: Railway project 9c6f87e9-2d41-438b-b92c-1f62120b4d6a · DB: PostgreSQL (Railway) | /Users/olesiarasing/Desktop/aLEXy/ |
| aLEXy landing page | Yes | Not yet in git · Future deploy: Netlify | /Users/olesiarasing/Desktop/aLEXy/landing page/aLexy_Netlify_READY_index.html |
| LexFlow-MVP (heritage) | Yes | GitHub: Ole00007/LexFlow-MVP · Deploy: Railway (separate project) · Read-only reference for merge work | Not yet confirmed — confirm exact local folder before merge work starts |

This table was folded into the "CONTEXT — Two repos" section of the main doc as prose bullets, dropping the table format and the local-path column to save space.

---

## 3. Ambiguous / Dropped Line from Original Draft

> "Chatbot chatbot. Goal: merge, no destruction. or build new from scratch."

This line was unclear in the original draft (possible typo/duplicate word, and it introduced a contradictory option — "build new from scratch" — that conflicts with the stated merge-not-replace goal elsewhere in the doc). It was dropped rather than guessed at.

**Open question for founder:** Confirm whether there's ever a scenario where "build new from scratch" is preferred over merge for a specific function, or whether merge-only is the rule with no exceptions.

---

## 4. Repo Structure — Stack Label Conflict (simplified in main doc, full detail here)

Original repo structure listed:
```
/apps/web       (labeled as Next.js)
/apps/api       (labeled as Node.js)
/packages/db    (schema+migrations)
/packages/ai    (model abstraction)
/packages/shared
/scripts
CLAUDE.md at root
```

This directly conflicts with the confirmed landing-page stack note: **Flask + PostgreSQL**, not Next.js/Node.js.

In the main doc, this was shortened to a bracketed flag: *"Confirm this structure matches actual Flask layout before use — flag if mismatched."* Full original labels are preserved here in case the Next.js/Node.js structure is actually correct for a different part of the system (e.g., if the landing page or a future frontend uses Next.js while the backend stays Flask).

**Open question for founder:** Is `/apps/web` + `/apps/api` a Next.js/Node.js structure, or should it be re-labeled for Flask (e.g., `/app`, `templates/`, `static/`, `models.py`, `routes/`)?

---

## 5. Commands — Original Node.js Commands (kept in main doc but flagged, full context here)

Original commands listed were Node.js-centric:
```
npm run dev
npm test
npm run db:migrate
npm run db:seed
npm run build
```

These were kept in the main doc with a parenthetical "(or Flask equivalents — confirm)" rather than guessing at Flask equivalents. Likely Flask equivalents to confirm with founder:

| Node.js command | Likely Flask equivalent (unconfirmed) |
|---|---|
| npm run dev | flask run / python app.py |
| npm test | pytest |
| npm run db:migrate | flask db upgrade (if using Flask-Migrate/Alembic) |
| npm run db:seed | python scripts/seed.py |
| npm run build | N/A for Flask (no build step) or frontend-only build if landing page uses a bundler |

---

## 6. Env Variable Naming Conflict

Main doc uses `NODE_ENV/FLASK_ENV` as a merged placeholder since the original didn't specify which framework's convention applies. Flask typically uses `FLASK_ENV` or `FLASK_DEBUG`; `NODE_ENV` is Node.js-only. This should be resolved once the stack conflict (#4 above) is settled.

---

## Summary of Open Questions for Founder

1. Is the aLEXy backend Flask-only, or is there a separate Next.js/Node.js frontend layer? (Affects repo structure and commands.)
2. Confirm exact local folder path for LexFlow-MVP before Phase 2 merge work starts.
3. Clarify the dropped "build new from scratch" line — is merge-only the hard rule, or are there exceptions?
4. Confirm Flask-equivalent commands for dev/test/migrate/seed/build.
5. Resolve `NODE_ENV` vs `FLASK_ENV` naming once stack is confirmed.

## Links
- Parent: [[aLEXy-INDEX]]
- Related: [[aLEXy_Backend_Handoff_v2]]
