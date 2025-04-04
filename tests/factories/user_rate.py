from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.anime import Anime
from src.models.user import User
from src.models.user_rate import Status, UserRate

faker = Faker()


class UserRateFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    def generate_user_rate(self, anime: Anime) -> UserRate:
        user_rate = UserRate(
            anime_id=anime.id,
            score=faker.random_digit(),
            status=faker.enum(Status),
            rewatches=faker.random_digit(),
            episodes=faker.random_int(min=1, max=1200),
            text=faker.text(),
        )
        return user_rate

    async def create_user_rate(self, user: User, anime: Anime) -> UserRate:
        user_rate = UserRate(
            user_id=user.id,
            anime_id=anime.id,
            score=faker.random_digit(),
            status=faker.enum(Status),
            rewatches=faker.random_digit(),
            episodes=faker.random_int(min=1, max=1200),
            text=faker.text(),
        )

        self.session.add(user_rate)
        await self.session.flush()
        await self.session.refresh(user_rate)
        return user_rate

    # async def create_bunch_user_rates(self, amount: int = 60) -> list[User]:
    #     user_rates_list = []

    #     for i in range(amount):
    #         user_rates_list.append(
    #             UserRate(
    #                 user_id=user.id,
    #                 anime_id=anime.id,
    #                 score=faker.random_digit(),
    #                 status=faker.enum(Status),
    #                 rewatches=faker.random_digit(),
    #                 episodes=faker.random_int(min=1, max=1200),
    #                 text=faker.text(),
    #     )
    #         )

    #     self.session.add_all(user_rates_list)
    #     await self.session.flush()
    #     return user_rates_list
