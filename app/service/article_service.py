import logging
import uuid
from typing import Any

from injectq import singleton

from app.persistence.model.article import Article, ArticleState
from app.persistence.model.media_content import MediaContent
from app.persistence.repository.article_repository import ArticleRepository
from app.persistence.repository.media_content_repository import MediaContentRepository
from app.source.base_media_source import BaseMediaSource

logger = logging.getLogger(__name__)

@singleton
class ArticleService:
    def __init__(self, media_source: BaseMediaSource, media_content_repository: MediaContentRepository,
                 article_repository: ArticleRepository) -> None:
        self.media_source = media_source
        self.media_content_repository = media_content_repository
        self.article_repository = article_repository

    async def find_articles(self) -> Any:
        logger.debug("Finding articles to save...")
        content = await self.media_source.get_content()
        media_content = MediaContent(content=content)

        async with self.article_repository.transaction():
            logger.debug("Finding articles to save...")
            await self.media_content_repository.add(media_content)
            article = Article(article_state=ArticleState.NEW, media_content=media_content)

            await self.article_repository.add(article)
