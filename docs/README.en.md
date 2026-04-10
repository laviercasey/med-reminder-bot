<div align="center">
  <h1>Med Reminder Bot</h1>
  <p>Telegram Mini App for medication tracking with smart reminders</p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.12" />
    <img src="https://img.shields.io/badge/Node.js-20-339933?style=flat-square&logo=nodedotjs&logoColor=white" alt="Node.js 20" />
    <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL 16" />
    <img src="https://img.shields.io/badge/Redis-7.4-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis 7.4" />
    <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
    <img src="https://img.shields.io/github/actions/workflow/status/laviercasey/med-reminder-bot/ci.yml?style=flat-square&label=CI" alt="CI Status" />
  </p>

  <p>
    <a href="../README.md">Русская версия</a>
  </p>
</div>

---

## Overview

Med Reminder Bot is a full-stack medication tracking system built as a Telegram Mini App. Users manage their medications through a React-based web interface embedded in Telegram, while an aiogram-powered bot delivers scheduled reminders with snooze and follow-up capabilities. The entire stack runs as a set of Docker containers orchestrated with Docker Compose, backed by PostgreSQL and Redis.

## Features

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Medication Management</strong></td>
      <td>Full CRUD for medications with name, schedule type (morning / day / evening / custom), and time via REST API and Telegram Mini App</td>
    </tr>
    <tr>
      <td><strong>Daily Checklists</strong></td>
      <td>Auto-generated daily checklists with per-medication taken/not-taken tracking; supports querying any date</td>
    </tr>
    <tr>
      <td><strong>Smart Reminders</strong></td>
      <td>Cron-based reminders at each medication's scheduled time with configurable follow-up repeat (1-60 min), snooze (5 / 15 / 30 min), and one-tap disable</td>
    </tr>
    <tr>
      <td><strong>Multilingual</strong></td>
      <td>Russian and English supported across bot messages and the frontend (i18next + bot localization layer)</td>
    </tr>
    <tr>
      <td><strong>Timezone Support</strong></td>
      <td>Per-user timezone setting; reminders and checklists respect the configured timezone</td>
    </tr>
    <tr>
      <td><strong>User Settings</strong></td>
      <td>Toggle reminders on/off, adjust repeat interval, change language -- all from the Mini App settings page</td>
    </tr>
    <tr>
      <td><strong>Admin Dashboard</strong></td>
      <td>Statistics (total/active users, DAU, registration trends, taken rate, top medications), user list with ban/unban, and audit logs</td>
    </tr>
    <tr>
      <td><strong>Real-time Sync</strong></td>
      <td>Redis Pub/Sub between API and Bot: creating or deleting a medication through the API triggers an immediate scheduler refresh in the bot</td>
    </tr>
    <tr>
      <td><strong>Telegram Auth</strong></td>
      <td>HMAC-SHA256 validation of Telegram WebApp <code>initData</code> with configurable token expiry</td>
    </tr>
    <tr>
      <td><strong>Rate Limiting</strong></td>
      <td>Redis-backed sliding window rate limiter at the API level plus Nginx <code>limit_req</code> at the reverse proxy level</td>
    </tr>
    <tr>
      <td><strong>Security Headers</strong></td>
      <td>HSTS, CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, and Permissions-Policy configured in Nginx</td>
    </tr>
  </tbody>
</table>

## Architecture

<details>
<summary>System Architecture</summary>

```
                        Telegram
                           |
              +------------+------------+
              |                         |
         Mini App UI               Bot (polling)
        (React / Vite)           (aiogram 3 + APScheduler)
              |                         |
              v                         v
           Nginx                  Redis Pub/Sub
         (reverse proxy,          (medications channel)
          static files,                 |
          rate limiting)                |
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

Container topology (Docker Compose):
+----------+  +----------+  +----------+  +----------+  +----------+  +----------+
| postgres |  |  redis   |  |   api    |  |   bot    |  |  nginx   |  | migrate  |
| :5432    |  | :6379    |  | :8000    |  |          |  | :80/:443 |  | (profile)|
+----------+  +----------+  +----------+  +----------+  +----------+  +----------+
```

</details>

