import logging

from injectq import singleton

from app.persistence.model.workflow_context import WorkflowContext, WorkflowStatus, WorkflowStages, WorkflowStageStatus
from app.persistence.repository.workflow_repository import WorkflowRepository
from app.workflow.stage.stage_factory import StageFactory

logger = logging.getLogger(__name__)

@singleton
class WorkFlowEngine:

    def __init__(
            self,
            factory: StageFactory,
            workflow_repository: WorkflowRepository
    ):
        self.factory = factory
        self.workflow_repository = workflow_repository

    async def execute(
            self,
            workflow_id,
    ) -> WorkflowContext:
        logger.info(f"Executing workflow {workflow_id}")

        while True:

            current_stage = self.factory.get_next_stage()
            if current_stage is None:
                break

            context = await self.workflow_repository.find_one_by(workflow_id=workflow_id)
            context = context.clone_model()
            context.workflow_state = WorkflowStatus.STARTED
            await self.workflow_repository.add(context)

            try:
                await current_stage.execute(context)

                context = context.clone_model()
                context.workflow_state = WorkflowStatus.COMPLETED
                context.current_workflow_stage = WorkflowStages.NONE
                context.current_workflow_stage_state = WorkflowStageStatus.NONE
                await self.workflow_repository.add(context)

            except Exception as exc:
                error_message = f"Error executing workflow {workflow_id}: {exc}"
                logger.error(error_message)

                context = context.clone_model()
                context.workflow_state = WorkflowStatus.FAILED
                context.current_workflow_stage = WorkflowStages.NONE
                context.current_workflow_stage_state = WorkflowStageStatus.NONE
                context.errors.append(error_message)

                await self.workflow_repository.add(context)
                return context

        logger.info(f"Finished workflow {workflow_id}")

        return context
