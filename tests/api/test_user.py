from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient

from src.utils.auth import verify_token
from tests.factories.user import UserFactory


async def test_get_current_user(
    auth_ac: AsyncClient,
    app: FastAPI,
    user_factory: UserFactory,
) -> None:
    token = auth_ac.headers["authorization"].split()[1]
    payload = verify_token(token)
    print("jfsdflsds", payload)

    url = app.url_path_for("get_current_user")
    response = await auth_ac.get(url)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == user_factory.test_user.id
    assert response_json["email"] == user_factory.test_user.email
    assert response_json["nickname"] == user_factory.test_user.nickname


async def test_update_user_no_changes(
    auth_ac: AsyncClient,
    app: FastAPI,
    user_factory: UserFactory,
) -> None:
    body: dict[str, Any] = {}
    url = app.url_path_for("update_user")
    response = await auth_ac.patch(url, json=body)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == user_factory.test_user.id
    assert response_json["email"] == user_factory.test_user.email
    assert response_json["nickname"] == user_factory.test_user.nickname


async def test_update_user_nickname(
    auth_ac: AsyncClient,
    app: FastAPI,
    user_factory: UserFactory,
) -> None:
    nickname = "new_nickname"

    body = {"nickname": nickname}
    url = app.url_path_for("update_user")
    response = await auth_ac.patch(url, json=body)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["nickname"] == nickname
    user_factory.test_user.nickname = nickname


async def test_update_user_bad_nickname(
    auth_ac: AsyncClient,
    app: FastAPI,
    user_factory: UserFactory,
) -> None:
    nickname = "nw"

    body = {"nickname": nickname}
    url = app.url_path_for("update_user")
    response = await auth_ac.patch(url, json=body)

    assert response.status_code == 422
