---
name: seo-cosmetologa-local
description: >
  Genera articoli di blog SEO/AEO/GEO + AI-first per cosmetologhe, centri estetici e
  operatori di skincare professionale in contesti locali italiani (Liguria, Genova,
  quartieri specifici). Ottimizzato per Google Search, AI Overviews, ChatGPT, Perplexity
  e lead generation via WhatsApp/prenotazione. Attivare quando l'utente chiede:
  "scrivi articolo blog cosmetologa", "contenuto SEO centro estetico Genova",
  "blog estetica AEO GEO", "FAQ schema beauty skincare locale".
license: MIT
metadata:
  version: "2.0"
  language: it
  domain: cosmetologia, skincare, estetica avanzata, beauty clinic
  geo_focus: Liguria, Genova, Italia
  compliance_note: >
    Non attribuire alla cosmetologa atti medici (filler, biorivitalizzazione,
    skin booster) salvo istruzioni documentate del cliente.
  ai_first: true
  lead_gen: true
allowed-tools:
  - search_web
  - create_text_file
  - create_research_report
---

# Skill: seo-cosmetologa-local

## Quando usare questa skill

Attivare per qualsiasi richiesta di:
- Articoli di blog per cosmetologhe / centri estetici locali (Genova, Liguria, Italia)
- Contenuti ottimizzati SEO + AEO + GEO + AI-first per beauty/skincare
- FAQ schema markup per siti di estetica
- CTA e lead generation via WhatsApp / prenotazione per centri estetici
- Costruzione di skill/template riutilizzabili per content creator nel settore beauty

---

## Istruzioni (step-by-step)

### FASE 0 — Raccolta INPUT (se mancanti, chiedi)

Raccogliere prima di scrivere:

| Campo | Esempio |
|---|---|
| `keyword_primaria` | "trattamento viso idratante Genova" |
| `keyword_secondarie` | 5–8 keyword (es. "skincare professionale", "pulizia viso profonda") |
| `localita` | Genova / Carignano / Sestri Ponente / Via XX Settembre / Liguria |
| `servizio_focus` | Pulizia viso profonda / Trattamento anti-age / Skincare personalizzata |
| `target_cliente` | donna 25–45 / donna 45+ / pelle sensibile / pelle secca / pelle spenta / antiage |
| `cta_finale` | prenota consulenza / richiedi analisi pelle / contattaci su WhatsApp |

Se uno o più campi mancano, usa placeholder `[INSERISCI]` visibili e segnalali all'utente.

---

### FASE 1 — Strategia SEO/AEO/GEO/AI-first

Prima di scrivere, pianifica mentalmente:

**SEO (Search Engine Optimization)**
- Keyword primaria nel: titolo SEO, H1, primo paragrafo, almeno un H2, CTA finale
- Keyword secondarie distribuite naturalmente nel testo
- Sinonimi semantici: trattamenti viso, skincare professionale, centro estetico, consulenza pelle, estetica avanzata, cura del viso, estetista qualificata
- Meta description ≤ 155 caratteri, con keyword primaria e CTA implicita
- URL slug suggerito: `/trattamento-[keyword]-[localita]`

**AEO (Answer Engine Optimization)**
- Almeno 3 H2 formulati come domande reali degli utenti
- Le prime 2–3 frasi sotto ogni domanda: risposta diretta e concisa (ottimale per featured snippet e AI Overview)
- FAQ finali: 5 domande con risposte ≤ 60 parole ciascuna — pronte per FAQPage schema JSON-LD
- Struttura scannable: H1 > H2 > risposta breve > approfondimento

**GEO (Generative Engine Optimization / Geographic)**
- ≥ 3 riferimenti locali naturali: città, quartiere o zona assegnata
- Collegare il servizio al contesto locale: accessibilità, quartiere, comodità, caratteristiche della clientela locale
- Entità locali citate: Genova, Liguria, quartiere specifico, eventuale riferimento a caratteristiche del territorio (clima marittimo, pelle sensibile al salmastro, ecc.)
- Pensare a come un LLM (ChatGPT, Perplexity, Gemini) citerebbe questo centro se interrogato su "cosmetologa a Genova"

**AI-first Content**
- Struttura ottimale per AI Overview: titolo → definizione breve → lista o paragrafo → FAQ
- Ogni sezione deve "funzionare" anche letta isolatamente (zero contesto esterno necessario)
- Usare tabelle comparative se il servizio si confronta con alternative (es. pulizia viso vs dermabrasione)
- Citazione-hook: includere almeno una frase-ancora autorevole che un LLM possa citare verbatim
- Evitare claim assoluti o promesse di risultati garantiti (compliance YMYL/E-E-A-T)

**Lead Generation & Conversione**
- CTA WhatsApp: link `https://wa.me/39NUMEROCELLULARE?text=Ciao%2C+vorrei+prenotare+una+consulenza`
- CTA prenotazione: link a calendario/booking oppure modulo contatti
- CTA analisi pelle: link a landing page o form dedicato
- Ogni CTA deve contenere la keyword primaria o il servizio focus
- Inserire micro-CTA testuali anche a metà articolo (non solo in fondo)
- Social proof: invitare a vedere recensioni Google o Instagram nella sezione "Perché scegliere"

