# Blueprint: contesto persistente tra thread, progetti e sessioni
Versione 2 | 13 novembre 2026 | Strumenti: Perplexity Projects, Claude Cowork

## 1. Regola di precedenza
L'affidabilità decresce in quest'ordine: 1) istruzioni di progetto scritte da te; 2) file di progetto che aggiorni; 3) memoria automatica; 4) testo delle chat precedenti. Inserisci ogni fatto critico nei livelli 1-2. Considera la memoria una comodità, mai il registro ufficiale.

## 2. Cosa persiste
| Livello | Perplexity Projects | Claude Cowork | Guasto principale |
|---|---|---|---|
| Istruzioni | Fino a 8.000 caratteri per progetto ([Help Center](https://www.perplexity.ai/help-center/en/articles/10352961-what-are-projects)) | Istruzioni di progetto più istruzioni globali ([Anthropic Academy](https://academy.claude.com/courses/introduction-to-claude-cowork/giving-cowork-context)) | Troppo lunghe, contraddittorie, superate |
| File | File system persistente del progetto ([Perplexity](https://www.perplexity.ai/hub/products/projects)) | Cartelle di progetto ([documentazione Claude](https://claude.com/docs/cowork/guide/projects)) | File obsoleto, versione errata, file mai salvato nel progetto |
| Memoria | Memoria di progetto ("Brain"); si applica anche la Memory personale, se attiva ([Memory](https://www.perplexity.ai/help-center/en/articles/10968016-memory)) | Automatica, limitata al progetto; condivisa con le chat fuori dai progetti, salvo memoria account disattivata ([supporto Claude](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork)) | Dato errato, obsoleto o trapelato |
| Testo dei thread | Non passa ai nuovi thread | Non passa ai nuovi task | Decisioni perse, domande ripetute |

Conflitto tra fonti: la pagina di supporto di Claude descrive dati di progetto salvati nell'account; la pagina della documentazione descrive cartelle sul tuo computer. Verifica prima di fidarti: crea un file e apri il progetto da un secondo dispositivo.

## 3. Rischi, trappole, mitigazioni
| # | Rischio | Conseguenza | Mitigazione |
|---|---|---|---|
| 1 | La memoria conserva un dato errato o superato | L'errore si ripete in silenzio in ogni thread | Controlla la memoria ogni mese; elimina gli errori; tieni ogni fatto critico nel registro dei fatti con fonte e data |
| 2 | Dichiarazioni dell'utente e fatti verificati si confondono | Un legale o una controparte riceve un'ipotesi come accertamento | Etichetta ogni riga: `[UTENTE]`, `[VERIFICATO + fonte + data]`, `[IPOTESI]`, `[DA VERIFICARE + chi]` |
| 3 | Domande già risolte vengono ripetute in un nuovo thread | Tempo perso; risposte incoerenti | Sezione "Risolte" nel file di stato; regola: non richiedere mai ciò che vi compare |
| 4 | Istruzioni gonfiate | Regole successive ignorate; limite raggiunto | Massimo 12 regole; sposta il materiale di riferimento nei file; ripeti i test dopo ogni modifica |
| 5 | Livelli in conflitto (globale, progetto, prompt) | Tono o formato imprevedibili | Dichiara la precedenza: il progetto prevale sul globale; il prompt prevale sul progetto solo se esplicito |
| 6 | Dati sensibili nei file di progetto (documenti d'identità, coordinate bancarie, dati societari) | Esposizione tramite condivisione, connettori o memoria | Conserva gli originali offline; carica copie oscurate; controlla condivisione e fonti collegate prima di ogni caricamento |
| 7 | La memoria passa da una pratica all'altra | I fatti della pratica A influenzano la pratica B | Un progetto per pratica; per le pratiche sensibili disattiva la memoria dell'account o personale |
| 8 | Proposizioni giuridiche senza fonte o inventate | Un parere errato raggiunge il legale | Regola: ogni proposizione riporta disposizione, data, link alla fonte, applicabilità; elementi non verificati segnalati; approvazione del legale |
| 9 | La norma cambia dopo la verifica | Analisi superata | Data su ogni verifica; ricontrolla prima di depositare o negoziare |
| 10 | File di stato non aggiornato | La sessione successiva parte da fatti vecchi | Rituale di chiusura (sezione 6); suffisso di versione `_v3`; confronta il nuovo file con il precedente prima di salvare |
| 11 | I file generati restano nella chat | Il progetto non contiene l'ultima versione | A fine sessione verifica che il file compaia tra i File del progetto; tieni una copia locale |
| 12 | Tono sicuro che nasconde prove deboli | Eccesso di fiducia | Chiedi: "Cosa potrebbe smentirlo? Quale affermazione poggia su una sola fonte?" |
| 13 | Lo stile si allontana | I testi non suonano più come i tuoi | Tieni un file di stile con tre paragrafi campione e un elenco di espressioni vietate |
| 14 | Un thread lungo degrada la qualità | Contraddizioni, regole dimenticate | Un prodotto per thread; sintetizza nel file di stato; apri un nuovo thread |
| 15 | Unico punto di guasto | Progetto perso o comportamento del prodotto modificato | Esporta i file ogni mese sul tuo disco |

## 4. Far crescere l'assistente
Metodo: ogni correzione diventa una regola o una voce nei file. Altrimenti lo stesso errore ritorna.

1. **Registro errori.** Dopo ogni sessione annota: cosa era sbagliato, la correzione, la nuova regola. File: `04_ERROR_LOG.md`.
2. **Promozione.** Una correzione ripetuta due volte passa nelle istruzioni. Le regole non usate da 60 giorni escono dalle istruzioni.
3. **Esempi di riferimento.** Conserva due elaborati finiti che hai approvato. Istruisci: "Replica struttura e densità dei file di riferimento."
4. **Prompt di regressione.** Tieni tre prompt di prova fissi (ad esempio: verifica di un fatto, verifica di una fonte giuridica, una sintesi). Eseguili dopo ogni modifica alle istruzioni e confronta con le risposte precedenti.
5. **Metriche settimanali.** Conta le domande ripetute, le affermazioni non verificate negli elaborati, le correzioni per elaborato. Obiettivo: calo settimana su settimana.
6. **Obiettivi espliciti.** Apri ogni sessione con obiettivo, prodotto, destinatario, scadenza. L'assistente non deduce le priorità.

## 5. Struttura dei file per progetto
| File | Contenuto |
|---|---|
| `00_STATUS.md` | Stato attuale, decisioni, domande risolte, domande aperte, prossimi passi |
| `01_FACTS_LEDGER.md` | Una riga per fatto: enunciato, etichetta, fonte, data |
| `02_SOURCES.md` | Link a disposizioni e documenti, data di consultazione |
| `03_VOICE.md` | Regole di tono, espressioni vietate, tre paragrafi campione |
| `04_ERROR_LOG.md` | Correzioni e regole che ne derivano |
| `05_SESSION_LOG.md` | Data, obiettivo, risultato, miglioramenti |

## 6. Prompt
**Apertura sessione**
```
Leggi 00_STATUS.md e 01_FACTS_LEDGER.md. Obiettivo di oggi: [x]. Prodotto: [x]. Destinatario: [x]. Elenca i fatti su cui ti basi e le lacune che bloccano l'obiettivo. Poni solo domande a cui i file non rispondono.
```
**Chiusura sessione**
```
Chiudi sessione. 1) Elenca nuovi fatti e decisioni con le etichette. 2) Restituisci il file 00_STATUS.md completo e aggiornato. 3) Aggiungi righe a 01_FACTS_LEDGER.md e 04_ERROR_LOG.md. 4) Elenca tre affermazioni che poggiano su una sola fonte o su una mia dichiarazione. 5) Indica tre miglioramenti ai miei prompt o alle istruzioni, in ordine di effetto.
```

## 7. Istruzioni di progetto da incollare (circa 1.700 caratteri)
```
RUOLO: Assistente di ricerca per [pratica]. Destinatario: [io / legale].
STILE: Italiano. Diretto. Paragrafi brevi. Tabelle per i confronti. Niente parole riempitive, niente sintesi finale che ripete il testo.
PRECEDENZA: Queste istruzioni prevalgono su quelle globali. Un prompt esplicito prevale su di esse solo per quel compito.
AVVIO: Leggi 00_STATUS.md e 01_FACTS_LEDGER.md. Non richiedere mai una domanda indicata come risolta.
ETICHETTE: Contrassegna ogni fatto [UTENTE], [VERIFICATO + fonte + data], [IPOTESI] o [DA VERIFICARE + chi].
DIRITTO: Ogni proposizione giuridica indica disposizione, data, link alla fonte e applicabilità. Segnala gli elementi non verificati. Indica i conflitti tra fonti.
CRITICA: Indica rischi, prove deboli e affermazioni su fonte unica. Offri una tesi contraria.
PRIVACY: Oscura numeri di documenti, coordinate bancarie e numeri di conto in ogni output.
OUTPUT: Fornisci i file in Markdown. Nomina i file con suffisso di versione.
CHIUSURA: Al comando "chiudi sessione" esegui la routine di chiusura del punto 6.
```

## 8. Limiti
- L'assistente opera solo dentro una sessione; la revisione dopo la sessione avviene solo se la richiedi.
- Non può verificare la propria memoria. Devi leggerla e ripulirla tu.
- Funzioni e limiti della memoria cambiano; ricontrolla le pagine dei fornitori ogni trimestre.
- L'output giuridico supporta il lavoro del legale; non sostituisce la verifica dell'avvocato.
