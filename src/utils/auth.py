from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
import jwt

from src.config import config
from src.schemas.auth import TokenPayload


def get_password_hash(password: str) -> str:
    hashed_password: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_password_correct = bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode(),
    )
    return is_password_correct


def create_access_token(
    subject: str | Any,
    expires_delta_minutes: int = config.auth.access_token_expire_minutes,
) -> str:
    to_encode = {
        "sub": str(subject),
    }
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta_minutes)
    expire_timestamp = str(int(expire.timestamp()))

    to_encode.update({"exp": expire_timestamp})
    token = jwt.encode(
        to_encode,
        config.auth.secret_key.get_secret_value(),
        algorithm=config.auth.algorithm,
    )

    return token


def verify_token(token: str) -> TokenPayload:
    payload = jwt.decode(
        token,
        config.auth.secret_key.get_secret_value(),
        algorithms=[config.auth.algorithm],
    )

    sub = payload.get("sub")
    return TokenPayload(sub=sub)
