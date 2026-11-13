# Guida di installazione (Windows 10/11 e macOS) - LexFlow locale + Claude Code + Claude Cowork
Valida per PC ASUS, Samsung, Microsoft (Windows) e Mac. Se un identificativo `winget`/`brew` non viene trovato, usare `winget search` / `brew search`: non improvvisare, annotare e scegliere l'alternativa verificata.

## 1. Requisiti minimi
- Claude Code: macOS 13+, Windows 10 1809+ (o Server 2019+), almeno 4 GB RAM, internet, account Claude. Su Windows non serve essere amministratori; Git for Windows e' consigliato ma facoltativo.
- Claude Desktop (con Cowork): disponibile per macOS e Windows.
- Spazio libero consigliato: 5 GB.

## 2. Programmi da installare (ordine consigliato)
| # | Programma | A cosa serve | Windows (winget) | macOS (brew) | Obbligatorio |
|---|---|---|---|---|---|
| 1 | Claude Desktop (Cowork) | chat e attivita' su file, plugin | scaricare dal sito Claude | scaricare dal sito Claude | si |
| 2 | Claude Code | agente da terminale | `irm https://claude.ai/install.ps1 \| iex` oppure `winget install Anthropic.ClaudeCode` | `curl -fsSL https://claude.ai/install.sh \| bash` | si |
| 3 | Git | scaricare LexFlow, versioni | `winget install Git.Git` | `brew install git` | si |
| 4 | Node.js LTS (>=18) | server MCP lanciati con npx | `winget install OpenJS.NodeJS.LTS` | `brew install node` | si |
| 5 | Python 3.11+ | LexFlow (Flask) e case_tools.py | `winget install Python.Python.3.12` | `brew install python` | si |
| 6 | uv / uvx | server MCP in Python | `winget install astral-sh.uv` | `brew install uv` | consigliato |
| 7 | PostgreSQL | database di LexFlow | `winget install PostgreSQL.PostgreSQL.16` | `brew install postgresql@16` | si (vedi nota LexFlow) |
| 8 | Tesseract + lingue ita, eng | OCR locale di screenshot/scansioni | `winget install UB-Mannheim.TesseractOCR` (selezionare "Italian") | `brew install tesseract tesseract-lang` | si per scansioni |
| 9 | ffmpeg | audio/video | `winget install Gyan.FFmpeg` | `brew install ffmpeg` | facoltativo |
| 10 | 7-Zip / zstd | archivio | `winget install 7zip.7zip` | `brew install zstd` | facoltativo (case_tools usa xz se manca zstd) |
| 11 | Pandoc | bozze in DOCX/PDF | `winget install JohnMacFarlane.Pandoc` | `brew install pandoc` | facoltativo |
| 12 | VS Code | modifica file | `winget install Microsoft.VisualStudioCode` | `brew install --cask visual-studio-code` | facoltativo |
OCRmyPDF e whisper.cpp su Windows possono richiedere WSL o passaggi extra: iniziare senza (Tesseract diretto), aggiungerli solo se servono. PC con processore ARM (alcuni Surface/Galaxy Book): se `pip install` fallisce su un pacchetto, segnalarlo e usare WSL2 o Docker come alternativa.

