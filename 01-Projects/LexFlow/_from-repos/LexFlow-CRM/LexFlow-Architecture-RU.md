# LexFlow CRM — Архитектура и план развития

> **Версия:** 1.0 (Август 2026)  
> **Ветка:** `lexflow_hermes_v1`  
> **Локально:** `http://localhost:5002`  
> **GitHub:** `github.com/Ole00007/lexflow-crm`  
> **Excel:** `03-Resources/Hermes-Setup-and-MCP/LexFlow_Architecture_RU_EN.xlsx`

---

## 1. Текущая архитектура (что уже сделано)

### Стек

| Слой | Технология |
|------|------------|
| Бэкенд | Flask 2.3 + SQLAlchemy 2.0 |
| Фронтенд | Jinja2 шаблоны, Vanilla JS |
| База данных | SQLite (локально) / PostgreSQL (Railway) |
| Аутентификация | JWT (24ч, Flask-JWT-Extended) |
| Миграции | Alembic (6 миграций) |
| Email | Resend API (бесплатно: 100/день) |
| WhatsApp | UltraMsg API (бесплатно: 100/день) |
| Календарь | Google API (mock-режим) |

### Структура проекта

```
lexflow-crm-build/
├── crm/                    # Основное приложение
│   ├── __init__.py         # Фабрика приложения
│   ├── config.py           # Конфигурация
│   ├── extensions.py       # SQLAlchemy, JWT, CORS, Limiter
│   ├── workspace.py        # Мульти-аренда (фильтрация)
│   ├── activity_logger.py  # Авто-логирование активности
│   ├── notification_service.py  # Email + WhatsApp
│   ├── validators.py       # Валидация
│   ├── models/             # 9 моделей SQLAlchemy
│   │   ├── user.py         # Пользователи (с workspace_id)
│   │   ├── workspace.py    # Рабочие пространства
│   │   ├── contact.py      # Контакты (с GDPR полями)
│   │   ├── case.py         # Дела
│   │   ├── task.py         # Задачи
│   │   ├── deadline.py     # Дедлайны
│   │   ├── calendar_event.py  # События календаря
│   │   ├── note.py         # Заметки (полиморфные)
│   │   ├── activity.py     # Лента активности
│   │   ├── notification.py # Уведомления
│   │   └── event.py        # События (чат-бот)
│   ├── routes/             # 12 blueprint'ов
│   ├── services/           # Сервисы (календарь, уведомления)
│   └── clients/            # Внешние интеграции
├── migrations/             # 6 миграций Alembic
├── templates/              # 10 Jinja2 шаблонов
├── static/                 # Статика (включая Pagliano LP)
├── wsgi.py                 # Точка входа
└── Procfile.crm            # Gunicorn конфиг
```

### Мульти-аренда: 5 рабочих пространств

| # | Slug | Название | Логин клиента |
|---|------|----------|---------------|
| 1 | `avibeagency` | AVIBE Agency | avibe@lexflow.test / Avibe@12345 |
| 2 | `pagliano` | Avvocato Pagliano | pagliano@lexflow.test / Pag@12345 |
| 3 | `romanelli-studio` | Studio Romanelli | romanelli@lexflow.test / Rom@12345 |
| 4 | `romanelli-audit` | Romanelli Audit | audit@lexflow.test / Audit@12345 |
| 5 | `tommasoferro` | Avv. Tommaso Ferro | ferro@lexflow.test / Ferro@12345 |
| — | — | **Superadmin** | olesya00007a@yahoo.com / Test12345! |

**Ключевой принцип:** каждый пользователь видит ТОЛЬКО свои данные. Superadmin видит все.

### Фронтенд страницы (10 шт.)

| Маршрут | Страница | Тип | Авторизация |
|---------|----------|-----|-------------|
| `/` | Форма intake | Публичная | Нет |
| `/dashboard` | Дашборд со статистикой | Внутренняя | Опционально |
| `/contacts` | Список контактов | Внутренняя | Опционально |
| `/kanban` | Доска Kanban (5 колонок) | Внутренняя | Опционально |
| `/calendar` | Календарь заседаний | Внутренняя | Опционально |
| `/tasks` | Список задач | Внутренняя | Опционально |
| `/book` | Форма записи на приём | Публичная | Нет |
| `/admin` | Список дел | Внутренняя | Опционально |
| `/admin/matter/:id` | Детали дела + таймлайн | Внутренняя | Опционально |
| `/pagliano` | Лендинг Пальяно | Публичная | Нет |

### API маршруты (42)

