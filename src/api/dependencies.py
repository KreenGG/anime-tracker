import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.user import UserDTO
from src.services.user import UserService
from src.utils.auth import verify_token

logger = logging.getLogger(__name__)
security = HTTPBearer(auto_error=False)

SessionDep = Annotated[AsyncSession, Depends(get_session)]

UnauthorizedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=[{"msg": "Could not validate credentials"}],
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    request: Request,
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: SessionDep,
) -> UserDTO:
    if not token and not request.cookies.get("access_token"):
        logger.warning("Token does not provided")
        raise UnauthorizedError
    elif request.cookies.get("access_token"):
        token = request.cookies.get("access_token")
    else:
        token = token.credentials

    user_service = UserService(session)
    try:
        payload = verify_token(token)
        if payload.sub:
            user_id = int(payload.sub)
        else:
            raise InvalidTokenError
    except InvalidTokenError:
        logger.exception("Could not validate credentials")
        raise UnauthorizedError
    user = await user_service.get_user_by_id(user_id)
    return user


UserDep = Annotated[UserDTO, Depends(get_current_user)]
