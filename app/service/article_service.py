from typing import Any

from app.repository.repository import Repository
from app.source.media_source import MediaSource


class ArticleService:
    def __init__(self, source: MediaSource, repository: Repository) -> None:
        self.source = source

    async def review(self) -> Any:
        async with self.source.get_data() as data:
            # process data here, still inside the managed context
            return data