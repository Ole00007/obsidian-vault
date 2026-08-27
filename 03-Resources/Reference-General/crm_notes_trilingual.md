# CRM / Sistema Gestionale / CRM-система

## Italiano

### Azioni da intraprendere

- [ ] Mettere per iscritto e condividere tutti i punti chiave discussi durante la riunione.
- [ ] Allineare Ivan, la direzione e il personale delle filiali sui requisiti e sulle procedure obbligatorie per la documentazione fotografica.
- [ ] Decidere se continuare a utilizzare il secondo programma di preventivazione (Infocar/Wincar) prima dell’avvio dell’integrazione con il CRM.
- [ ] Caricare manualmente i fogli dati esistenti nel nuovo sistema come primo passo di integrazione, prima di qualsiasi collegamento via API.
- [ ] Inviare esempi del formato di sistema preferito per la revisione e l’analisi dei gap.

### Panoramica CRM / Sistema Gestionale

- Il sistema deve compilare automaticamente i dati nei moduli, riducendo in modo significativo il lavoro manuale; attualmente si perde circa mezza giornata in attività manuali.
- La soluzione viene indicata come “Sistema Gestionale” (gestionale / CRM).
- L’azienda opera su più filiali, mentre gli ordini sono attualmente gestiti in modo centralizzato.
- È stato proposto un sistema cloud con accessi limitati e specifici per ruolo per ciascun membro del personale di filiale.
- Tutta la documentazione e tutti i processi esistenti devono essere consolidati digitalmente all’interno del nuovo sistema.

### Requisiti per le checklist

- Sono state individuate tre checklist distinte come necessarie:
  - Accettazione ordine: documenti richiesti e procedura di accettazione.
  - Lavorazione in officina: lavorazioni effettuate e foto in ogni fase.
  - Chiusura: foto finale, foto di lavorazione, posizione contabile del cliente e firma del cliente.
- Una checklist è necessaria anche per il personale esperto, poiché si verificano comunque lacune.
- La checklist deve fungere anche da guida procedurale, coprendo tutti i passaggi per tutte le filiali.
- Le checklist e le schede di lavoro già presenti in Infocar possono essere riutilizzate come base di partenza.
- Sono richiesti alert dei lavori e checklist operative collegate agli stati della pratica.

### Documentazione fotografica

- Le foto devono essere scattate in tre momenti chiave: all’arrivo del veicolo, durante la lavorazione e al completamento.
- Questo requisito è stato definito fondamentale, ma al momento non viene rispettato in modo coerente.
- È stata rilevata una certa resistenza da parte del personale; è stata proposta l’adozione di un dispositivo condiviso da utilizzare in officina.
- Le foto devono poter essere caricate direttamente nella pratica/ordine all’interno del CRM.
- La filiale di Sturla è stata indicata come conforme alle procedure fotografiche; le altre filiali devono ancora allinearsi.

### Gestione calendario e scadenze

- Un calendario integrato nel CRM deve tracciare le scadenze per revisioni/esami, invio della documentazione e stati delle pratiche.
- Il sistema deve mostrare automaticamente l’esame o la pratica rilevante all’apertura della relativa scheda.
- Devono essere generati avvisi o pop-up quando un veicolo è pronto o quando un’auto di cortesia non è più disponibile.
- È desiderabile la possibilità di inviare messaggi o notifiche direttamente dal gestionale.

### Gestione auto di cortesia

- Le auto di cortesia vengono fornite ai clienti quando il loro veicolo è in riparazione, in particolare per interventi legati a pratiche assicurative.
- Il sistema deve tracciare la disponibilità delle auto di cortesia, collegarla alla data di riparazione e visualizzare un pop-up quando l’auto viene restituita o non è disponibile.
- Parco attuale: due auto presso la sede principale e un’ulteriore unità.
- Riferimenti per il costo di noleggio: 25 € al giorno come tariffa standard; 50 € al giorno per periodi inferiori a 5 giorni; tetto massimo di 500 € al mese a partire dal 15° giorno.
- Il checklist dei danni del veicolo (schema fronte/retro, livello carburante, danni preesistenti) deve far parte del processo di consegna dell’auto di cortesia.
- È stato proposto un oggetto di database per ciascuna auto di cortesia, con una lista dei danni persistente, aggiornata a ogni utilizzo.

