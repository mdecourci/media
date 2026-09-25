from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from inoreader_auth import (
    exchange_code_for_token,
    get_authorization_url,
)


app = FastAPI()


@app.get(
    "/"
)
def home():

    url = get_authorization_url()

    return HTMLResponse(
        f"""
        <html>
            <body>
                <h1>
                    NESO Media Intelligence
                </h1>

                <p>
                    Connect to Inoreader:
                </p>

                <a href="{url}">
                    Authorise Inoreader
                </a>
            </body>
        </html>
        """
    )


@app.get(
    "/oauth/callback"
)
def oauth_callback(
    code: str,
):

    tokens = (
        exchange_code_for_token(
            code
        )
    )

    return {
        "message": (
            "Inoreader authentication "
            "successful."
        ),
        "access_token": tokens[
            "access_token"
        ],
        "refresh_token": tokens[
            "refresh_token"
        ],
    }
