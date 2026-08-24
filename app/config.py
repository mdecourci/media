# config.py
import logging
import sys
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    # Define fields with type hints. Pydantic validates these at runtime.
    db_user: str = Field(default="postgres", alias="POSTGRES_USER")
    db_password: str = Field(default="mypassword", alias="POSTGRES_PASSWORD")
    db_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    db_port: int = Field(default=5432, alias="POSTGRES_PORT")
    db_name: str = Field(default="local_vector_db", alias="POSTGRES_DB")

    # Pydantic Settings configuration block
    model_config = SettingsConfigDict(
        # Looks for a local .env file first, falling back to system env vars
        env_file=".env",
        env_file_encoding="utf-8",
        # Extra fields in the env file that aren't defined above will be ignored safely
        extra="ignore",
        populate_by_name=True,
    )

    # config.py
    @property
    def connection_string(self) -> str:
        """Dynamically builds the Asyncpg driver connection string for LangChain."""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class MediaSourceSettings(BaseSettings):
    # Define fields with type hints. Pydantic validates these at runtime.
    source: str = Field(default="postgres", alias="MEDIA_SOURCE")

    # Pydantic Settings configuration block
    model_config = SettingsConfigDict(
        # Looks for a local .env file first, falling back to system env vars
        env_file=".env",
        env_file_encoding="utf-8",
        # Extra fields in the env file that aren't defined above will be ignored safely
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def file(self) -> Path:
        return Path(self.source)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format=("%(asctime)s | " "%(levelname)s | " "%(name)s | " "%(message)s"),
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )

    logging.getLogger("uvicorn").setLevel(logging.DEBUG)

    logging.getLogger("injectq").setLevel(logging.DEBUG)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)


# Instantiate a single global instance for application-wide imports
databaseSettings = DatabaseSettings()
mediaSourceSettings = MediaSourceSettings()
