from injectq import singleton
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.model.article import Article
from app.persistence.repository.repository import Repository


@singleton
class ArticleRepository(Repository[Article]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Article)
