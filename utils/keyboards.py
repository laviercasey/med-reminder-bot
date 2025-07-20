from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.localization import get_text
from datetime import datetime, time


def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language:ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="language:en")
    )
    return builder.as_markup()


def get_settings_keyboard(language: str) -> InlineKeyboardMarkup:
    """Get keyboard for settings menu"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text="🌐 " + get_text("change_language", language, default="Change language"),
            callback_data="settings:language"
        ),
        InlineKeyboardButton(
            text="⏰ " + get_text("reminder_settings", language),
            callback_data="settings:reminders"
        )
    )
    
    builder.adjust(1)
    return builder.as_markup()

def get_main_menu_keyboard(language: str) -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=get_text("add_pill", language))],
        [KeyboardButton(text=get_text("today_pills", language)), KeyboardButton(text=get_text("my_medications", language))],
        [KeyboardButton(text=get_text("settings", language)), KeyboardButton(text=get_text("subscription", language))]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_schedule_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=get_text("morning", language), callback_data="schedule:morning"),
        InlineKeyboardButton(text=get_text("day", language), callback_data="schedule:day"),
        InlineKeyboardButton(text=get_text("evening", language), callback_data="schedule:evening"),
        InlineKeyboardButton(text=get_text("custom_time", language), callback_data="schedule:custom")
    )
    builder.adjust(2)
    return builder.as_markup()

def get_time_keyboard(schedule: str, language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if schedule == "morning":
        times = ["06:00", "07:00", "08:00", "09:00"]
    elif schedule == "day":
        times = ["12:00", "13:00", "14:00", "15:00"]
    elif schedule == "evening":
        times = ["18:00", "19:00", "20:00", "21:00"]
    else:
        return InlineKeyboardMarkup()
    
    for t in times:
        builder.add(InlineKeyboardButton(text=t, callback_data=f"time:{t}"))
    
    builder.adjust(2)
    return builder.as_markup()

def get_checklist_keyboard(pill_id: int, language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=get_text("mark_as_taken", language),
            callback_data=f"mark_taken:{pill_id}"
        )
    )
    return builder.as_markup()

def get_subscription_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=get_text("monthly_plan", language), callback_data="subscribe:monthly"),
        InlineKeyboardButton(text=get_text("yearly_plan", language), callback_data="subscribe:yearly"),
        InlineKeyboardButton(text=get_text("lifetime_plan_purchase", language), callback_data="subscribe:lifetime")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_admin_keyboard(language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=get_text("admin_stats", language), callback_data="admin:stats"),
        InlineKeyboardButton(text=get_text("admin_users", language), callback_data="admin:users"),
        InlineKeyboardButton(text=get_text("admin_logs", language), callback_data="admin:logs")
    )
    builder.adjust(1)
    return builder.as_markup()

def get_admin_users_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Ban User", callback_data="admin:ban"),
        InlineKeyboardButton(text="Unban User", callback_data="admin:unban"),
        InlineKeyboardButton(text="Extend Subscription", callback_data="admin:extend")
    )
    builder.adjust(1)
    return builder.as_markup()


def get_reminder_settings_keyboard(language: str, reminders_enabled: bool) -> InlineKeyboardMarkup:
    """Get keyboard for reminder settings"""
    builder = InlineKeyboardBuilder()
    
    if reminders_enabled:
        builder.add(InlineKeyboardButton(
            text=get_text("disable_reminders", language),
            callback_data="reminder_settings:disable"
        ))
    else:
        builder.add(InlineKeyboardButton(
            text=get_text("enable_reminders", language),
            callback_data="reminder_settings:enable"
        ))
    
    builder.add(
        InlineKeyboardButton(
            text=get_text("5_minutes", language),
            callback_data="reminder_repeat:5"
        ),
        InlineKeyboardButton(
            text=get_text("15_minutes", language),
            callback_data="reminder_repeat:15"
        ),
        InlineKeyboardButton(
            text=get_text("30_minutes", language),
            callback_data="reminder_repeat:30"
        )
    )
    
    builder.adjust(1, 3)
    return builder.as_markup()

def get_reminder_action_keyboard(checklist_id: int, language: str) -> InlineKeyboardMarkup:
    """Get keyboard for reminder actions"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text=get_text("take_now", language),
            callback_data=f"mark_taken:{checklist_id}"
        ),
        InlineKeyboardButton(
            text=get_text("snooze", language),
            callback_data=f"snooze:{checklist_id}"
        ),
        InlineKeyboardButton(
            text=get_text("disable_this_reminder", language),
            callback_data=f"disable_reminder:{checklist_id}"
        )
    )
    
    builder.adjust(2, 1)
    return builder.as_markup()

def get_snooze_options_keyboard(checklist_id: int, language: str) -> InlineKeyboardMarkup:
    """Get keyboard for snooze options"""
    builder = InlineKeyboardBuilder()
    
    builder.add(
        InlineKeyboardButton(
            text=get_text("5_minutes", language),
            callback_data=f"snooze:{checklist_id}:5"
        ),
        InlineKeyboardButton(
            text=get_text("15_minutes", language),
            callback_data=f"snooze:{checklist_id}:15"
        ),
        InlineKeyboardButton(
            text=get_text("30_minutes", language),
            callback_data=f"snooze:{checklist_id}:30"
        )
    )
    
    builder.adjust(3)
    return builder.as_markup()
