# LexFlow — P4 Final Build Prompt: Alessia Chatbot Widget
**Approved: 13 May 2026 — Ready to paste into Claude Code**

---

## INSTRUCTIONS FOR CLAUDE CODE

You are a senior Python + JavaScript engineer extending LexFlow, a Flask + SQLite legal intake app.

Read all existing files before touching anything.
Output ONLY the files that change: app.py, templates/index.html
Do NOT rewrite, rename, or restructure anything that already works.

---

## CONTEXT (what already exists)

- `app.py` — Flask app, sqlite3 direct (no ORM)
- `matters` table: id, created_at, token, client_name, email, phone, company,
  practice_area, urgency, description, status, internal_notes, ai_suggestion,
  ai_flag, ai_confidence, ai_accepted
- `POST /submit` — creates matter from intake form → redirects to /status/<token>
- `GET /admin` and `GET /admin/<matter_id>` — admin dashboard
- P7 dark theme applied — CSS vars: --color-surface, --color-border, --color-text,
  --color-text-muted, --color-primary (#7C5CFC as --color-ai)
- Resend email notification working on POST /submit

---

## TASK — Add Alessia Chat Widget + /chat-submit route

### ═══ PART 1: app.py changes (surgical only) ═══

**1a. Safe column additions in init_db() — use ALTER TABLE IF NOT EXISTS pattern:**

```python
safe_columns = [
    "ALTER TABLE matters ADD COLUMN source TEXT DEFAULT 'form'",
    "ALTER TABLE matters ADD COLUMN suggested_lawyer_id INTEGER DEFAULT NULL",
    "ALTER TABLE matters ADD COLUMN suggested_lawyer_reason TEXT DEFAULT NULL",
]
for col_sql in safe_columns:
    try:
        db.execute(col_sql)
    except Exception:
        pass  # column already exists — safe to ignore
```

**1b. Add LAWYERS constant after imports (top of app.py):**

```python
LAWYERS = [
    {"id": 1, "name": "Avv. Marco Rossi",    "specialty": "Corporate, Contracts, M&A"},
    {"id": 2, "name": "Avv. Laura Bianchi",  "specialty": "Family Law, Divorce, Custody"},
    {"id": 3, "name": "Avv. Giovanni Ferri", "specialty": "Criminal Law, Litigation, Urgent matters"},
]
```

**1c. Add/replace classify_intake() helper (full version with lawyer assignment):**

```python
def classify_intake(description):
    """Call Gemini → Claude Haiku → return dict or None on total failure."""
    lawyers_str = "; ".join([f"{l['id']}: {l['name']} ({l['specialty']})" for l in LAWYERS])
    prompt = (
        "You are a legal intake triage assistant for an Italian law firm. "
        "Analyze this intake description and return ONLY valid JSON (no markdown, no explanation) "
        "with exactly these keys: "
        "urgency_override (one of: Low/Medium/High/Critical), "
        "risk_flag (max 12 words, plain language, specific, in Italian), "
        "confidence (integer 0-100), "
        "suggested_lawyer_id (integer, best match from: " + lawyers_str + "), "
        "suggested_lawyer_reason (max 8 words in Italian, plain language). "
        "Description: " + description
    )
    # PRIMARY: Gemini
    try:
        from google import genai as google_genai
        import json, os
        client = google_genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)
    except Exception:
        pass
    # FALLBACK: Claude Haiku
    try:
        import anthropic, json, os
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        text = message.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)
    except Exception:
        pass
    return None
```

**1d. Extract send_notification() helper (if not already extracted) and call from both routes.**

**1e. Add new route POST /chat-submit:**

```python
@app.route("/chat-submit", methods=["POST"])
def chat_submit():
    import secrets
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    description = (data.get("description") or "").strip()
    urgency = data.get("urgency", "Medium")
    language = data.get("language", "it")

    if not name or len(name) < 2:
        return jsonify({"error": "missing_name"}), 400
    if not email or "@" not in email:
        return jsonify({"error": "missing_email"}), 400
    if not description or len(description) < 5:
        return jsonify({"error": "missing_description"}), 400
    if urgency not in ["Low", "Medium", "High", "Critical"]:
        urgency = "Medium"

    token = secrets.token_hex(8).upper()

    try:
        db = get_db()
        db.execute(
            """INSERT INTO matters
               (token, client_name, email, phone, company, practice_area,
                urgency, description, status, internal_notes, source)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (token, name, email, "", "", "General",
             urgency, description, "Nuovo contatto", "", "chatbot")
        )
        db.commit()
        matter_id = db.execute(
            "SELECT id FROM matters WHERE token=?", (token,)
        ).fetchone()["id"]

        result = classify_intake(description)
        if result:
            db.execute(
                """UPDATE matters SET
                   ai_suggestion=?, ai_flag=?, ai_confidence=?,
                   suggested_lawyer_id=?, suggested_lawyer_reason=?
                   WHERE id=?""",
                (
                    result.get("urgency_override"),
                    result.get("risk_flag"),
                    result.get("confidence"),
                    result.get("suggested_lawyer_id"),
                    result.get("suggested_lawyer_reason"),
                    matter_id
                )
            )
            db.commit()

        # Send Resend notification (reuse existing helper)
        try:
            send_notification(name, email, description, urgency, token)
        except Exception:
            pass  # never crash if email fails

        return jsonify({
            "token": token,
            "status_url": url_for("status", token=token),
            "name": name
        })

    except Exception as e:
        app.logger.error(f"chat_submit error: {e}")
        return jsonify({"error": "server_error"}), 500
```

---

### ═══ PART 2: index.html — Add Alessia Chat Widget ═══

Add the following block at the very end of `<body>`, just before `</body>`.
Do NOT modify any existing HTML above it.

**ALESSIA AVATAR:**
Use this image URL directly in the widget:
`https://user-gen-media-assets.s3.amazonaws.com/gemini_images/cf17ce27-fe5a-42dc-b46a-cc1cae8cc093.png`

**WHATSAPP NUMBER:** +393450234084

**Widget HTML + CSS + JS block to insert:**

```html
<!-- ═══ ALESSIA CHAT WIDGET ═══ -->
<style>
/* ── Trigger Button ── */
#chat-trigger {
  position: fixed; bottom: 24px; right: 24px; z-index: 1000;
  width: 60px; height: 60px; border-radius: 50%;
  background: #7C5CFC;
  box-shadow: 0 4px 20px rgba(124,92,252,0.5);
  cursor: pointer; border: none;
  display: flex; align-items: center; justify-content: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  animation: pulse-chat 2s ease-in-out 3;
}
#chat-trigger:hover { transform: scale(1.08); box-shadow: 0 6px 28px rgba(124,92,252,0.65); }
@keyframes pulse-chat {
  0%,100% { box-shadow: 0 4px 20px rgba(124,92,252,0.5); }
  50% { box-shadow: 0 4px 32px rgba(124,92,252,0.85); }
}

/* ── Panel ── */
#chat-panel {
  position: fixed; bottom: 96px; right: 24px; z-index: 999;
  width: 340px; height: 500px;
  background: var(--color-surface, #1c1b19);
  border: 1px solid var(--color-border, #393836);
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.45);
  display: none; flex-direction: column; overflow: hidden;
  transform: translateY(16px); opacity: 0;
  transition: transform 0.25s ease-out, opacity 0.25s ease-out;
}
#chat-panel.open {
  display: flex; transform: translateY(0); opacity: 1;
}

/* ── Header ── */
#chat-header {
  padding: 12px 16px;
  background: linear-gradient(135deg, #7C5CFC 0%, #5B3FD4 100%);
  display: flex; align-items: center; gap: 10px; flex-shrink: 0;
}
#chat-avatar {
  width: 40px; height: 40px; border-radius: 50%;
  object-fit: cover; border: 2px solid rgba(255,255,255,0.3);
  flex-shrink: 0;
}
#chat-header-info { flex: 1; }
#chat-header-name { color: #fff; font-weight: 600; font-size: 0.9rem; line-height: 1.2; }
#chat-header-sub { color: rgba(255,255,255,0.75); font-size: 0.72rem; }
#chat-header-status { display: flex; align-items: center; gap: 4px; margin-top: 2px; }
.online-dot { width: 7px; height: 7px; border-radius: 50%; background: #4ade80; flex-shrink: 0; }
#chat-close {
  background: none; border: none; color: rgba(255,255,255,0.8);
  cursor: pointer; padding: 4px; border-radius: 6px; line-height: 1;
  font-size: 1.1rem; transition: color 0.15s;
}
#chat-close:hover { color: #fff; }

/* ── Language toggle ── */
#lang-toggle {
  display: flex; gap: 4px; margin-left: auto; margin-right: 8px;
}
.lang-btn {
  background: rgba(255,255,255,0.15); border: none;
  color: rgba(255,255,255,0.7); font-size: 0.68rem; font-weight: 600;
  padding: 2px 7px; border-radius: 10px; cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.lang-btn.active { background: rgba(255,255,255,0.35); color: #fff; }

/* ── Messages ── */
#chat-messages {
  flex: 1; overflow-y: auto; padding: 14px;
  display: flex; flex-direction: column; gap: 10px;
  scroll-behavior: smooth;
}
#chat-messages::-webkit-scrollbar { width: 4px; }
#chat-messages::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 4px; }

.msg { display: flex; align-items: flex-end; gap: 8px; max-width: 88%; animation: msgIn 0.2s ease-out; }
@keyframes msgIn { from { opacity:0; transform: translateY(6px); } to { opacity:1; transform: translateY(0); } }
.msg.bot { align-self: flex-start; }
.msg.user { align-self: flex-end; flex-direction: row-reverse; }
.msg-avatar { width: 26px; height: 26px; border-radius: 50%; object-fit: cover; flex-shrink: 0; }
.msg-bubble {
  padding: 9px 13px; font-size: 0.835rem; line-height: 1.45;
  max-width: 100%; word-break: break-word;
}
.msg.bot .msg-bubble {
  background: var(--color-surface-2, #201f1d);
  color: var(--color-text, #cdccca);
  border-radius: 4px 14px 14px 14px;
}
.msg.user .msg-bubble {
  background: #7C5CFC; color: #fff;
  border-radius: 14px 4px 14px 14px;
}

/* Typing dots */
.typing-dots { display: flex; gap: 4px; padding: 12px 14px; align-items: center; }
.typing-dots span {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--color-text-muted, #797876);
  animation: dot-bounce 1.2s ease-in-out infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot-bounce { 0%,80%,100%{transform:translateY(0)} 40%{transform:translateY(-6px)} }

/* Quick reply buttons */
#quick-replies {
  display: flex; flex-wrap: wrap; gap: 6px;
  padding: 8px 14px 4px;
}
.qr-btn {
  padding: 6px 14px; border-radius: 20px; font-size: 0.78rem;
  border: 1.5px solid #7C5CFC; color: #7C5CFC;
  background: transparent; cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.qr-btn:hover, .qr-btn.selected {
  background: #7C5CFC; color: #fff;
}

/* WhatsApp button */
#whatsapp-btn {
  margin: 6px 14px 10px;
  display: flex; align-items: center; justify-content: center; gap: 8px;
  background: #25D366; color: #fff;
  border: none; border-radius: 10px; padding: 11px;
  font-size: 0.85rem; font-weight: 600; cursor: pointer;
  text-decoration: none; transition: background 0.15s;
}
#whatsapp-btn:hover { background: #1ebe5c; }
#whatsapp-btn svg { flex-shrink: 0; }

/* ── Input area ── */
#chat-input-area {
  padding: 10px 12px;
  border-top: 1px solid var(--color-border, #393836);
  display: flex; gap: 8px; align-items: center; flex-shrink: 0;
}
#chat-input {
  flex: 1; background: var(--color-surface-offset, #1d1c1a);
  border: 1px solid var(--color-border, #393836);
  border-radius: 20px; padding: 8px 14px;
  color: var(--color-text, #cdccca); font-size: 0.835rem;
  outline: none; resize: none; line-height: 1.4;
  transition: border-color 0.15s;
}
#chat-input:focus { border-color: #7C5CFC; }
#chat-input::placeholder { color: var(--color-text-faint, #5a5957); }
#chat-send {
  width: 38px; height: 38px; border-radius: 50%;
  background: #7C5CFC; border: none;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; flex-shrink: 0;
  transition: background 0.15s, opacity 0.15s;
}
#chat-send:disabled { opacity: 0.35; cursor: not-allowed; }
#chat-send:not(:disabled):hover { background: #6a48f5; }

/* ── Mobile ── */
@media (max-width: 480px) {
  #chat-panel {
    width: 100vw; height: 72vh;
    bottom: 0; right: 0;
    border-radius: 20px 20px 0 0;
  }
  #chat-trigger { bottom: 16px; right: 16px; }
}
</style>

<!-- Trigger button -->
<button id="chat-trigger" aria-label="Apri chat con Alessia">
  <svg id="chat-icon-open" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
  </svg>
  <svg id="chat-icon-close" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" style="display:none">
    <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
  </svg>
</button>

<!-- Chat panel -->
<div id="chat-panel" role="dialog" aria-label="Chat con Alessia">
  <div id="chat-header">
    <img id="chat-avatar" src="https://user-gen-media-assets.s3.amazonaws.com/gemini_images/cf17ce27-fe5a-42dc-b46a-cc1cae8cc093.png" alt="Alessia">
    <div id="chat-header-info">
      <div id="chat-header-name">Alessia</div>
      <div id="chat-header-status">
        <span class="online-dot"></span>
        <span id="chat-header-sub">Studio Legale — Accoglienza</span>
      </div>
    </div>
    <div id="lang-toggle">
      <button class="lang-btn active" data-lang="it" onclick="setLang('it')">IT</button>
      <button class="lang-btn" data-lang="en" onclick="setLang('en')">EN</button>
    </div>
    <button id="chat-close" aria-label="Chiudi chat">✕</button>
  </div>

  <div id="chat-messages"></div>
  <div id="quick-replies" style="display:none"></div>
  <a id="whatsapp-btn" href="https://wa.me/393450234084" target="_blank" rel="noopener noreferrer" style="display:none">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="#fff"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.126.558 4.121 1.529 5.849L0 24l6.335-1.508A11.934 11.934 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.891 0-3.667-.497-5.207-1.367l-.374-.22-3.759.895.952-3.656-.243-.386A9.935 9.935 0 012 12C2 6.478 6.478 2 12 2s10 4.478 10 10-4.478 10-10 10z"/></svg>
    <span id="wa-label">Chiamaci ora su WhatsApp</span>
  </a>

  <div id="chat-input-area">
    <input id="chat-input" type="text" placeholder="Scrivi qui..." autocomplete="off" aria-label="Messaggio">
    <button id="chat-send" disabled aria-label="Invia">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
      </svg>
    </button>
  </div>
</div>

<script>
(function() {
  const AVATAR_URL = "https://user-gen-media-assets.s3.amazonaws.com/gemini_images/cf17ce27-fe5a-42dc-b46a-cc1cae8cc093.png";
  const WA_NUMBER = "393450234084";

  let lang = "it";
  let step = 0;
  let collected = { name: "", email: "", description: "", urgency: "", language: "it" };
  let isOpen = false;
  let started = false;

  const STRINGS = {
    it: {
      placeholder: "Scrivi qui...",
      waLabel: "Chiamaci ora su WhatsApp",
      headerSub: "Studio Legale — Accoglienza",
      steps: [
        "Buongiorno! Sono Alessia, la responsabile dell'accoglienza. Sono qui per assicurarmi che la sua richiesta arrivi alla persona giusta. 🤝

Come si chiama?",
        (name) => `Piacere, ${name}. Capisco che contattare uno studio legale non è sempre semplice.

Può descrivermi brevemente la situazione per cui cerca assistenza?`,
        "Grazie per aver condiviso questo con me.

Come descriverebbe l'urgenza della sua situazione?",
        (u) => (["High","Critical"].includes(u)
          ? "Capisco, non perdiamo tempo.

A quale email possiamo scriverle per aggiornarla?"
          : "Capito. Voglio assicurarmi che venga seguito dalla persona giusta.

A quale email possiamo scriverle?"),
        (name, email) => `Perfetto, ${name}. Ho trasmesso la sua richiesta al team.

Riceverà conferma a breve a ${email}.

Siamo con lei. 🤝`,
      ],
      urgencyBtns: ["Bassa","Media","Alta","Critica"],
      urgencyVals: ["Low","Medium","High","Critical"],
      errorMsg: "Mi dispiace, si è verificato un problema tecnico. Può riprovare o contattarci direttamente.",
      statusLabel: "Segua lo stato della sua pratica:",
      offTopic: (q) => `Capisco. Per procedere ho bisogno solo di questa informazione. ${q}`,
    },
    en: {
      placeholder: "Type here...",
      waLabel: "Call us on WhatsApp now",
      headerSub: "Legal Firm — Reception",
      steps: [
        "Hello! I'm Alessia, the firm's reception manager. I'm here to make sure your request reaches the right person. 🤝

May I have your name?",
        (name) => `Nice to meet you, ${name}. I understand reaching out to a law firm isn't always easy.

Could you briefly describe the situation you need help with?`,
        "Thank you for sharing that with me.

How would you describe the urgency of your situation?",
        (u) => (["High","Critical"].includes(u)
          ? "I understand — let's not waste time.

What email address can we reach you at?"
          : "Understood. I want to make sure you're seen by the right person.

What email address can we reach you at?"),
        (name, email) => `Perfect, ${name}. Your request has been forwarded to our team.

You'll receive confirmation shortly at ${email}.

You're in good hands. 🤝`,
      ],
      urgencyBtns: ["Low","Medium","High","Critical"],
      urgencyVals: ["Low","Medium","High","Critical"],
      errorMsg: "I'm sorry, a technical issue occurred. Please try again or contact us directly.",
      statusLabel: "Track your case status:",
      offTopic: (q) => `I understand. To proceed I just need this information. ${q}`,
    }
  };

  const trigger = document.getElementById("chat-trigger");
  const panel = document.getElementById("chat-panel");
  const messages = document.getElementById("chat-messages");
  const input = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-send");
  const quickReplies = document.getElementById("quick-replies");
  const whatsappBtn = document.getElementById("whatsapp-btn");
  const iconOpen = document.getElementById("chat-icon-open");
  const iconClose = document.getElementById("chat-icon-close");
  const waLabel = document.getElementById("wa-label");
  const headerSub = document.getElementById("chat-header-sub");

  window.setLang = function(l) {
    lang = l;
    collected.language = l;
    document.querySelectorAll(".lang-btn").forEach(b => b.classList.toggle("active", b.dataset.lang === l));
    input.placeholder = STRINGS[l].placeholder;
    waLabel.textContent = STRINGS[l].waLabel;
    headerSub.textContent = STRINGS[l].headerSub;
  };

  trigger.addEventListener("click", () => {
    isOpen = !isOpen;
    if (isOpen) {
      panel.style.display = "flex";
      setTimeout(() => panel.classList.add("open"), 10);
      iconOpen.style.display = "none";
      iconClose.style.display = "block";
      if (!started) { started = true; setTimeout(() => botMessage(STRINGS[lang].steps[0]), 400); }
      input.focus();
    } else {
      closePanel();
    }
  });

  document.getElementById("chat-close").addEventListener("click", closePanel);

  function closePanel() {
    isOpen = false;
    panel.classList.remove("open");
    setTimeout(() => { if (!isOpen) panel.style.display = "none"; }, 220);
    iconOpen.style.display = "block";
    iconClose.style.display = "none";
  }

  input.addEventListener("input", () => { sendBtn.disabled = input.value.trim() === ""; });
  input.addEventListener("keydown", e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } });
  sendBtn.addEventListener("click", handleSend);

  function botMessage(text) {
    showTyping();
    setTimeout(() => {
      removeTyping();
      const msg = document.createElement("div");
      msg.className = "msg bot";
      msg.innerHTML = `<img class="msg-avatar" src="${AVATAR_URL}" alt="Alessia">
        <div class="msg-bubble">${text.replace(/\n/g,"<br>")}</div>`;
      messages.appendChild(msg);
      scrollBottom();
    }, 900);
  }

  function userMessage(text) {
    const msg = document.createElement("div");
    msg.className = "msg user";
    msg.innerHTML = `<div class="msg-bubble">${escHtml(text)}</div>`;
    messages.appendChild(msg);
    scrollBottom();
  }

  function showTyping() {
    const t = document.createElement("div");
    t.className = "msg bot"; t.id = "typing-indicator";
    t.innerHTML = `<img class="msg-avatar" src="${AVATAR_URL}" alt="">
      <div class="msg-bubble typing-dots"><span></span><span></span><span></span></div>`;
    messages.appendChild(t); scrollBottom();
  }
  function removeTyping() {
    const t = document.getElementById("typing-indicator");
    if (t) t.remove();
  }

  function scrollBottom() { messages.scrollTop = messages.scrollHeight; }
  function escHtml(s) { return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }

  function showQuickReplies(labels, vals, callback) {
    quickReplies.style.display = "flex";
    quickReplies.innerHTML = "";
    input.style.display = "none";
    sendBtn.style.display = "none";
    labels.forEach((label, i) => {
      const btn = document.createElement("button");
      btn.className = "qr-btn"; btn.textContent = label;
      btn.addEventListener("click", () => {
        document.querySelectorAll(".qr-btn").forEach(b => b.disabled = true);
        btn.classList.add("selected");
        userMessage(label);
        quickReplies.style.display = "none";
        input.style.display = "";
        sendBtn.style.display = "";
        callback(vals[i], label);
      });
      quickReplies.appendChild(btn);
    });
    // Show WhatsApp on urgency step
    whatsappBtn.style.display = "flex";
    whatsappBtn.href = `https://wa.me/${WA_NUMBER}`;
  }

  function handleSend() {
    const text = input.value.trim();
    if (!text) return;
    input.value = ""; sendBtn.disabled = true;
    processStep(text);
  }

  function processStep(text) {
    const s = STRINGS[lang];
    userMessage(text);

    if (step === 0) {
      // Name
      if (text.length < 2) { botMessage(s.offTopic(s.steps[0])); return; }
      collected.name = text;
      step = 1;
      setTimeout(() => botMessage(typeof s.steps[1] === "function" ? s.steps[1](text) : s.steps[1]), 300);

    } else if (step === 1) {
      // Description
      if (text.length < 5) { botMessage(s.offTopic(typeof s.steps[1] === "function" ? s.steps[1](collected.name) : s.steps[1])); return; }
      collected.description = text;
      step = 2;
      setTimeout(() => {
        botMessage(s.steps[2]);
        setTimeout(() => showQuickReplies(s.urgencyBtns, s.urgencyVals, (val, label) => {
          collected.urgency = val;
          step = 3;
          const msg = typeof s.steps[3] === "function" ? s.steps[3](val) : s.steps[3];
          botMessage(msg);
        }), 1100);
      }, 300);

    } else if (step === 3) {
      // Email
      if (!text.includes("@") || !text.includes(".")) {
        botMessage(s.offTopic(typeof s.steps[3] === "function" ? s.steps[3](collected.urgency) : s.steps[3]));
        return;
      }
      collected.email = text;
      step = 4;
      whatsappBtn.style.display = "none";
      submitChat();
    }
  }

  function submitChat() {
    const s = STRINGS[lang];
    showTyping();
    fetch("/chat-submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: collected.name,
        email: collected.email,
        description: collected.description,
        urgency: collected.urgency,
        language: lang
      })
    })
    .then(r => r.json())
    .then(data => {
      removeTyping();
      if (data.error) throw new Error(data.error);
      const successMsg = typeof s.steps[4] === "function"
        ? s.steps[4](collected.name, collected.email)
        : s.steps[4];
      const link = `<br><br><a href="${data.status_url}" style="color:#7C5CFC;text-decoration:underline;" target="_blank">${s.statusLabel}</a>`;
      const msg = document.createElement("div");
      msg.className = "msg bot";
      msg.innerHTML = `<img class="msg-avatar" src="${AVATAR_URL}" alt="Alessia">
        <div class="msg-bubble">${successMsg.replace(/\n/g,"<br>")}${link}</div>`;
      messages.appendChild(msg);
      scrollBottom();
      input.style.display = "none";
      sendBtn.style.display = "none";
      document.getElementById("chat-input-area").style.display = "none";
    })
    .catch(() => {
      removeTyping();
      botMessage(s.errorMsg);
      whatsappBtn.style.display = "flex";
    });
  }
})();
</script>
<!-- ═══ END ALESSIA CHAT WIDGET ═══ -->
```

---

## VERIFICATION CHECKLIST (run before committing)

- [ ] `python app.py` starts without error
- [ ] Open index.html → purple chat bubble visible bottom-right
- [ ] Click bubble → Alessia panel opens with chignon avatar
- [ ] Complete 4-step conversation (IT and EN)
- [ ] Urgency quick-reply buttons appear, WhatsApp button visible
- [ ] Submit → check matter appears in /admin with source="chatbot"
- [ ] Purple AI badge appears in admin if Gemini/Claude key present
- [ ] /status/<token> page works from chat link
- [ ] Mobile 375px: panel fills bottom of screen
- [ ] POST /submit (original form) still works unchanged
- [ ] If GEMINI_API_KEY missing → intake still saves, NULL in AI columns

## requirements.txt additions
```
google-genai
anthropic
```

## Links
- Parent: [[widget png-INDEX]]
