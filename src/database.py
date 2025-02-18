from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config import config

SQLALCHEMY_DATABASE_URL = config.db.url
DATABASE_PARAMS = {
    "echo": config.db.echo,
}

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, **DATABASE_PARAMS,
)


class Base(DeclarativeBase):
    pass


async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
