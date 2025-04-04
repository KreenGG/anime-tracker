from logging import getLogger

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.anime import AnimeDAO
from src.dao.user_rate import UserRateDAO
from src.exceptions.base import AlreadyExistsError, ForbiddenError, NotFoundError
from src.schemas.user import UserDTO
from src.schemas.user_rate import UserRateCreate, UserRateGet, UserRateUpdate

logger = getLogger(__name__)


class UserRateService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_rate_dao = UserRateDAO(self.session)
        self.anime_dao = AnimeDAO(self.session)

    async def get_all(self, user_id: int) -> list[UserRateGet]:
        user_rates = await self.user_rate_dao.get_all(user_id)
        if not user_rates:
            return []

        return [UserRateGet.model_validate(user_rate) for user_rate in user_rates]

    async def create(self, user_rate_in: UserRateCreate, user: UserDTO) -> UserRateGet:
        anime = await self.anime_dao.get_single_or_none(id=user_rate_in.anime_id)
        if not anime:
            raise NotFoundError(f"Anime with id={user_rate_in.anime_id} not found")

        existing_user_rate = await self.user_rate_dao.get_single_or_none(
            anime_id=user_rate_in.anime_id, user_id=user.id
        )
        if existing_user_rate:
            raise AlreadyExistsError(
                detail=(
                    f"User rate for {user_rate_in.anime_id=} and "
                    + f"{user.id=} already exists"
                )
            )

        user_rate = await self.user_rate_dao.create(user_rate_in, user)

        await self.session.commit()
        await self.session.refresh(user_rate)

        return UserRateGet.model_validate(user_rate)

    async def update(
        self, user_id: int, user_rate_id: int, update_data: UserRateUpdate
    ) -> UserRateGet:
        user_rate = await self.user_rate_dao.get_single_or_none(id=user_rate_id)
        if not user_rate:
            raise NotFoundError(
                detail=f"User rate id={user_rate_id} not found",
            )
        if user_rate.user_id != user_id:
            raise ForbiddenError()
        data_to_update = update_data.model_dump(exclude_unset=True)
        updated_user_rate = await self.user_rate_dao.update(user_rate, data_to_update)
        await self.session.commit()
        await self.session.refresh(updated_user_rate)
        return updated_user_rate

    async def delete(self, user_id: int, user_rate_id: int) -> None:
        user_rate = await self.user_rate_dao.get_single_or_none(id=user_rate_id)
        if not user_rate:
            raise NotFoundError(
                detail=f"User rate id={user_rate_id} not found",
            )
        if user_rate.user_id != user_id:
            raise ForbiddenError()
        await self.user_rate_dao.delete(user_rate_id)
        await self.session.commit()
        logger.debug("User rate id=%d deleted", user_rate_id)
