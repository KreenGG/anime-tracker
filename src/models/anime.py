from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Anime(Base):
    __tablename__ = "anime"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    russian: Mapped[str] = mapped_column(nullable=True)
    english: Mapped[str] = mapped_column(nullable=True)
    japanese: Mapped[str] = mapped_column(nullable=True)
    episodes: Mapped[int] = mapped_column(nullable=True)
    episodes_aired: Mapped[int] = mapped_column(nullable=True)
    duration: Mapped[int] = mapped_column(nullable=True)
    poster: Mapped[str] = mapped_column(nullable=True)  # Буду брать тупо jpeg
    # Жанры можно прикрутить позже
    description: Mapped[str] = mapped_column(nullable=True)
    description_html: Mapped[str] = mapped_column(nullable=True)
    description_source: Mapped[str] = mapped_column(nullable=True)
