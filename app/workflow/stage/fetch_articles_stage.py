import logging
import uuid

from injectq import singleton

from app.persistence.model.workflow_context import WorkflowContext, WorkflowStages
from app.persistence.repository.workflow_repository import WorkflowRepository
from app.workflow.stage.base_stage import BaseStage
from app.container import container
from app.service.article_service import ArticleService

logger = logging.getLogger(__name__)

@singleton
class FetchArticlesStage(BaseStage):
    def __init__(self, workflow_repository: WorkflowRepository, article_service: ArticleService) -> None:
        super().__init__(workflow_repository)
        self.article_service = article_service

    # Import the container configuration first so that all
    # dependency bindings are registered.
    from app.container import container
    from app.service.article_service import ArticleService
    async def _execute_stage(self, context: WorkflowContext):
        logger.info(f"context is {vars(context)} and stage {self.name()}")

        await self.article_service.find_articles()

        return context.workflow_id

    def name(self) -> WorkflowStages:
        return WorkflowStages.FETCH