## Tech Stack

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Technology</th>
      <th>Version</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr><td rowspan="6"><strong>Backend</strong></td><td>Python</td><td>3.12</td><td>Runtime</td></tr>
    <tr><td>FastAPI</td><td>0.115+</td><td>REST API framework</td></tr>
    <tr><td>SQLAlchemy</td><td>2.0+</td><td>Async ORM (asyncpg driver)</td></tr>
    <tr><td>Alembic</td><td>1.13+</td><td>Database migrations</td></tr>
    <tr><td>Pydantic</td><td>2.5+</td><td>Request/response validation</td></tr>
    <tr><td>Uvicorn</td><td>0.34+</td><td>ASGI server</td></tr>
    <tr><td rowspan="3"><strong>Bot</strong></td><td>aiogram</td><td>3.2+</td><td>Telegram Bot framework</td></tr>
    <tr><td>APScheduler</td><td>3.10+</td><td>Cron and one-shot reminder scheduling</td></tr>
    <tr><td>redis-py</td><td>5.2+</td><td>Pub/Sub listener, FSM storage</td></tr>
    <tr><td rowspan="8"><strong>Frontend</strong></td><td>React</td><td>18.3</td><td>UI library</td></tr>
    <tr><td>TypeScript</td><td>5.7</td><td>Type safety</td></tr>
    <tr><td>Vite</td><td>6.0</td><td>Build tool and dev server</td></tr>
    <tr><td>Tailwind CSS</td><td>4.2</td><td>Utility-first styling</td></tr>
    <tr><td>React Router</td><td>7.1</td><td>Client-side routing</td></tr>
    <tr><td>TanStack Query</td><td>5.62</td><td>Server state management</td></tr>
    <tr><td>Zustand</td><td>5.0</td><td>Client state management</td></tr>
    <tr><td>i18next</td><td>24.2</td><td>Internationalization</td></tr>
    <tr><td rowspan="2"><strong>Database</strong></td><td>PostgreSQL</td><td>16.6</td><td>Primary data store</td></tr>
    <tr><td>Redis</td><td>7.4</td><td>Rate limiting, Pub/Sub, bot FSM storage</td></tr>
    <tr><td rowspan="2"><strong>Infrastructure</strong></td><td>Docker Compose</td><td>-</td><td>Container orchestration (dev, prod, migrate profiles)</td></tr>
    <tr><td>Nginx</td><td>1.27</td><td>Reverse proxy, static file serving, security headers</td></tr>
    <tr><td rowspan="3"><strong>CI/CD</strong></td><td>GitHub Actions</td><td>-</td><td>CI pipeline (7 parallel jobs) and deploy workflow</td></tr>
    <tr><td>GHCR</td><td>-</td><td>Container registry for API and Bot images</td></tr>
    <tr><td>SSH Deploy</td><td>-</td><td>Deploy with health check and automatic rollback</td></tr>
    <tr><td rowspan="4"><strong>Testing</strong></td><td>pytest</td><td>8.3+</td><td>Backend tests with async support</td></tr>
    <tr><td>Vitest</td><td>2.1</td><td>Frontend unit tests</td></tr>
    <tr><td>Testing Library</td><td>16.1</td><td>React component testing</td></tr>
    <tr><td>Ruff</td><td>-</td><td>Python linting and formatting</td></tr>
  </tbody>
</table>

## Project Structure

<details>
<summary>Directory tree</summary>

```
med-reminder-bot/
|-- api/                          # FastAPI backend (Repository / Service / Router)
|   |-- core/                     # Config, security (Telegram auth), exceptions, response envelope
|   |-- middleware/                # Redis-backed rate limiter
|   |-- services/
|   |   |-- admin/                # Stats, user list, ban/unban, audit logs
|   |   |-- checklist/            # Daily checklist CRUD
|   |   |-- medication/           # Medication CRUD
|   |   |-- pubsub/               # Redis publisher for medication events
|   |   |-- settings/             # User settings (reminders, timezone, language)
|   |   `-- user/                 # User profile
|   |-- dependencies.py           # FastAPI dependency injection (auth, services, sessions)
|   `-- main.py                   # App factory, middleware registration, health check
|
|-- bot/                          # Telegram bot (aiogram 3)
|   |-- handlers/                 # /start, language selection, reminder callbacks (snooze, taken, disable)
|   |-- services/                 # APScheduler reminders, Redis Pub/Sub listener
|   |-- keyboards.py              # Inline keyboards (language, reminder actions, snooze options)
|   |-- localization.py           # i18n texts (ru, en)
|   `-- main.py                   # Bot entry point, dispatcher setup, daily scheduler init
|
|-- shared/                       # Code shared between API and Bot
|   |-- config.py                 # Pydantic Settings (env vars)
|   |-- database/
|   |   |-- db.py                 # Async engine, session maker, Base
|   |   `-- models.py             # User, Medication, Checklist, UserSettings, AdminLog
|   |-- logging.py                # Structured logger setup
|   `-- redis.py                  # Redis client singleton
|
|-- frontend/                     # React Telegram Mini App (Feature-Sliced Design)
|   `-- src/
|       |-- app/                  # Providers, routes, global styles
|       |-- entities/             # User, Medication, Checklist data models and UI
|       |-- features/             # Add/edit/delete medication, mark taken, change language, privacy consent
|       |-- pages/                # Checklist, Medications, Settings, Admin
|       |-- shared/               # API client, i18n config, UI components, utilities
|       `-- widgets/              # Checklist group, medication list, navigation
|
|-- migrations/                   # Alembic migration versions
|-- tests/                        # pytest backend tests (health, security, all API services)
|-- docker/
|   |-- api.Dockerfile            # Multi-stage Python 3.12 build
|   |-- bot.Dockerfile            # Multi-stage Python 3.12 build
|   `-- nginx/                    # Production and development Nginx configs
|-- docker-compose.yml            # Base compose (postgres, redis, api, bot, nginx, migrate)
|-- docker-compose.dev.yml        # Development overrides (hot reload, exposed ports)
|-- docker-compose.prod.yml       # Production overrides (resource limits, restart policies, workers)
|-- .github/workflows/
|   |-- ci.yml                    # 7-job CI: lint, security, test (backend + frontend), Docker build
|   `-- deploy.yml                # Build/push to GHCR, SSH deploy with health check and rollback
|-- .env.example                  # Template for required environment variables
|-- requirements.txt              # Python dependencies
|-- pyproject.toml                # pytest configuration
`-- ruff.toml                     # Ruff linter/formatter settings
```

