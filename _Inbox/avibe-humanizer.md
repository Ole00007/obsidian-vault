---
name: avibe-multilingual-humanizer
description: >-
  Load when a user asks to humanize, de-AI, rewrite, localize, polish, or adapt English, Italian, or Russian copy while preserving meaning and brand voice. Supports optional, explicitly requested jargon in legal, automotive, car repair, cosmetology, real estate, AI/SaaS, and content-creation contexts.
license: Proprietary - AVIbe internal use
compatibility: Perplexity Skills and Hermes Agent; no network access or executable scripts required.
metadata:
  version: "1.0.0"
  owner: "AVIbe Agency / Alessia_Code"
  languages: "en,it,ru"
---

# AVIbe Multilingual Humanizer

## Purpose

Rewrite English, Italian, and Russian text so it sounds natural, specific, culturally appropriate, and genuinely written by a person. Preserve the author’s meaning, facts, brand voice, risk disclosures, formatting, and intended action.

This skill improves language. It does not invent facts, perform legal or medical review, diagnose a vehicle, or guarantee that automated detection systems will classify text in any particular way.

## Activate when

Load this skill when the user asks to:

- humanize, de-AI, de-slop, naturalize, polish, or make text less robotic;
- rewrite English, Italian, or Russian copy in a more authentic voice;
- localize copy between these languages while preserving intent and cultural tone;
- adapt tone for a named audience, brand, platform, or professional field;
- selectively use domain terminology after the user explicitly requests jargon.

Do not load this skill merely because a text mentions law, cars, beauty, property, AI, SaaS, or content creation. Topic alone is not permission to add jargon.

## Required inputs

Infer what is safe to infer. Ask one concise question only when a missing choice would materially change the result.

- `TEXT`: source text or file.
- `OUTPUT_LANGUAGE`: English, Italian, or Russian. Default: source language.
- `AUDIENCE`: general public, client, peer professional, executive, social follower, or other.
- `PURPOSE`: inform, sell, explain, persuade, reassure, entertain, or convert.
- `TONE`: preserve source tone unless specified.
- `BRAND_PROFILE`: use the active Project/client profile if available.
- `JARGON`: `off`, `limited`, or `full`. Default: `off`.
- `DOMAIN`: legal, automotive, car repair, cosmetology, real estate, AI/SaaS, or content creation. Use only when jargon is enabled.

## Non-negotiable jargon rule

**Jargon is OFF by default.**

Use new domain jargon only when the user explicitly requests it, for example:

- “Use legal terminology.”
- “Write for mechanics; jargon: full.”
- “Keep this technical for SaaS founders.”
- `JARGON: limited | DOMAIN: real estate`

If the user names a domain but does not request jargon:

1. Keep the language accessible.
2. Preserve technical terms already present when removing them would alter meaning.
3. Do not add specialist vocabulary merely to sound authoritative.
4. Prefer a plain explanation over an acronym or insider expression.

Jargon levels:

- `off`: plain language; retain only essential source terms.
- `limited`: use a few precise, audience-appropriate terms and make meaning clear from context.
- `full`: use established professional terminology for an expert audience; do not become obscure or ornamental.

Never mix several domain vocabularies unless the user explicitly requests a cross-domain text.

## Workflow

1. **Lock meaning.** Identify factual claims, promises, names, dates, figures, quotations, links, CTAs, disclaimers, placeholders, and formatting that must not change.
2. **Identify voice.** Determine language, audience, relationship, emotional temperature, platform, formality, and brand profile.
3. **Check jargon permission.** Default to `off`. If enabled, use only the named domain and requested level.
4. **Detect artificial patterns.** Look for inflated claims, generic openings, repetitive conclusions, excessive headings, symmetrical lists, vague abstractions, unnecessary transitions, repeated sentence shapes, empty intensifiers, fake quotations, and formulaic “not only X but Y” structures.
5. **Rewrite for real speech and reading.** Make the text concrete, varied, direct, and rhythmically natural. Keep useful irregularity without adding mistakes.
6. **Localize, do not calque.** Rebuild idioms, syntax, politeness, humor, CTA, and register for the target language. Do not translate word for word.
7. **Run fidelity QA.** Confirm that no fact, promise, legal effect, safety warning, consent statement, price, specification, or disclosure changed.
8. **Deliver cleanly.** Return the rewritten text first. Add brief notes only when requested or when an ambiguity creates material risk.

