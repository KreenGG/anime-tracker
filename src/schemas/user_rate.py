from datetime import datetime

from pydantic import BaseModel, Field

from src.models.user_rate import Status


class UserRateRead(BaseModel):
    id: int
    user_id: int
    anime_id: int
    score: int = Field(default=0, ge=0, le=10)
    status: Status
    rewatches: int = Field(default=0, ge=0)
    episodes: int = Field(default=0, ge=0)
    text: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