The backend follows the **Repository / Service / Router** pattern: each domain module has its own repository for data access, a service for business logic, a router for HTTP endpoints, and Pydantic schemas for validation.

The frontend follows **Feature-Sliced Design (FSD)**: layers are `app > pages > widgets > features > entities > shared`, with each slice containing its own model, UI, and tests.

</details>

## Getting Started

### Prerequisites

- Docker and Docker Compose
- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- Node.js 20+ (for frontend development outside Docker)

### Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

<table>
  <thead>
    <tr>
      <th>Variable</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><code>BOT_TOKEN</code></td><td>Telegram bot token from BotFather</td><td><em>required</em></td></tr>
    <tr><td><code>ADMIN_IDS</code></td><td>Comma-separated Telegram user IDs with admin access</td><td><em>required</em></td></tr>
    <tr><td><code>DB_HOST</code></td><td>PostgreSQL hostname</td><td><code>postgres</code></td></tr>
    <tr><td><code>DB_PORT</code></td><td>PostgreSQL port</td><td><code>5432</code></td></tr>
    <tr><td><code>DB_USER</code></td><td>PostgreSQL username</td><td><code>med_user</code></td></tr>
    <tr><td><code>DB_PASS</code></td><td>PostgreSQL password</td><td><em>required</em></td></tr>
    <tr><td><code>DB_NAME</code></td><td>PostgreSQL database name</td><td><code>med_reminder</code></td></tr>
    <tr><td><code>REDIS_URL</code></td><td>Redis connection URL</td><td><code>redis://redis:6379/0</code></td></tr>
    <tr><td><code>DOMAIN</code></td><td>Production domain for the application</td><td><em>empty</em></td></tr>
    <tr><td><code>MINI_APP_URL</code></td><td>Full URL of the Telegram Mini App (used for CORS and bot links)</td><td><em>empty</em></td></tr>
    <tr><td><code>API_PORT</code></td><td>Port the API listens on inside the container</td><td><code>8000</code></td></tr>
    <tr><td><code>ENVIRONMENT</code></td><td><code>development</code> or <code>production</code></td><td><code>development</code></td></tr>
    <tr><td><code>RATE_LIMIT_PER_MINUTE</code></td><td>Max API requests per IP per minute</td><td><code>60</code></td></tr>
    <tr><td><code>MAX_AUTH_AGE</code></td><td>Telegram auth data validity period in seconds</td><td><code>86400</code></td></tr>
    <tr><td><code>CORS_ORIGINS</code></td><td>Comma-separated allowed CORS origins (falls back to <code>MINI_APP_URL</code>)</td><td><em>empty</em></td></tr>
  </tbody>
</table>

### Development Setup

Build the frontend before starting containers (Nginx serves the static build):

```bash
cd frontend && npm ci && npm run build && cd ..
```

Start all services with hot reload for the API and bot:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

Run database migrations:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml --profile migrate up migrate
```

Services available in development:

<table>
  <thead>
    <tr>
      <th>Service</th>
      <th>URL</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Mini App (via Nginx)</td><td><code>http://localhost:8080</code></td></tr>
    <tr><td>API (direct)</td><td><code>http://localhost:8000</code></td></tr>
    <tr><td>PostgreSQL</td><td><code>localhost:5432</code></td></tr>
    <tr><td>Redis</td><td><code>localhost:6379</code></td></tr>
  </tbody>
</table>

### Production Deployment

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml --profile migrate up migrate -d --wait
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
```

