import logging

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.repository import RecordNotFoundError
from src.models.user import User

logger = logging.getLogger(__name__)


class UserDAO:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_single(self, **kwargs) -> User:
        logger.debug("Getting user by: %s", kwargs)
        stmt = select(User).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise RecordNotFoundError
        return user

    async def create(self, user: User) -> None:
        self.session.add(user)

    async def is_already_exists(self, email: str, nickname: str) -> bool:
        stmt = select(User).filter(or_(User.email == email, User.nickname == nickname))
        result = await self.session.execute(stmt)
        user = result.scalars().first()
        if user:
            return True
        return False
