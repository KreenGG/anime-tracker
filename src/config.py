import secrets
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import (
    Field,
    PostgresDsn,
    SecretStr,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
load_dotenv(find_dotenv(str(BASE_DIRECTORY / ".env")))


class AppConfig(BaseSettings):
    log_level: str = "INFO"


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    user: str | None = Field(alias="POSTGRES_USER", default="username")
    password: SecretStr = SecretStr(secrets.token_urlsafe())
    host: str | None = "localhost"
    port: int | None = 5432
    database: str | None = Field(alias="POSTGRES_DB", default="db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"
    echo: bool = False

    def url(self, testing: bool = False) -> str:
        dsn: PostgresDsn = PostgresDsn.build(
            scheme=f"{self.database_system}+{self.driver}",
            username=self.user,
            password=self.password.get_secret_value() if self.password else None,
            host="localhost" if testing else self.host,
            port=self.port,
            path=self.database,
        )
        return dsn.unicode_string()

    @property
    def test_postgres_db(self) -> str:
        return f"test_{self.database}"

    @property
    def test_postgres_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@localhost:{self.port}/{self.test_postgres_db}"


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AUTH_")

    secret_key: SecretStr = SecretStr(secrets.token_urlsafe())
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"


class Config(BaseSettings):
    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()
    auth: AuthConfig = AuthConfig()


config = Config()
