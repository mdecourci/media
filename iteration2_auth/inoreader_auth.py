from urllib.parse import urlencode

import requests

from config import (
    INOREADER_CLIENT_ID,
    INOREADER_CLIENT_SECRET,
    INOREADER_REDIRECT_URI,
)


AUTH_URL = (
    "https://www.inoreader.com/oauth2/auth"
)

TOKEN_URL = (
    "https://www.inoreader.com/oauth2/token"
)


def get_authorization_url() -> str:

    parameters = {
        "client_id": INOREADER_CLIENT_ID,
        "redirect_uri": INOREADER_REDIRECT_URI,
        "response_type": "code",
        "scope": "read",
        "state": "media-intelligence",
    }

    return (
        f"{AUTH_URL}?"
        f"{urlencode(parameters)}"
    )


def exchange_code_for_token(
    code: str,
) -> dict:

    response = requests.post(
        TOKEN_URL,
        data={
            "code": code,
            "redirect_uri": INOREADER_REDIRECT_URI,
            "client_id": INOREADER_CLIENT_ID,
            "client_secret": INOREADER_CLIENT_SECRET,
            "scope": "read",
            "grant_type": "authorization_code",
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def refresh_access_token(
    refresh_token: str,
) -> dict:

    response = requests.post(
        TOKEN_URL,
        data={
            "client_id": INOREADER_CLIENT_ID,
            "client_secret": INOREADER_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()
