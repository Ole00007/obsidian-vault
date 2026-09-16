# Hermes task — Final FAQ update for LexFlow

Target page:
- http://localhost:9097/lexflow-faq.html

Source page reviewed:
- FAQ — LexFlow currently contains short accordion Q&As about pricing, integrations, security, languages, AI add-on, migration, client access, accessibility, and team size fit.[page:1]

## Scope of this task
Update the FAQ content on the existing page while keeping the current visual style, structure, accordion behaviour, and concise tone.

Do **not** redesign the page.
Do **not** change the overall layout logic.
Do **not** remove existing useful QAs unless they are being replaced below.

Write for mixed audiences at once:
- lawyers,
- assistants and staff, even with low legal or technical background,
- general visitors with no legal or software knowledge.

Use plain language first. When a technical, legal, privacy, or product term appears, explain it simply where relevant.

## Persistent rule to save as default
Save this as a **default rule for future work**, not as a one-off instruction for this page only:

- explain technical, legal, privacy, compliance, and product terms in simple English where relevant,
- also prepare reusable glossary/help text in English, Russian, and Italian when the topic deserves it,
- keep explanations short, natural, and non-jargony,
- adapt wording so both professionals and non-experts can understand,
- when useful, integrate such explanations naturally into the site instead of keeping them only in internal notes.

Also save these as default build/content rules for future sites and apps:
- add relevant internal links by default,
- add relevant trusted external links when useful,
- write for SEO, GEO, and AEO from the start,
- prefer direct answers in the first sentence,
- keep content crawlable and semantically structured,
- avoid absolute product claims unless verified,
- check mobile reality before publishing cross-device claims,
- make copy easy for humans and AI answer engines to quote.

## Replace / revise these existing FAQs

### 1) Does LexFlow integrate with existing case management tools?
Replace current answer with:

**Yes. LexFlow supports 30+ integrations, and our team can guide data migration from your current tools.**

### 2) Is my client data secure with LexFlow?
Replace current answer with:

**Yes. LexFlow applies strong encryption and secure access controls designed to protect client information. In simple terms, encryption means data is scrambled so unauthorised people cannot read it, and secure access controls mean only the right people can open the right information.**

Important:
- avoid overclaiming unless verified,
- if “bank-grade encryption”, “zero-knowledge storage”, or “SOC2-aligned” are not fully verified for the current product/infrastructure wording, replace them with safer accurate phrasing.

### 3) Can I use LexFlow in Italian or Russian?
Replace current answer with:

**Yes. Use the globe icon in the navigation bar to switch languages at any time. Additional languages are planned in upcoming versions.**

### 4) What is the LexFlow AI Add-on and how is it priced?
Replace current answer with:

**The LexFlow AI Add-on adds legal research, case-context summaries, document-context summaries, and analysis workflows to any plan. Pricing is quoted individually based on scope of work, integration setup, infrastructure, and number of users.**

### 5) Which practice areas does LexFlow support?
Replace current answer with:

**LexFlow supports firms working across multiple practice areas, including Civil, Corporate, Family, Criminal, Real Estate, Intellectual Property, Immigration, Labour, Administrative, Constitutional, and Human Rights law. Intake forms can be configured by practice area so submissions are organised correctly from the start.**

### 6) How do I migrate my existing data to LexFlow?
Replace current answer with:

**Our onboarding team provides guided or white-glove migration. “Guided” means your team migrates data with our support, while “white-glove” means we handle most of the migration work for you.**

### 7) Does the client need to install anything?
Replace current answer with:

**No. LexFlow runs in the browser, so clients open it through a link without installing software.**

Add internal developer note/comment for review:
- double-check actual behaviour on iPhone/iPad Safari and Samsung/Android Chrome before claiming broader “any device” support,
- verify forms, uploads, status page, touch interactions, layout, and any CRM/frontend constraints,
- if stronger cross-device support needs upgrades, document that before publishing broader claims.

### 8) Does the client need to create an account or login?
Replace the question and answer with:

