from datetime import datetime

from pydantic import BaseModel, Field

from src.models.user_rate import Status


class UserRateCreate(BaseModel):
    user_id: int
    anime_id: int
    status: Status
    score: int = Field(default=0, ge=0, le=10)
    rewatches: int = Field(default=0, ge=0)
    episodes: int = Field(default=0, ge=0)
    text: str | None = None


class UserRateGet(BaseModel):
    id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
