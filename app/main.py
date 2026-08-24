# main.py
import asyncio

# Import the container configuration first so that all
# dependency bindings are registered.
from app.container import container
from app.service.article_service import ArticleService


async def main() -> None:
    article_service = container[ArticleService]

    await article_service.find_articles()


if __name__ == "__main__":
    asyncio.run(main())
