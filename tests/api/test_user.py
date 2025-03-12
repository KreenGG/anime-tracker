from fastapi import FastAPI
from httpx import AsyncClient

from tests.utils.user import TEST_USER


async def test_get_current_user(
    auth_ac: AsyncClient,
    app: FastAPI,
) -> None:
    url = app.url_path_for("get_current_user")
    response = await auth_ac.get(url)

    assert response.status_code == 200
    response_json = response.json()

    assert response_json["id"] == TEST_USER.id
    assert response_json["email"] == TEST_USER.email
    assert response_json["nickname"] == TEST_USER.nickname
