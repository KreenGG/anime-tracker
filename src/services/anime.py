import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.anime import Anime as AnimeModel
from src.schemas.anime import Anime

logger = logging.getLogger(__name__)


class AnimeService:
    async def get_all(
        self,
        session: AsyncSession,
        offset: int = 0,
        limit: int = 10,
    ) -> list[Anime] | None:
        stmt = select(AnimeModel).offset(offset).limit(limit)
        result = await session.execute(stmt)
        animes = result.scalars().all()
        if not animes:
            return None
        animes = [Anime.model_validate(anime) for anime in animes]
        return animes

    async def get_single(self, session: AsyncSession, id: int) -> Anime | None:
        stmt = select(AnimeModel).where(AnimeModel.id == id)
        result = await session.execute(stmt)
        anime = result.scalars().first()
        if not anime:
            return None
        anime = Anime.model_validate(anime)
        return anime
