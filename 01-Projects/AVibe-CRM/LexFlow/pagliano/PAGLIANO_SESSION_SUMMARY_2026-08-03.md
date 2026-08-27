PAGLIANO PROJECT — SESSION SUMMARY
Date: 2026-08-03
Author: Hermes agent (lexflow_dev_head_admin profile), for Ole

SCOPE: Avv. Diego Pagliano civil-law intake site. Work limited to pagliano/
folder + root backend (crm/, app.py, wsgi.py, templates/, migrations/) with
explicit user permission. NO changes to the LexFlow GitHub repo were made
beyond the committed, pushed backend fixes below (all in Ole00007/LexFlow-MVP).

=====================================================================
1. WHAT WAS DONE TODAY
=====================================================================

A. LP wiring (pagliano/ — live on Netlify)
   - Click target: Diego's photo placeholder in "Il Professionista"
     (.about-photo div, id="aboutPhoto"). No second CTA existed.
   - Click / Enter / Space -> smooth-scroll to intake form + focus name field;
     form submit POSTs to /api/intake. Image-agnostic (bound to container
     div, not the image file — real PNG swap needs zero code change).
   - Added visible "Richiedi una consulenza" chip overlay + hover/focus styles.
   - Added LOGIN button in header next to theme toggle ->
     https://web-production-ab54f.up.railway.app/
   - Files: pagliano/index.html + pagliano/templates/pagliano.html (synced).

B. Backend (root — committed to Ole00007/LexFlow-MVP, auto-deployed to
   Railway "compassionate-trust" / web-production-ab54f)
   - CORS: flask-cors in crm/__init__.py, origins allow
     https://verdant-crumble-021449.netlify.app + *.netlify.app on /api/*.
   - Auth gate (session-based): /login (GET form + POST), /logout,
     login_required decorator on /admin, /admin/matter/<id>, /load-demo.
     Root "/" now redirects to /admin -> /login when unauthenticated.
     New templates/login.html (Italian, themed). Admin user seeded at
     startup from env ADMIN_EMAIL + ADMIN_PASSWORD (idempotent).
   - /admin now shows CRM intake (contacts + cases: name, email, phone,
     area, priority, status, source, created) in new "Richieste clienti
     (intake)" section; legacy matters table kept below.
   - wsgi.py: registered login/logout routes; admin seed; migration block
     wrapped in PostgreSQL advisory lock (single-flight across gunicorn
     workers + Procfile).

C. Database: ephemeral SQLite -> persistent PostgreSQL
   - Root cause: DATABASE_URL was NOT set -> app used ephemeral
     crm_local.db inside the container -> ALL data wiped on every redeploy.
   - Fix: DATABASE_URL now points to existing Postgres service in Railway
     project "perceptive-achievement" via public TCP proxy
     (postgresql://postgres:***@viaduct.proxy.rlwy.net:37017/railway).
   - Migrations fixed for Postgres compatibility:
       * 9c2d3e4f5a6b: SQLite-only DATETIME -> TIMESTAMP (raw SQL)
       * c3d4e5f6g7h8: gdpr_consent default sa.text('0') -> sa.text("'0'")
     Migrations now at head c3d4e5f6g7h8.
   - Verified: intake POST 201 -> row in Postgres contacts; login 302;
     /admin shows data; data SURVIVED a full redeploy (definitive proof).

D. Admin credentials (final, user-approved)
   - ADMIN_EMAIL = olesya00007@yahoo.com
   - ADMIN_PASSWORD = pagliano0826
   - Old admin@pagliano.it user deleted from Postgres; new user seeded.
   - Verified: new login 302 -> /admin; wrong password 401; old email 401.

=====================================================================
2. COMMITS PUSHED TODAY (Ole00007/LexFlow-MVP, branch main)
=====================================================================
   90c4d65  fix: CORS for Pagliano LP origin on /api/*; LP photo wired to
            intake flow
   bd92752  feat: admin login gate (session auth), CRM intake visible in
            /admin, LP LOGIN button
   3be1d26  fix: use TIMESTAMP not SQLite-only DATETIME in migration
            9c2d3e4f5a6b (Postgres compat)
   fec2114  fix: Postgres-compatible gdpr_consent default; single-flight
            migrations via advisory lock
   (local HEAD == origin/main == fec2114; working tree clean except
    untracked .netlify/ CLI artifact)

=====================================================================
3. KEY URLS / HOSTS
=====================================================================
   LP (Netlify):        https://verdant-crumble-021449.netlify.app
   Backend (Railway):   https://web-production-ab54f.up.railway.app
   Login page:          https://web-production-ab54f.up.railway.app/login
   Admin:               https://web-production-ab54f.up.railway.app/admin
   Intake API:          POST https://web-production-ab54f.up.railway.app/api/intake
                        (also /api/intake/ — both 201, application/json)
   Netlify site ID:     b060d5c1-c7fe-4c3a-be3a-f74d6b3fac18 (team AVibe Agent)
   Railway project:     compassionate-trust (5fb4dd26-3a6b-4646-a8d8-65dddd85eb1f)
   Railway web service: web-production-ab54f, repo Ole00007/LexFlow-MVP (auto-deploy)
   Postgres service:    project perceptive-achievement (1fe25c7a-6a68-4c21-b27f-50c3e69daaf3),
                        service "Postgres" (a5e4ef6c-7a41-402b-b256-c6007790e3df)
   Postgres public URL: postgresql://postgres:***@viaduct.proxy.rlwy.net:37017/railway
   Netlify CLI token:   nfp_aZjSwDnAJhJBpnBwNHwW5VbVdWzETUijdae6 (user-provided)

=====================================================================
4. OPEN ITEMS / FOLLOW-UPS (not implemented, by instruction)
=====================================================================
   - Diego login works, but no "change password" UI yet — suggest adding it.
   - Postgres is shared with the other project (perceptive-achievement);
     Option B (new DB in compassionate-trust + pg_dump/restore) available
     if co-location / private network wanted. Railway does NOT support
     moving a service between projects (manual process).
   - Test rows in Postgres contacts (emails like *0803@example.com) can be
     deleted; harmless if left.
   - .netlify/ folder in repo root is an untracked CLI artifact — safe to
     delete: rm -rf .netlify

## Links
- Parent: [[pagliano-INDEX]]
- Related: [[STYLEBOOK]]
