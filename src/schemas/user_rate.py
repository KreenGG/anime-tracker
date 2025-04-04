from datetime import datetime

from pydantic import BaseModel, Field

from src.models.user_rate import Status


class UserRateCreate(BaseModel):
    anime_id: int
    status: Status
    score: int = Field(default=0, ge=0, le=10)
    rewatches: int = Field(default=0, ge=0)
    episodes: int = Field(default=0, ge=0)
    text: str | None = None


class UserRateGet(UserRateCreate):
    id: int
    user_id: int

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserRateUpdate(BaseModel):
    anime_id: int | None = None
    status: Status | None = None
    score: int | None = Field(default=None, ge=0, le=10)
    rewatches: int | None = Field(default=None, ge=0)
    episodes: int | None = Field(default=None, ge=0)
    text: str | None = None