### Sistemi esistenti: Infocar & Wincar

- L’azienda utilizza attualmente due sistemi: Infocar (per preventivazione ricambi e gestione ordini) e Wincar.
- Il secondo sistema al momento non può essere aggiornato a causa di un problema hardware del PC ed è di fatto inattivo.
- Il secondo sistema talvolta offre prezzi migliori, ma si aggiorna lentamente, con il rischio che i prezzi cambino prima dell’effettivo inserimento dell’ordine.
- È necessaria una decisione se mantenere, dismettere o integrare il secondo sistema nel CRM prima di procedere con lo sviluppo.
- L’integrazione iniziale sarà manuale prima di qualsiasi collegamento via API.

### Tipologie di veicolo e variazioni dei moduli

- L’officina gestisce sia auto sia motocicli; i campi dati sono simili, ma i moduli differiscono leggermente in base al tipo di veicolo.
- È importante standardizzare la struttura dei moduli tra le varie tipologie di veicolo per garantire la coerenza del sistema.

### Controllo costi, redditività e personale

- Il preventivo risulta spesso più alto del costo effettivo della riparazione.
- Il sistema deve aiutare a tenere sotto controllo il guadagno e il margine reale per pratica.
- Va valutato se monitorare il personale in base a ore lavorate, disponibilità ed efficienza.
- È richiesto un controllo degli operai, in particolare preparatore e verniciatore.
- Battilama e lamierista sono spesso specialisti a partita IVA; va confermato con Ivan se imputare o meno su di loro il costo della fattura.
- Occorre monitorare costi ed efficienza del personale e delle singole sedi.
- Nella pratica dovrebbe essere possibile inserire ulteriori elementi amministrativi e allegati rilevanti.
- La fattura emessa in chiusura deve essere collegata alla pratica.

### Note aggiuntive

- per controllare i costi dei lavori
- costi dei ricambi in casi particolari (in caso di “nero”)

---

## English

### Action Items

- [ ] Write down and share all key points discussed during the meeting.
- [ ] Align Ivan, management, and branch staff on mandatory photo documentation requirements and procedures.
- [ ] Decide whether to continue using the secondary pricing program (Infocar/Wincar) before CRM integration begins.
- [ ] Manually upload existing data sheets into the new system as a first integration step, before any API connection.
- [ ] Send examples of the preferred system format for review and gap analysis.

### CRM / Management System Overview

- The system should automatically populate data into forms, significantly reducing manual work; currently approximately half a day is lost to manual processes.
- The solution is referred to as the “Sistema Gestionale” (management system / CRM).
- The business operates across multiple branches, while orders are currently centralized.
- A cloud-based system with limited, role-specific access for each branch staff member was proposed.
- All existing documentation and processes should be digitally consolidated into the new system.

### Checklist Requirements

- Three distinct checklists were identified as necessary:
  - Order intake: required documents and intake procedure.
  - Workshop processing: work being performed and photos at each stage.
  - Closing: final photo, processing photo, customer account position, and customer signature.
- A checklist is needed even for experienced staff, as operational gaps still occur.
- The checklist should also serve as a procedural guideline, covering all steps across all branches.
- Existing checklists and work cards from Infocar can be reused as a starting point.
- Work alerts and checklist flows linked to case status are also required.

### Photo Documentation

- Photos must be taken at three key moments: when the vehicle arrives, during processing, and upon completion.
- This is considered a fundamental requirement, but it is not currently followed consistently.
- Staff resistance was acknowledged; the use of a shared device in the workshop was suggested.
- Photos should be uploaded directly into the case/order record in the CRM.
- The Sturla branch was noted as compliant with photo procedures; other branches still need alignment.

