from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext

from src.config import config
from src.schemas.user import UserDTO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
    user: UserDTO,
    expires_delta_minutes: int=config.auth.access_token_expire_minutes,
) -> str:
    to_encode = {
        "sub": user.id,
    }
    expire = datetime.now(UTC) + timedelta(minutes=expires_delta_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        config.auth.secret_key.get_secret_value(),
        algorithm=config.auth.algorithm,
    )

    return encoded_jwt
