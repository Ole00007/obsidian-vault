# Blueprint v4: contesto persistente tra thread, progetti, dispositivi e agenti
Versione 4 | 13 novembre 2026 | Strumenti: Perplexity Projects, Claude Cowork, Claude Code, Obsidian, Hindsight, Hermes Agent
Condiviso per il brainstorming con il legale. Non contiene dati dei clienti.

## 1. Regola di precedenza
L'affidabilità decresce in quest'ordine: 1) istruzioni di progetto scritte da te; 2) file che aggiorni (il registro dei fatti prevale su qualsiasi memoria); 3) memoria automatica (Claude, Hindsight); 4) testo delle chat precedenti. Inserisci ogni fatto critico nei livelli 1-2.

## 2. Cosa persiste
| Livello | Perplexity Projects | Claude Cowork | Guasto principale |
|---|---|---|---|
| Istruzioni | Fino a 8.000 caratteri per progetto ([Help Center](https://www.perplexity.ai/help-center/en/articles/10352961-what-are-projects)) | Istruzioni di progetto più globali ([Anthropic Academy](https://academy.claude.com/courses/introduction-to-claude-cowork/giving-cowork-context)) | Troppo lunghe, contraddittorie, superate |
| File | File system persistente del progetto ([Perplexity](https://www.perplexity.ai/hub/products/projects)) | Cartelle sul tuo computer, montate a ogni sessione | File obsoleto, versione errata, mai salvato nel progetto |
| Memoria | Memoria di progetto ("Brain"); si applica anche la Memory personale, se attiva ([Memory](https://www.perplexity.ai/help-center/en/articles/10968016-memory)) | Automatica, limitata al progetto; condivisa con le chat fuori dai progetti, salvo "Usa la memoria dell'account" disattivato | Dato errato, obsoleto o trapelato |
| Testo dei thread | Non passa ai nuovi thread | Non passa ai nuovi task | Decisioni perse, domande ripetute |

### Claude Cowork: dove stanno i dati
- La [pagina di supporto](https://support.claude.com/it/articles/14116274-organizza-le-tue-attivita-con-i-progetti-in-claude-cowork) (aggiornata il 12 novembre 2026) indica che i nuovi progetti sono salvati nel tuo account Claude: nome, descrizione, istruzioni, link a Google Drive, copia della memoria del progetto. Cartelle e file restano sul tuo computer.
- La [pagina della documentazione](https://claude.com/docs/cowork/guide/projects) indica che i progetti vivono sul computer e non sono sincronizzati. Considerala superata per Pro, Max e Ultra.
- Team ed Enterprise senza "Chat e Cowork unificati": i progetti creati da una cartella esistente restano solo su quel computer.
- Risultato: istruzioni e memoria seguono l'account. I file seguono solo la cartella scelta.

## 3. Dove collocare la cartella del progetto
La cartella si sceglie per ogni progetto; nelle pagine trovate non esiste un'impostazione globale predefinita. Cowork lavora con un percorso locale, quindi vale qualsiasi posizione che il computer vede come cartella.

| Opzione | Cowork | Secondo dispositivo | Costo | Sicurezza | Insidia |
|---|---|---|---|---|---|
| Cartella locale semplice | Sì | No | 0 | Solo cifratura del disco | Unico punto di guasto |
| Vault Obsidian + Obsidian Sync | Sì | Altro computer o telefono (app Obsidian) | 4 USD/mese annuale, 5 USD mensile (Standard) | Cifratura end-to-end (AES-256) | Standard: 1 vault, 1 GB, 5 MB per file |
| Vault in iCloud Drive | Sì | Dispositivi Apple | Incluso nel piano iCloud | Chiavi gestite da Apple | Problemi segnalati su Windows |
| Vault in Google Drive o OneDrive (client desktop) | Sì | Sì | Livello gratuito | Chiavi gestite dal fornitore | Conflitti di sincronizzazione |
| Syncthing | Sì | Computer, Android | Gratis | Da dispositivo a dispositivo | Nessuna app iOS ufficiale |
| Connettore Drive o Microsoft 365 | Solo lettura e ricerca per impostazione predefinita | Sì | Costo del piano | Condizioni del fornitore | Non può essere la cartella di lavoro |

Fonti: [Claude Academy](https://academy.claude.com/courses/introduction-to-claude-cowork/getting-set-up); [prezzi Obsidian](https://obsidian.md/pricing.html); [limiti del piano Standard](https://obsidian.md/blog/standard-plan/); [confronto sync](https://ob-lite.app/guide/en/obsidian-sync-alternatives).

Verdetto: più veloce = cartella del vault scelta alla creazione del progetto; più economica = cartella locale o Syncthing (0), gestita = Obsidian Sync Standard; massima sicurezza = Obsidian Sync (end-to-end) o vault solo locale. La cifratura end-to-end protegge i file a riposo e tra i dispositivi; il testo che Claude legge è trattato secondo le condizioni di Anthropic. I prezzi sono in USD come pubblicati; conferma l'importo in euro all'acquisto.

## 4. Scenari con un secondo dispositivo
Principio: Claude Cowork su telefono o web non apre una cartella locale ([Claude Academy](https://academy.claude.com/courses/introduction-to-claude-cowork/getting-set-up)). I file viaggiano solo tramite il livello di sincronizzazione (Obsidian Sync). Istruzioni e memoria di Claude viaggiano con l'account. Un agente Hermes è un prodotto diverso: non legge il record del progetto Cowork né la memoria di Claude.

| Scenario | File | Istruzioni | Memoria | Verdetto |
|---|---|---|---|---|
| A. Secondo PC con Claude Desktop, stesso account | Obsidian Sync replica il vault | Account | Account | Parità completa a sync terminata |
| B. Telefono, solo app Obsidian | Lettura e modifica note | Nessuna | Nessuna | Solo lettura e appunti |
| C. Telefono, Telegram verso un agente Hermes | Solo se l'host dell'agente vede il vault | Configurazione Hermes (separata) | Banca Hindsight se colleghi entrambi | Funziona; il vault è l'unico registro condiviso |
| D. Telefono, app o web Claude | Non la cartella locale | Account | Account | Solo connettori |
| E. Altro front end di chat (ad esempio Lexflow) | Stessa regola di C: dipende da ciò che l'host dietro di esso può leggere | Configurazione propria | Propria | Non ricercato; non ho trovato documentazione su "Elis Lexflow" |

### Test A: secondo PC
1. PC1: crea il vault, attiva Obsidian Sync (password di cifratura end-to-end nel gestore di password), crea un progetto Cowork su quella cartella, salva `test_A.md`.
2. PC2: installa Obsidian e Claude Desktop, accedi ad entrambi gli account, apri lo stesso vault sincronizzato.
3. Verifica in ordine: `test_A.md` presente; progetto e istruzioni visibili in Cowork; apri il progetto sulla cartella del vault e chiedi: "Leggi test_A.md e cita la riga 1."
4. Esito positivo: tutti e tre i passaggi funzionano. Errore sul file: sync non terminato o vault sbagliato. Errore sul progetto: account o impostazione del piano errati.
5. Modifica da un PC alla volta; attendi la fine del sync prima di cambiare.

### Test C: telefono tramite Telegram e Hermes
1. Decidi dove gira Hermes. Hermes gira su una VM cloud o sul tuo computer, e il gateway serve Telegram, Discord, Slack, WhatsApp, Signal ([repository Hermes](https://github.com/nousresearch/hermes-agent)). Legge il vault solo se l'host ha la cartella del vault. Opzioni non verificate: far girare Hermes su un PC che ha il vault sincronizzato; oppure dare al container un clone git privato del vault.
2. Limita l'accesso: imposta `TELEGRAM_BOT_TOKEN` e `TELEGRAM_ALLOWED_USERS` solo con il tuo ID ([documentazione Telegram di Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram)).
3. Invia: "Leggi test_A.md e cita la riga 1." Esito positivo: citazione corretta. Errore: l'agente non vede il vault; correggi l'host, non il prompt.
4. Invia un fatto che l'agente deve trattenere, poi apri una nuova chat Telegram e chiedilo. Positivo solo se il livello di memoria funziona.
5. Tieni il vault in sola lettura per l'agente finché il test non passa (rischio 20).

## 5. Hindsight: la tua installazione privata
La tua configurazione: solo backend, clonato dal tuo repository GitHub privato, distribuito su Railway, modalità local external. Correzioni al mio testo precedente e cosa dicono le fonti:
- **"Flag"** indica le opzioni da riga di comando `--server self-hosted --api-url ...` dell'installer di Vectorize per Claude Code. La modalità predefinita dell'installer è `cloud`, che invia le sessioni a Hindsight Cloud, il servizio ospitato da Vectorize ([Starry Hope](https://www.starryhope.com/ai/hindsight-memory-for-coding-agents/)). Contano solo se esegui quell'installer. Il tuo server Railway non è il servizio di Vectorize. La tua configurazione prevale sul default; controlla `serverMode` e `apiUrl` in `~/.hindsight/coding-agent.json` su ogni macchina.
- **Chiave LLM.** Il template Railway di Hindsight è fornito con provider LLM impostato su `none`: Hindsight funziona come archivio semantico su modelli locali inclusi; provider e chiave servono solo per estrazione dei fatti, reflect e consolidamento ([template Railway](https://railway.com/deploy/hindsight--hindsight-memory-api)). La mia affermazione precedente che devi fornire una chiave valeva solo per quelle funzioni. La tua istanza può differire; controlla le variabili su Railway.
- **MCP.** Lo stesso template richiede la chiave API "su ogni richiesta REST e MCP", e l'installer registra un server MCP per Claude Code. Se la tua build ha rimosso MCP, indicalo nelle note per il legale; altrimenti presumi che esista.
- **Autenticazione.** La guida Starry Hope dice che l'API non ha login per impostazione predefinita e che l'esempio `docker run` di Hindsight pubblica le porte su ogni interfaccia. Il template Railway attiva l'autenticazione con chiave API. Verifica la tua.
- **Percorso di integrazione.** Hindsight si collega a Claude Code con hook e MCP, e a Hermes con un plugin in modalità `local_external` ([plugin Hermes](https://hermes-agent.nousresearch.com/docs/plugins/hindsight)). Non ho trovato fonti che affermino che Cowork esegua gli hook di Claude Code. Considera il collegamento con Cowork come estensione incrementale tramite Claude Code e verificalo (test D).

### Perché due memorie possono contraddirsi
La memoria di Claude e Hindsight estraggono ciascuna fatti dalle stesse conversazioni, con modelli, regole e tempi diversi. Hindsight inietta il richiamo nel primo prompt della sessione. Il modello vede quindi entrambe le versioni. Un fatto cambiato (una data, una decisione) si aggiorna in un archivio e resta obsoleto nell'altro. Un fatto in Hindsight può essere modificato o invalidato ma non cancellato (issue #3509, secondo [Starry Hope](https://www.starryhope.com/ai/hindsight-memory-for-coding-agents/)). Obsidian aggiunge una terza versione. Mitigazione: il registro dei fatti è l'archivio ufficiale; istruzione: "se memoria e registro differiscono, prevale il registro e la differenza va segnalata."

### Test D: ponte Hindsight
1. Crea una banca col nome della pratica. Da Claude Code (o dal plugin Hermes) trattieni un fatto fittizio: "Fatto di prova: il colore del progetto è verde."
2. Dall'altro agente chiedi il colore del progetto.
3. Cambia il fatto nel registro in "blu"; chiedi di nuovo. Esito positivo: la risposta segnala il conflitto o segue il registro. Errore: dichiara "verde" senza avviso; rafforza l'istruzione.

## 6. Rischi, trappole, mitigazioni
| # | Rischio | Conseguenza | Mitigazione |
|---|---|---|---|
| 1 | La memoria conserva un dato errato o superato | L'errore si ripete in ogni thread | Controlla la memoria ogni mese; elimina o invalida gli errori; tieni ogni fatto critico nel registro con fonte e data |
| 2 | Dichiarazioni dell'utente e fatti verificati si confondono | Un legale riceve un'ipotesi come accertamento | Etichetta ogni riga: `[UTENTE]`, `[VERIFICATO + fonte + data]`, `[IPOTESI]`, `[DA VERIFICARE + chi]` |
| 3 | Domande già risolte vengono ripetute | Tempo perso; risposte incoerenti | Sezione "Risolte" nel file di stato; non richiedere mai |
| 4 | Istruzioni gonfiate | Regole successive ignorate | Massimo 12 regole; il materiale di riferimento va nei file; ripeti i test dopo ogni modifica |
| 5 | Livelli in conflitto (globale, progetto, prompt) | Output imprevedibile | Dichiara la precedenza nelle istruzioni |
| 6 | Dati sensibili (documenti d'identità, coordinate bancarie, dati societari) in file, memoria o sync | Esposizione | Originali offline; copie oscurate; controlla condivisione e fonti collegate prima dei caricamenti |
| 7 | La memoria passa da una pratica all'altra | I fatti della pratica A influenzano la B | Un progetto e una banca di memoria per pratica; disattiva la memoria dell'account per le pratiche sensibili |
| 8 | Proposizioni giuridiche senza fonte o inventate | Un parere errato raggiunge il legale | Disposizione, data, link, applicabilità per ciascuna; elementi non verificati segnalati; approvazione del legale |
| 9 | La norma cambia dopo la verifica | Analisi superata | Data su ogni verifica; ricontrolla prima di depositare |
| 10 | File di stato non aggiornato | La sessione successiva parte da fatti vecchi | Routine di chiusura (sezione 8); suffisso di versione; confronta i file prima di salvare |
| 11 | I file generati restano nella chat | La cartella non contiene l'ultima versione | A fine sessione verifica che il file compaia nella cartella del progetto |
| 12 | Tono sicuro che nasconde prove deboli | Eccesso di fiducia | Chiedi: "Cosa potrebbe smentirlo? Quale affermazione poggia su una sola fonte?" |
| 13 | Lo stile si allontana | I testi non suonano più come i tuoi | File di stile con tre paragrafi campione ed espressioni vietate |
| 14 | Un thread lungo degrada la qualità | Contraddizioni | Un prodotto per thread; sintetizza nel file di stato |
| 15 | Unico punto di guasto | Progetto perso o modifica del prodotto | Copia mensile della cartella in una seconda posizione; esporta il database Hindsight |
| 16 | Conflitti di sincronizzazione quando un agente scrive durante il sync | Duplicati o sovrascritture | Un solo scrittore attivo; attendi il sync; cronologia delle versioni attiva |
| 17 | Due o tre sistemi di memoria (Claude, Hindsight, Obsidian) | Fatti contraddittori | Il registro è l'archivio ufficiale; esegui il test D della sezione 5 dopo ogni modifica |
| 18 | API Hindsight raggiungibile senza login | Chiunque abbia l'URL legge o scrive memoria | Usa l'autenticazione con chiave API del template o la rete privata di Railway; nessun indirizzo pubblico; ruota le chiavi |
| 19 | L'estrazione dei fatti invia testo a un provider LLM | Il testo del cliente esce dal tuo server | Provider `none` per le pratiche dei clienti, oppure un provider con accordo di trattamento dei dati; documenta la scelta |
| 20 | Hermes può eseguire comandi shell nel suo container, e anche chi possiede la sua chiave API ([template Railway](https://railway.com/deploy/hermes-agent-with-hindsight-memory)) | Esecuzione remota di comandi sull'host che contiene il vault | Consenti solo il tuo ID Telegram; chiavi API riservate; vault montato in sola lettura; nessun segreto su quell'host |
| 21 | Telegram come canale per contenuti dei clienti | I messaggi restano su una piattaforma terza (verifica le condizioni di cifratura delle Bot API) | Invia comandi e nomi di file, non fatti del cliente |
| 22 | Nessun controllo accessi per team, agente o memoria in Hindsight (issue aperta #2235, secondo Starry Hope) | Un server condiviso espone ogni banca a ogni agente collegato | Un server o una chiave per cliente; non mescolare pratiche del legale e tue |
| 23 | Cowork potrebbe non eseguire gli hook di Claude Code | Il ponte di memoria non fa nulla in silenzio | Esegui il test D; leggi i log in `~/.hindsight/coding-agents-logs/` |
| 24 | Costi di token e hosting crescono con le sessioni (il reflect del primo prompt è stata la quota maggiore nel test della guida) | Fatture impreviste | Con provider `none` il costo è solo l'hosting; con un provider, controlla la scheda LLM Requests dopo un giorno e fissa un tetto di spesa |
| 25 | Presupposti sbagliati del legale sulla tua configurazione | Brainstorming su premesse false | Condividi questo file con le "correzioni" della sezione 5 intatte |

## 7. Far crescere l'assistente
Ogni correzione diventa una regola o una voce nei file; altrimenti l'errore ritorna.
1. **Registro errori** (`04_ERROR_LOG.md`): cosa era sbagliato, correzione, nuova regola.
2. **Promozione:** una correzione ripetuta due volte passa nelle istruzioni; le regole non usate da 60 giorni escono.
3. **Esempi di riferimento:** due elaborati approvati; istruisci "replica struttura e densità."
4. **Prompt di regressione:** tre prompt di prova fissi (verifica di un fatto, di una fonte giuridica, sintesi) dopo ogni modifica alle istruzioni.
5. **Metriche settimanali:** domande ripetute, affermazioni non verificate, correzioni per elaborato; ognuna deve calare.
6. **Obiettivi espliciti:** obiettivo, prodotto, destinatario, scadenza a ogni avvio di sessione.

## 8. File, prompt, istruzioni
| File | Contenuto |
|---|---|
| `00_STATUS.md` | Stato, decisioni, domande risolte e aperte, prossimi passi |
| `01_FACTS_LEDGER.md` | Una riga per fatto: enunciato, etichetta, fonte, data |
| `02_SOURCES.md` | Link a disposizioni e documenti, data di consultazione |
| `03_VOICE.md` | Regole di tono, espressioni vietate, tre paragrafi campione |
| `04_ERROR_LOG.md` | Correzioni e regole |
| `05_SESSION_LOG.md` | Data, obiettivo, risultato, miglioramenti |

**Apertura sessione**
```
Leggi 00_STATUS.md e 01_FACTS_LEDGER.md. Obiettivo di oggi: [x]. Prodotto: [x]. Destinatario: [x]. Elenca i fatti su cui ti basi e le lacune che bloccano l'obiettivo. Poni solo domande a cui i file non rispondono. Se la memoria richiamata differisce dal registro, segnalalo e segui il registro.
```
**Chiusura sessione**
```
Chiudi sessione. 1) Elenca nuovi fatti e decisioni con le etichette. 2) Restituisci il file 00_STATUS.md completo e aggiornato. 3) Aggiungi righe a 01_FACTS_LEDGER.md e 04_ERROR_LOG.md. 4) Elenca tre affermazioni che poggiano su una sola fonte o su una mia dichiarazione. 5) Indica tre miglioramenti ai miei prompt o alle istruzioni, in ordine di effetto.
```
**Istruzioni di progetto (circa 1.800 caratteri)**
```
RUOLO: Assistente di ricerca per [pratica]. Destinatario: [io / legale].
STILE: Italiano. Diretto. Paragrafi brevi. Tabelle per i confronti. Niente parole riempitive, niente sintesi finale che ripete il testo.
PRECEDENZA: Queste istruzioni prevalgono su quelle globali. Il registro dei fatti prevale su qualsiasi memoria. Un prompt esplicito prevale su di esse solo per quel compito.
AVVIO: Leggi 00_STATUS.md e 01_FACTS_LEDGER.md. Non richiedere mai una domanda indicata come risolta.
ETICHETTE: Contrassegna ogni fatto [UTENTE], [VERIFICATO + fonte + data], [IPOTESI] o [DA VERIFICARE + chi].
DIRITTO: Ogni proposizione giuridica indica disposizione, data, link alla fonte e applicabilità. Segnala gli elementi non verificati. Indica i conflitti tra fonti.
CRITICA: Indica rischi, prove deboli e affermazioni su fonte unica. Offri una tesi contraria.
PRIVACY: Oscura numeri di documenti, coordinate bancarie e numeri di conto in ogni output.
OUTPUT: Fornisci i file in Markdown con suffisso di versione.
CHIUSURA: Al comando "chiudi sessione" esegui la routine di chiusura.
```

## 9. Limiti
- L'assistente opera solo dentro una sessione; la revisione dopo la sessione avviene solo su richiesta.
- Non può verificare la propria memoria; devi leggerla e ripulirla tu.
- Piani, prezzi e funzioni cambiano; ricontrolla le pagine dei fornitori ogni trimestre.
- Le affermazioni su Hermes, Hindsight e Lexflow poggiano su documentazione pubblica e sulla tua descrizione; la tua installazione non è stata ispezionata.
- L'output giuridico supporta il lavoro del legale; non sostituisce la verifica dell'avvocato.
