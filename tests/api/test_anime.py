import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.anime import create_anime


async def test_get_all_anime(
    ac: AsyncClient,
) -> None:
    response = await ac.get("/api/anime")

    assert response.status_code == 200

    default_limit = 50

    assert len(response.json()["data"]) == default_limit


@pytest.mark.parametrize("limit", [10, 20])
async def test_get_all_anime_with_limit(
    ac: AsyncClient,
    limit: int,
) -> None:
    response = await ac.get(f"/api/anime?limit={limit}")

    assert response.status_code == 200
    assert len(response.json()["data"]) == limit


async def test_get_all_anime_with_limit_zero(
    ac: AsyncClient,
) -> None:
    response = await ac.get("/api/anime?limit=0")

    assert response.status_code == 404


@pytest.mark.parametrize("offset", [0, 10, 20])
async def test_get_all_anime_with_offset(
    ac: AsyncClient,
    offset: int,
) -> None:
    response = await ac.get(f"/api/anime?offset={offset}")
    assert response.status_code == 200

    first_anime = response.json()["data"][0]
    expected_id = offset + 1

    assert first_anime["id"] == expected_id


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
    offset: int,
    limit: int,
) -> None:
    response = await ac.get(f"/api/anime?offset={offset}&limit={limit}")
    assert response.status_code == 200

    json_anime_list = response.json()["data"]
    expected_id = offset + 1

    assert json_anime_list[0]["id"] == expected_id
    assert len(json_anime_list) == limit


async def test_get_anime_by_id(ac: AsyncClient, db_session: AsyncSession) -> None:
    anime = await create_anime(db_session)
    response = await ac.get(f"/api/anime/{anime.id}")

    assert response.status_code == 200

    anime_json = response.json()["data"]

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
) -> None:
    response = await ac.get("/api/anime/100000")

    assert response.status_code == 404
