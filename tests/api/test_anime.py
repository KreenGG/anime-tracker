import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.anime import create_anime


async def test_get_all_anime(
    ac: AsyncClient,
    app: FastAPI,
) -> None:
    url = app.url_path_for("get_animes")
    response = await ac.get(url)

    assert response.status_code == 200

    default_limit = 50

    assert len(response.json()["data"]) == default_limit


@pytest.mark.parametrize("limit", [10, 20])
async def test_get_all_anime_with_limit(
    ac: AsyncClient,
    app: FastAPI,
    limit: int,
) -> None:
    url = app.url_path_for("get_animes")
    response = await ac.get(f"{url}?limit={limit}")

    assert response.status_code == 200
    assert len(response.json()["data"]) == limit


async def test_get_all_anime_with_limit_zero(
    ac: AsyncClient,
    app: FastAPI,
) -> None:
    url = app.url_path_for("get_animes")
    response = await ac.get(f"{url}?limit=0")

    assert response.status_code == 404


@pytest.mark.parametrize("offset", [0, 10, 20])
async def test_get_all_anime_with_offset(
    ac: AsyncClient,
    app: FastAPI,
    offset: int,
) -> None:
    url = app.url_path_for("get_animes")
    response = await ac.get(f"{url}?offset={offset}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "offset,limit",
    [
        (0, 10),
        (10, 20),
        (20, 10),
    ],
)
async def test_get_all_anime_with_offset_and_limit(
    ac: AsyncClient,
    app: FastAPI,
    offset: int,
    limit: int,
) -> None:
    url = app.url_path_for("get_animes")
    response = await ac.get(f"{url}?offset={offset}&limit={limit}")
    assert response.status_code == 200

    json_anime_list = response.json()["data"]

    assert len(json_anime_list) == limit


async def test_get_anime_by_id(
    ac: AsyncClient, app: FastAPI, db_session: AsyncSession
) -> None:
    anime = await create_anime(db_session)

    url = app.url_path_for("get_single_anime", id=anime.id)
    response = await ac.get(url)

    assert response.status_code == 200

    anime_json = response.json()

    assert anime_json["id"] == anime.id
    assert anime_json["name"] == anime.name
    assert anime_json["russian"] == anime.russian
    assert anime_json["english"] == anime.english
    assert anime_json["japanese"] == anime.japanese
    assert anime_json["episodes"] == anime.episodes
    assert anime_json["episodes_aired"] == anime.episodes_aired
    assert anime_json["duration"] == anime.duration
    assert anime_json["poster"] == anime.poster


async def test_get_anime_by_id_not_found(
    ac: AsyncClient,
    app: FastAPI,
) -> None:
    url = app.url_path_for("get_single_anime", id=100000)

    response = await ac.get(url)

    assert response.status_code == 404
