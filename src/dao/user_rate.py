import logging
from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.models.user_rate import UserRate
from src.schemas.user import UserDTO
from src.schemas.user_rate import UserRateCreate

logger = logging.getLogger(__name__)


class UserRateDAO:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_all(self, user_id: int) -> Sequence[UserRate] | None:
        stmt = select(UserRate).join(User).where(User.id == user_id)
        result = await self.session.execute(stmt)

        user_rates = result.scalars().all()
        return user_rates

    async def get_single_or_none(self, **kwargs) -> UserRate | None:
        stmt = select(UserRate).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        user_rate = result.scalars().first()
        return user_rate

    async def create(self, user_rate_in: UserRateCreate, user: UserDTO) -> UserRate:
        user_rate = UserRate(user_id=user.id, **user_rate_in.model_dump())

        self.session.add(user_rate)
        return user_rate

    async def delete(self, id: int) -> None:
        stmt = delete(UserRate).where(UserRate.id == id)
        await self.session.execute(stmt)
