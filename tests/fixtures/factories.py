import pytest

from tests.factories.anime import AnimeFactory
from tests.factories.user import UserFactory
from tests.factories.user_rate import UserRateFactory


@pytest.fixture(scope="module")
def anime_factory(db_session) -> AnimeFactory:
    return AnimeFactory(db_session)


@pytest.fixture(scope="module")
def user_factory(db_session) -> UserFactory:
    return UserFactory(db_session)


@pytest.fixture(scope="module")
def user_rate_factory(db_session) -> UserRateFactory:
    return UserRateFactory(db_session)
