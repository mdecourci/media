import logging
import uuid
from uuid import UUID

from injectq import singleton

from app.persistence.model.workflow_context import WorkflowContext, WorkflowStatus, WorkflowStageStatus
from app.persistence.repository import workflow_repository
from app.persistence.repository.workflow_repository import WorkflowRepository
from app.workflow.workflow_engine import WorkFlowEngine

logger = logging.getLogger(__name__)


@singleton
class WorkFlowRunner():
    def __init__(self,
                 workflow_engine: WorkFlowEngine,
                 workflow_repository: WorkflowRepository):
        self.workflow_engine = workflow_engine
        self.workflow_repository = workflow_repository

    async def run(self):

        async with self.workflow_repository.transaction():
            context = WorkflowContext()
            context.workflow_id = uuid.uuid4()
            context.workflow_state = WorkflowStatus.CREATED
            context.current_workflow_stage_state = WorkflowStageStatus.NONE
            logger.info(f"Created workflow {context.workflow_id}")

            context = await self.workflow_repository.add(context)
            await self.workflow_engine.execute(context.workflow_id)

        logger.info(f"Finished workflow {context.workflow_id}")
