import logging
import uuid
from contextlib import asynccontextmanager
from typing import Generic, TypeVar, Type, Sequence, Any, AsyncIterator

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.model.entity_base import Base

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)

class Repository(Generic[ModelType]):
    """Generic CRUD repository — works for any SQLModel table."""

    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        self.session = session
        self.model = model

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        """Commits on success, rolls back on failure. Hides session entirely from callers."""
        logger.debug("Transaction started")
        try:
            yield
            await self.session.commit()
            logger.debug("Transaction completed")
        except Exception:
            await self.session.rollback()
            logger.exception("Transaction failed, rolled back")
            raise

    async def add(self, item: ModelType) -> ModelType:
        logger.debug("add: {}".format(item))
        self.session.add(item)
        await self.session.flush()
        return item

    async def update(self, item: ModelType) -> ModelType:
        logger.debug("update: {}".format(item))
        await self.add(item)
        return item

    async def find_by_id(self, item_id: uuid.UUID) -> ModelType | None:
        logger.debug("find_by_id: {}".format(item_id))
        return await self.session.get(self.model, item_id)

    async def find_all(self) -> Sequence[ModelType]:
        logger.debug("find_all")
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def find_by(self, **conditions: Any) -> Sequence[ModelType]:
        logger.debug("find_by: {}".format(conditions))
        """
        Filter by exact field equality, e.g.:
            await repo.find_by(source_type=MediaSourceType.REST)
        """
        statement = select(self.model)
        for field_name, value in conditions.items():
            column = getattr(self.model, field_name)
            statement = statement.where(
                column == value
            )

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def find_one_by(self, **conditions: Any) -> ModelType | None:
        logger.debug("find_one_by: {}".format(conditions))
        results = await self.find_by(**conditions)
        return results[0] if results else None
    #
    # async def find_where(self, **conditions: Any) -> Sequence[ModelType]:
    #     """Generic equality filter — every field/value pair is AND-ed together."""
    #     statement = select(self.model)
    #     for field_name, value in conditions.items():
    #         column = getattr(self.model, field_name)
    #         statement = statement.where(column == value)
    #
    #     result = await self.session.execute(statement)
    #     return result.scalars().all()

    async def delete(self, item: ModelType) -> None:
        logger.debug("delete: {}".format(item))
        await self.session.delete(item)
        await self.session.flush()
