from typing import Generic, TypeVar, Type, Sequence, Any
import uuid

from sqlalchemy import ColumnElement
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)

class Repository(Generic[ModelType]):
    """Generic CRUD repository — works for any SQLModel table."""

    def __init__(self, session: AsyncSession, model: Type[ModelType]) -> None:
        self.session = session
        self.model = model

    async def add(self, item: ModelType) -> ModelType:
        self.session.add(item)
        await self.session.flush()
        return item

    async def update(self, item: ModelType) -> ModelType:
        await self.add(item)
        return item

    async def find_by_id(self, item_id: uuid.UUID) -> ModelType | None:
        return await self.session.get(self.model, item_id)

    async def find_all(self) -> Sequence[ModelType]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def find_by(self, **conditions: Any) -> Sequence[ModelType]:
        """
        Filter by exact field equality, e.g.:
            await repo.find_by(source_type=MediaSourceType.REST)
        """
        statement = select(self.model)
        for field_name, value in conditions.items():
            column = getattr(self.model, field_name)
            statement = statement.where(column == value)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def find_one_by(self, **conditions: Any) -> ModelType | None:
        results = await self.find_by(**conditions)

    async def find_where(self, *conditions: ColumnElement[bool]) -> Sequence[ModelType]:
        """
        Filter using arbitrary SQLAlchemy expressions, e.g.:
            await repo.find_where(IngestionMetadata.created_at > cutoff)
            await repo.find_where(MediaContent.content.like("%error%"))
        """
        statement = select(self.model).where(*conditions)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def delete(self, item: ModelType) -> None:
        await self.session.delete(item)
        await self.session.flush()