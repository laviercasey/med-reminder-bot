# 💊 MedReminderBot — Telegram бот-напоминалка о приеме лекарств

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?style=flat&logo=postgresql)
![Aiogram](https://img.shields.io/badge/Framework-Aiogram-2ec866?style=flat&logo=telegram)

> Умный Telegram-бот для контроля приема лекарств: добавляйте таблетки, отмечайте, принимали ли вы их, и получайте напоминания — все в привычном мессенджере.

---

## 🚀 Возможности

- Мультиязычный интерфейс: 🇷🇺 Русский и 🇬🇧 Английский
- Добавление и удаление лекарств с гибким расписанием
- 📆 Чеклист приема лекарств на сегодня
- ⏰ Умные напоминания (с повтором, snooze и кастомным временем)
- 🧠 Лимит лекарств для бесплатных пользователей
- 💳 Подписка с оплатой через Telegram Pay
- 👑 Панель администратора: статистика, CSV-экспорт, бан/разбан, продление подписки

---

## ⚙️ Быстрый старт

1. **Клонируйте репозиторий**

```bash
git clone https://github.com/yourname/med_reminder_bot.git
cd med_reminder_bot
```

2. **Создайте .env файл**

```bash
BOT_TOKEN=your_telegram_bot_token
PAYMENT_PROVIDER_TOKEN=your_payment_token
ADMIN_IDS=123456789
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=123
DB_NAME=med
```

3. **Установите зависимости**

pip install -r requirements.txt

4. **Запустите бота**

python bot.py

---

## 🧪 Технологии

Python 3.10+

Aiogram 3

SQLAlchemy

Alembic

PostgreSQL

APScheduler

[dotenv, pydantic, asyncio]


## 👩‍💻 Админка

Администраторы (по ID из .env) получают доступ к панели управления:

Статистика (кол-во пользователей, премиумов, доход)

Блокировка и разблокировка пользователей

Продление подписок

Экспорт CSV с данными пользователей

## 📂 Миграции

alembic upgrade head
Для генерации новой миграции:

alembic revision --autogenerate -m "add new_table"
        
