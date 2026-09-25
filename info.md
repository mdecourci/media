
Yes. Based on the setup we discussed, you want a simple Python application that uses a Microsoft Foundry project, does not create a model deployment, and calls an instant-access model.
Microsoft's current documentation confirms that instant-access models can be called by model name without creating a deployment. gpt-5-mini is currently listed as an example of an instant-access model. The preview currently requires the Foundry project to be in West US 3.

One important point: "instant access" does not necessarily mean free of Azure charges. It means no model deployment is required. Quota/usage still applies, so check the model's pricing/quota shown in your Foundry project before using it extensively.

1. Project structure
I'd keep the test application very small:
media-agent/
├── .env
├── .gitignore
├── requirements.txt
└── main.py
2. requirements.txt
azure-ai-projects
azure-identity
python-dotenv
openai
Install them:
pip install -r requirements.txt
The current Microsoft example uses AIProjectClient and obtains an OpenAI client from the Foundry project.
3. .env
Put your Foundry project endpoint in .env:
AZURE_AI_PROJECT_ENDPOINT=https://YOUR-RESOURCE.services.ai.azure.com/api/projects/YOUR-PROJECT
For example:
AZURE_AI_PROJECT_ENDPOINT=https://myfoundry.services.ai.azure.com/api/projects/media-project
Do not put your Azure subscription ID or model deployment name here.
There is no deployment name because we're using instant access.

Also add:

FOUNDRY_MODEL=gpt-5-mini
So the complete file is:
AZURE_AI_PROJECT_ENDPOINT=https://YOUR-RESOURCE.services.ai.azure.com/api/projects/YOUR-PROJECT
FOUNDRY_MODEL=gpt-5-mini
4. Full main.py
Here is the complete application:
import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def get_environment_variable(name: str) -> str:
    """Read a required environment variable."""
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Environment variable '{name}' has not been configured."
        )

    return value


def create_client() -> tuple[AIProjectClient, object]:
    """Create the Microsoft Foundry project and OpenAI clients."""

    project_endpoint = get_environment_variable(
        "AZURE_AI_PROJECT_ENDPOINT"
    )

    credential = DefaultAzureCredential()

    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=credential,
    )

    openai_client = project_client.get_openai_client()

    return project_client, openai_client


def generate_summary(
    openai_client: object,
    article: str,
) -> str:
    """Send an article to the Foundry model and return a summary."""

    model = os.getenv(
        "FOUNDRY_MODEL",
        "gpt-5-mini",
    )

    prompt = f"""
You are an AI news summarisation agent for NESO.

Summarise the following article.

Requirements:
- Produce a concise factual summary.
- Identify the main topic.
- Identify the organisations mentioned.
- Identify any important energy-sector implications.
- Do not invent information.
- Do not include information that is not supported by the article.
- Use clear professional English.

Article:

{article}
"""

    response = openai_client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=1000,
    )

    result = response.output_text

    if not result or not result.strip():
        raise RuntimeError(
            "The model returned an empty response."
        )

    return result.strip()


def main() -> None:
    """Application entry point."""

    print("Starting NESO Media AI Agent...")

    project_client, openai_client = create_client()

    print("Connected to Microsoft Foundry.")
    print(
        f"Using model: "
        f"{os.getenv('FOUNDRY_MODEL', 'gpt-5-mini')}"
    )

    article = """
    The UK's energy system is undergoing significant change as
    renewable generation increases and the electricity network
    needs to accommodate new sources of low-carbon power.

    National Energy System Operator is working with industry
    stakeholders to improve the way energy-system data is shared
    and used to support planning and real-time operations.
    """

    print("\nGenerating summary...\n")

    summary = generate_summary(
        openai_client,
        article,
    )

    print("----- SUMMARY -----")
    print(summary)
    print("-------------------")


if __name__ == "__main__":
    main()
5. Azure authentication
This version deliberately uses:
DefaultAzureCredential()
rather than an API key.
Microsoft's current Foundry examples use DefaultAzureCredential for the project endpoint.

For your local Mac, the simplest development setup is:

az login
Then run:
python main.py
Your Azure CLI login supplies the credentials to:
DefaultAzureCredential()
You therefore don't need to put an Azure password, client secret or API key in .env.
6. Give your user access to the project
Your Azure account needs access to the Foundry project. Microsoft's current documentation refers to the Foundry User role for using instant-access models.
In the Azure/Foundry portal, check the project's access/IAM settings and make sure your account has the appropriate Foundry project role.

