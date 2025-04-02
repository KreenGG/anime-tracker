import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.user import UserDAO
from src.exceptions.auth import InvalidCredentialsError, UserAlreadyExistsError
from src.exceptions.repository import RecordNotFoundError
from src.models.user import User as UserModel
from src.schemas.auth import Token
from src.schemas.user import UserDTO, UserLogin, UserRegister, UserUpdate
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
        is_already_exists = await self.user_dao.is_already_exists(
            user_data.email,
            user_data.nickname,
        )
        if is_already_exists:
            raise UserAlreadyExistsError

        hashed_password = get_password_hash(user_data.password)
        user = UserModel(
            email=user_data.email,
            hashed_password=hashed_password,
            nickname=user_data.nickname,
        )

        await self.user_dao.create(user)
        await self.session.commit()
        logger.debug("User %s created", user.email)

    async def authenticate_user(
        self,
        user_data: UserLogin,
    ) -> Token:
        try:
            user_db = await self.user_dao.get_single(email=user_data.email)
        except RecordNotFoundError:
            raise InvalidCredentialsError

        if not verify_password(user_data.password, user_db.hashed_password):
            raise InvalidCredentialsError

        user = UserDTO.model_validate(user_db)
        token = create_access_token(user.id)

        logger.debug("Token for user %s created", user.email)

        return Token(access_token=token, token_type="Bearer")

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        user_db = await self.user_dao.get_single(id=user_id)
        user = UserDTO.model_validate(user_db)

        return user

    async def update_user(self, user_id: int, update_data: UserUpdate) -> UserDTO:
        db_user = await self.user_dao.get_single(id=user_id)

        for var, value in vars(update_data).items():
            setattr(db_user, var, value) if value else None
        await self.session.commit()

        return UserDTO.model_validate(db_user)
