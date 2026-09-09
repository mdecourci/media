import logging
from typing import TypeVar

from injectq import singleton
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from app.persistence.model.media_content import MediaContent
from app.persistence.repository.repository import Repository

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=SQLModel)


@singleton
class MediaContentRepository(Repository[MediaContent]):
    """Generic CRUD repository — works for any SQLModel table."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, MediaContent)