The production configuration sets resource limits, runs Uvicorn with 4 workers, and enables `restart: unless-stopped` for all services.

## API Reference

All endpoints return a consistent envelope:

```json
{
  "success": true,
  "data": { },
  "error": null
}
```

Authentication is performed via the `Authorization` header containing the Telegram Mini App `initData` string (optionally prefixed with `tma `).

<details>
<summary>Health</summary>

#### `GET /api/health`

No authentication required. Probes PostgreSQL and Redis connectivity.

**Response:**

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

Returns the authenticated user's profile.

**Response data:**

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

Returns all medications for the authenticated user.

**Response data:**

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

Returns a single medication by ID.

#### `POST /api/medications`

Creates a new medication and auto-generates a checklist entry for today. Publishes a `medication_created` event via Redis Pub/Sub to refresh the bot scheduler.

**Request body:**

```json
{
  "name": "Vitamin D",
  "schedule": "morning",
  "time": "08:00"
}
```

`schedule` must be one of: `morning`, `day`, `evening`, `custom`.

#### `PUT /api/medications/{medication_id}`

Updates an existing medication. Publishes a `medication_updated` event.

**Request body:** same as `POST`.

#### `DELETE /api/medications/{medication_id}`

Deletes a medication and all associated checklist entries. Publishes a `medication_deleted` event.

</details>

<details>
<summary>Checklist</summary>

#### `GET /api/checklist`

Returns the checklist for today (or a specified date). Auto-generates missing entries for all active medications.

**Query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `date` | `YYYY-MM-DD` | Target date (defaults to today) |

**Response data:**

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

Marks a checklist item as taken or not taken.

**Request body:**

```json
{
  "status": true
}
```

</details>

<details>
<summary>Settings</summary>

#### `GET /api/settings`

Returns the authenticated user's settings.

**Response data:**

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

Partially updates settings. All fields are optional.

**Request body:**

```json
{
  "reminders_enabled": true,
  "reminder_repeat_minutes": 15,
  "language": "ru"
}
```

`reminder_repeat_minutes` must be between 1 and 60. `language` must be `en` or `ru`.

</details>

<details>
<summary>Admin (requires admin access)</summary>

Admin endpoints require the authenticated user's Telegram ID to be listed in the `ADMIN_IDS` environment variable.

#### `GET /api/admin/stats`

Returns platform-wide statistics.

**Response data:**

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

Returns a paginated user list.

**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | `int` | `100` | Max results (1-500) |
| `offset` | `int` | `0` | Pagination offset |

#### `POST /api/admin/ban`

Blocks a user by Telegram ID.

**Request body:**

```json
{ "telegram_id": 123456789 }
```

#### `POST /api/admin/unban`

Unblocks a user by Telegram ID.

**Request body:**

```json
{ "telegram_id": 123456789 }
```

#### `GET /api/admin/logs`

Returns recent admin action audit logs.

**Query parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | `int` | `50` | Max results (1-500) |

</details>

## CI/CD Pipeline

<details>
<summary>CI Workflow (ci.yml)</summary>

Triggered on push and pull request to `main`. Runs 7 parallel jobs:

| Job | Description |
|-----|-------------|
| **Backend Lint** | Ruff linting and format check |
| **Backend Security** | `pip-audit` dependency vulnerability scan |
| **Backend Test** | pytest with coverage (80% minimum threshold, covers `api`, `bot`, `shared`) |
| **Frontend Lint** | ESLint (zero warnings) and TypeScript type check |
| **Frontend Security** | `npm audit` at high severity level |
| **Frontend Test** | Vitest with 80% coverage thresholds (lines, functions, branches, statements) |
| **Docker Build** | Builds API and Bot images (runs after lint and test jobs pass) |

</details>

<details>
<summary>Deploy Workflow (deploy.yml)</summary>

Triggered on push to `main` after CI passes.

1. Logs into GitHub Container Registry (GHCR)
2. Builds and pushes API and Bot images tagged with `latest` and the short commit SHA
3. SSHs into the production server and runs `docker compose pull` followed by `up -d`
4. Waits 10 seconds, then checks the API container health status
5. On health check failure: rolls back to the previous image tags and exits with error
6. On success: prunes unused images

</details>

## Testing

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

Both backend and frontend enforce a minimum 80% code coverage threshold in CI.

## Database Migrations

Generate a new migration after modifying models:

```bash
alembic revision --autogenerate -m "description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

In Docker, migrations run via the `migrate` profile:

```bash
docker compose --profile migrate up migrate
```
