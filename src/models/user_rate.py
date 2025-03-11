from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.anime import Anime
    from src.models.user import User


class Status(Enum):
    planned = "planned"
    watching = "watching"
    completed = "completed"
    on_hold = "on_hold"
    dropped = "dropped"
    rewatching = "rewatching"


class UserRate(Base):
    __tablename__ = "user_rate"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    user: Mapped["User"] = relationship(back_populates="user_rates")

    anime_id: Mapped[int] = mapped_column(
        ForeignKey("anime.id", ondelete="CASCADE"), nullable=False
    )
    # ? Не знаю как это влияет на запросы, возможно это стоит убрать
    # ? Оно может брать все отзывы для аниме, и если их будут тысячи,
    # ? может работать медленно
    anime: Mapped["Anime"] = relationship(back_populates="user_rates")

    score: Mapped[int] = mapped_column(default=0, nullable=False)
    status: Mapped["Status"] = mapped_column(default=Status.planned, nullable=False)
    rewatches: Mapped[int] = mapped_column(default=0, nullable=False)
    episodes: Mapped[int] = mapped_column(default=0, nullable=False)
    text: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
        onupdate=datetime.now(UTC),
    )
