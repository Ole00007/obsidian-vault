# 2DI Carrozzeria – Piano di visibilità e lancio sito (Genova)

> Stato: bozza operativa. Dati aziendali (indirizzo, telefono, orari, servizi, garanzie) da confermare con il titolare prima della pubblicazione.

## 1. Piattaforme da coprire

| Gruppo | Piattaforme |
|---|---|
| Ricerca locale primaria | Google Search, Google Maps |
| Copertura aggiuntiva | Bing, Bing Maps, Apple Maps, DuckDuckGo, Yahoo Search |
| Discovery AI di Google | AI Overviews, AI Mode, Gemini |
| Altre ricerche assistite da AI | ChatGPT Search, Microsoft Copilot, Perplexity, Claude con ricerca web |

Sono superfici diverse, non un unico sistema di ranking.

### Ordine di priorità
1. Google Search e Google Business Profile / Maps.
2. Indicizzazione Bing e schede locali accurate.
3. Accessibilità del sito ai crawler di ricerca AI.
4. Misurazione di richieste e referral reali, non solo menzioni occasionali nelle AI.

Google raccomanda di tenere aggiornate le informazioni del Business Profile. OpenAI raccomanda di consentire `OAI-SearchBot` per comparire in sintesi e snippet di ChatGPT Search.

## 2. Architettura iniziale del sito

```text
/
 /servizi/
 /servizi/riparazione-carrozzeria-genova/
 /chi-siamo/
 /contatti/
 /blog/
 /blog/preventivo-carrozzeria-genova/
 /blog/graffi-auto-genova-lucidatura-verniciatura/
```

Aggiungi pagine dedicate (verniciatura, lucidatura, paraurti, sinistri) solo dopo aver confermato i servizi. Ogni pagina deve rispondere a un bisogno distinto, senza duplicare lo stesso testo con keyword diversa.

## 3. Checklist di lancio

| Area | Implementazione |
|---|---|
| Identità aziendale | Conferma ragione sociale, dati legali, indirizzo esatto, telefono, orari e URL Instagram ufficiale. Usa gli stessi dati ovunque. |
| Informazioni locali | Indirizzo, indicazioni, contatti e orari in una pagina Contatti utile. Mantieni aggiornato il Google Business Profile. |
| Scansionabilità | Pagine pubbliche, indicizzabili, non bloccate da `robots.txt`, login, tag `noindex` accidentali o regole di hosting. |
| Scoperta | Invia la sitemap in Google Search Console e configura Bing Webmaster Tools. IndexNow può avvisare i motori partecipanti dei cambiamenti; non garantisce l'indicizzazione. |
| Dati strutturati | Markup LocalBusiness con il sottotipo più specifico, indirizzo, telefono, URL e orari verificati; valida prima del lancio. |
| Accesso AI-search | Verifica l'accesso di `OAI-SearchBot` (ChatGPT). Controlla separatamente i crawler di ricerca di Perplexity e Claude rispetto alle policy di addestramento. |
| Prove | Foto reali approvate dal titolare ed esempi autentici di riparazioni. Descrivi solo lavori davvero eseguiti. |
| Conversione | Pulsanti chiama/contatta funzionanti, testati da mobile. WhatsApp solo se è un canale aziendale approvato. |
