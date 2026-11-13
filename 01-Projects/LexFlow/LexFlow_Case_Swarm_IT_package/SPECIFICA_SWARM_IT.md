# Case Swarm - Specifica (IT, v0.3)
## 1. Principi
1. Gli originali non vengono mai modificati; si calcola prima l'hash SHA-256.
2. Tutto il materiale e' considerato prodotto da persone e reale, salvo chiari segni contrari nel documento: in tal caso l'agente chiede all'avvocato.
3. I conteggi (frasi ripetute, sinonimi) sono fatti da script, non dal modello.
4. Ogni affermazione cita la fonte nel formato [S1:M12] (fonte:messaggio). Lo script `citecheck` deve dare PASS.
5. Le esportazioni WhatsApp (.zip/.txt) si importano esattamente (`parse-wa`); l'OCR serve solo per screenshot e scansioni, con due motori diversi.
6. Fatti e inferenze sono sempre distinti; controaccuse e lacune (chiamate, vocali, messaggi cancellati) sono elencate.
7. Materiale sensibile di terzi (terapia, dati sanitari, registrazioni di dubbia liceita') viene segnalato dal Privacy Guard: si usa solo dopo decisione dell'avvocato.
8. Nessun invio automatico di lettere o email.

## 2. Cartelle (python case_tools.py init <nome>)
00_originali 01_fonti 02_trascrizioni_A 02_trascrizioni_B 03_unificato 04_analisi 05_sintesi 06_prodotti 07_verifica 08_archivio
(nei comandi restano i nomi inglesi: 00_originals ... 08_archive).

## 3. Flusso (le approvazioni sono in MAIUSCOLO)
P0 ACQUISIZIONE: copiare in 00_originals, `hash`.
P0b VIA PROCEDURALE: il Navigatore pone il questionario (modello 08) e propone le vie R1-R4 (sez. 6). APPROVAZIONE 0 (cliente + avvocato).
P1 IMPORT/TRASCRIZIONE: WhatsApp -> `parse-wa --rename "You=Nome Cliente"`; screenshot/scansioni -> OCR A (Tesseract ita) e B (secondo motore); audio -> trascrizione automatica etichettata come tale.
P2 STRUTTURA: messaggi, cronologia, partecipanti; differenze tra OCR A/B elencate.
P3 ANALISI: autenticita', Privacy Guard, `count` con lessico (sinonimi e voci ambigue approvati dall'avvocato).
P4 SINTESI E DOMANDE: bozza con citazioni, `citecheck`, domande all'avvocato/cliente. APPROVAZIONE 1.
P5 ALTRI DOCUMENTI: l'agente propone documenti utili gia' visti; si acquisiscono solo dopo APPROVAZIONE 2; poi tutto confluisce in UN unico fascicolo.
P6 PRODOTTI: strategia negoziale per ciascun rappresentante della controparte (A, B, C, D), struttura del caso, bozza degli atti, lettere (modelli 01-05, 10).
P7 DOMANDE OSTILI: simulazione dell'esame della controparte e risposte preparate (modello 09).
P8 VERIFICA: ricalcolo conteggi, citecheck, nessun segnaposto non compilato. APPROVAZIONE 3.
P9 ARCHIVIO: solo dopo il file ANALYSIS_COMPLETE (`python case_tools.py archive`).

## 4. Conteggio frasi ed emozioni
Per partecipante, per file e totale. Tipi: letterale (identica frase normalizzata di 1-5 parole, almeno 2 volte); gruppo di sinonimi (elenco dichiarato nel lessico, dettaglio per voce); ambiguo (non conteggiato, con domanda di chiarimento; emoji isolate incluse). Le emozioni sono riportate come parole espresse, non come diagnosi.

## 5. Test minimi prima dell'uso reale
T1 conteggi con risultati noti; T2 immagine sfocata segnalata; T3 segno di contenuto generato da IA -> domanda; T4 citecheck; T5 archivio rifiutato senza ANALYSIS_COMPLETE; T6 nessun documento aggiunto senza approvazione; T9 import WhatsApp Android+iOS con righe di sistema e messaggi multilinea; T10 Privacy Guard; T11 nessun segnaposto "[...]" nelle lettere finali.

## 6. Vie procedurali (da verificare dall'avvocato)
Dal 28 febbraio 2023 la separazione segue il rito unico (artt. 473-bis ss. c.p.c., D.Lgs. 149/2022).
R1 Ricorso congiunto in tribunale (art. 473-bis.51): condizioni concordate; allegati tipici: estratto atto di matrimonio, certificati di residenza e stato di famiglia, atti di nascita dei figli, dichiarazioni dei redditi degli ultimi tre anni, documentazione patrimoniale, piano genitoriale se vi sono figli.
R2 Negoziazione assistita (DL 132/2014): un avvocato per parte; con figli minori l'accordo e' trasmesso al Pubblico Ministero per il nulla osta/autorizzazione.
R3 Davanti all'ufficiale di stato civile: solo senza figli minori (o maggiorenni incapaci/non autosufficienti) e senza trasferimenti patrimoniali.
R4 Separazione giudiziale (art. 473-bis.12): ricorso con ufficio, dati di parti e figli, procura, oggetto, fatti ed elementi di diritto, conclusioni, indicazione specifica dei mezzi di prova e dei documenti, altri procedimenti pendenti, piano genitoriale, redditi e conti degli ultimi tre anni, documentazione immobiliare.
Possibile cumulo separazione-divorzio (art. 473-bis.49). Consiglio operativo: preparare fin dall'inizio gli allegati di R4, anche se si tenta R1/R2.
Solo l'avvocato: addebito, mantenimento, assegnazione della casa familiare, affidamento, giurisdizione (Reg. UE 2019/1111), valore probatorio dei messaggi.
