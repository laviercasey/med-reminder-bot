from datetime import datetime

from pydantic import BaseModel


class UserProfileResponse(BaseModel):
    id: int
    telegram_id: int
    language: str
    is_admin: bool = False
    created_at: datetime | None = None
    last_active: datetime | None = None
    medications_count: int = 0

    model_config = {"from_attributes": True}