### Calendar and Deadline Management

- A calendar integrated into the CRM should track deadlines for inspections/exams, document submissions, and case statuses.
- The system should automatically surface the relevant exam or case when a record is opened.
- Notifications or pop-ups should be generated when a vehicle is ready or when a courtesy car is no longer available.
- The ability to send messages or notifications directly from the system is considered desirable.

### Courtesy Car Management

- Courtesy cars are provided to clients when their vehicle is being repaired, especially for insurance-related work.
- The system should track courtesy car availability, link it to the repair date, and display a pop-up when the car is returned or unavailable.
- Current fleet: two cars at the main location and one additional unit.
- Rental cost references: €25/day standard rate; €50/day for periods under 5 days; capped at €500/month starting from day 15.
- The vehicle damage checklist (front/back diagram, fuel level, pre-existing damage) should be part of the courtesy car handover process.
- A database object for each courtesy car with a persistent damage list was proposed, updated at each handover.

### Existing Systems: Infocar & Wincar

- The business currently uses two systems: Infocar (for spare parts pricing and order management) and Wincar.
- The second system cannot currently be updated due to a PC hardware issue and is effectively inactive.
- The second system sometimes offers better pricing, but it updates slowly, so prices may change before an order is placed.
- A decision is required on whether to keep, discontinue, or integrate the secondary system into the CRM before development proceeds.
- Initial integration will be manual before any API connection is established.

### Vehicle Types and Form Variations

- The workshop handles both cars and motorbikes; data fields are similar, but forms differ slightly depending on vehicle type.
- Standardizing form structure across vehicle types is important for system consistency.

### Cost Control, Profitability, and Staff Tracking

- The estimate is often higher than the actual repair cost.
- The system should help keep profit and real margin per case under control.
- It should be evaluated whether staff should be monitored based on worked hours, availability, and efficiency.
- Worker control is needed, especially for the prep technician and the painter.
- Panel beater and body specialist roles are often external VAT-registered specialists; it must be confirmed with Ivan whether their invoice cost should be assigned directly to them or handled differently.
- The system should monitor staff costs and efficiency, as well as branch-level efficiency.
- The case record should allow insertion of additional relevant administrative items and attachments.
- The closing invoice must be linked to the case.

### Additional Notes

- to control the costs of works
- spare parts costs in special cases (in case of “off-the-books” work)

---

## Русский

### Дальнейшие действия

- [ ] Зафиксировать письменно и распространить все ключевые пункты, обсуждавшиеся на встрече.
- [ ] Согласовать с Иваном, руководством и сотрудниками филиалов обязательные требования и процедуры по фотофиксации.
- [ ] Принять решение, продолжать ли использовать вторую программу расчета стоимости (Infocar/Wincar) до начала интеграции с CRM.
- [ ] Вручную загрузить существующие таблицы и листы данных в новую систему как первый этап интеграции, до любого API-подключения.
- [ ] Отправить примеры предпочтительного формата системы для анализа и выявления расхождений.

### Обзор CRM / Управленческой системы

- Система должна автоматически подставлять данные в формы, существенно сокращая ручную работу; в настоящее время на ручные процессы уходит примерно полдня.
- Решение обозначается как “Sistema Gestionale” (управленческая система / CRM).
- Компания работает через несколько филиалов, при этом заказы сейчас централизованы.
- Была предложена облачная система с ограниченным ролевым доступом для каждого сотрудника филиала.
- Вся существующая документация и процессы должны быть в цифровом виде объединены в новой системе.

### Требования к чек-листам

- Были определены три обязательных чек-листа:
  - Прием заказа: необходимые документы и процедура приема.
  - Работа в мастерской: выполняемые работы и фотографии на каждом этапе.
  - Закрытие: финальное фото, фото процесса, данные клиента и подпись клиента.
