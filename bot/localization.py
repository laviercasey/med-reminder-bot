from typing import Any

TEXTS = {
    "ru": {
        "welcome": (
            "Добро пожаловать в МедНапоминалку!"
            " Я буду помогать вам не забывать принимать лекарства вовремя."
        ),
        "language_selected": "Вы выбрали русский язык.",
        "select_language": "Выберите язык / Select language:",
        "user_blocked": (
            "Вы были заблокированы администратором."
            " Обратитесь в поддержку для выяснения причин."
        ),
        "reminder": "Напоминание: Пора принять {name}!",
        "reminder_repeat": "Напоминаю: Вы ещё не отметили приём лекарства {name}!",
        "take_now": "Принять сейчас",
        "snooze": "Отложить",
        "disable_this_reminder": "Отключить это напоминание",
        "reminder_disabled": "Напоминание отключено",
        "snoozed_for": "Напоминание отложено на {minutes} минут",
        "5_minutes": "5 минут",
        "15_minutes": "15 минут",
        "30_minutes": "30 минут",
        "select_snooze_time": "Выберите время отложки:",
        "mark_as_taken": "✅ Принято",
        "marked_as_taken": "Отмечено как принято: {name}",
        "open_app": "Открыть приложение",
        "error": "Произошла ошибка",
    },
    "en": {
        "welcome": (
            "Welcome to MedReminder!"
            " I will help you remember to take your medications on time."
        ),
        "language_selected": "You have selected English language.",
        "select_language": "Select language / Выберите язык:",
        "user_blocked": (
            "You have been blocked by the administrator."
            " Please contact support for more information."
        ),
        "reminder": "Reminder: Time to take {name}!",
        "reminder_repeat": "Reminder: You haven't marked {name} as taken yet!",
        "take_now": "Take now",
        "snooze": "Snooze",
        "disable_this_reminder": "Disable this reminder",
        "reminder_disabled": "Reminder disabled",
        "snoozed_for": "Reminder snoozed for {minutes} minutes",
        "5_minutes": "5 minutes",
        "15_minutes": "15 minutes",
        "30_minutes": "30 minutes",
        "select_snooze_time": "Select snooze time:",
        "mark_as_taken": "✅ Taken",
        "marked_as_taken": "Marked as taken: {name}",
        "open_app": "Open App",
        "error": "Error occurred",
    },
}


def get_text(key: str, language: str, **kwargs: Any) -> str:
    language = language if language in TEXTS else "en"
    text = TEXTS[language].get(key, TEXTS["en"].get(key, f"Missing text for: {key}"))
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text