## Universal style rules

- Prefer concrete nouns and active verbs.
- Vary sentence length naturally; do not force every sentence to be short.
- Replace vague praise with specific value already supported by the source.
- Remove throat-clearing and repeated summaries.
- Use transitions only when they clarify logic.
- Keep contractions and fragments only when natural for the language, channel, and brand.
- Keep a strong original phrase if it already sounds human.
- Preserve deliberate humor, edge, warmth, slang, and imperfections unless they harm clarity or safety.
- Never make all brands sound casual, witty, luxurious, or provocative by default.
- Do not add emojis, hashtags, exclamation marks, trendy slang, or rhetorical questions unless requested or established by the brand.
- Do not make text “more human” by inserting fake personal stories, opinions, emotions, quotations, results, or client experiences.
- Do not add claims such as “proven,” “guaranteed,” “best,” “safe,” “risk-free,” or “viral” without supplied evidence and permission.
- Preserve required sponsorship, AI-content, safety, medical, privacy, and legal disclosures.

## English rules

- Choose the requested regional variety; otherwise preserve the source variety.
- Use contractions when they fit the relationship and channel, not in formal clauses or warnings.
- Prefer direct verbs over noun-heavy constructions: “decide” rather than “make a decision” when meaning is unchanged.
- Avoid canned AI phrases such as “in today’s fast-paced world,” “delve into,” “unlock the power of,” “navigate the landscape,” “game-changer,” “it is important to note,” and automatic “in conclusion.”
- Avoid stacking adjectives, em dashes, three-part slogans, and polished-but-empty parallelism.
- Keep professional writing confident without making it sound like corporate legal copy unless requested.

## Italian rules

- Decide and preserve `tu`, `Lei`, or an impersonal/professional register. Never switch between them accidentally.
- Prefer natural Italian syntax over English-shaped sentence order.
- Avoid unnecessary subject pronouns, heavy nominalization, repeated gerunds, and bureaucratic fillers such as “andare a,” “al fine di,” or “procedere con” when a direct verb works.
- Use accepted English loanwords only when they are genuinely normal for the audience or when jargon is enabled.
- Avoid translating English marketing formulas literally. Rebuild the sentence as an Italian speaker would naturally say it.
- Keep punctuation, capitalization, articles, gender, number, prepositions, and apostrophes idiomatic.
- For Italian professional audiences, clarity and elegance take priority over imported buzzwords.

## Russian rules

- Use natural Russian information order rather than copying English syntax.
- Prefer verbs and concrete wording over chains of verbal nouns and bureaucratic канцелярит.
- Remove empty intensifiers, repeated participial constructions, excessive introductory phrases, and unnatural strings of genitives.
- Use established loanwords only when normal for the audience or when jargon is enabled; otherwise prefer a clear Russian equivalent.
- Preserve the chosen level of address and formality. Do not switch casually between `вы`, `Вы`, and impersonal constructions.
- Preserve the source convention for `е/ё` unless ambiguity requires `ё` or the user specifies a house style.
- Avoid literal translation of English hooks, idioms, and calls to action. Recreate the effect in Russian.
- Keep punctuation and dash use natural; do not imitate stereotypical AI rhythm with constant long dashes.

## Domain terminology bank

These are controlled examples, not mandatory words. Use them only when `JARGON` is explicitly enabled. Select the term that fits the jurisdiction, market, audience, and context. Do not dump terminology into the text.

### Legal

Legal concepts may not map one-to-one across jurisdictions. Never treat a multilingual label as proof of legal equivalence. When legal effect matters, preserve the source term, name the jurisdiction, or flag the need for a qualified lawyer/translator.

