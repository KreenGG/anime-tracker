import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.user import User
from src.services.user import UserService
from src.utils.auth import verify_token

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    user_service = UserService(session)
    try:
        payload = verify_token(token)
        if payload.sub:
            user_id = int(payload.sub)
        else:
            raise InvalidTokenError
    except InvalidTokenError as e:
        logger.exception("Could not validate credentials")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    user = await user_service.get_user_by_id(user_id)
    return user


UserDep = Annotated[User, Depends(get_current_user)]
