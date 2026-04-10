from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.localization import get_text


def get_language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="language:ru"),
        InlineKeyboardButton(text="🇬🇧 English", callback_data="language:en"),
    )
    return builder.as_markup()


def get_reminder_action_keyboard(checklist_id: int, language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=get_text("take_now", language),
            callback_data=f"mark_taken:{checklist_id}",
        ),
        InlineKeyboardButton(
            text=get_text("snooze", language),
            callback_data=f"snooze:{checklist_id}",
        ),
        InlineKeyboardButton(
            text=get_text("disable_this_reminder", language),
            callback_data=f"disable_reminder:{checklist_id}",
        ),
    )
    builder.adjust(2, 1)
    return builder.as_markup()


def get_snooze_options_keyboard(checklist_id: int, language: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=get_text("5_minutes", language),
            callback_data=f"snooze:{checklist_id}:5",
        ),
        InlineKeyboardButton(
            text=get_text("15_minutes", language),
            callback_data=f"snooze:{checklist_id}:15",
        ),
        InlineKeyboardButton(
            text=get_text("30_minutes", language),
            callback_data=f"snooze:{checklist_id}:30",
        ),
    )
    builder.adjust(3)
    return builder.as_markup()
