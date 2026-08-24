import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, ForeignKey, TIMESTAMP, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import SQLModel, Field, Relationship

from app.domain.media_content import MediaContent


class MediaSourceType(str, enum.Enum):
    FILE = "FILE"
    REST = "REST"


class ArticleState(str, enum.Enum):
    NEW = "NEW"
    REVIEWING = "REVIEWING";
    SUMMARIZED = "SUMMARIZED"
    RETRIED = "RETRIED"
    FAILED = "FAILED"


class Article(SQLModel, table=True):
    __tablename__ = "article"

    id: uuid.UUID | None = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True),
    )

    article_state: ArticleState = Field(
        sa_column=Column(
            SAEnum(
                ArticleState,
                name="article_state",
                create_type=False,  # prevents SQLAlchemy from auto-creating the type on create_all()
            ),
            nullable=False,
            server_default=text("'NEW'")  # database-level default, not Python-side
        )
    )

    created_at: datetime | None = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()")
        )
    )

    media_content_id: uuid.UUID | None = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("media_content.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        )
    )

    media_content: "MediaContent" = Relationship(
        back_populates="article",
        sa_relationship_kwargs={"uselist": False},
    )
