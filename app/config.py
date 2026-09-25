# config.py
import logging
import sys
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

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
        print(self.POSTGRES_SERVER)
        print(self.POSTGRES_PORT)
        print(self.POSTGRES_USER)
        # print(self.POSTGRES_PASSWORD)
        print(self.POSTGRES_DB)
        url = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        print(f"Database URL: {url}")
        return url


class MediaSourceSettings(BaseSettings):
    # Define fields with type hints. Pydantic validates these at runtime.
    MEDIA_SOURCE: str = Field(validation_alias="MEDIA_SOURCE")

    # Pydantic Settings configuration block
    model_config = _base_config

    @property
    def file(self) -> Path:
        return Path(self.MEDIA_SOURCE)

# Instantiate a single global instance for application-wide imports
mediaSourceSettings = MediaSourceSettings()  # type: ignore[call-arg]
databaseSettings = DatabaseSettings()  # type: ignore[call-arg,call-arg]
