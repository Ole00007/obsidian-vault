---
title: LexFlow Web-Site — agent-facing surface (WebMCP, ai-plugin.json, openapi.yaml, llms.txt, schema)
created: 2026-09-16
tags: [lexflow, web-site, agent-surface, webmcp, openapi, llms-txt, schema, vault-logging]
status: active
repo: /Users/olesiarasing/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site
commit: b9b406a (agent surface) · repo HEAD 88f6cc9
source_card: t_c421f430
---

# LexFlow Web-Site — agent-facing surface

Vault logging requested by `frontend-developer` (kanban card `t_c421f430`), captured and
re-verified against the repo and live endpoints on **2026-09-16**. Project is the
**LexFlow marketing web-site** (static, trilingual) — NOT the Flask CRM.

Repo: `/Users/olesiarasing/Desktop/projects/services/LEGAL/LEXFLOW Production/LEXFLOW Web-Site`

## 1. OpenAI-style plugin manifest — `.well-known/ai-plugin.json`

- 1,563 bytes, `auth: none`, points at the OpenAPI below.
- Hard guardrails in `description_for_model`: no legal advice; ISO/IEC 27001 & 27701
  **in progress and NOT held**; SOC 2 is an auditing framework, not a certification;
  notifications / cloud / calendar sync are **planned, not available**.
- Committed in `b9b406a` (the agent-surface commit).

## 2. Public contract — `.well-known/openapi.yaml`

- 3,983 bytes. Documents the single public unauthenticated write the site needs:
  **`POST /api/public/intake`**.
- Status: **contract-defined, not yet enabled.** Re-verified live 2026-09-16 against
  `https://web-production-031a6.up.railway.app`: `POST /api/public/intake` → **404**,
  `POST /api/contacts` → **401**, `GET /api/chatbot` → **404**.
- Maps to operator-installer cards `t_d6065167` and `t_85d62411` (both since superseded —
  see [[LexFlow-Public-Intake-Contract-2026-09-15]]).

## 3. WebMCP tool registration — `assets/webmcp.js`

- W3C Community Group proposal (webmachinelearning.github.io/webmcp), registered via
  `navigator.modelContext.registerTool`.
- Six tools, **verified by grep on 2026-09-16**: `get_product_facts`, `get_pricing`,
  `request_demo`, `ask_elisa`, `contact_lexflow`, `find_article`.
- Progressive enhancement: no-ops where the API is absent. Loaded on all 19 English pages
  plus all localised pages.

## 4. `llms.txt` refreshed

- Corrected stale facts ("small law firms", "firms of roughly 5-20 people",
  "Starter / Professional").
- Added seven missing article links and a new section
  **"Machine-readable and agent surfaces"** (verified present in the file's headings).
- Known residual: line 18's "calendar/cloud/notifications NOT shipping" contradicts the
  FAQ (`faq_a15`) — flagged 2026-09-15, still the first copy fix to make.

## 5. Site schema upgraded on `lexflow-index.html`

- Single `Organization` JSON-LD node became **Organization + WebSite + SoftwareApplication**
  with stable `@id` anchors.
- `knowsLanguage` / `inLanguage` **en / it / ru**; sales `ContactPoint` with
  `availableLanguage`; `potentialAction` targeting the demo form.

## 6. Sitemap regenerated

- **48 `<loc>` URLs** (verified 2026-09-16): 9 articles × EN/IT/RU plus main pages.
- The `.well-known` manifests are not page URLs and are deliberately NOT in the sitemap.

## Durable facts worth keeping

- Agent surface committed as **`b9b406a`**; later repo HEAD is **`88f6cc9`**
  ("Article info box: real links to the intake form and Elisa"). Nothing pushed, nothing deployed.
- The repo has **NO git remote and NO deploy config** (`git remote -v` empty; no
  `netlify.toml`, `vercel.json`, `wrangler.toml`) — deployment is impossible until a
  host/remote is chosen. See [[LexFlow-Ecosystem-Index-v3-2026-09-16]].
- **74 files** still carry the `lexflow.example.com` placeholder (canonical, OG, sitemap,
  plugin manifest, OpenAPI servers) — must be replaced before launch.
- `assets/site-config.js` still has **33 nulls** (webhooks), placeholder prices, and an
  unconfirmed WhatsApp number.
- **Content pipeline fact:** localised article bodies come from `templates/article_content.py`
  (`ARTICLES`). An article not registered there silently stays ENGLISH on `/it/` and `/ru/` —
  that was the recurring "page not translated" bug (`matter-tracker`, `client-intake`), now
  fixed by registering all nine.
- The build regenerates `it/`, `ru/` and `sitemap.xml`; **never hand-edit those**. Run:
  `python3 templates/build-lang-sites.py`.
- Working tree was **dirty (31 modified files)** on 2026-09-16 because of the in-flight
  CTA-wiring card `t_198870bd`; nothing was committed or reverted by this logging pass.

## Links

- Parent: [[LexFlow-INDEX]]
- Related: [[LexFlow-Public-Intake-Contract-2026-09-15]]
- Related: [[LexFlow-Web-Site-Session-Recap-Batch2-2026-09-13]]
- Related: [[LexFlow-Ecosystem-Index-v3-2026-09-16]]
