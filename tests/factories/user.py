from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.utils.auth import get_password_hash

faker = Faker()


class UserFactory:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.test_user_plain_password = "test"
        self.test_user = User(
            email="test@test.com",
            hashed_password=get_password_hash(self.test_user_plain_password),
            nickname="TestUser",
        )

    async def create_user(self) -> User:
        user = User(
            email=faker.email(),
            hashed_password=get_password_hash(faker.password(20)),
            nickname=faker.user_name(),
        )

        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def create_test_user(self) -> User:
        self.session.add(self.test_user)
        await self.session.commit()
        await self.session.refresh(self.test_user)
        return self.test_user

    async def create_bunch_users(self, amount: int = 60) -> list[User]:
        user_list = []

        for i in range(amount):
            user_list.append(
                User(
                    email=faker.email(),
                    hashed_password=faker.password(20),
                    nickname=faker.user_name() + str(i),
                )
            )

        self.session.add_all(user_list)
        await self.session.flush()
        return user_list
