from datetime import datetime

from pydantic import BaseModel


class TopMedicationResponse(BaseModel):
    name: str
    users: int


class RecentUserResponse(BaseModel):
    id: int
    registered_ago: str
    meds_count: int


class AdminStatsResponse(BaseModel):
    total_users: int
    active_users: int
    avg_pills: float
    taken_rate: float
    dau: int
    new_today: int
    new_week: int
    new_month: int
    weekly_registrations: list[int]
    recent_users: list[RecentUserResponse]
    top_medications: list[TopMedicationResponse]


class AdminUserResponse(BaseModel):
    id: int
    telegram_id: int
    language: str
    is_blocked: bool
    created_at: datetime | None = None
    last_active: datetime | None = None

    model_config = {"from_attributes": True}


class AdminUserListResponse(BaseModel):
    users: list[AdminUserResponse]
    total: int


class AdminBanRequest(BaseModel):
    telegram_id: int


class AdminLogResponse(BaseModel):
    id: int
    admin_id: int
    action: str
    details: str | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class AdminLogListResponse(BaseModel):
    logs: list[AdminLogResponse]
    count: int
