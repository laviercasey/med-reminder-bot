<div align="center">
  <h1>Med Reminder Bot</h1>
  <p>Telegram Mini App для отслеживания приема лекарств с умными напоминаниями</p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12" />
    <img src="https://img.shields.io/badge/Node.js-20-339933?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node.js 20" />
    <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL 16" />
    <img src="https://img.shields.io/badge/Redis-7.4-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis 7.4" />
    <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
    <img src="https://img.shields.io/github/actions/workflow/status/laviercasey/med-reminder-bot/ci.yml?style=flat-square&label=CI" alt="CI Status" />
  </p>

  <p>
    <a href="https://t.me/MedNapominalkaBot">
      <img src="https://img.shields.io/badge/Попробовать_в_Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Попробовать в Telegram" />
    </a>
  </p>

  <p>
    <a href="docs/README.en.md">English version</a>
  </p>
</div>

---

## Обзор

Med Reminder Bot -- полнофункциональная система для отслеживания приема лекарств, реализованная как Telegram Mini App. Пользователи управляют лекарствами через React-интерфейс, встроенный в Telegram, а aiogram-бот доставляет напоминания по расписанию с поддержкой отложенного повтора и snooze. Весь стек работает в Docker-контейнерах, управляемых через Docker Compose, с PostgreSQL и Redis в качестве хранилищ.

## Возможности

<table>
  <thead>
    <tr>
      <th>Область</th>
      <th>Описание</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Управление лекарствами</strong></td>
      <td>Полный CRUD: название, тип расписания (утро / день / вечер / произвольное) и время приема через REST API и Telegram Mini App</td>
    </tr>
    <tr>
      <td><strong>Ежедневные чеклисты</strong></td>
      <td>Автоматическая генерация чеклиста на каждый день с отметкой принято/не принято по каждому лекарству; поддержка просмотра за любую дату</td>
    </tr>
    <tr>
      <td><strong>Надежные напоминания</strong></td>
      <td>Cron-напоминания в назначенное время с настраиваемым повтором (1-60 мин), отложенным напоминанием (5 / 15 / 30 мин), защитой от переотправки (поле <code>reminder_sent_at</code>) и автоматическим восстановлением пропущенных при перезагрузке</td>
    </tr>
    <tr>
      <td><strong>Мультиязычность</strong></td>
      <td>Русский и английский язык в сообщениях бота и фронтенде (i18next + слой локализации бота)</td>
    </tr>
    <tr>
      <td><strong>Поддержка часовых поясов</strong></td>
      <td>Индивидуальная настройка часового пояса для каждого пользователя; напоминания и чеклисты учитывают его</td>
    </tr>
    <tr>
      <td><strong>Настройки пользователя</strong></td>
      <td>Включение/выключение напоминаний, настройка интервала повтора, смена языка -- все из страницы настроек Mini App</td>
    </tr>
    <tr>
      <td><strong>Панель администратора</strong></td>
      <td>Статистика (всего/активных пользователей, DAU, тренды регистраций, процент приема, топ лекарств), список пользователей с бан/разбан, журнал действий</td>
    </tr>
    <tr>
      <td><strong>Синхронизация в реальном времени</strong></td>
      <td>Redis Pub/Sub между API и ботом: создание или удаление лекарства через API мгновенно обновляет планировщик напоминаний бота</td>
    </tr>
    <tr>
      <td><strong>JWT Сессионная аутентификация</strong></td>
      <td>Валидация инициального Telegram <code>initData</code> HMAC-SHA256, выдача пары токенов (access + refresh), ротация токенов с защитой от переиспользования</td>
    </tr>
    <tr>
      <td><strong>Rate Limiting</strong></td>
      <td>Redis-бэкенд скользящего окна на уровне API + <code>limit_req</code> на уровне реверс-прокси (Nginx в dev, Caddy в prod)</td>
    </tr>
    <tr>
      <td><strong>Заголовки безопасности</strong></td>
      <td>HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy и Permissions-Policy на уровне реверс-прокси (Nginx в dev, Caddy в prod)</td>
    </tr>
  </tbody>
