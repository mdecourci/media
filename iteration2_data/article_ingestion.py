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
