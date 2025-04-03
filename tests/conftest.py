import logging
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import sqlalchemy as sa
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import Config
from src.config import config as app_config
from src.main import create_app
from tests.utils.anime import create_bunch_anime

from .utils.user import TEST_USER, create_bunch_users

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def config() -> Config:
    return app_config


@pytest.fixture(scope="session", autouse=True)
async def async_engine(config: Config) -> AsyncGenerator[AsyncEngine, Any]:
    """Создает тестовую БД"""

    test_db_name = config.db.test_postgres_db

    assert "test_" in test_db_name, "try to create/drop production db"

    engine_for_create_db = create_async_engine(
        config.db.url(testing=True),
        isolation_level="AUTOCOMMIT",
    )

    connection_for_create_test_db = await engine_for_create_db.connect()
    engine_with_test_db = None

    try:
        is_test_db_exists = await connection_for_create_test_db.execute(
            sa.text(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}';"),
        )

        if not is_test_db_exists.one_or_none():
            await connection_for_create_test_db.execute(
                sa.text(f'CREATE DATABASE "{test_db_name}";')
            )

        engine_with_test_db = create_async_engine(
            config.db.test_postgres_url,
            # poolclass нужен чтобы избежать
            # RuntimeError Task attached to a different loop
            poolclass=NullPool,
        )

        yield engine_with_test_db

    finally:
        if engine_for_create_db:
            await engine_for_create_db.dispose()

        await connection_for_create_test_db.close()


@pytest.fixture(scope="session", autouse=True)
async def create_tables(async_engine: AsyncEngine):
    from src.database import Base

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="session")
async def async_session_maker(async_engine):
    return async_sessionmaker(
        async_engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )


@pytest.fixture(scope="session", autouse=True)
async def fill_tables(async_session_maker):
    async with async_session_maker() as session:
        await create_bunch_anime(session)
        await create_bunch_users(session)


@pytest.fixture(scope="session")
async def db_session(async_session_maker):
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def app(db_session: AsyncSession) -> FastAPI:
    from src.database import get_session

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