| Метод | Маршрут | Описание |
|-------|---------|----------|
| POST | `/api/auth/login` | Вход → JWT токен |
| GET | `/api/auth/me` | Текущий пользователь |
| CRUD | `/api/contacts` | Контакты (с фильтрацией по workspace) |
| CRUD | `/api/cases` | Дела (с 5 статусами) |
| CRUD | `/api/tasks` | Задачи по делам |
| CRUD | `/api/calendar` | События календаря |
| CRUD | `/api/notes` | Заметки (полиморфные) |
| CRUD | `/api/deadlines` | Дедлайны |
| GET | `/api/activity` | Лента активности |
| CRUD | `/api/notifications` | Уведомления |
| POST | `/api/webhooks/chatbot/message` | Вебхук чат-бота |
| CRUD | `/api/admin/users` | Управление пользователями |
| POST | `/api/intake/{workspace_slug}` | Приём обращений с LP |

### Модели данных (9 таблиц)

```
Workspaces ──┬── Users ── (workspace_id)
             ├── Contacts (с GDPR полями: consent, source, consent_ts)
             ├── Cases ───┬── Tasks
             │             ├── Deadlines
             │             └── CalendarEvents (суд, судья, тип заседания)
             ├── Notes (полиморфные: case/contact/task)
             ├── ActivityLog (авто-логирование)
             ├── Notifications (внутренние уведомления)
             ├── Events (чат-бот/webhooks)
             └── ContactRelationships
```

### Безопасность

- JWT с 24-часовым сроком, workspace_id в токене
- Rate limiting: 1/мин логин, 60/мин чтение, 30/мин запись
- Security headers: HSTS, CSP, X-Frame-Options
- Soft delete на всех таблицах
- Валидация ввода на всех write-маршрутах

### Система уведомлений

```
Клиент заполняет форму записи
  → Создаётся CalendarEvent в БД
  → Email (Resend) клиенту — подтверждение
  → Email (Resend) адвокату — уведомление
  → WhatsApp (UltraMsg) клиенту — если указан телефон
  → WhatsApp (UltraMsg) адвокату — если настроен ULTRAMSG
```

---

## 2. Плановая архитектура (что будет построено)

### Фаза 2 — Портал документов для клиентов ⬅️ СЛЕДУЮЩАЯ

**Цель:** Каждый адвокат (Pagliano, Ferro, Romanelli) получает свой клиентский портал, куда их клиенты могут загружать документы напрямую в нужное workspace.

**Архитектура:**
```
Клиент Pagliano ──загружает договор──▶ /portal/pagliano/case/42
                                            │
                                            ▼
                                     uploads/workspace_2/case_42/
                                            │
                                            ▼
                              Email адвокату: "Новый документ"
```

**Маршруты:**
- `GET /portal/{workspace_slug}/case/{case_id}?token=...` — страница портала
- `POST /portal/{workspace_slug}/case/{case_id}/upload` — загрузка файла
- `GET /portal/{workspace_slug}/case/{case_id}/docs` — список документов

**Новая модель:**
```python
class Document(db.Model):
    id, workspace_id, case_id, uploaded_by, filename, filepath, file_size, uploaded_at
```

**Сложность:** 3-4 часа

### Фаза 3 — Hindsight Knowledge Graph

**Цель:** Синхронизировать все сущности CRM в граф знаний Hindsight для автоматического discovery связей.

**Архитектура:**
```
CRM (Flask)                    Hindsight (avibe-hq)
    │                                │
    │  Cron (каждые 15 минут)         │
    │  ───POST /api/graph/nodes──▶    │  contact:42, case:7
    │  ───POST /api/graph/edges──▶   │  client_of, similar_to
    │                                │
    │  ───Запрос "дела как #42"──▶   │  → case:#12, case:#38
```

**Что синхронизируем:**
- Узлы: Contact, Case, Workspace, CalendarEvent, Document
- Связи: `client_of` (контакт → workspace), `involves` (дело → контакт), `similar_to` (дело → другое дело)

**Что даёт:**
- Hindsight автоматически находит похожие дела (одинаковый casetype + суд)
- Кросс-воркспейс инсайты: "Pagliano и Ferro вели дела в одном суде"
- Таймлайн адвоката: все дела, события, документы одного workspace

**Сложность:** 6-8 часов

### Фаза 4 — Google Календарь (Live)

- Заменить mock на реальный OAuth2
- События из CRM → Google Calendar
- Обратная синхронизация: изменение в Google Calendar → CRM

**Сложность:** 2 часа

### Фаза 5 — Генератор многоязычных LP

- Шаблон landing page для каждого workspace
- Авто-генерация: Pagliano → итальянский, Ferro → итальянский/английский
- SEO-оптимизация: schema.org, Open Graph, meta tags