7. Important: no deployment
The important line in the Python application is:
model = os.getenv(
    "FOUNDRY_MODEL",
    "gpt-5-mini",
)
and then:
response = openai_client.responses.create(
    model=model,
    input=prompt,
    max_output_tokens=1000,
)
Notice that there is no deployment name.
With the instant-access functionality, this:

gpt-5-mini
is the model name.
You don't do:

deployment = ...
and you don't need to create:
gpt-5-mini-deployment
in Foundry.
Microsoft explicitly documents this pattern for instant-access models.

8. Test it
Run:
python main.py
You should see something similar to:
Starting NESO Media AI Agent...
Connected to Microsoft Foundry.
Using model: gpt-5-mini

Generating summary...

----- SUMMARY -----
The UK energy system is undergoing a transition toward
greater renewable generation. NESO is working with industry
stakeholders to improve energy-system data sharing...
-------------------
9. .gitignore
I'd also create this immediately:
.env
.venv/
__pycache__/
*.pyc
.idea/
This prevents your .env from accidentally being committed.
One correction to the earlier approach
If your objective is specifically "Foundry project + no model deployment + try an available model at no/very-low cost", don't use the traditional Azure OpenAI deployment approach.
Use:

Foundry Project
       │
       └── Instant-access model
               │
               └── gpt-5-mini
rather than:
Foundry Project
       │
       └── Model Deployment
               │
               └── gpt-5-mini deployment
The first approach is the current Microsoft Foundry instant-access mechanism.
If you want, the next step can be to modify this exact code so that it becomes your NESO Media Agent, accepting an article from your Inoreader pipeline and returning a structured JSON summary suitable for storing in PostgreSQL.
It seems like I can’t do more advanced data analysis right now. Please try again later. 
generate code that call inoreader as well
Yes. If you want Python to actually call Inoreader, rather than reading the publishers' RSS URLs directly, we should use the Inoreader API with OAuth 2.0.
There is one important cost point: Inoreader currently says that API access for normal use requires Pro; Free-plan users are not granted developer API access.

The API does exactly what you need: it can retrieve the contents of an Inoreader stream/folder, with up to 100 articles per request.

Architecture
For the Inoreader-API version:
                 Inoreader
                     │
              OAuth 2.0 login
                     │
                     ▼
              Python application
                     │
             Inoreader API
                     │
                     ▼
              Articles / JSON
                     │
                     ▼
                PostgreSQL
                     │
                     ▼
              Foundry AI Agent
                     │
                     ▼
                  Summary
The API uses OAuth 2.0 rather than asking your Python application for your Inoreader password.
1. Create an Inoreader application
In Inoreader, go to:
Preferences → Create new application

Inoreader will give you:

App ID
App Key
and you configure an OAuth redirect URI.
For local development, use something such as:

http://localhost:8000/oauth/callback
You'll then have:
INOREADER_CLIENT_ID=...
INOREADER_CLIENT_SECRET=...
Don't send those credentials to me.
2. Updated project
I'd now structure your project like this:
media/
│
├── .env
├── .gitignore
├── requirements.txt
│
├── main.py
│
├── config.py
├── database.py
├── models.py
│
├── inoreader.py
├── inoreader_auth.py
│
├── article_ingestion.py
│
├── tools.py
└── media_agent.py
3. requirements.txt
Add FastAPI because we'll use a tiny local callback endpoint for OAuth:
openai>=2.0.0
python-dotenv>=1.0.0
fastapi>=0.115.0
uvicorn>=0.30.0
requests>=2.32.0
sqlalchemy>=2.0.0
psycopg[binary]>=3.2.0
Install:
pip install -r requirements.txt
4. .env
Your .env becomes:
AZURE_AI_PROJECT_ENDPOINT=https://media-ai-agents.services.ai.azure.com/api/projects/media-intelligence
AZURE_AI_API_KEY=YOUR_FOUNDRY_API_KEY
FOUNDRY_MODEL=gpt-5-mini

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=media
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD

INOREADER_CLIENT_ID=YOUR_INOREADER_APP_ID
INOREADER_CLIENT_SECRET=YOUR_INOREADER_APP_KEY

INOREADER_REDIRECT_URI=http://localhost:8000/oauth/callback