## 3. LexFlow in locale (dal repository verificato `lexflow-crm`)
Stato verificato: Flask 2.3.3, SQLAlchemy, Flask-Migrate, Flask-JWT-Extended, psycopg2-binary (PostgreSQL), gunicorn, resend (email). File `.env.example` con RESEND_API_KEY, EMAIL_FROM, EMAIL_FROM_NAME, WEBHOOK_SECRET, ADMIN_EMAIL. Avvio CRM: `run_crm.py` (porta 5000). ATTENZIONE: `app.py` e il Procfile avviano la vecchia app di intake, non il CRM.
Non verificato (da controllare nel repository aggiornato): nome della variabile del database (es. DATABASE_URL), comandi di migrazione, e se il repository corrente e' `lexflow-crm` o quello in uso al titolare (backend Flask + frontend React/TypeScript). Chiedere al titolare il repository e il ramo corretti.
Passi:
1. `git clone <URL-del-repository> lexflow` e `cd lexflow`.
2. `python -m venv .venv` ; attivare: Windows `.venv\Scripts\Activate.ps1`, macOS `source .venv/bin/activate`.
3. `pip install -r requirements.txt`.
4. Copiare `.env.example` in `.env` e compilare (mai pubblicare .env). L'invio email e' facoltativo per la prova.
5. Creare il database PostgreSQL locale e impostare la stringa di connessione come da repository; poi migrazioni (`flask db upgrade`, se previsto).
6. Avviare: `python run_crm.py` e aprire http://127.0.0.1:5000.
7. Sicurezza su PC con dati clienti: l'avvio predefinito usa host 0.0.0.0 e debug attivo; limitare a 127.0.0.1 e disattivare il debug (modifica da far fare e rivedere a Claude Code, con commit separato). Se la porta 5000 e' occupata su Mac (AirPlay), usare un'altra porta.
8. Dati reali di clienti in LexFlow: solo dopo verifica di backup, accessi e cifratura del disco (BitLocker/FileVault).

## 4. Collegare Claude (Code e Cowork) agli strumenti (MCP)
- Claude Code: `claude --version`, poi `claude mcp add --transport http <nome> <URL>` per server remoti; per server locali `claude mcp add <nome> -- <comando> [args]`. Su Windows nativo i server avviati con npx vanno avvolti con `cmd /c` (altrimenti errore "spawn npx ENOENT"): `claude mcp add fascicoli -- cmd /c npx -y @modelcontextprotocol/server-filesystem C:/Casi/caso_demo`. In alternativa file `.mcp.json` nella radice del progetto (con `"command": "cmd"` e `"args": ["/c","npx",...]`, percorsi con barre dritte). Verificare con `claude mcp list` e `/doctor`.
- Claude Desktop/Cowork: Impostazioni > Developer > Edit Config apre `claude_desktop_config.json` (Windows `%APPDATA%\Claude\`, macOS `~/Library/Application Support/Claude/`); aggiungere i server sotto `mcpServers`, salvare e RIAVVIARE completamente l'app. Le estensioni `.mcpb` si installano da Impostazioni > Estensioni senza modificare il JSON. I plugin di Cowork possono raggruppare connettori MCP, competenze (skills), comandi, hook e sub-agenti.
- Esempi in `mcp_esempi/`. Principio: un server per sistema, accesso alle sole cartelle del fascicolo, niente accesso all'intero disco.
- Server per iniziare: filesystem (limitato alla cartella pratiche); ffmpeg-mcp-lite (facoltativo); OCR: Tesseract da terminale tramite Claude Code (nessun server necessario).

## 5. Test di accettazione (solo dati sintetici)
T0 `claude --version`, `node --version`, `python --version`, `git --version`, `tesseract --list-langs` (deve comparire ita).
T1 `python case_tools.py init demo`; copiare demo_messages.csv in 04_analysis/messages.csv; `python case_tools.py count <cartella> lexicon_starter.json`. Atteso: Anna 'sorry' letterale=2; gruppo 'apology' Anna S1=3 e totale=4; Bob 'ok' letterale=2 e ambiguo=2; emoji isolata ambigua=1.
T4 `python case_tools.py citecheck file.md`: FAIL su riga lunga senza citazione, PASS con [S1:M1].
T5 `archive` rifiutato senza il file ANALYSIS_COMPLETE; con il file crea archivio e indice; poi `verify`.
T9 import WhatsApp: due esportazioni finte (Android, iOS), `parse-wa --rename "You=Anna"`: righe di sistema escluse, messaggi multilinea intatti.
T12 LexFlow: `python run_crm.py` risponde su http://127.0.0.1:5000.
T13 MCP: `claude mcp list` mostra il server filesystem; in Claude Code chiedere di elencare i file della cartella del fascicolo.
Se un test non passa: annotare l'errore esatto, non modificare gli script, chiedere assistenza.

## 6. Dopo i test
Copiare CLAUDE.md nella cartella del fascicolo; copiare i blocchi di AGENTI_CLAUDE_CODE.md in `.claude/agents/` (verificare la sintassi con `/agents`); iniziare con un fascicolo di prova.
