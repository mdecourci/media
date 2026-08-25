from pathlib import Path

from injectq import singleton

from app.config import mediaSourceSettings
from app.source.media_source import MediaSource


@singleton
class MediaFileSource(MediaSource):
    def __init__(self) -> None:
        self.folder_path = mediaSourceSettings.file

    async def _fetch_data(self) -> str:
        return self.folder_path.read_text(encoding="utf-8")
