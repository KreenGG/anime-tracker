import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.models.user import User
from src.schemas.auth import Token
from src.schemas.user import UserDTO, UserLogin, UserRegister
from src.utils.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)

logger = logging.getLogger(__name__)

async def create_user(
    user_data: UserRegister,
    session: AsyncSession,
) -> None:
    stmt = select(User).where(User.email == user_data.email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user:
        raise UserAlreadyExistsError

    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
    )

    session.add(user)
    await session.commit()
    logger.debug("User %s created", user.email)

async def authenticate_user(
    user_data: UserLogin,
    session: AsyncSession,
) -> Token:
    stmt = select(User).where(User.email == user_data.email)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if not user:
        raise InvalidCredentialsError
    if not verify_password(user_data.password, user.hashed_password):
        raise InvalidCredentialsError

    user = UserDTO.model_validate(user)
    token = create_access_token(user)
    
    logger.debug("Token for user %s created", user.email)

    return token

async def get_user_by_id(
    user_id: int,
    session: AsyncSession,
) -> UserDTO:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()
    user = UserDTO.model_validate(user)

    return user
