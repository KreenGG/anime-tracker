from sqlalchemy import select

from src.database import async_session_maker
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.models.user import User
from src.schemas.auth import Token
from src.schemas.user import UserDTO, UserLogin, UserRegister
from src.utils.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)


async def create_user(user_data: UserRegister) -> None:
    async with async_session_maker() as session:
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

async def authenticate_user(user_data: UserLogin) -> Token:
    async with async_session_maker() as session:
        stmt = select(User).where(User.email == user_data.email)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise InvalidCredentialsError
        if not verify_password(user_data.password, user.hashed_password):
            raise InvalidCredentialsError

        user = UserDTO.model_validate(user)
        token = create_access_token(user)

        return token

async def get_user_by_id(user_id: int) -> UserDTO:
    async with async_session_maker() as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        user = UserDTO.model_validate(user)

        return user
