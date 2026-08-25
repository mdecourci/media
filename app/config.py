# config.py
import logging
import sys
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

_base_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore", validate_default=False)

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"  # adjust based on config.py's actual location

print(ENV_FILE.exists())


class DatabaseSettings(BaseSettings):
    # Define fields with type hints. Pydantic validates these at runtime.
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # Pydantic Settings configuration block
    model_config = _base_config

    # config.py
    @property
    def database_url(self) -> str:
        """Dynamically builds the Asyncpg driver connection string for LangChain."""
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )


class MediaSourceSettings(BaseSettings):
    # Define fields with type hints. Pydantic validates these at runtime.
    MEDIA_SOURCE: str = Field(validation_alias="MEDIA_SOURCE")

    # Pydantic Settings configuration block
    model_config = _base_config

    @property
    def file(self) -> Path:
        return Path(self.MEDIA_SOURCE)


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
