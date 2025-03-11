import pytest
from httpx import AsyncClient


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
