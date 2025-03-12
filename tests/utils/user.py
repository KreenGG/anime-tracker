from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.utils.auth import get_password_hash

faker = Faker()


TEST_USER = User(
    email="test@test.com",
    hashed_password=get_password_hash("test"),
    nickname="TestUser",
)


async def create_user(db_session: AsyncSession) -> User:
    user = User(
        email=faker.email(),
        hashed_password=get_password_hash(faker.password(20)),
        nickname=faker.user_name(),
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def create_bunch_users(db_session: AsyncSession, amount: int = 100) -> list[User]:
    user_list = [TEST_USER]

    for i in range(amount):
        user_list.append(
            User(
                email=faker.email(),
                hashed_password=faker.password(20),
                nickname=faker.user_name() + str(i),
            )
        )

    db_session.add_all(user_list)
    await db_session.commit()
    await db_session.refresh(TEST_USER)
    return user_list