</table>

## Архитектура

<details>
<summary>Схема системы</summary>

```
                        Telegram
                           |
              +------------+------------+
              |                         |
         Mini App UI               Bot (polling)
        (React / Vite)           (aiogram 3 + APScheduler)
              |                         |
              v                         v
     Nginx (dev) / Caddy (prod)  Redis Pub/Sub
       (реверс-прокси,            (канал medications)
        статика, rate limiting,         |
        security headers)               |
              |                         |
              v                         |
          FastAPI                       |
       (REST API, auth,        <--------+
        CORS, rate limit)
              |
              v
         PostgreSQL 16
      (users, medications,
       checklists, settings,
       admin_logs)

Топология контейнеров (Docker Compose):
+----------+  +----------+  +----------+  +----------+  +----------+  +----------+
| postgres |  |  redis   |  |   api    |  |   bot    |  |  nginx   |  | migrate  |
| :5432    |  | :6379    |  | :8000    |  |          |  | :80/:443 |  | (profile)|
+----------+  +----------+  +----------+  +----------+  +----------+  +----------+
```

</details>

## Стек технологий

<table>
  <thead>
    <tr>
      <th>Категория</th>
      <th>Технология</th>
      <th>Версия</th>
      <th>Назначение</th>
    </tr>
  </thead>
  <tbody>
    <tr><td rowspan="7"><strong>Backend</strong></td><td>Python</td><td>3.12</td><td>Среда выполнения</td></tr>
    <tr><td>FastAPI</td><td>0.115+</td><td>REST API фреймворк</td></tr>
    <tr><td>SQLAlchemy</td><td>2.0+</td><td>Асинхронная ORM (драйвер asyncpg)</td></tr>
    <tr><td>Alembic</td><td>1.13+</td><td>Миграции базы данных</td></tr>
    <tr><td>Pydantic</td><td>2.5+</td><td>Валидация запросов/ответов</td></tr>
    <tr><td>PyJWT</td><td>2.8+</td><td>Подпись и верификация JWT токенов</td></tr>
    <tr><td>Uvicorn</td><td>0.34+</td><td>ASGI-сервер</td></tr>
    <tr><td rowspan="3"><strong>Bot</strong></td><td>aiogram</td><td>3.2+</td><td>Фреймворк Telegram-бота</td></tr>
    <tr><td>APScheduler</td><td>3.10+</td><td>Планировщик cron- и одноразовых напоминаний</td></tr>
    <tr><td>redis-py</td><td>5.2+</td><td>Pub/Sub подписчик</td></tr>
    <tr><td rowspan="8"><strong>Frontend</strong></td><td>React</td><td>18.3</td><td>UI-библиотека</td></tr>
    <tr><td>TypeScript</td><td>5.7</td><td>Типизация</td></tr>
    <tr><td>Vite</td><td>6.0</td><td>Сборщик и dev-сервер</td></tr>
    <tr><td>Tailwind CSS</td><td>4.2</td><td>Utility-first стилизация</td></tr>
    <tr><td>React Router</td><td>7.1</td><td>Клиентская маршрутизация</td></tr>
    <tr><td>TanStack Query</td><td>5.62</td><td>Управление серверным состоянием</td></tr>
    <tr><td>Zustand</td><td>5.0</td><td>Управление клиентским состоянием</td></tr>
    <tr><td>i18next</td><td>24.2</td><td>Интернационализация</td></tr>
    <tr><td rowspan="2"><strong>База данных</strong></td><td>PostgreSQL</td><td>16.6</td><td>Основное хранилище</td></tr>
    <tr><td>Redis</td><td>7.4</td><td>Rate limiting, Pub/Sub</td></tr>
    <tr><td rowspan="3"><strong>Инфраструктура</strong></td><td>Docker Compose</td><td>-</td><td>Оркестрация контейнеров (dev, prod, migrate)</td></tr>
    <tr><td>Nginx</td><td>1.27</td><td>Реверс-прокси в dev-стеке, раздача статики, заголовки безопасности</td></tr>
    <tr><td>Caddy</td><td>2.9</td><td>Реверс-прокси в prod, автоматический HTTPS (Let's Encrypt), HTTP/3</td></tr>
    <tr><td rowspan="3"><strong>CI/CD</strong></td><td>GitHub Actions</td><td>-</td><td>CI-пайплайн (7 параллельных задач) и деплой</td></tr>
    <tr><td>GHCR</td><td>-</td><td>Реестр контейнеров для образов API и бота</td></tr>
    <tr><td>SSH Deploy</td><td>-</td><td>Деплой с проверкой здоровья и автоматическим откатом</td></tr>
    <tr><td rowspan="4"><strong>Тестирование</strong></td><td>pytest</td><td>8.3+</td><td>Бэкенд-тесты с поддержкой async</td></tr>
    <tr><td>Vitest</td><td>2.1</td><td>Фронтенд юнит-тесты</td></tr>
    <tr><td>Testing Library</td><td>16.1</td><td>Тестирование React-компонентов</td></tr>
    <tr><td>Ruff</td><td>-</td><td>Линтинг и форматирование Python</td></tr>
  </tbody>
</table>

## Структура проекта

<details>
<summary>Дерево каталогов</summary>

```
med-reminder-bot/
|-- api/                          # FastAPI backend (Repository / Service / Router)
|   |-- core/                     # Конфигурация, безопасность (Telegram auth), исключения, обертка ответа
|   |-- middleware/                # Rate limiter на Redis
|   |-- services/
|   |   |-- admin/                # Статистика, список пользователей, бан/разбан, журнал действий
|   |   |-- checklist/            # CRUD ежедневного чеклиста
|   |   |-- medication/           # CRUD лекарств
|   |   |-- pubsub/               # Redis publisher событий лекарств
|   |   |-- settings/             # Настройки пользователя (напоминания, часовой пояс, язык)
|   |   `-- user/                 # Профиль пользователя
|   |-- dependencies.py           # FastAPI Dependency Injection (auth, сервисы, сессии)
|   `-- main.py                   # Фабрика приложения, регистрация middleware, health check
|
|-- bot/                          # Telegram-бот (aiogram 3)
|   |-- handlers/                 # /start, выбор языка, колбэки напоминаний (snooze, принято, отключить)
|   |-- services/                 # APScheduler напоминания, Redis Pub/Sub подписчик
|   |-- keyboards.py              # Inline-клавиатуры (язык, действия, snooze)
|   |-- localization.py           # Тексты i18n (ru, en)
|   `-- main.py                   # Точка входа бота, настройка диспетчера, инициализация планировщика
|
|-- shared/                       # Общий код для API и бота
|   |-- config.py                 # Pydantic Settings (переменные окружения)
|   |-- database/
|   |   |-- db.py                 # Async engine, session maker, Base
|   |   `-- models.py             # User, Medication, Checklist, UserSettings, AdminLog
|   |-- logging.py                # Настройка структурированного логгера
|   `-- redis.py                  # Синглтон Redis-клиента
|
|-- frontend/                     # React Telegram Mini App (Feature-Sliced Design)
|   `-- src/
|       |-- app/                  # Провайдеры, маршруты, глобальные стили
|       |-- entities/             # Модели данных и UI: User, Medication, Checklist
|       |-- features/             # Добавить/редактировать/удалить лекарство, отметить прием, сменить язык
|       |-- pages/                # Чеклист, Лекарства, Настройки, Админ
|       |-- shared/               # API-клиент, конфигурация i18n, UI-компоненты, утилиты
|       `-- widgets/              # Группа чеклиста, список лекарств, навигация
|
|-- migrations/                   # Версии миграций Alembic
|-- tests/                        # pytest тесты бэкенда (health, security, все API-сервисы)
|-- docker/
|   |-- api.Dockerfile            # Multi-stage сборка Python 3.12
|   |-- bot.Dockerfile            # Multi-stage сборка Python 3.12
|   `-- nginx/                    # Конфигурации Nginx для prod и dev
|-- docker-compose.yml            # Базовый compose (postgres, redis, api, bot, nginx, migrate)
|-- docker-compose.dev.yml        # Dev-оверрайды (hot reload, открытые порты)
|-- docker-compose.prod.yml       # Prod-оверрайды (лимиты ресурсов, restart policies, воркеры)
|-- .github/workflows/
|   |-- ci.yml                    # 7 параллельных задач CI: lint, security, test, Docker build
|   `-- deploy.yml                # Сборка/push в GHCR, SSH-деплой с health check и rollback
|-- .env.example                  # Шаблон переменных окружения
|-- requirements.txt              # Python-зависимости
|-- pyproject.toml                # Конфигурация pytest
`-- ruff.toml                     # Настройки линтера/форматтера Ruff
```

Бэкенд построен по паттерну **Repository / Service / Router**: каждый доменный модуль содержит собственный репозиторий для доступа к данным, сервис для бизнес-логики, роутер для HTTP-эндпоинтов и Pydantic-схемы для валидации.

Фронтенд построен по архитектуре **Feature-Sliced Design (FSD)**: слои `app > pages > widgets > features > entities > shared`, каждый слайс содержит свою модель, UI и тесты.

</details>

## Быстрый старт

### Требования

- Docker и Docker Compose
- Токен Telegram-бота от [@BotFather](https://t.me/BotFather)
- Node.js 20+ (для локальной разработки фронтенда)

### Переменные окружения

Скопируйте файл-пример и заполните значения:

```bash
cp .env.example .env
```

<table>
  <thead>
    <tr>
      <th>Переменная</th>
      <th>Описание</th>
      <th>По умолчанию</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>BOT_TOKEN</code></td><td>Токен Telegram-бота от BotFather</td><td><em>обязательно</em></td></tr>
    <tr><td><code>ADMIN_IDS</code></td><td>Telegram ID администраторов через запятую</td><td><em>обязательно</em></td></tr>
    <tr><td><code>DB_HOST</code></td><td>Хост PostgreSQL</td><td><code>postgres</code></td></tr>
    <tr><td><code>DB_PORT</code></td><td>Порт PostgreSQL</td><td><code>5432</code></td></tr>
    <tr><td><code>DB_USER</code></td><td>Имя пользователя PostgreSQL</td><td><code>med_user</code></td></tr>
    <tr><td><code>DB_PASS</code></td><td>Пароль PostgreSQL</td><td><em>обязательно</em></td></tr>
    <tr><td><code>DB_NAME</code></td><td>Имя базы данных</td><td><code>med_reminder</code></td></tr>
    <tr><td><code>REDIS_URL</code></td><td>URL подключения к Redis</td><td><code>redis://redis:6379/0</code></td></tr>
    <tr><td><code>DOMAIN</code></td><td>Домен приложения в продакшене</td><td><em>не задано</em></td></tr>
    <tr><td><code>MINI_APP_URL</code></td><td>Полный URL Telegram Mini App (используется для CORS и ссылок бота)</td><td><em>не задано</em></td></tr>
    <tr><td><code>API_PORT</code></td><td>Порт API внутри контейнера</td><td><code>8000</code></td></tr>
    <tr><td><code>ENVIRONMENT</code></td><td><code>development</code> или <code>production</code></td><td><code>development</code></td></tr>
    <tr><td><code>RATE_LIMIT_PER_MINUTE</code></td><td>Максимум запросов к API на IP в минуту</td><td><code>60</code></td></tr>
    <tr><td><code>MAX_AUTH_AGE</code></td><td>Срок действия Telegram auth данных в секундах</td><td><code>86400</code></td></tr>
    <tr><td><code>CORS_ORIGINS</code></td><td>Разрешенные CORS-источники через запятую (фоллбэк на <code>MINI_APP_URL</code>)</td><td><em>не задано</em></td></tr>
    <tr><td><code>JWT_SECRET</code></td><td>Тайный ключ для подписания JWT токенов (сгенерировать: <code>python -c "import secrets; print(secrets.token_urlsafe(48))"</code>)</td><td><em>обязательно</em></td></tr>
    <tr><td><code>JWT_ACCESS_TTL_SECONDS</code></td><td>Время жизни access-токена в секундах</td><td><code>900</code> (15 минут)</td></tr>
    <tr><td><code>JWT_REFRESH_TTL_SECONDS</code></td><td>Время жизни refresh-токена в секундах</td><td><code>604800</code> (7 дней)</td></tr>
    <tr><td><code>JWT_ISSUER</code></td><td>Издатель JWT токена (для верификации)</td><td><code>med-reminder-api</code></td></tr>
    <tr><td><code>JWT_AUDIENCE</code></td><td>Целевая аудитория JWT токена (для верификации)</td><td><code>med-reminder-miniapp</code></td></tr>
  </tbody>
</table>

### Запуск для разработки

Соберите фронтенд перед запуском контейнеров (Nginx раздает статическую сборку):

```bash
cd frontend && npm ci && npm run build && cd ..
```

Запустите все сервисы с hot reload для API и бота:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

Запустите миграции базы данных:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml --profile migrate up migrate
```

Доступные сервисы в режиме разработки:

<table>
  <thead>
    <tr>
      <th>Сервис</th>
      <th>URL</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Mini App (через Nginx)</td><td><code>http://localhost:8080</code></td></tr>
    <tr><td>API (напрямую)</td><td><code>http://localhost:8000</code></td></tr>
    <tr><td>PostgreSQL</td><td><code>localhost:5432</code></td></tr>
    <tr><td>Redis</td><td><code>localhost:6379</code></td></tr>
  </tbody>
</table>

### Деплой в продакшен

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml --profile migrate up migrate -d --wait
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
```

Продакшен-конфигурация устанавливает лимиты ресурсов, запускает Uvicorn с 4 воркерами и включает `restart: unless-stopped` для всех сервисов.

## Аутентификация

Система использует **JWT сессионную аутентификацию** с парой токенов и ротацией:

1. **Вход** (`POST /api/auth/login`): Отправьте Telegram Mini App `initData`. API проверяет HMAC-SHA256 подпись.
2. **Выдача пары**: API возвращает `access_token` (15 минут) и `refresh_token` (7 дней).
3. **Защита от переиспользования**: Каждый refresh токен привязан к устройству (User-Agent) и может быть использован только один раз. При переиспользовании все токены пользователя аннулируются.
4. **Использование**: На все защищённые запросы отправляйте заголовок `Authorization: Bearer <access_token>`.
5. **Обновление** (`POST /api/auth/refresh`): Когда access токен истёк, отправьте refresh токен для получения новой пары.
6. **Выход** (`POST /api/auth/logout`): Аннулирует refresh токен.

## Справочник API

Все эндпоинты возвращают ответ в едином формате:

```json
{
  "success": true,
  "data": { },
  "error": null
}
```

<details>
<summary>Auth</summary>

#### `POST /api/auth/login`

Вход пользователя с помощью Telegram Mini App `initData`. Возвращает пару токенов для аутентификации.

**Тело запроса:**

```json
{
  "init_data": "query_id=..&user=..&..."
}
```

**Данные ответа:**

```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "...",
  "token_type": "Bearer",
  "expires_in": 900,
  "expires_at": 1705334400,
  "refresh_expires_at": 1706539200
}
```

#### `POST /api/auth/refresh`

Получение новой пары токенов при истечении access токена.

**Тело запроса:**

```json
{
  "refresh_token": "..."
}
```

**Данные ответа:** то же самое, что в `/login`.

#### `POST /api/auth/logout`

Аннулирует refresh токен.

**Требует аутентификации.** Тело запроса:

```json
{
  "refresh_token": "..."
}
```

**Данные ответа:**

```json
{
  "revoked": true
}
```

</details>

<details>
<summary>Health</summary>

#### `GET /api/health`

Не требует аутентификации. Проверяет подключение к PostgreSQL и Redis.

**Ответ:**

```json
{
  "status": "ok",
  "database": "ok",
  "redis": "ok"
}
```

</details>

<details>
<summary>User</summary>

#### `GET /api/me`

Возвращает профиль аутентифицированного пользователя.

**Данные ответа:**

```json
{
  "id": 1,
  "telegram_id": 123456789,
  "language": "en",
  "is_admin": false,
  "created_at": "2025-01-01T00:00:00Z",
  "last_active": "2025-01-15T12:30:00Z",
  "medications_count": 3
}
```

</details>

<details>
<summary>Medications</summary>

#### `GET /api/medications`

Возвращает все лекарства аутентифицированного пользователя.

**Данные ответа:**

```json
{
  "medications": [
    {
      "id": 1,
      "name": "Vitamin D",
      "schedule": "morning",
      "time": "08:00",
      "created_at": "2025-01-01T00:00:00Z"
    }
  ],
  "count": 1
}
```

#### `GET /api/medications/{medication_id}`

Возвращает одно лекарство по ID.

#### `POST /api/medications`

Создает новое лекарство и автоматически генерирует запись чеклиста на сегодня. Публикует событие `medication_created` через Redis Pub/Sub для обновления планировщика бота.

**Тело запроса:**

```json
{
  "name": "Vitamin D",
  "schedule": "morning",
  "time": "08:00"
}
```

`schedule` должен быть одним из: `morning`, `day`, `evening`, `custom`.

#### `PUT /api/medications/{medication_id}`

Обновляет существующее лекарство. Публикует событие `medication_updated`.

**Тело запроса:** аналогично `POST`.

#### `DELETE /api/medications/{medication_id}`

Удаляет лекарство и все связанные записи чеклиста. Публикует событие `medication_deleted`.

</details>

<details>
<summary>Checklist</summary>

#### `GET /api/checklist`

Возвращает чеклист на сегодня (или на указанную дату). Автоматически создает недостающие записи для всех активных лекарств.

**Параметры запроса:**

| Параметр | Тип | Описание |
|----------|-----|----------|
| `date` | `YYYY-MM-DD` | Целевая дата (по умолчанию -- сегодня) |

**Данные ответа:**

```json
{
  "items": [
    {
      "id": 1,
      "medication_id": 1,
      "medication_name": "Vitamin D",
      "medication_time": "08:00",
      "schedule": "morning",
      "date": "2025-01-15",
      "status": false,
      "updated_at": null
    }
  ],
  "date": "2025-01-15",
  "total": 1,
  "taken": 0
}
```

#### `PATCH /api/checklist/{checklist_id}`

Отмечает запись чеклиста как принятую или не принятую.

**Тело запроса:**

```json
{
  "status": true
}
```

</details>

<details>
<summary>Settings</summary>

#### `GET /api/settings`

Возвращает настройки аутентифицированного пользователя.

**Данные ответа:**

```json
{
  "reminders_enabled": true,
  "reminder_repeat_minutes": 30,
  "language": "en",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-15T12:00:00Z"
}
```

#### `PATCH /api/settings`

Частично обновляет настройки. Все поля опциональны.

**Тело запроса:**

```json
{
  "reminders_enabled": true,
  "reminder_repeat_minutes": 15,
  "language": "ru"
}
```

`reminder_repeat_minutes` -- от 1 до 60. `language` -- `en` или `ru`.

</details>

<details>
<summary>Admin (требуется доступ администратора)</summary>

Эндпоинты администратора требуют, чтобы Telegram ID пользователя был указан в переменной окружения `ADMIN_IDS`.

#### `GET /api/admin/stats`

Возвращает общую статистику платформы.

**Данные ответа:**

```json
{
  "total_users": 150,
  "active_users": 42,
  "avg_pills": 2.3,
  "taken_rate": 78.5,
  "dau": 18,
  "new_today": 3,
  "new_week": 12,
  "new_month": 45,
  "weekly_registrations": [2, 1, 3, 0, 2, 1, 3],
  "recent_users": [
    { "id": 10, "registered_ago": "2h ago", "meds_count": 3 }
  ],
  "top_medications": [
    { "name": "Vitamin D", "users": 25 }
  ]
}
```

#### `GET /api/admin/users`

Возвращает список пользователей с пагинацией.

**Параметры запроса:**

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `limit` | `int` | `100` | Максимум записей (1-500) |
| `offset` | `int` | `0` | Смещение для пагинации |

#### `POST /api/admin/ban`

Блокирует пользователя по Telegram ID.

**Тело запроса:**

```json
{ "telegram_id": 123456789 }
```

#### `POST /api/admin/unban`

Разблокирует пользователя по Telegram ID.

**Тело запроса:**

```json
{ "telegram_id": 123456789 }
```

#### `GET /api/admin/logs`

Возвращает журнал действий администраторов.

**Параметры запроса:**

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `limit` | `int` | `50` | Максимум записей (1-500) |

</details>

## CI/CD пайплайн

<details>
<summary>CI Workflow (ci.yml)</summary>

Запускается при push и pull request в `main`. Выполняет 7 параллельных задач:

| Задача | Описание |
|--------|----------|
| **Backend Lint** | Проверка Ruff (lint + format) |
| **Backend Security** | Аудит Python-зависимостей через `pip-audit` |
| **Backend Test** | pytest с покрытием (порог 80%, охват `api`, `bot`, `shared`) |
| **Frontend Lint** | ESLint (без предупреждений) и проверка типов TypeScript |
| **Frontend Security** | `npm audit` на уровне high |
| **Frontend Test** | Vitest с порогами покрытия 80% (строки, функции, ветки, выражения) |
| **Docker Build** | Сборка образов API и Bot (запускается после успешных lint и test) |

</details>

<details>
<summary>Deploy Workflow (deploy.yml)</summary>

Запускается при push в `main` после прохождения CI.

1. Авторизация в GitHub Container Registry (GHCR)
2. Сборка и push образов API и Bot с тегами `latest` и коротким SHA коммита
3. SSH-подключение к серверу, `docker compose pull` и `up -d`
4. Ожидание 10 секунд, проверка статуса здоровья API-контейнера
5. При провале health check: откат на предыдущие теги образов, завершение с ошибкой
6. При успехе: очистка неиспользуемых образов

</details>

## Тестирование

**Backend:**

```bash
pip install -r requirements.txt pytest-cov
pytest --cov=api --cov=bot --cov=shared --cov-report=term-missing --cov-fail-under=80
```

**Frontend:**

```bash
cd frontend
npm ci
npx vitest run --coverage
```

В CI для обоих стеков установлен минимальный порог покрытия 80%.

## Миграции базы данных

Генерация новой миграции после изменения моделей:

```bash
alembic revision --autogenerate -m "описание изменений"
```

Применение миграций:

```bash
alembic upgrade head
```

В Docker миграции запускаются через профиль `migrate`:

```bash
docker compose --profile migrate up migrate
```
