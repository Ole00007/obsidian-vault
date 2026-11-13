# Regole del progetto: Case Swarm (studio legale)
Lingua di lavoro: italiano. Atti e lettere per controparte/tribunale: italiano formale. Non sei un avvocato: ogni riferimento normativo e' "da verificare dall'avvocato".

## Divieti
- Non inviare email, PEC, messaggi. Solo bozze in 06_deliverables/.
- Non modificare ne' cancellare file in 00_originals. Non cancellare nulla senza la frase CONFIRM DELETE.
- Non caricare dati del fascicolo su GitHub, servizi esterni o repository. Non stampare chiavi o file .env.
- Non inventare fatti, date, importi, norme o giurisprudenza. Se manca un dato: scrivere [DA COMPLETARE] e chiedere.

## Metodo
1. Cartella fascicolo creata con `python case_tools.py init <nome>`.
2. `python case_tools.py hash <cartella>` prima di qualsiasi elaborazione.
3. Chat WhatsApp: `python case_tools.py parse-wa <cartella> --rename "You=<Nome cliente>"`; verificare con l'avvocato il nome dei mittenti e l'ordine giorno/mese su 3 messaggi.
4. Screenshot/scansioni: OCR con due motori diversi; differenze elencate, mai risolte in silenzio. Immagini al modello solo con consenso dell'avvocato.
5. Conteggi: solo `python case_tools.py count <cartella> lexicon.json`. Tipi: letterale, gruppo di sinonimi, ambiguo (non conteggiato, con domanda).
6. Ogni frase dei prodotti cita [S#:M#]. Verifica: `python case_tools.py citecheck <file.md>` deve dare PASS.
7. Fatti e inferenze separati; includere controaccuse e lacune. Materiale sensibile di terzi: segnalare e fermarsi.
8. Tutto il materiale e' considerato umano e reale salvo chiari segni contrari: in quel caso chiedere.

## Approvazioni (fermarsi e aspettare risposta esplicita)
APPROVAZIONE 0 via procedurale (R1-R4) / 1 sintesi / 2 acquisizione altri documenti / 3 rilascio finale.
Archivio solo dopo file ANALYSIS_COMPLETE: `python case_tools.py archive <cartella>`.

## Prodotti (in 06_deliverables/, partendo da ../modelli/)
strategia negoziale per rappresentante A-D (modello 07); struttura del caso; bozza degli atti (modello 06); lettere (01-05, 10); domande ostili e risposte (09); indice delle prove (CSV).
Nessun segnaposto [..] deve restare nei documenti finali.
