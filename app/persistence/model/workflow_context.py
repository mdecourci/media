from __future__ import annotations

from sqlalchemy import inspect

import enum
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    Enum, func, TIMESTAMP, String, inspect,
)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.persistence.model.entity_base import EntityBase

class WorkflowStageStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    NONE = "NONE"

class WorkflowStatus(str, enum.Enum):
    STARTED = "STARTED"
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class WorkflowStages(str, enum.Enum):
    NONE = "NONE"
    DISCOVER = "DISCOVER"
    FETCH = "FETCH"
    NORMALISE = "NORMALISE"
    DEDUPLICATE = "DEDUPLICATE"
    ENTITY_RESOLUTION = "ENTITY_RESOLVED"
    ENRICH = "ENRICH"
    PENDING_REVIEW = "REVIEW"
    # PUBLISH = "PUBLISH"

class WorkflowContext(EntityBase):
    __tablename__ = "workflow_context"

    workflow_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=False,
        nullable=False,
        index=True,
    )

    workflow_state: Mapped[WorkflowStatus] = mapped_column(
        Enum(
            WorkflowStatus,
            name="workflow_state",
        ),
        nullable=False)

    current_workflow_stage: Mapped[WorkflowStages] = mapped_column(
        Enum(
            WorkflowStages,
            name="workflow_stage",
        ),
        nullable=False,
        default=WorkflowStages.NONE,
    )

    current_workflow_stage_state: Mapped[WorkflowStageStatus] = mapped_column(
        Enum(
            WorkflowStageStatus,
            name="workflow_stage_status",
        ),
        nullable=True
    )

    # topic_id: Mapped[str] = mapped_column(nullable=True)
    context_metadata: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=True,
        default=dict
    )

    # article_ids: Mapped[list[str]] = mapped_column(
    #     ARRAY(str),
    #     nullable=True,
    #     default=list
    # )
    # insight_ids: Mapped[list[str]] = mapped_column(
    #     ARRAY(str),
    #     nullable=True,
    #     default=list
    # )

    errors: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=True,
        default=list
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def clone_model(obj):
        cls = type(obj)

        data = {
            c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs
            if c.key != "id" and
               c.key != "created_at" and
               c.key != "updated_at"
        }

        return cls(**data)
