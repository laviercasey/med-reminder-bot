from datetime import datetime

from pydantic import BaseModel, Field


class SettingsResponse(BaseModel):
    reminders_enabled: bool
    reminder_repeat_minutes: int
    language: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class SettingsUpdateRequest(BaseModel):
    reminders_enabled: bool | None = None
    reminder_repeat_minutes: int | None = Field(None, ge=1, le=60)
    language: str | None = Field(None, pattern="^(en|ru)$")
