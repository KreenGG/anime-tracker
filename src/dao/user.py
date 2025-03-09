import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User

logger = logging.getLogger(__name__)


class UserDAO:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_single(self, **kwargs) -> User | None:
        logger.debug("Getting user by: %s", kwargs)
        stmt = select(User).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if not user:
            return None
        return user

    async def create(self, user: User) -> None:
        self.session.add(user)
