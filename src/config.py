import secrets

from dotenv import find_dotenv, load_dotenv
from pydantic import (
    Field,
    PostgresDsn,
    SecretStr,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(".env"))


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POSTGRES_")

    username: str | None = Field(alias="POSTGRES_USER", default=None)
    password: SecretStr = SecretStr(secrets.token_urlsafe())
    host: str | None = None
    port: int | None = None
    database: str | None = Field(alias="POSTGRES_DB", default=None)

    driver: str = "asyncpg"
    database_system: str = "postgresql"
    echo: bool = True

    @property
    def url(self) -> str:
        dsn: PostgresDsn = PostgresDsn.build(
            scheme=f"{self.database_system}+{self.driver}",
            username=self.username,
            password=self.password.get_secret_value() if self.password else None,
            host=self.host,
            port=self.port,
            path=self.database,
        )
        return dsn.unicode_string()


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AUTH_")

    secret_key: SecretStr = SecretStr(secrets.token_urlsafe())
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"


class Config(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    auth: AuthConfig = AuthConfig()


config = Config()
