# Case Swarm - pacchetto per lo studio legale (versione italiana)
Uso: strumento di lavoro per organizzare, analizzare e preparare bozze su un fascicolo (es. separazione), con Claude Code e Claude Cowork sul PC dell'avvocato, collegato a LexFlow in locale.
Non e' un parere legale: ogni bozza, riferimento normativo e strategia va verificato dall'avvocato. Nessun agente invia nulla: solo bozze.

## Contenuto
- SPECIFICA_SWARM_IT.md - flusso di lavoro, regole, verifiche, test.
- GUIDA_INSTALLAZIONE_IT.md - programmi da installare (Windows ASUS/Samsung/Microsoft e Mac), collegamenti a Claude Code/Cowork, MCP, test.
- CLAUDE.md - regole di progetto che Claude Code legge automaticamente (copiare nella cartella del fascicolo).
- AGENTI_CLAUDE_CODE.md - istruzioni dei sub-agenti (da copiare in .claude/agents/).
- ruoli_agenti_IT.csv, formati_strumenti_IT.csv - tabelle di riferimento.
- case_tools.py, lexicon_starter.json, demo_messages.csv - strumenti deterministici (conteggi, hash, import WhatsApp, archivio) e dati di prova.
- modelli/ - 10 modelli in italiano (lettere, piano genitoriale, proposta di accordo, schema di ricorso, strategia, questionario, domande ostili, checklist).
- mcp_esempi/ - esempi di configurazione MCP per Windows e macOS.

## Primo avvio (30 minuti)
1. Seguire la GUIDA_INSTALLAZIONE_IT.md fino ai test T1-T5 (solo dati sintetici).
2. Creare un fascicolo: `python case_tools.py init nome_pratica`.
3. Copiare CLAUDE.md nella cartella del fascicolo; aprire Claude Code in quella cartella.
4. Lavorare per fasi con le approvazioni (GATE) indicate in CLAUDE.md.

## Riservatezza
Dati dei clienti: segreto professionale e GDPR. Prima di usare dati reali, verificare il piano Claude utilizzato (conservazione dati, uso per addestramento, DPA) e le impostazioni dello studio. Per le immagini preferire OCR locale. Non caricare dati reali su GitHub o repository.
