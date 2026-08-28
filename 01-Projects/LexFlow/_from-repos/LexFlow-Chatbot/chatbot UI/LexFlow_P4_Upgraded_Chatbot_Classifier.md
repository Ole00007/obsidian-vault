# LexFlow — P4 Upgraded: AI Chatbot Intake Classifier
**Updated: 13 May 2026 — Surgical upgrade to P4**

---

## What Changed vs. Original P4

The original P4 was: submit form → AI classifies → purple badge in admin.

The upgraded P4 is: **chatbot widget on client-facing site** → friendly conversation collects intake data → same AI classifier runs → same purple badge in admin → auto-assigns to lawyer.

Everything in the admin stays identical. Only the client-side input method changes.

---

## Architecture: How It Works

```
CLIENT WEBSITE (index.html)
  └── Chat widget (bottom-right bubble, pure JS + CSS)
        └── Guided conversation: 3–4 questions max
              └── On "Send" → POST /chat-submit (new route)
                    └── Stores matter in SQLite (same table, same columns)
                          └── Calls AI classifier (same function, reused)
                                └── Returns token → shows status page link to user
                                      └── Purple badge appears in admin ✅
```

No new tables. No new DB columns beyond the original P4 ones. One new route. One new template partial.

---

## Question 2: Free AI Alternatives to GPT-4o-mini

No paid subscriptions. Ranked by ease for your Flask stack:

| Option | Cost | How to get key | Quality | Notes |
|---|---|---|---|---|
| **Google Gemini 1.5 Flash** ✅ | Free (1M tokens/day) | aistudio.google.com → Get API key | ⭐⭐⭐⭐ | Best free option. Fast, JSON-reliable, generous limit |
| **Groq (Llama 3.1 8B)** ✅ | Free tier (generous) | console.groq.com → free account | ⭐⭐⭐ | Extremely fast. Slightly less precise on structured JSON |
| **Claude via API** | Free trial credits | console.anthropic.com | ⭐⭐⭐⭐⭐ | Best quality. Trial credits run out, then paid |
| ~~GPT-4o-mini~~ | Paid after trial | — | — | Removed per your constraint |

**My pick for you: Google Gemini 1.5 Flash.**
- Free API key in 2 minutes at aistudio.google.com
- No credit card required
- 1 million tokens/day free — enough for thousands of intakes
- Python library: `google-generativeai` (one pip install, same interface pattern)

---

## Surgical Changes to the P4 Prompt

### CHANGE 1 — Replace GPT-4o-mini with Gemini Flash

**Remove from prompt:**
```
- API key from env: os.getenv("OPENAI_API_KEY")
- Call OpenAI API (gpt-4o-mini)
- Add openai to requirements.txt
```

**Replace with:**
```
- API key from env: os.getenv("GEMINI_API_KEY")
- Use google-generativeai library:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    result = json.loads(response.text)
- Add google-generativeai to requirements.txt
- Same try/except fallback: NULL on any failure, never crash the form
```

---

### CHANGE 2 — Add Chat Widget to index.html

**Add to the prompt after task 4 (store result in DB):**