| English | Italian | Russian |
|---|---|---|
| agreement / contract | accordo / contratto | соглашение / договор |
| clause | clausola | условие / пункт договора |
| liability | responsabilità | ответственность |
| breach of contract | inadempimento contrattuale | нарушение договора |
| governing law | legge applicabile | применимое право |
| jurisdiction | giurisdizione / foro competente | юрисдикция / подсудность |
| power of attorney | procura | доверенность |
| due diligence | due diligence / verifica approfondita | комплексная проверка / due diligence |
| indemnity | indennizzo / manleva, depending on context | возмещение убытков / гарантия возмещения, по контексту |
| data controller | titolare del trattamento | оператор персональных данных, where legally appropriate |
| data processor | responsabile del trattamento | обработчик данных / лицо, обрабатывающее данные, by jurisdiction |
| cease-and-desist notice | diffida | требование о прекращении нарушения |

### Automotive industry

| English | Italian | Russian |
|---|---|---|
| powertrain | gruppo propulsore | силовая установка |
| drivetrain | catena cinematica / sistema di trasmissione | трансмиссия / привод, by context |
| torque | coppia motrice | крутящий момент |
| horsepower | cavalli / potenza in CV | лошадиные силы / мощность |
| chassis | telaio | шасси / рама, by construction |
| trim level | allestimento | комплектация |
| model year | anno modello | модельный год |
| internal-combustion engine | motore a combustione interna | двигатель внутреннего сгорания |
| battery-electric vehicle | veicolo elettrico a batteria | аккумуляторный электромобиль |
| plug-in hybrid | ibrido plug-in | подключаемый гибрид |
| range | autonomia | запас хода |
| homologation | omologazione | омологация / сертификация типа |

### Car repair and workshop

| English | Italian | Russian |
|---|---|---|
| OBD diagnostics | diagnosi OBD | OBD-диагностика |
| diagnostic trouble code | codice guasto / DTC | код неисправности / DTC |
| fault finding | ricerca guasto | поиск неисправности |
| brake pads | pastiglie dei freni | тормозные колодки |
| timing belt | cinghia di distribuzione | ремень ГРМ |
| control arm | braccio oscillante | рычаг подвески |
| wheel alignment | assetto ruote / convergenza, by task | сход-развал / регулировка углов установки колёс |
| misfire | mancata accensione | пропуски зажигания |
| coolant leak | perdita di liquido refrigerante | утечка охлаждающей жидкости |
| labour time | tempo di manodopera | трудоёмкость / нормо-часы |
| OEM part | ricambio originale / OEM | оригинальная запчасть / OEM |
| aftermarket part | ricambio aftermarket | неоригинальная запчасть / aftermarket |

Do not change torque values, part numbers, fault codes, service intervals, fluid specifications, safety warnings, or diagnostic certainty. Do not turn a suspected fault into a confirmed diagnosis.

### Cosmetology and aesthetic medicine

| English | Italian | Russian |
|---|---|---|
| consultation | consulto / visita | консультация |
| treatment plan | piano di trattamento | план лечения / план процедур |
| indication | indicazione | показание |
| contraindication | controindicazione | противопоказание |
| informed consent | consenso informato | информированное согласие |
| downtime | tempo di recupero | период восстановления |
| adverse event | evento avverso | нежелательное явление |
| skin barrier | barriera cutanea | кожный барьер |
| hyaluronic-acid filler | filler a base di acido ialuronico | филлер на основе гиалуроновой кислоты |
| botulinum toxin | tossina botulinica | ботулинический токсин |
| patch test | patch test / test epicutaneo | патч-тест / кожная проба |
| maintenance session | seduta di mantenimento | поддерживающая процедура |

Do not replace a clinician’s wording with trendier language if this changes indications, contraindications, consent, risk, expected outcome, or regulatory status. Never convert “may,” “can,” or “typically” into a guarantee.

### Real estate

| English | Italian | Russian |
|---|---|---|
| property listing | annuncio immobiliare | объявление о недвижимости |
| asking price | prezzo richiesto | цена предложения |
| floor plan | planimetria | планировка / поэтажный план |
| title document | titolo di proprietà | правоустанавливающий документ |
| cadastral data | dati catastali | кадастровые сведения |
| encumbrance | gravame / vincolo | обременение |
| preliminary contract | contratto preliminare | предварительный договор |
| deposit | deposito / caparra, depending on legal function | депозит / задаток / обеспечительный платёж, by function |
| closing / completion | rogito / perfezionamento, by market | закрытие сделки / завершение сделки |
| rental yield | rendimento locativo | доходность от аренды |
| capitalization rate | tasso di capitalizzazione | ставка капитализации |
| due diligence | due diligence immobiliare | проверка объекта / due diligence |

