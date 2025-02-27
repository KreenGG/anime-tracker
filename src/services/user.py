from sqlalchemy import select

from src.database import async_session_maker
from src.exceptions.user import InvalidCredentialsError, UserAlreadyExistsError
from src.models.user import User
from src.schemas.user import TokenGet, UserDTO, UserLogin, UserRegister
from src.utils.auth import create_access_token, get_password_hash, verify_password


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

async def login_user(user_data: UserLogin) -> TokenGet:
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
