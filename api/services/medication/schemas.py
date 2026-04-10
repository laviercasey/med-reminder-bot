from datetime import datetime, time

from pydantic import BaseModel, Field


class MedicationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    schedule: str = Field(..., pattern="^(morning|day|evening|custom)$")
    time: time


class MedicationUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    schedule: str = Field(..., pattern="^(morning|day|evening|custom)$")
    time: time


class MedicationResponse(BaseModel):
    id: int
    name: str
    schedule: str
    time: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class MedicationListResponse(BaseModel):
    medications: list[MedicationResponse]
    count: int
