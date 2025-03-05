from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from src.config import config
from src.schemas.auth import TokenPayload
from src.schemas.user import User


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
    user: User,
    expires_delta_minutes: int = config.auth.access_token_expire_minutes,
) -> str:
    to_encode = {
        "sub": str(user.id),
    }
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta_minutes)
    to_encode.update({"exp": expire})
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

    user_id = payload.get("sub")
    return TokenPayload(user_id=user_id)