**Сложность:** 3 часа

### Фаза 6 — AEO/SEO автоматизация

- FAQ mining из дел адвоката
- Контент-брифы по практике (Diritto di Famiglia, Recupero Crediti, etc.)
- Schema.org генерация для каждой страницы

**Сложность:** 5 часов

### Фаза 7 — Счета и оплаты

- Счёт из дела (PDF генерация)
- Отправка email с счётом
- Статус: отправлен / оплачен / просрочен

**Сложность:** 4 часа

### Фаза 8 — Telegram бот

- Быстрый поиск дела: `/case 42`
- Дедлайны сегодня: `/deadlines today`
- Статус обращения: `/status [email]`

**Сложность:** 3 часа

---

## 3. Инфраструктура и бюджет

| Сервис | Стоимость | Примечание |
|--------|-----------|------------|
| Railway — PostgreSQL | ~$5/мес | Бесплатный уровень есть |
| Railway — Flask app | ~$5-10/мес | 1 worker, 512MB RAM |
| Railway — кастомный домен | Бесплатно | CNAME |
| Resend Email | Бесплатно | 100 писем/день |
| UltraMsg WhatsApp | Бесплатно | 100 сообщ/день |
| Google Calendar API | Бесплатно | |
| Hindsight (Railway) | ~$5/мес | Уже запущен |
| Cloudinary / S3 | ~$5/мес или бесплатно | Для документов |
| **ИТОГО** | **~$15-25/мес** | |

**Уже оплачено:** Nous Portal Plus — $20/мес (Hermes agent)

---

## 4. Дорожная карта с точками проверки

| Фаза | Задача | Время | Точка проверки |
|------|--------|-------|----------------|
| ✅ **1** | Пуш в GitHub | 15 мин | `lexflow_hermes_v1` на GitHub |
| **2** | **Портал документов** | **3-4ч** | **Клиент загружает PDF → адвокат видит** |
| 2.1 | Модель Document + миграция | 30м | `db upgrade` без ошибок |
| 2.2 | Маршрут /portal/{slug}/case/{id} | 1ч | 200 OK для правильного workspace |
| 2.3 | Magic-link авторизация | 30м | Без токена → 401, с токеном → 200 |
| 2.4 | Загрузка файлов + storage | 1ч | Файл в `uploads/workspace_{id}/` |
| 2.5 | Email уведомление о загрузке | 30м | Письмо адвокату |
| 2.6 | Проверка изоляции | 15м | Портал Pagliano ≠ портал Ferro |
| **3** | **Hindsight CRM Sync** | **6-8ч** | **Сущность CRM → узел в Hindsight** |
| 3.1 | hindsight_synced_at миграция | 15м | Колонка на всех таблицах |
| 3.2 | Sync скрипт (contacts + cases) | 2ч | Создать контакт → запустить → узел |
| 3.3 | Sync связей (edges) | 1ч | В графе есть ребро `client_of` |
| 3.4 | Cron задание 15 мин | 15м | Cron запускается, нет ошибок |
| 3.5 | NLP поиск связей | 2ч | 2 дела в одном суде → Hindsight связывает |
| 3.6 | Проверка поиска | 30м | "дела как #42" → связанные дела |
| **4** | **Google Календарь (Live)** | **2ч** | **Событие CRM → в Google Calendar** |
| **5** | **Генератор LP** | **3ч** | **Бренд Ferro ≠ бренд Pagliano** |
| **6** | **AEO/SEO движок** | **5ч** | **Schema.org на каждой LP** |
| **7** | **Счета + оплаты** | **4ч** | **Счёт из дела, статус оплаты** |
| **8** | **Telegram бот** | **3ч** | **"дедлайны сегодня" → ответ** |

---

## 5. Ключевые решения

1. **Мульти-аренда через workspace_id** — строка изоляции на уровне БД, middleware автоматически фильтрует
2. **Портал документов — подпапки, не поддомены** — проще, быстрее, не требует DNS
3. **Hindsight sync — cron first, hooks потом** — безопаснее, без риска сломать CRM
4. **Документы — локально/Fallback, потом S3** — для старта хватит локального storage
5. **Бесплатные сервисы везде** — Resend, UltraMsg, Railway free tier — пока не вырастем

---

## 6. Agents / Hindsight

Этот документ проиндексирован Hindsight (`avibe-hq`). Любой Hermes агент может найти архитектуру по запросу "LexFlow CRM архитектура" или загрузив этот файл из Obsidian.

[[03-Resources/Hermes-Setup-and-MCP/LexFlow-CRM-Architecture]]
[[01-Projects/LexFlow/LexFlow-MVP-Status]]