```
5. Add a chat intake widget to index.html:
   - Floating button bottom-right: purple circle with chat icon (✦ or ✉)
     style: position fixed; bottom 24px; right 24px; z-index 1000;
            background #7C5CFC; border-radius 50%; width 56px; height 56px;
            cursor pointer; box-shadow 0 4px 16px rgba(124,92,252,0.4)
   - Click opens a chat panel (240px wide, 380px tall, above the button):
     style: position fixed; bottom 92px; right 24px; background var(--color-surface);
            border-radius var(--radius-lg); box-shadow var(--shadow-lg);
            display flex; flex-direction column; overflow hidden
   - Chat panel has: header "LexFlow Assistant", message area, input + Send button
   - The conversation is purely JS — no new backend routes for the chat itself
   - Script handles a linear 4-step flow stored in a JS array:

     STEP 0 (auto): "Ciao! Sono l'assistente LexFlow. Come posso aiutarti oggi?"
     STEP 1: "Qual è il tuo nome completo?"  → stores name
     STEP 2: "In breve, descrivi il tuo problema legale."  → stores description
     STEP 3: "Come valuteresti l'urgenza? (Bassa / Media / Alta / Critica)"  → stores urgency
     STEP 4: "Qual è la tua email per ricevere aggiornamenti?"  → stores email

   - After step 4: show "Sto elaborando la tua richiesta..." (1.5s delay)
   - Then: JS submits a hidden form via fetch() POST to /chat-submit with collected fields
   - On success response (JSON with token): show "✅ Richiesta inviata!
     Segui lo stato qui: [link to /status/<token>]"
   - On error: show "Si è verificato un errore. Riprova."

6. Add new route POST /chat-submit to app.py:
   - Accepts JSON body: name, description, urgency, email
   - Inserts into matters table with:
       client_name = name
       email = email
       description = description
       urgency = urgency
       practice_area = "General"  (default — no practice area in chat flow)
       status = "New intake"
       token = secrets.token_hex(8).upper()
   - Runs the SAME AI classifier function (extract to a helper def classify_intake(description))
   - Sends the same Resend notification email
   - Returns JSON: {"token": "<token>", "status_url": "/status/<token>"}

IMPORTANT — extract AI call to a reusable helper:
   def classify_intake(description):
       # ... Gemini call here ...
       # returns dict with ai_suggestion, ai_flag, ai_confidence or None on failure

   Call this helper from BOTH POST /submit (form) AND POST /chat-submit (chatbot).
   This avoids duplicating the AI logic.
```

---

## What the Admin Sees (Unchanged)

The purple badge appears identically whether the intake came from the form or the chatbot.
The only difference: matters from chatbot will show `practice_area = "General"` until a lawyer reassigns.
This is fine for MVP — P3 (lawyer assignment) handles routing next.

---

## Revised Full P4 Prompt (Complete, Ready to Paste)

