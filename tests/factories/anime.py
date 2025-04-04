from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.anime import Anime

faker = Faker()


class AnimeFactory:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_bunch_anime(
        self,
        amount: int = 60,
    ) -> list[Anime]:
        anime_list = []
        for i in range(amount):
            anime_list.append(
                Anime(
                    name=faker.name(),
                    russian=faker.name(),
                    english=faker.name(),
                    japanese=faker.name(),
                    episodes=faker.random_int(min=1, max=1200),
                    episodes_aired=faker.random_int(min=10, max=120),
                    duration=faker.random_int(min=10, max=120),
                    poster=faker.image_url(),
                    description=faker.text(),
                    description_html=faker.text(),
                    description_source=faker.url(),
                )
            )
        self.session.add_all(anime_list)
        await self.session.flush()
        return anime_list

    async def create_anime(self) -> Anime:
        anime = Anime(
            name=faker.name(),
            russian=faker.name(),
            english=faker.name(),
            japanese=faker.name(),
            episodes=faker.random_int(min=1, max=1200),
            episodes_aired=faker.random_int(min=10, max=120),
            duration=faker.random_int(min=10, max=120),
            poster=faker.image_url(),
            description=faker.text(),
            description_html=faker.text(),
            description_source=faker.url(),
        )

        self.session.add(anime)
        await self.session.flush()
        await self.session.refresh(anime)
        return anime
