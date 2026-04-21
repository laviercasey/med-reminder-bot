import asyncio
import json
import logging

from aiogram import Bot
from redis.asyncio import Redis

from shared.config import settings

logger = logging.getLogger("med_reminder_bot")


class RedisPubSubListener:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._redis: Redis | None = None
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        self._redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        self._running = True
        pubsub = self._redis.pubsub()
        await pubsub.subscribe("medications")
        logger.info("Redis pub/sub listener started on channel: medications")

        self._task = asyncio.create_task(self._listen(pubsub))

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        if self._redis:
            await self._redis.aclose()

    async def _listen(self, pubsub) -> None:
        try:
            while self._running:
                message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
                if message is None:
                    await asyncio.sleep(0.1)
                    continue

                channel = message.get("channel", "")
                data_raw = message.get("data")

                if not isinstance(data_raw, str):
                    continue

                try:
                    data = json.loads(data_raw)
                except (json.JSONDecodeError, TypeError):
                    logger.warning("Invalid JSON on channel %s: %s", channel, data_raw)
                    continue

                if channel == "medications":
                    await self._handle_medication_event(data)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error("Pub/sub listener error: %s", e, exc_info=e)
        finally:
            await pubsub.unsubscribe()

    async def _handle_medication_event(self, data: dict) -> None:
        event = data.get("event", "")
        if event in ("medication_created", "medication_updated", "medication_deleted"):
            logger.info("Medication changed, refreshing scheduler")
            from bot.services.reminders import setup_medication_reminders

            await setup_medication_reminders(self._bot)
