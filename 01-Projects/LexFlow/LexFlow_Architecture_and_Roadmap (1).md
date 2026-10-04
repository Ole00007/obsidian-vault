# LexFlow — Architecture (Current) & Automation Roadmap

> Открывай в VS Code / Obsidian / GitHub — диаграммы Mermaid рендерятся автоматически как визуальные схемы.

## 1. Текущая архитектура (as of Sept 3, 2026)

```mermaid
flowchart TB
    subgraph LP["Landing Pages (static, per tenant)"]
        LP1["LexFlow LP<br/>poetic-kleicha (Netlify)"]
        LP2["Romanelli LP<br/>...workers.dev"]
        LP3["Pagliano LP<br/>verdant-crumble"]
    end

    LP1 -->|"/login?ws=lexflow"| APP
    LP2 -->|"/login?ws=romanelli"| APP
    LP3 -->|"/login?ws=pagliano"| APP

    subgraph APP["ONE Flask App (Railway: web-production-031a6)"]
        direction TB
        JINJA["Jinja2 templates + vanilla JS<br/>(NOT React, one shared codebase)"]
        JWT["JWT session (localStorage, per browser)"]
        WSFILTER["workspace_filter() — app-level row isolation"]
    end

    APP --> DB

    subgraph DB["ONE PostgreSQL (perceptive-achievement)"]
        T1["workspaces"]
        T2["users"]
        T3["cases"]
        T4["contacts"]
        T5["tasks"]
        T6["notifications"]
        RLS["Row-Level Security (feat/rls branch)<br/>⚠️ NOT MERGED — pending 18-test Postgres run + NOBYPASSRLS"]
    end

    subgraph TENANTS["Active Tenants"]
        WS7["ws7 — LexFlow"]
        WS9["ws9 — Pagliano"]
        WS10["ws10 — Romanelli Studio"]
        CL1["cl1 — Romanelli client-of-client #1"]
        CL2["cl2 — Romanelli client-of-client #2"]
    end

    WS10 --> CL1
    WS10 --> CL2

    APP -.->|"Resend (status unclear — needs fact-check)"| EMAIL["Email notifications"]
    APP -.->|"Google Calendar OAuth (connected)"| GCAL["Google Calendar sync"]

    UPLOADS["/app/uploads<br/>Railway Volume (web-uploads)<br/>persists across redeploys"]
    APP --> UPLOADS
```

### Известные разрывы / открытые вопросы
- RLS построен на `feat/rls`, но не влит — защита изоляции только на уровне приложения (`workspace_filter()`), без резервного слоя в БД.
- Webhook-дыра закрыта (commit a2781f5) — подпись теперь обязательна, workspace_id больше не NULL.
- Resend/email интеграция: точный статус (Railway vs отдельный проект) — ожидает подтверждения от Operator-Installer.
- Uploads volume: `web-uploads`, mount `/app/uploads`, план подтверждён, ожидает финального go на редеплой.

---

## 2. Roadmap автоматизации (инкрементально, без "скачков")

```mermaid
flowchart LR
    P1["Phase 1 (Now)<br/>Базовый reflection:<br/>intake → Contacts/Kanban/Calendar<br/>+ ручной ввод имени (done)"]
    P2["Phase 2 (Next sprint)<br/>Conflict-check gate +<br/>первый follow-up email (24h) +<br/>WhatsApp integration scoped"]
    P3["Phase 3<br/>Полный drip (24h/72h/7d) +<br/>suppression rules +<br/>scheduled_actions table"]
    P4["Phase 4<br/>Client portal notifications +<br/>WhatsApp status updates"]
    P5["Phase 5<br/>Contacts redesign<br/>(HubSpot/Salesforce style) +<br/>сегментация для рассылок"]
    P6["Phase 6 (End of September target)<br/>AI adaptive/reflective email agent<br/>поверх scheduled_actions"]

    P1 --> P2 --> P3 --> P4 --> P5 --> P6

    style P1 fill:#10B981,color:#fff
    style P2 fill:#3B7DD8,color:#fff
    style P3 fill:#3B7DD8,color:#fff
    style P4 fill:#8B5CF6,color:#fff
    style P5 fill:#8B5CF6,color:#fff
    style P6 fill:#F59E0B,color:#fff
```

### Технический выбор по типу задачи

| Тип задачи | Модель триггера | Технология | Когда апгрейдить |
|---|---|---|---|
| Мгновенное письмо-подтверждение | Event-driven (instant) | Прямой вызов Resend API в handler'е | Не требуется |
| Отложенный follow-up (24ч/72ч/7д) | Event-driven + delay | Postgres `scheduled_actions` + Railway worker (MVP) → Celery+Redis (масштаб) | При >500 задач/день или нужны retries |
| Напоминания о слушаниях | Time-based (cron) | Railway worker, ежедневный скан дат | Не требуется — cron корректен здесь |
| WhatsApp-уведомления | Event-driven | WhatsApp Business API (Twilio/Meta Cloud API) | Новая интеграция |
| AI adaptive follow-up | Event-driven + AI decision layer | AI-агент читает activity_log + notifications | Строить после Phase 3 |

---

## 3. Параллельные треки (текущий спринт)

```mermaid
flowchart TB
    OI["Operator-Installer<br/>P1/P2 + inventory + cl1-cl10 local test"]
    BD["backend-dev<br/>Full app audit (read-only) +<br/>proactive suggestions +<br/>Contacts redesign (→ frontend-dev)"]
    HA["LexFlow Head Admin<br/>Resend email test<br/>(Pagliano/ws9 only, isolated)"]

    OI -.->|"не пересекается"| BD
    OI -.->|"не пересекается"| HA
    BD -.->|"привлекает при необходимости"| FD["frontend-dev"]

    style OI fill:#3B7DD8,color:#fff
    style BD fill:#10B981,color:#fff
    style HA fill:#F59E0B,color:#fff
    style FD fill:#8B5CF6,color:#fff
```
