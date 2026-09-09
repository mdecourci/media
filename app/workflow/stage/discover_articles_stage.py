import logging
import uuid
from uuid import UUID

from injectq import singleton

from app.persistence.model.workflow_context import WorkflowContext
from app.persistence.repository.workflow_repository import WorkflowRepository
from app.workflow.stage.base_stage import BaseStage, WorkflowStages

logger = logging.getLogger(__name__)

@singleton
class DiscoverArticlesStage(BaseStage):
    def __init__(self, workflow_repository: WorkflowRepository) -> None:
        super().__init__(workflow_repository)

    async def _execute_stage(self, context: WorkflowContext):
        print(f"context is {vars(context)} and stage {self.name()}")
        raise Exception("Not implemented")
        return context.workflow_id

    def name(self) -> WorkflowStages:
        return WorkflowStages.DISCOVER
