import logging
from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import test_config
from src.database import Base, get_session
from src.main import create_app

logger = logging.getLogger(__name__)

# Подключаю фикстуры из стороннего пакета
pytest_plugins = ("mocks",)

SQLALCHEMY_DATABASE_URL = test_config.url
logger.debug("Testing database url=%s", SQLALCHEMY_DATABASE_URL)

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    # poolclass нужен чтобы избежать RuntimeError Task attached to a different loop
    poolclass=NullPool,
)
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="session")
async def db_session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def app(db_session) -> FastAPI:
    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    main_app = create_app()
    main_app.dependency_overrides[get_session] = override_get_db
    return main_app


@pytest.fixture(scope="function")
async def ac(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