Property and transaction terms differ by legal system. Do not replace jurisdiction-specific terms with apparently similar foreign terms without verification.

### AI and SaaS

| English | Italian | Russian |
|---|---|---|
| onboarding | onboarding / attivazione iniziale | онбординг / первичная настройка |
| workspace | area di lavoro / workspace | рабочее пространство |
| seat | utenza / postazione / seat | пользовательское место / лицензия |
| usage-based pricing | prezzo basato sull’utilizzo | тарификация по использованию |
| API | API / interfaccia di programmazione | API / программный интерфейс |
| webhook | webhook | вебхук |
| retrieval-augmented generation | generazione aumentata dal recupero / RAG | генерация с дополнением поиском / RAG |
| agentic workflow | flusso di lavoro agentico | агентный рабочий процесс |
| model context window | finestra di contesto del modello | контекстное окно модели |
| tenant | tenant / istanza cliente | тенант / изолированная среда клиента |
| single sign-on | accesso unico / SSO | единый вход / SSO |
| churn | abbandono clienti / churn | отток клиентов |
| human in the loop | supervisione umana nel processo | человек в контуре принятия решений |
| hallucination | allucinazione del modello | галлюцинация модели |

Do not imply that an AI feature is autonomous, private, compliant, accurate, or secure unless the source supports that claim. Distinguish model, agent, workflow, tool, integration, API, automation, and SaaS product.

### Content creation and social media

| English | Italian | Russian |
|---|---|---|
| hook | gancio / hook | хук / зацепка |
| call to action / CTA | invito all’azione / CTA | призыв к действию / CTA |
| B-roll | B-roll / immagini di copertura | B-roll / перебивки |
| watch time | tempo di visualizzazione | время просмотра |
| audience retention | mantenimento del pubblico / retention | удержание аудитории |
| pattern interrupt | rottura dello schema | смена паттерна / сбивка внимания |
| content pillar | pilastro editoriale | контентная рубрика / контент-пиллар |
| storyboard | storyboard | раскадровка |
| caption | didascalia / caption | подпись к публикации |
| cover text | testo di copertina | текст на обложке |
| repurposing | riuso / adattamento dei contenuti | переупаковка контента |
| talking-head video | video parlato in camera | видео с говорящей головой |
| user-generated content / UGC | contenuto generato dagli utenti / UGC | пользовательский контент / UGC |
| content brief | brief editoriale | контент-бриф |

Do not use “viral” as a guaranteed outcome. Prefer “viral potential,” “testable hook,” or “distribution hypothesis” only when those meanings are accurate.

## Output modes

### Default

Return only the polished text, preserving the source structure where useful.

### With notes

When the user requests explanation, add no more than five bullets:

- Voice changes
- Clarity changes
- Localization choices
- Terminology choices
- Material ambiguity or risk

### Multiple versions

Only when requested, provide clearly differentiated versions such as:

- Natural and neutral
- Warm and conversational
- Expert with limited jargon
- Bold social version

Do not provide several nearly identical rewrites.

## Examples

### English — jargon off

**Input:**
“In today’s rapidly evolving digital landscape, our innovative solution empowers businesses to unlock their full potential.”

**Output:**
“Our software helps small teams automate repetitive work and see what needs attention next.”

Reason: removes generic claims and replaces them with a concrete benefit without adding technical vocabulary.

### English — AI/SaaS jargon explicitly enabled

**Request:** `JARGON: limited | DOMAIN: AI/SaaS | AUDIENCE: product leads`

**Output style:**
“Connect the API, map the webhook events, and test the human-in-the-loop approval step before moving the workflow into production.”

### Italian — jargon off

**Input:**
“La nostra missione è quella di andare a creare contenuti di valore che possano permettere al brand di distinguersi nel panorama digitale.”

**Output:**
“Creiamo contenuti utili e riconoscibili, pensati per far emergere il brand online.”

### Italian — car-repair jargon explicitly enabled

