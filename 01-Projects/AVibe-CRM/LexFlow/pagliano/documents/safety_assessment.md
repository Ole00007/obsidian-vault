# Safe to do NOW (zero risk, no breakage)

| Action | Risk | Effort |
|---|---|---|
| **Phase 1 multi-tenancy** — add `tenant_id VARCHAR(50) DEFAULT NULL` to contacts, cases, tasks, events | **Zero** — no code queries it; existing data gets NULL, everything keeps working | 10 min |
| **Auto-task on intake** — after Contact+Case created, add one `Task(title="Follow up — {name}", status="pending")` | **Zero** — additive only, returns same 201 | 15 min |
| **Formatted case ID** — computed property `case_number` on Case model, no schema change | **Zero** | 5 min |
| **Resend email** — set API key in Railway, wire `notify_case_status_changed` to send email to client | **Needs key** — code is already structured, just needs the env var | 10 min |

# NOT safe to do now (will break queries/auth)

| Action | Why |
|---|---|
| **Full tenant isolation (filters, auth, login)** | Every query needs `WHERE tenant_id=…`, login flow needs membership table, existing data has NULL tenant_id. Needs Phases 2–4. |
| **WhatsApp/email webhook integration** | New external dependency, testing needed |
| **AI model for summarization** | Needs provider key + integration + UI |

---

# Current LP state

**Latest file:** `/Users/olesiarasing/Desktop/projects/services/LexFlow-MVP/pagliano/index.html` (79 KB, MD5 `6bf782f0`)
**Synced copy:** `…/pagliano/templates/pagliano.html` (identical)
**Served at:** http://localhost:8877/index.html
**Live on Netlify:** https://verdant-crumble-021449.netlify.app

All today's work is in the working folder at the above path. Ready for your directory of choice.
## Links
- Parent: [[documents-INDEX]]
- Related: [[multi_tenancy_plan]]
