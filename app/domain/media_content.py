import uuid
from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, Text, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import SQLModel, Field, Relationship

class MediaContent(SQLModel, table=True):
    __tablename__ = "media_content"

    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True),
    )
    content: str = Field(sa_column=Column(Text, nullable=False))

    created_at: datetime | None = (
        Field(
            sa_column=Column(
                TIMESTAMP(timezone=True),
                nullable=False,
                server_default=text("now()")
            )
        ))

    article: "Article" = Relationship(
        back_populates="media_content",
        sa_relationship_kwargs={"uselist": False},
    )
