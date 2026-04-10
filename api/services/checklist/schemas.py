from datetime import date, datetime

from pydantic import BaseModel


class ChecklistItemResponse(BaseModel):
    id: int
    medication_id: int
    medication_name: str
    medication_time: str
    schedule: str
    date: date
    status: bool
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


class ChecklistResponse(BaseModel):
    items: list[ChecklistItemResponse]
    date: date
    total: int
    taken: int


class ChecklistMarkRequest(BaseModel):
    status: bool = True