**Internal Linking (topical cluster)**
- Suggerire 2–3 link interni a pagine servizio correlate (da personalizzare dal cliente)
- Suggerire 1 link esterno autorevole (es. FNOPI, AIDECO, o fonte scientifica skincare)
- Struttura pillar-cluster: questo articolo si collega a una pagina servizio principale

---

### FASE 2 — Struttura obbligatoria dell'articolo

Produrre nell'ordine:

```
1. TITOLO SEO (tag <title>, max 60 caratteri)
2. META DESCRIPTION (max 155 caratteri)
3. H1 (titolo principale pagina, può differire dal titolo SEO)
4. ARTICOLO COMPLETO (900–1300 parole):
   - Intro breve (keyword + località + hook empatico)
   - 4–6 sezioni H2 (almeno 3 come domande reali)
   - H3 solo dove utili
   - Sezione "Per chi è indicato"
   - Sezione "Come funziona la consulenza / il trattamento"
   - Sezione "Perché scegliere [LOCALITÀ / CENTRO]"
   - Micro-CTA a metà articolo
5. 5 FAQ FINALI (formato Q&A, pronte per schema)
6. CTA FINALE (con keyword primaria e link)
7. 3 VARIANTI CTA (testo alternativo per test A/B)
8. SUGGERIMENTI TECNICI (schema JSON-LD FAQ, slug URL, internal linking)
```

---

### FASE 3 — Regole editoriali e compliance

1. **Tono**: professionale, rassicurante, locale — né troppo clinico né troppo commerciale
2. **Italiano naturale**: evitare anglicismi non necessari, gergo medico eccessivo, frasi passive ridondanti
3. **Focus commerciale**: ogni paragrafo deve avere una direzione verso la prenotazione o la fiducia
4. **No promesse mediche**: non garantire risultati, non usare "elimina", "guarisce", "risolve definitivamente"
5. **Atti medici**: filler, biorivitalizzazione, PRP, skin booster → trattare solo in chiave informativa/comparativa o rimandare a medico abilitato
6. **Keyword stuffing**: vietato — massimo 2 occorrenze della keyword primaria ogni 300 parole
7. **E-E-A-T signals**: citare la professionalità della cosmetologa, eventuali certificazioni, anni di esperienza — senza inventare dati specifici
8. **Lunghezza**: 900–1300 parole corpo articolo (esclusi FAQ e CTA)

---

### FASE 4 — Output tecnico aggiuntivo (AI-first)

Dopo l'articolo, fornire sempre:

#### A. Schema JSON-LD FAQPage (pronto da incollare)
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[DOMANDA 1]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[RISPOSTA 1]"
      }
    }
    // ... ripetere per tutte le FAQ
  ]
}
```

#### B. Slug URL suggerito
`/[servizio-focus-slug]-[localita-slug]`
Esempio: `/pulizia-viso-profonda-genova-carignano`

#### C. Topical cluster — Internal linking suggerito
- Link 1 → [Pagina servizio principale]
- Link 2 → [Articolo correlato: tipo di pelle]
- Link 3 → [Pagina contatti / prenotazione]

#### D. Distribuzione contenuto (repurposing)
- **Instagram Reel**: estratto hook intro + CTA WhatsApp
- **Stories**: le 5 FAQ come slides Q&A
- **Email**: intro + sezione "Per chi è indicato" + CTA prenotazione
- **Google Business Post**: risposta alla FAQ più cercata + link articolo

---

## Esempi

### Input esempio
```yaml
keyword_primaria: "pulizia viso profonda Genova"
keyword_secondarie: ["trattamento viso", "skincare professionale", "pelle mista Genova",
  "centro estetico Carignano", "estetista qualificata", "cura del viso professionale"]
localita: "Genova Carignano"
servizio_focus: "Pulizia viso profonda"
target_cliente: "donna 25–45 / pelle mista"
cta_finale: "prenota consulenza"
```

### Output atteso (struttura)
- Titolo SEO: `Pulizia Viso Profonda a Genova | Centro Estetico Carignano`
- Meta: `Scopri la pulizia viso profonda a Genova Carignano: skincare professionale su misura per pelle mista. Prenota la tua consulenza oggi.`
- H1: `Pulizia viso profonda a Genova: la skincare professionale che la tua pelle mista merita`
- Articolo completo con struttura obbligatoria
- FAQ schema-ready
- 3 varianti CTA
- JSON-LD + slug + cluster

---

## Note per estensioni future

- Aggiungere variante per **lingua inglese** (turismo medicale / expat Genova)
- Aggiungere variante per **campagne stagionali** (trattamenti estivi sole/mare, autunnali rigenerazione)
- Aggiungere modulo **analisi competitor locale** (Genova: top 5 centri estetici per keyword)
- Integrare con skill `marketing-performance-analytics` per tracking conversioni CTA


## Links
- Parent: [[_Inbox-INDEX]]
- Related: [[industry-competitive-analyst-skill (2)]]
