import logging
import uuid

from injectq import singleton
from sqlalchemy.ext.asyncio import AsyncSession

from app.persistence.model.workflow_context import WorkflowContext, WorkflowStatus
from app.persistence.repository.repository import Repository


@singleton
class WorkflowRepository(Repository[WorkflowContext]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, WorkflowContext)
