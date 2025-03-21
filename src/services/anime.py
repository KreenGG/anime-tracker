import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.anime import AnimeDAO
from src.schemas.anime import Anime

logger = logging.getLogger(__name__)


class AnimeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.anime_dao = AnimeDAO(self.session)

    async def get_all(
        self,
        search: str,
        offset: int,
        limit: int,
    ) -> list[Anime] | None:
        animes_db = await self.anime_dao.get_all(
            search=search,
            offset=offset,
            limit=limit,
        )
        if not animes_db:
            return None
        animes = [Anime.model_validate(anime) for anime in animes_db]
        return animes

    async def get_single_by_id(self, id: int) -> Anime | None:
        anime_db = await self.anime_dao.get_single_or_none(id=id)
        if not anime_db:
            return None
        anime = Anime.model_validate(anime_db)
        return anime
