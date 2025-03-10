import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.anime import Anime

faker = Faker()

ROW_AMOUNT = 100


@pytest.fixture(scope="module")
async def filled_anime_db(db_session: AsyncSession):
    anime_list = []
    for i in range(ROW_AMOUNT):
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
