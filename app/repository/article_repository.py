from injectq import singleton
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.article import Article
from app.repository.repository import Repository


@singleton
class ArticleaRepository(Repository[Article]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Article)
