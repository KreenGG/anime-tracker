from fastapi import FastAPI
from httpx import AsyncClient

from src.models.user import User
from tests.factories.anime import AnimeFactory
from tests.factories.user import UserFactory
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


async def test_create_user_rate_anime_not_found(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    anime = await anime_factory.create_anime()
    user_rate = user_rate_factory.generate_user_rate(anime)

    body = {
        "anime_id": user_rate.anime_id + 1,
        "status": user_rate.status.value,
        "score": user_rate.score,
        "rewatches": user_rate.rewatches,
        "episodes": user_rate.episodes,
        "text": user_rate.text,
    }

    url = app.url_path_for("create_user_rate")
    response = await auth_ac.post(url, json=body)
    assert response.status_code == 400


async def test_create_user_rate_already_exists(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    anime = await anime_factory.create_anime()
    user_rate = await user_rate_factory.create_user_rate(user, anime)
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
    assert response.status_code == 409


async def test_update_user_rate(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    anime = await anime_factory.create_anime()
    user_rate = await user_rate_factory.create_user_rate(user, anime)
    body = {
        "status": "planned",
        "score": 7,
        "rewatches": 2,
        "episodes": 12,
        "text": "Not bad",
    }

    url = app.url_path_for("update_user_rate", id=user_rate.id)
    response = await auth_ac.patch(url, json=body)
    assert response.status_code == 200


async def test_update_user_rate_single_field(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    anime = await anime_factory.create_anime()
    user_rate = await user_rate_factory.create_user_rate(user, anime)
    rewatches = user_rate.rewatches
    body = {
        "rewatches": user_rate.rewatches + 1,
    }

    url = app.url_path_for("update_user_rate", id=user_rate.id)
    response = await auth_ac.patch(url, json=body)
    assert response.status_code == 200

    assert response.json()["rewatches"] == rewatches + 1
    assert response.json()["text"] == user_rate.text


async def test_update_user_rate_not_found(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_factory: UserFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    anime = await anime_factory.create_anime()
    other_user = await user_factory.create_user("fdf")
    user_rate = await user_rate_factory.create_user_rate(other_user, anime)

    body = {
        "rewatches": 12,
    }

    url = app.url_path_for("update_user_rate", id=user_rate.id)
    response = await auth_ac.patch(url, json=body)
    assert response.status_code == 403


async def test_update_user_rate_forbidden(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user
    body = {
        "rewatches": 12,
    }

    url = app.url_path_for("update_user_rate", id=101)
    response = await auth_ac.patch(url, json=body)
    assert response.status_code == 400


async def test_delete_user_rate(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    anime = await anime_factory.create_anime()
    user_rate = await user_rate_factory.create_user_rate(user, anime)

    url = app.url_path_for("delete_user_rate", id=user_rate.id)
    response = await auth_ac.delete(url)
    assert response.status_code == 204


async def test_delete_user_rate_not_found(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    url = app.url_path_for("delete_user_rate", id=100)
    response = await auth_ac.delete(url)
    assert response.status_code == 400


async def test_delete_user_rate_forbidden(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    anime_factory: AnimeFactory,
    user_factory: UserFactory,
    user_rate_factory: UserRateFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    # Simulate another user
    other_user = await user_factory.create_user("qwe")

    anime = await anime_factory.create_anime()
    user_rate = await user_rate_factory.create_user_rate(other_user, anime)

    url = app.url_path_for("delete_user_rate", id=user_rate.id)
    response = await auth_ac.delete(url)
    assert response.status_code == 403
