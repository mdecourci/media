import uuid
from typing import Any

from injectq import singleton

from app.domain.article import Article, ArticleState
from app.domain.article import MediaContent
from app.repository.article_repository import ArticleaRepository
from app.repository.media_content_repository import MediaContentRepository
from app.source.media_source import MediaSource


@singleton
class ArticleService:
    def __init__(self, media_source: MediaSource, media_content_repository: MediaContentRepository,
                 article_repository: ArticleaRepository) -> None:
        self.media_source = media_source
        self.media_content_repository = media_content_repository
        self.article_repository = article_repository

    async def find_articles(self) -> Any:
        content_id = uuid.uuid4()
        content = await self.media_source.get_content()
        media_content = MediaContent(content=content)

        async with self.article_repository.transaction():
            await self.media_content_repository.add(media_content)
            article = Article(article_state=ArticleState.NEW, media_content=media_content)

            await self.article_repository.add(article)
