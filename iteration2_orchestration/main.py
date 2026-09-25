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