**Request:** `JARGON: limited | DOMAIN: car repair | AUDIENCE: workshop customers`

**Output style:**
“La diagnosi OBD indica un problema da verificare, ma il codice guasto da solo non basta per confermare quale componente sia da sostituire.”

### Russian — jargon off

**Input:**
“В условиях современного динамично развивающегося мира наша компания предоставляет комплексные решения, направленные на повышение эффективности вашего бизнеса.”

**Output:**
“Мы помогаем командам убрать лишнюю ручную работу и быстрее решать ежедневные задачи.”

### Russian — content jargon explicitly enabled

**Request:** `JARGON: limited | DOMAIN: content creation | AUDIENCE: creators`

**Output style:**
“Хук обещает быстрый ответ, поэтому первый смысловой payoff должен появиться до того, как начнёт падать удержание.”

## Gotchas

- “Human” does not always mean casual. A contract email, medical explanation, workshop estimate, luxury-property description, and Reel caption need different voices.
- Do not delete necessary repetition from safety, legal, consent, or instructional text merely to improve style.
- Do not convert uncertainty into certainty.
- Do not simplify a technical term when simplification changes the concept.
- Do not use false friends across languages. Legal and property concepts require jurisdiction awareness.
- Do not translate brand names, product names, model names, legal entity names, URLs, handles, fault codes, SKUs, or hashtags unless instructed.
- Do not “correct” intentional non-native voice if the author wants to retain it; polish without erasing identity.
- Do not introduce fashionable English terms into Italian or Russian merely because the source concerns technology or marketing.
- Do not use jargon as decoration or evidence of expertise.
- Do not remove AI, advertising, sponsorship, risk, or consent disclosures to make copy smoother.

## Safety and fidelity check

Before delivering, verify:

- Meaning preserved
- No new facts or promises
- Numbers, names, dates, URLs, codes, and specifications unchanged
- Brand and audience match
- Correct target language and register
- Jargon used only with explicit permission
- Jargon belongs only to the requested domain
- Terminology is context-appropriate
- Legal/medical/safety uncertainty preserved
- CTA and disclosure preserved
- Output sounds natural when read aloud

If a material term is uncertain, do not guess. Preserve the source term and add:

`TERMINOLOGY CHECK NEEDED: [term, language, jurisdiction/context]`

## Evaluation cases

### Should activate

1. “Humanize this English proposal but keep it professional.”
2. “Riscrivi questa caption in un italiano più naturale, senza gergo.”
3. “Сделай текст живее. Аудитория — владельцы автосервисов, jargon: limited.”
4. “Localize this SaaS onboarding email into Italian and Russian; use technical vocabulary for product managers.”

### Should activate cautiously

1. “Make this legal notice sound natural in Italian.” Preserve legal meaning and flag terminology requiring jurisdiction review.
2. “Humanize this clinic caption.” Preserve medical qualifications and claims; do not add promotional certainty.
3. “Rewrite the repair estimate for customers.” Keep codes, parts, quantities, and diagnostic uncertainty unchanged.

### Should not activate by itself

1. “Research Italian real-estate law.” Use a research/legal workflow.
2. “Diagnose fault code P0300.” Use an automotive diagnostic workflow with appropriate safety limits.
3. “Create a content calendar.” Use the content-strategy/calendar skill.
4. “Translate this word for word.” Use a translation workflow unless natural localization is also requested.
5. “Verify whether this cosmetic claim is legal.” Use compliance research and qualified human review.

## Maintenance references

Use these sources to maintain the skill structure and terminology policy; they are not permission to add jargon automatically.

- Agent Skills specification: https://agentskills.io/specification
- Agent Skills authoring guidance: https://agentskills.io/skill-creation/best-practices
- Perplexity skill-design guidance: https://www.perplexity.ai/hub/blog/designing-refining-and-maintaining-agent-skills-at-perplexity
- Hermes bundled humanizer: https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/creative/creative-humanizer
- EU multilingual terminology database (IATE): https://iate.europa.eu/home
- European e-Justice legal glossaries: https://e-justice.europa.eu/topics/legislation-and-case-law/glossaries-and-translations_en
- NIST trustworthy AI glossary: https://airc.nist.gov/glossary/
