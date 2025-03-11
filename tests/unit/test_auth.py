import secrets

import pytest

from src.utils.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
    verify_token,
)


@pytest.mark.parametrize(
    "plain_password", ["212121121", "ghgdf13!", secrets.token_urlsafe()]
)
def test_password_encoding(plain_password):
    hashed_password = get_password_hash(plain_password)

    assert verify_password(plain_password, hashed_password)


@pytest.mark.parametrize("sub", [10, "12", "q13f3c-saw12"])
def test_jwt_token(sub):
    token = create_access_token(sub)
    payload = verify_token(token)

    assert payload.sub == str(sub)
