# config.py
import logging
import sys
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"  # adjust based on config.py's actual location

print(ENV_FILE.exists())

class DatabaseSettings(BaseSettings):
    # Define fields with type hints. Pydantic validates these at runtime.
    database_user: str = Field(validation_alias="POSTGRES_USER")
    database_password: str = Field(validation_alias="POSTGRES_PASSWORD")
    database_host: str = Field(validation_alias="POSTGRES_HOST")
    database_port: int = Field(validation_alias="POSTGRES_PORT")
    database_db: str = Field(validation_alias="POSTGRES_DB")

    # Pydantic Settings configuration block
    model_config = SettingsConfigDict(
        # Looks for a local .env file first, falling back to system env vars
        env_file=".env",
        env_file_encoding="utf-8",
        # Extra fields in the env file that aren't defined above will be ignored safely
        extra="ignore",
    )

    # config.py
    @property
    def connection_string(self) -> str:
        """Dynamically builds the Asyncpg driver connection string for LangChain."""
        return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_db}"


class MediaSourceSettings(BaseSettings):
    # Define fields with type hints. Pydantic validates these at runtime.
    media_source: str = Field(validation_alias="MEDIA_SOURCE")

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
        return Path(self.media_source)


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
