from __future__ import annotations

import enum
from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    Enum,
    ForeignKey,
    TIMESTAMP, func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.persistence.model.entity_base import EntityBase
from app.persistence.model.media_content import MediaContent


class ArticleState(str, enum.Enum):
    NEW = "NEW"
    REVIEWING = "REVIEWING"
    SUMMARIZED = "SUMMARIZED"
    RETRIED = "RETRIED"
    FAILED = "FAILED"


class Article(EntityBase):
    __tablename__ = "article"

    article_state: Mapped[ArticleState] = mapped_column(
        Enum(
            ArticleState,
            name="article_state",
        ),
        nullable=False,
        default=ArticleState.NEW,
    )

    media_content_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "media_content.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    media_content: Mapped["MediaContent"] = relationship(
        back_populates="article",
        uselist=False,
        lazy="selectin",
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