INOREADER_ACCESS_TOKEN=
INOREADER_REFRESH_TOKEN=
The access/refresh tokens will be populated after you authorise the application.
5. config.py
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
6. inoreader_auth.py
This handles the Inoreader OAuth 2.0 flow.
Inoreader's documented OAuth flow is:

authorization code
       ↓
access token
       +
refresh token
and access tokens can subsequently be refreshed.
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
7. inoreader.py
This is the actual Inoreader API client.
The Inoreader API endpoint is:

https://www.inoreader.com/reader/api/0
and stream contents are retrieved using:
/stream/contents/{streamId}
with up to 100 items per request.
from typing import Any
from urllib.parse import quote

import requests


BASE_URL = (
    "https://www.inoreader.com"
    "/reader/api/0"
)


class InoreaderClient:

    def __init__(
        self,
        access_token: str,
    ) -> None:

        self.access_token = (
            access_token
        )

    def _headers(self) -> dict[str, str]:

        return {
            "Authorization": (
                f"Bearer {self.access_token}"
            ),
            "User-Agent": (
                "NESO-Media-Intelligence/1.0"
            ),
        }

    def get_user_info(
        self,
    ) -> dict[str, Any]:

        response = requests.get(
            f"{BASE_URL}/user-info",
            headers=self._headers(),
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def get_subscriptions(
        self,
    ) -> list[dict[str, Any]]:

        response = requests.get(
            f"{BASE_URL}/subscription/list",
            headers=self._headers(),
            timeout=30,
        )

        response.raise_for_status()

        return response.json().get(
            "subscriptions",
            [],
        )

    def get_tags(
        self,
    ) -> list[dict[str, Any]]:

        response = requests.get(
            f"{BASE_URL}/tag/list",
            headers=self._headers(),
            timeout=30,
        )

        response.raise_for_status()

        return response.json().get(
            "tags",
            [],
        )

    def get_stream_contents(
        self,
        stream_id: str,
        limit: int = 100,
        newer_than: int | None = None,
    ) -> list[dict[str, Any]]:

        encoded_stream_id = quote(
            stream_id,
            safe="",
        )

        url = (
            f"{BASE_URL}"
            f"/stream/contents/"
            f"{encoded_stream_id}"
        )

        parameters: dict[str, Any] = {
            "n": min(limit, 100),
        }

        if newer_than is not None:
            parameters["ot"] = newer_than

        response = requests.get(
            url,
            headers=self._headers(),
            params=parameters,
            timeout=30,
        )

        response.raise_for_status()

        return response.json().get(
            "items",
            [],
        )
8. Finding your Inoreader streams
This is an important part.
After authentication, run:

client.get_subscriptions()
You'll get information similar to:
[
  {
    "id": "feed/http://example.com/rss",
    "title": "Example News",
    "categories": []
  }
]
You can also retrieve your folders/tags with:
client.get_tags()
Inoreader's API provides a folder/tag list and subscription list.
A folder stream ID looks like:

user/-/label/NESO Media
The API allows the - placeholder instead of your actual user ID.
So your eventual configuration could be:

INOREADER_STREAM_ID=user/-/label/NESO Media
Then Python retrieves everything in that folder.
9. models.py
Use the article model from the previous version, but I'd add the Inoreader article ID:
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database import Base


class Article(Base):

    __tablename__ = "articles"

    __table_args__ = (
        UniqueConstraint(
            "inoreader_id",
            name="uq_articles_inoreader_id",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    inoreader_id: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="NEW",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
10. Convert Inoreader articles to PostgreSQL
Create article_ingestion.py:
from datetime import datetime, timezone

from sqlalchemy import select

from database import get_session
from models import Article


def convert_timestamp(
    timestamp_usec: str | None,
) -> datetime | None:

    if not timestamp_usec:
        return None

    timestamp = int(
        timestamp_usec
    ) / 1_000_000

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    )


def extract_content(
    item: dict,
) -> str:

    summary = item.get(
        "summary",
        {},
    )

    content = summary.get(
        "content",
        "",
    )

    if not content:

        origin = item.get(
            "origin",
            {},
        )

        content = origin.get(
            "title",
            "",
        )

    return content


def save_inoreader_article(
    item: dict,
) -> bool:

    inoreader_id = item["id"]

    origin = item.get(
        "origin",
        {},
    )

    source = origin.get(
        "title",
        "Unknown",
    )

    canonical = item.get(
        "canonical",
        [],
    )

    url = ""

    if canonical:
        url = canonical[0].get(
            "href",
            "",
        )

    title = item.get(
        "title",
        "Untitled",
    )

    content = extract_content(
        item
    )

    published_at = convert_timestamp(
        item.get(
            "timestampUsec"
        )
    )

    with get_session() as session:

        existing = session.scalar(
            select(Article).where(
                Article.inoreader_id
                == inoreader_id
            )
        )

        if existing:

            return False

        article = Article(
            inoreader_id=inoreader_id,
            source=source,
            title=title,
            url=url,
            content=content,
            published_at=published_at,
            status="NEW",
        )

        session.add(article)

        session.commit()

        return True
11. Authentication callback
Create auth_server.py:
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
Run it:
uvicorn auth_server:app --reload
Then open:
http://localhost:8000
Click:
Authorise Inoreader
You'll be sent to Inoreader, log in, and approve the application.
Inoreader then redirects to:

http://localhost:8000/oauth/callback
The callback exchanges the authorization code for an access token and refresh token, as specified by Inoreader's OAuth documentation.
12. Get your Inoreader subscriptions
Once authenticated, put the returned access token into:
INOREADER_ACCESS_TOKEN=...
Then create:
from config import INOREADER_ACCESS_TOKEN
from inoreader import InoreaderClient


client = InoreaderClient(
    INOREADER_ACCESS_TOKEN
)

subscriptions = (
    client.get_subscriptions()
)

for subscription in subscriptions:

    print(
        subscription["id"],
        subscription["title"],
    )
You should see your Inoreader feeds.
For example:

feed/http://example.com/rss    Example Energy News
feed/http://example.org/rss    Ofgem
feed/http://example.net/rss    NESO
13. Get articles
Once you know the stream/folder ID:
articles = client.get_stream_contents(
    stream_id="user/-/label/NESO Media",
    limit=100,
)
The API supports retrieving up to 100 items per request.
Then:

for article in articles:

    saved = save_inoreader_article(
        article
    )

    if saved:
        print(
            f"Saved: "
            f"{article['title']}"
        )
14. The complete flow
Your eventual main.py becomes:
from config import (
    INOREADER_ACCESS_TOKEN,
)

from database import Base
from database import engine

from inoreader import (
    InoreaderClient,
)

from article_ingestion import (
    save_inoreader_article,
)

from media_agent import (
    summarise_article,
)

from database import get_session
from models import Article

from sqlalchemy import select


INOREADER_STREAM_ID = (
    "user/-/label/NESO Media"
)


def initialise_database():

    Base.metadata.create_all(
        bind=engine
    )


def ingest_from_inoreader():

    client = InoreaderClient(
        INOREADER_ACCESS_TOKEN
    )

    articles = (
        client.get_stream_contents(
            stream_id=INOREADER_STREAM_ID,
            limit=100,
        )
    )

    saved = 0

    for article in articles:

        if save_inoreader_article(
            article
        ):

            saved += 1

    return saved


def process_articles():

    with get_session() as session:

        articles = session.scalars(
            select(Article)
            .where(
                Article.status == "NEW"
            )
        ).all()

        for article in articles:

            print(
                f"AI processing: "
                f"{article.title}"
            )

            try:

                summary = summarise_article(
                    title=article.title,
                    content=article.content,
                )

                article.summary = summary

                article.status = (
                    "SUMMARISED"
                )

                session.commit()

            except Exception as exc:

                session.rollback()

                article.status = (
                    "ERROR"
                )

                session.commit()

                print(
                    f"Error: {exc}"
                )


def main():

    initialise_database()

    print(
        "Reading Inoreader..."
    )

    saved = ingest_from_inoreader()

    print(
        f"New articles: {saved}"
    )

    print(
        "Generating AI summaries..."
    )

    process_articles()

    print(
        "Pipeline complete."
    )


if __name__ == "__main__":
    main()
If your goal is specifically to learn/build the complete agent pipeline, the API version above is the more representative architecture. If your goal is zero cost, keep the earlier direct-public-RSS implementation.
Also, the Inoreader API has relatively small default request limits; for Pro, the documented defaults are 100 requests/day in each API zone. For your daily 6pm pipeline, that's potentially sufficient for a small prototype, but you should design the ingestion to batch requests and avoid unnecessary polling.