**Does the legal firm’s client need to create an account or log in?**

**No. Each legal firm’s client receives a unique token-secured URL that opens their personal matter page directly. In simple terms, a token-secured URL is a private access link generated for that specific matter, so the client can enter without registration or a password while access remains restricted and secure. This allows the client to track the progress of their case or matter without having to contact their lawyer or a legal assistant every time, giving the client more peace of mind while saving time for the firm. Lawyers stay focused on core legal work and keep communication organised around the milestones that truly matter, while more routine or technical updates are handled through automation.**

### 9) Is LexFlow suitable for a firm of 5–20 people?
Replace current answer with:

**Yes — LexFlow is built exactly for firms of this size. It is structured enough to handle real matter volume, simple enough to need no IT department, and any team member can usually get up and running in under ten minutes.**

## Add these new FAQs

### Do clients need to download an app?
**No. LexFlow runs entirely in the browser. Clients receive a link by email and open it on phone, tablet, or desktop — no download or installation required.**

### Do clients need to create an account or remember a password?
**No. Each client receives a unique token-secured URL. They simply click the link to access their personal matter page — no registration and no password to remember.**

### How is client data protected?
**Data is managed in line with EU GDPR requirements and supported by recognised security and privacy management practices. Internal firm notes are never visible to clients, and each status page is accessible only through the unique token assigned to that matter.**

### Does it work for firms with multiple practice areas?
**Yes. Intake forms can be pre-configured for each practice area, including Criminal, Civil, Labour, Family, Real Estate, Corporate, Intellectual Property, Immigration, Administrative, Constitutional, and Human Rights law. Each submission can then be categorised by area at the point of submission.**

### Can it integrate with email, cloud storage, or other tools?
**Yes — this is on the roadmap. Upcoming versions are planned to include automated email notifications, cloud storage, and connections to existing firm tools, while the current MVP focuses on the core flow: intake, dashboard, and client tracking.**

## Add one more FAQ for technical terms
Integrate the glossary/help content somewhere visible on the site. Best option: add one more FAQ item so the explanations are part of the site experience rather than hidden in notes.

Add this new FAQ:

### What do the technical and privacy terms on this page mean?
**Here is a plain-language explanation of the main technical, privacy, and product terms used on this page. These explanations are written for both legal professionals and non-technical clients.**

Under that FAQ, integrate the multilingual glossary/help content below in a clean, readable format that matches the site style. If a table looks visually off in the current design, use stacked cards or grouped lists instead, but keep all three languages available.

## Multilingual glossary/help text to integrate on the site

### English

- **Encryption** — Encryption means data is converted into a protected form so unauthorised people cannot read it.
- **Secure access controls** — Secure access controls mean only authorised users can open specific data or functions.
- **Data migration** — Data migration means moving existing data from one system into another system.
- **Guided migration** — Guided migration means your team moves the data with step-by-step support from LexFlow.
- **White-glove migration** — White-glove migration means LexFlow handles most of the migration work for you.
- **Token-secured URL** — A token-secured URL is a private access link generated for one specific matter or user, used to limit access without a password.
- **Matter page** — A matter page is the page where the client sees updates, documents, or information related to their legal case or file.
- **GDPR** — GDPR is the main European Union law on personal data protection and privacy.
- **ISO/IEC 27001** — ISO/IEC 27001 is an international standard for managing information security.
- **ISO/IEC 27701** — ISO/IEC 27701 is an international standard for privacy information management.
- **SOC 2** — SOC 2 is an auditing framework used to assess how organisations protect customer data.
- **Practice area** — A practice area is a category of legal work, such as family law, criminal law, or real estate law.

### Russian