```
You are a senior Python engineer extending a Flask + SQLite app called LexFlow.

CONTEXT:
- app.py uses sqlite3 directly (no ORM)
- matters table: id, created_at, token, client_name, email, phone, company,
  practice_area, urgency, description, status, internal_notes
- POST /submit creates a matter from the intake form, redirects to /status/<token>
- Admin at /admin and /admin/<matter_id>
- P7 dark theme applied — purple accent is #7C5CFC (CSS var --color-ai)
- Resend email notification already working on POST /submit

TASK — Upgraded P4: AI Classifier + Chatbot Widget

═══ PART A: Gemini AI Classifier ═══

1. Add to init_db() matters table (ALTER TABLE safe pattern — only add if column missing):
   ai_suggestion TEXT DEFAULT NULL
   ai_flag TEXT DEFAULT NULL
   ai_confidence INTEGER DEFAULT NULL
   ai_accepted INTEGER DEFAULT 0   (0=pending, 1=accepted, 2=dismissed)

2. Add a reusable helper function:
   def classify_intake(description):
       try:
           import google.generativeai as genai, json, os
           genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
           model = genai.GenerativeModel("gemini-1.5-flash")
           prompt = (
               "You are a legal intake triage assistant. "
               "Analyze this intake description and return ONLY valid JSON "
               "with exactly these keys: "
               "urgency_override (one of: Low/Medium/High/Critical), "
               "risk_flag (max 12 words, plain language, specific), "
               "confidence (integer 0-100). "
               "Description: " + description
           )
           response = model.generate_content(prompt)
           return json.loads(response.text)
       except Exception:
           return None

3. In POST /submit, after INSERT, call classify_intake(description):
   - If result is not None: UPDATE matters SET ai_suggestion, ai_flag, ai_confidence
   - If None: leave columns as NULL — never crash the form

═══ PART B: Admin UI (same as original P4) ═══

4. admin.html — add AI column to matter list:
   - ai_flag not NULL + ai_accepted==0: purple badge "⚡ AI Flag"
     style: background #7C5CFC; color white; border-radius 12px;
            padding 2px 10px; font-size 0.75rem; font-weight 500
   - ai_accepted==1: small green "✓ Accepted"
   - ai_accepted==2: small muted grey "Dismissed"
   - ai_flag is NULL: "—"

5. admin_matter.html — AI Insights card:
   - Title: "⚡ AI Intake Analysis" with #7C5CFC left-border accent
   - Show: Suggested urgency | Risk flag | Confidence % bar (CSS only, color #7C5CFC)
   - Buttons (only if ai_accepted==0):
     "Accept" → POST /admin/<id>/ai-accept
     "Dismiss" → POST /admin/<id>/ai-dismiss

6. New routes:
   POST /admin/<int:matter_id>/ai-accept  → ai_accepted=1, redirect back
   POST /admin/<int:matter_id>/ai-dismiss → ai_accepted=2, redirect back

═══ PART C: Chat Widget on index.html ═══

7. Add to index.html (at bottom of <body>, before </body>):
   A floating chat button + panel — pure HTML/CSS/JS, no external libraries.

   Chat button: fixed bottom-right purple circle (56×56px, #7C5CFC, shadow)
   Chat panel: opens above button, 300px wide, 400px tall, dark surface card

   4-step guided conversation (JS state machine, array of steps):
     Bot opens with: "Ciao! Come posso aiutarti?"
     Step 1 — asks: "Il tuo nome completo?"
     Step 2 — asks: "Descrivi brevemente il problema legale."
     Step 3 — asks: "Urgenza? (Bassa / Media / Alta / Critica)"
     Step 4 — asks: "La tua email per gli aggiornamenti?"

   After step 4:
   - Show typing indicator (animated dots, 1.5s)
   - fetch() POST to /chat-submit with JSON body:
     {name, description, urgency, email}
   - On success: show "✅ Inviato! Segui qui: <a href='/status/<token>'>stato pratica</a>"
   - On error: show "Errore. Riprova."

   Style: match existing dark theme variables (--color-surface, --color-primary,
   --color-text, --color-border). Messages: user messages right-aligned #7C5CFC bg,
   bot messages left-aligned --color-surface-2 bg.

8. New route POST /chat-submit in app.py:
   - Accepts JSON: name, email, description, urgency
   - Validates: name and email required (return 400 JSON error if missing)
   - INSERT into matters:
       client_name, email, description, urgency,
       practice_area="General", status="New intake",
       token=secrets.token_hex(8).upper(),
       phone="", company="", internal_notes=""
   - Call classify_intake(description) → store result same as POST /submit
   - Send Resend notification email (same as POST /submit — extract to helper if not already)
   - Return JSON: {"token": "<token>", "status_url": url_for("status", token=token)}

RULES:
- Extend only. Do NOT rename columns, change existing form fields, or rewrite routes.
- Output only changed files: app.py, templates/index.html, templates/admin.html,
  templates/admin_matter.html
- Add google-generativeai to requirements.txt
- classify_intake() must be called from both POST /submit and POST /chat-submit
- Graceful fallback everywhere — if Gemini fails, NULL in DB, intake still saved
- Chat widget must not break the existing intake form (they coexist on index.html)
- Keep all existing CSS variables and theme intact
- No horizontal scroll at 375px mobile

VERIFY before outputting:
- POST /submit works without GEMINI_API_KEY (NULL fallback, no crash)
- Chat widget opens/closes on button click
- Chat completes 4 steps and submits to /chat-submit
- /chat-submit creates matter + returns token JSON
- Purple badge appears in admin after both form AND chat intake
- Accept/Dismiss updates DB
```

---

## Task Checklist (Updated)

| # | Task | Time |
|---|---|---|
| 1 | Get Gemini API key at aistudio.google.com (free, no card) | 5 min |
| 2 | Add GEMINI_API_KEY to Railway Variables (app service) | 3 min |
| 3 | Paste the full prompt above into Claude Code with your current app.py | 5 min |
| 4 | Copy returned files into project | 10 min |
| 5 | Run `python app.py` locally → test form intake → check badge | 15 min |
| 6 | Test chat widget: complete conversation → check matter in admin | 15 min |
| 7 | `git add . && git commit -m "P4: AI classifier + chat widget" && git push origin main` | 5 min |
| 8 | Verify on Railway live URL | 10 min |

**Total: ~1.5 hours**

---

## Demo Moment (Upgraded)

1. Open the client website on your phone
2. Tap the purple bubble bottom-right
3. Have the lawyer friend watch the chat: 4 questions, friendly Italian
4. Submit → status page link appears in chat
5. Switch to admin on laptop: purple AI badge already there
6. *"It read the description, flagged the urgency, and assigned it — before I touched anything."*
