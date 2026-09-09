from __future__ import annotations

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.persistence.model.entity_base import EntityBase


class MediaContent(EntityBase):
    __tablename__ = "media_content"

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    article: Mapped["Article"] = relationship(
        back_populates="media_content",
        uselist=False,
        lazy="selectin", )
