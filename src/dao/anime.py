from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.anime import Anime


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

    # FIXME возможно не пригодится
    # async def get_single_by_id(self, id: int) -> Anime | None:
    #     stmt = select(Anime).where(Anime.id == id)
    #     result = await self.session.execute(stmt)
    #     anime_db = result.scalars().first()
    #     if not anime_db:
    #         return None
    #     return anime_db

    async def get_single(self, **kwargs) -> Anime | None:
        stmt = select(Anime).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        anime_db = result.scalars().first()
        if not anime_db:
            return None
        return anime_db
