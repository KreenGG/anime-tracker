import logging
from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database import Base, get_session
from src.main import create_app
from tests.utils.anime import create_bunch_anime

from .config import test_config
from .utils.user import TEST_USER, create_bunch_users

logger = logging.getLogger(__name__)

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


@pytest.fixture(scope="session", autouse=True)
async def fill_tables():
    async with async_session_maker() as session:
        await create_bunch_anime(session)
        await create_bunch_users(session)


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

    app = create_app()
    app.dependency_overrides[get_session] = override_get_db
    return app


@pytest.fixture
async def ac(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
async def auth_ac(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        url = app.url_path_for("login")

        response = await ac.post(
            url,
            json={
                "email": TEST_USER.email,
                "password": "test",
            },
        )

        access_token = str(response.json()["access_token"])
        assert access_token
        authorization = "Bearer " + access_token
        ac.headers["Authorization"] = authorization

        yield ac