- Чек-лист нужен даже для опытного персонала, поскольку рабочие пробелы все равно возникают.
- Чек-лист должен также выполнять функцию процедурной инструкции для всех филиалов.
- Существующие чек-листы и рабочие карточки из Infocar можно использовать как отправную точку.
- Также требуются alerts по работам и логика чек-листов, привязанная к статусам дела.

### Фотофиксация

- Фотографии должны делаться в три ключевых момента: при поступлении автомобиля, в процессе работ и после завершения.
- Это считается базовым требованием, но сейчас соблюдается непоследовательно.
- Была отмечена сопротивляемость со стороны персонала; предложено использовать общее устройство в мастерской.
- Фотографии должны загружаться напрямую в карточку дела/заказа в CRM.
- Филиал Sturla был отмечен как соблюдающий процедуры фотофиксации; остальные филиалы еще нужно выровнять.

### Календарь и сроки

- Календарь, встроенный в CRM, должен отслеживать сроки по проверкам/экзаменам, отправке документов и статусам дел.
- Система должна автоматически показывать соответствующий экзамен или дело при открытии записи.
- Должны формироваться уведомления или pop-up, когда автомобиль готов или когда подменный автомобиль больше недоступен.
- Желательной функцией также является возможность отправлять сообщения или уведомления прямо из системы.

### Управление подменными автомобилями

- Подменные автомобили предоставляются клиентам, когда их автомобиль находится в ремонте, особенно по страховым случаям.
- Система должна отслеживать доступность подменных автомобилей, связывать ее с датой ремонта и показывать pop-up, когда автомобиль возвращен или недоступен.
- Текущий парк: две машины на основной площадке и еще одна дополнительная единица.
- Ориентиры по стоимости аренды: 25 € в день как стандартная ставка; 50 € в день для периодов менее 5 дней; максимум 500 € в месяц начиная с 15-го дня.
- Чек-лист повреждений автомобиля (схема спереди/сзади, уровень топлива, уже имеющиеся повреждения) должен входить в процесс передачи подменного автомобиля.
- Для каждого подменного автомобиля предложено создать отдельный объект в базе данных с постоянным списком повреждений, который обновляется при каждой выдаче.

### Существующие системы: Infocar и Wincar

- Компания в настоящее время использует две системы: Infocar (для расчета стоимости запчастей и управления заказами) и Wincar.
- Вторая система сейчас не может быть обновлена из-за аппаратной проблемы на ПК и фактически не используется.
- Вторая система иногда дает более выгодные цены, но обновляется медленно, поэтому цены могут измениться до момента размещения заказа.
- До продолжения разработки необходимо принять решение: сохранить, отказаться или интегрировать вторую систему в CRM.
- Начальная интеграция будет выполняться вручную до любого API-подключения.

### Типы транспортных средств и различия форм

- Мастерская работает как с автомобилями, так и с мотороллерами/мотоциклами; поля данных похожи, но формы немного отличаются в зависимости от типа транспортного средства.
- Для согласованности системы важно стандартизировать структуру форм для разных типов транспортных средств.

### Контроль затрат, прибыльности и персонала

- Смета часто оказывается выше фактической стоимости ремонта.
- Система должна помогать контролировать прибыль и реальную маржу по каждому делу.
- Нужно определить, следует ли учитывать персонал по отработанным часам, доступности и эффективности.
- Требуется контроль по рабочим, особенно по подготовщику и маляру.
- Жестянщик и кузовной специалист часто являются внешними специалистами с ИП/самозанятостью; необходимо подтвердить с Иваном, относить ли стоимость их счета непосредственно на них или учитывать иначе.
- Необходимо отслеживать затраты и эффективность персонала, а также эффективность отдельных филиалов.
- В карточку дела должна быть возможность добавлять дополнительные административные элементы и важные вложения.
- Финальный счет, выставляемый при закрытии, должен быть связан с делом.

### Дополнительные заметки

- для контроля стоимости работ
- стоимость запчастей в особых случаях (в случае «черного» учета)

## Links
- Parent: [[Reference-General-INDEX]]
- Related: [[Point4_Excel_Legal_Financial_Iteration]]
