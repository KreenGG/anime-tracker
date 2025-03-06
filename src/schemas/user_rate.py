from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Status(Enum):
    planned = "planned"
    watching = "watching"
    completed = "completed"
    on_hold = "on_hold"
    dropped = "dropped"
    rewatching = "rewatching"

class UserRate(BaseModel):
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
