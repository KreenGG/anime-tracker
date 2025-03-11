from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.anime import Anime

faker = Faker()


async def create_bunch_anime(
    db_session: AsyncSession, amount: int = 100
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
    db_session.add_all(anime_list)
    await db_session.commit()
    return anime_list
