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

    username: str = Field(alias="POSTGRES_USER")
    password: SecretStr
    host: str = "localhost"
    port: int = 5432
    database: str = Field(alias="POSTGRES_DB")

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

    secret_key: SecretStr
    access_token_expire_minutes: int
    algorithm: str


class Config(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    auth: AuthConfig = AuthConfig()


config = Config()
