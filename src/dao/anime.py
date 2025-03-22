import logging
from collections.abc import Sequence

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.anime import Anime

logger = logging.getLogger(__name__)


class AnimeDAO:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_all(
        self,
        search: str = "",
        offset: int = 0,
        limit: int = 50,
    ) -> Sequence[Anime]:
        stmt = (
            select(Anime)
            .filter(
                or_(
                    Anime.english.ilike(f"%{search}%"),
                    Anime.russian.ilike(f"%{search}%"),
                    Anime.name.ilike(f"%{search}%"),
                    Anime.japanese.ilike(f"%{search}%"),
                )
            )
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        animes = result.scalars().all()
        return animes

    async def get_single_or_none(self, **kwargs) -> Anime | None:
        logger.debug("Getting anime by: %s", kwargs)
        stmt = select(Anime).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        anime_db = result.scalars().first()
        if not anime_db:
            return None
        return anime_db
