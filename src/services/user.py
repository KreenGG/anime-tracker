import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.user import UserDAO
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.models.user import User as UserModel
from src.schemas.auth import Token
from src.schemas.user import User, UserLogin, UserRegister
from src.utils.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_dao = UserDAO(self.session)

    async def create_user(
        self,
        user_data: UserRegister,
    ) -> None:
        user = await self.user_dao.get_single(email=user_data.email)
        if user:
            raise UserAlreadyExistsError

        hashed_password = get_password_hash(user_data.password)
        user = UserModel(
            email=user_data.email,
            hashed_password=hashed_password,
        )

        # FIXME try except
        await self.user_dao.create(user)
        await self.session.commit()
        logger.debug("User %s created", user.email)

    async def authenticate_user(
        self,
        user_data: UserLogin,
    ) -> Token:
        user_db = await self.user_dao.get_single(email=user_data.email)
        if not user_db:
            raise InvalidCredentialsError
        if not verify_password(user_data.password, user_db.hashed_password):
            raise InvalidCredentialsError

        user = User.model_validate(user_db)
        token = create_access_token(user.id)

        logger.debug("Token for user %s created", user.email)

        return Token(access_token=token, token_type="Bearer")

    async def get_user_by_id(self, user_id: int) -> User:
        user_db = await self.user_dao.get_single(id=user_id)
        user = User.model_validate(user_db)

        return user
