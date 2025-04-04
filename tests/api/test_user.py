from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient

from src.models.user import User
from tests.factories.user import UserFactory


async def test_get_current_user(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
) -> None:
    auth_ac, user = auth_ac_and_user

    url = app.url_path_for("get_current_user")
    response = await auth_ac.get(url)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == user.id
    assert response_json["email"] == user.email
    assert response_json["nickname"] == user.nickname


async def test_update_user_no_changes(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    user_factory: UserFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    body: dict[str, Any] = {}
    url = app.url_path_for("update_user")
    response = await auth_ac.patch(url, json=body)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == user.id
    assert response_json["email"] == user.email
    assert response_json["nickname"] == user.nickname


async def test_update_user_nickname(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    user_factory: UserFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    nickname = "new_nickname"

    body = {"nickname": nickname}
    url = app.url_path_for("update_user")
    response = await auth_ac.patch(url, json=body)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["nickname"] == nickname
    user.nickname = nickname


async def test_update_user_bad_nickname(
    auth_ac_and_user: tuple[AsyncClient, User],
    app: FastAPI,
    user_factory: UserFactory,
) -> None:
    auth_ac, user = auth_ac_and_user

    nickname = "nw"

    body = {"nickname": nickname}
    url = app.url_path_for("update_user")
    response = await auth_ac.patch(url, json=body)

    assert response.status_code == 422
