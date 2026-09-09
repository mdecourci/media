from injectq import singleton

from app.workflow.stage.base_stage import WorkflowStages
from app.workflow.stage.discover_articles_stage import DiscoverArticlesStage
from app.workflow.stage.fetch_articles_stage import FetchArticlesStage


@singleton
class StageFactory:
    def __init__(
            self,
            discover_articles_stage: DiscoverArticlesStage,
            fetch_articles_stage: FetchArticlesStage,
    ) -> None:
        self.workflow_stages = [
            (WorkflowStages.DISCOVER, discover_articles_stage),
            (WorkflowStages.FETCH, fetch_articles_stage),
            # (WorkFlowStages.NORMALISE, NormalizeArticlesStage()),
            # (WorkFlowStages.DEDUPLICATE, DeduplicateArticlesStage()),
            # (WorkFlowStages.ENTITY_RESOLUTION, ResolutionStage()),
            # (WorkFlowStages.ENRICH, EnrichmentStage()),
            # (WorkFlowStages.PENDING_REVIEW, PendingReviewStage()),
        ]
        self.initial_stage = self.workflow_stages[0]
        self.current_stage = None

    def get_next_stage(self):
        if self.current_stage is None:
            self.current_stage = self.initial_stage
            return self.current_stage[1]

        next_stage = next(
            (self.workflow_stages[i + 1]
             for i, (key, _) in enumerate(self.workflow_stages)
             if key == self.current_stage[0] and i + 1 < len(self.workflow_stages)),
            None
        )
        self.current_stage = next_stage
        if self.current_stage is None:
            return None
        return self.current_stage[1]
