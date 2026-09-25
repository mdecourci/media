import os

from dotenv import load_dotenv


load_dotenv()


def required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Environment variable '{name}' has not been configured."
        )

    return value


FOUNDRY_ENDPOINT = required_env(
    "AZURE_AI_PROJECT_ENDPOINT"
)

FOUNDRY_API_KEY = required_env(
    "AZURE_AI_API_KEY"
)

FOUNDRY_MODEL = os.getenv(
    "FOUNDRY_MODEL",
    "gpt-5-mini",
)


POSTGRES_HOST = required_env(
    "POSTGRES_HOST"
)

POSTGRES_PORT = int(
    os.getenv(
        "POSTGRES_PORT",
        "5432",
    )
)

POSTGRES_DATABASE = required_env(
    "POSTGRES_DATABASE"
)

POSTGRES_USER = required_env(
    "POSTGRES_USER"
)

POSTGRES_PASSWORD = required_env(
    "POSTGRES_PASSWORD"
)


INOREADER_CLIENT_ID = required_env(
    "INOREADER_CLIENT_ID"
)

INOREADER_CLIENT_SECRET = required_env(
    "INOREADER_CLIENT_SECRET"
)

INOREADER_REDIRECT_URI = required_env(
    "INOREADER_REDIRECT_URI"
)

INOREADER_ACCESS_TOKEN = os.getenv(
    "INOREADER_ACCESS_TOKEN",
    ""
)

INOREADER_REFRESH_TOKEN = os.getenv(
    "INOREADER_REFRESH_TOKEN",
    ""
)
