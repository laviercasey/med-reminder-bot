import logging
from typing import TYPE_CHECKING, Callable, Awaitable

from sqlalchemy.ext.asyncio import AsyncSession

from shared.database.models import NotificationOutbox
from shared.notifications.outbox_repository import OutboxRepository

if TYPE_CHECKING:
    from aiogram import Bot

logger = logging.getLogger("med_reminder_bot")

SendCallback = Callable[["Bot", NotificationOutbox, AsyncSession], Awaitable[None]]


async def process_outbox_entry(
    session: AsyncSession,
    bot: "Bot",
    entry: NotificationOutbox,
    send: SendCallback,
) -> None:
    repo = OutboxRepository(session)
    try:
        await send(bot, entry, session)
    except Exception as e:
        logger.error("Outbox entry %s send failed: %s", entry.id, e, exc_info=e)
        await repo.mark_failed(entry.id, str(e))
        return
    await repo.mark_sent(entry.id)
