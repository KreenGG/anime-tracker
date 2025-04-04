from fastapi import FastAPI
from httpx import AsyncClient

from src.models.user import User
from tests.factories.anime import AnimeFactory
from tests.factories.user_rate import UserRateFactory


async def test_get_user_rates(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user
    anime = await anime_factory.create_anime()
    user_rate = await user_rate_factory.create_user_rate(
        user,
        anime,
    )

    url = app.url_path_for("get_user_rates")
    response = await auth_ac.get(url)
    assert response.status_code == 200

    response_json = response.json()["data"]
    assert len(response_json) == 1

    assert response_json[0]["anime_id"] == anime.id
    assert response_json[0]["status"] == user_rate.status.value


async def test_create_user_rate(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    anime = await anime_factory.create_anime()
    user_rate = user_rate_factory.generate_user_rate(anime)

    body = {
        "anime_id": user_rate.anime_id,
        "status": user_rate.status.value,
        "score": user_rate.score,
        "rewatches": user_rate.rewatches,
        "episodes": user_rate.episodes,
        "text": user_rate.text,
    }

    url = app.url_path_for("create_user_rate")
    response = await auth_ac.post(url, json=body)
    assert response.status_code == 201
    assert response.json()["anime_id"] == anime.id
    assert response.json()["status"] == user_rate.status.value
