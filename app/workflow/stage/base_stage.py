import logging
import uuid
from abc import abstractmethod, ABC

from app.persistence.model.workflow_context import WorkflowContext, WorkflowStages, WorkflowStageStatus, WorkflowStatus
from app.persistence.repository.workflow_repository import WorkflowRepository

logger = logging.getLogger(__name__)

class BaseStage(ABC):
    def __init__(self, workflow_repository: WorkflowRepository) -> None:
        self.workflow_repository = workflow_repository

    async def execute(self, workflow_context: WorkflowContext) :
        logger.debug(f"Executing stage {self.name()} .. started")
        logger.info(f"Running workflow {workflow_context.workflow_id} with stage {self.name()}")

        workflow_context.workflow_state = WorkflowStatus.RUNNING
        workflow_context.current_workflow_stage = self.name()
        workflow_context.current_workflow_stage_state = WorkflowStageStatus.RUNNING
        await self.workflow_repository.add(workflow_context)

        try:
            await self._execute_stage(workflow_context)
        except Exception as exc:
            error_message = f"Error executing stage {self.name()} in workflow with id {workflow_context.workflow_id}: {exc}"
            logger.error(error_message)
            failed_context = workflow_context.clone_model()

            failed_context.current_workflow_stage_state = WorkflowStageStatus.FAILED
            failed_context.errors.append(error_message)
            await self.workflow_repository.add(failed_context)

            raise

        next_context = workflow_context.clone_model()

        next_context.current_workflow_stage_state = WorkflowStageStatus.COMPLETED
        await self.workflow_repository.add(next_context)
        logger.debug(f"Executing stage {self.name()} .. completed")

    @abstractmethod
    async def _execute_stage(self, workflow_context: WorkflowContext):
        pass

    async def _rollback(self, workflow_id) -> None:
        pass

    @abstractmethod
    def name(self) -> WorkflowStages:
        pass

    async def _get_new_workflow_context(self, workflow_id) -> WorkflowContext:
        context = await self.workflow_repository.find_one_by(
            workflow_id=workflow_id
        )
        next_context = context.clone_model()
        next_context.current_workflow_stage = self.name()
        return next_context
