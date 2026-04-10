import json

from redis.asyncio import Redis


class RedisPublisher:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def publish(self, channel: str, data: dict) -> int:
        message = json.dumps(data, default=str)
        return await self._redis.publish(channel, message)

    async def publish_medication_created(self, user_id: int, medication_id: int) -> int:
        return await self.publish(
            "medications",
            {
                "event": "medication_created",
                "user_id": user_id,
                "medication_id": medication_id,
            },
        )

    async def publish_medication_updated(self, user_id: int, medication_id: int) -> int:
        return await self.publish(
            "medications",
            {
                "event": "medication_updated",
                "user_id": user_id,
                "medication_id": medication_id,
            },
        )

    async def publish_medication_deleted(self, user_id: int, medication_id: int) -> int:
        return await self.publish(
            "medications",
            {
                "event": "medication_deleted",
                "user_id": user_id,
                "medication_id": medication_id,
            },
        )
