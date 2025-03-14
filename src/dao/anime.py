import logging
from collections.abc import Sequence

from sqlalchemy import select
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
        offset: int,
        limit: int,
    ) -> Sequence[Anime] | None:
        stmt = select(Anime).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        animes = result.scalars().all()
        if not animes:
            return None
        return animes

    async def get_single(self, **kwargs) -> Anime | None:
        logger.debug("Getting anime by: %s", kwargs)
        stmt = select(Anime).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        anime_db = result.scalars().first()
        if not anime_db:
            return None
        return anime_db