- **Шифрование** — Шифрование — это способ преобразовать данные в защищённый вид, чтобы посторонние не могли их прочитать.
- **Безопасное управление доступом** — Это означает, что только авторизованные пользователи могут открывать определённые данные или функции.
- **Миграция данных** — Миграция данных — это перенос существующих данных из одной системы в другую.
- **Миграция с сопровождением** — Это означает, что ваша команда переносит данные с пошаговой поддержкой LexFlow.
- **Миграция white-glove** — Это означает, что LexFlow берёт на себя почти всю работу по переносу данных.
- **URL, защищённый токеном** — Это приватная ссылка доступа, созданная для конкретного пользователя или дела, чтобы ограничить доступ без пароля.
- **Страница дела** — Это страница, где клиент видит обновления, документы или информацию по своему юридическому делу.
- **GDPR** — GDPR — это основной закон Европейского союза о защите персональных данных и конфиденциальности.
- **ISO/IEC 27001** — Это международный стандарт по управлению информационной безопасностью.
- **ISO/IEC 27701** — Это международный стандарт по управлению информацией о конфиденциальности.
- **SOC 2** — Это аудиторская система оценки того, как организации защищают данные клиентов.
- **Направление практики** — Это категория юридической работы, например семейное, уголовное или недвижимое право.

### Italian

- **Crittografia** — La crittografia è un metodo per trasformare i dati in una forma protetta, così chi non è autorizzato non può leggerli.
- **Controlli di accesso sicuro** — Significa che solo gli utenti autorizzati possono aprire determinati dati o funzioni.
- **Migrazione dei dati** — La migrazione dei dati è il trasferimento dei dati esistenti da un sistema a un altro.
- **Migrazione guidata** — Significa che il vostro team trasferisce i dati con supporto passo dopo passo da parte di LexFlow.
- **Migrazione white-glove** — Significa che LexFlow gestisce per voi la maggior parte del lavoro di trasferimento dei dati.
- **URL protetto da token** — È un link privato generato per uno specifico utente o fascicolo, usato per limitare l’accesso senza password.
- **Pagina pratica** — È la pagina in cui il cliente vede aggiornamenti, documenti o informazioni relative al proprio caso o fascicolo.
- **GDPR** — Il GDPR è la principale normativa dell’Unione Europea sulla protezione dei dati personali e sulla privacy.
- **ISO/IEC 27001** — È uno standard internazionale per la gestione della sicurezza delle informazioni.
- **ISO/IEC 27701** — È uno standard internazionale per la gestione delle informazioni sulla privacy.
- **SOC 2** — È un framework di auditing usato per valutare come le organizzazioni proteggono i dati dei clienti.
- **Area di attività** — È una categoria di lavoro legale, come diritto di famiglia, penale o immobiliare.

## Internal linking rules for this task
From each relevant FAQ answer, add contextual internal links to the most relevant existing LexFlow pages or sections.

Use descriptive anchor text. Do not use “click here”.

Potential link targets to connect where available:
- pricing / plans,
- book demo / request demo,
- practice areas,
- security / compliance,
- languages,
- onboarding / migration,
- intake,
- dashboard,
- client tracking,
- homepage.

The current page already links to sign in, book a demo, request demo, WhatsApp, email, and other site pages, so expand internal linking consistently rather than leaving the FAQ isolated.[page:1]

## SEO + AEO rules for this page
Apply while editing this page:
- keep one clear H1 and logical H2/H3 structure,
- make each FAQ answer self-contained,
- place the direct answer in the first sentence,
- define product and compliance terms clearly,
- strengthen entity clarity around LexFlow, LexFlow AI Add-on, matter page, intake, dashboard, client tracking, and practice areas,
- keep wording concise enough for answer-engine snippets,
- avoid keyword stuffing,
- preserve accessible semantic HTML,
- make sure content remains in the DOM and readable to crawlers,
- where valid and appropriate later, prepare for FAQ structured data.

## Deliverable
Return all of the following:
1. updated FAQ HTML block ready to paste into the existing page,
2. the integrated multilingual glossary/help block in site-ready format,
3. a short list of all internal links added,
4. a short list of any claims that still need product verification before publication,
5. confirmation that the persistent rules above were saved as default rules for future site/app work.
