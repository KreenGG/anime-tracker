import secrets
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(str(BASE_DIRECTORY / ".env")))


class TestConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TEST_")

    username: str | None = Field(alias="TEST_POSTGRES_USER", default=None)
    password: str = Field(
        alias="TEST_POSTGRES_PASSWORD", default=secrets.token_urlsafe()
    )
    host: str | None = Field(alias="TEST_POSTGRES_HOST", default="localhost")
    port: int | None = Field(alias="TEST_POSTGRES_PORT", default=5431)
    database: str | None = Field(alias="TEST_POSTGRES_DB", default="test_db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"
    echo: bool = True

    @property
    def url(self) -> str:
        dsn: PostgresDsn = PostgresDsn.build(
            scheme=f"{self.database_system}+{self.driver}",
            username=self.username,
            password=self.password if self.password else None,
            host=self.host,
            port=self.port,
            path=self.database,
        )
        return dsn.unicode_string()


test_config = TestConfig()
