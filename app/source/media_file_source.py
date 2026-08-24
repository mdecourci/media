from pathlib import Path

from injectq import singleton

from app.source.media_source import MediaSource


@singleton
class MediaFileSource(MediaSource):
    def __init__(self, folder_path: Path) -> None:
        self.folder_path = folder_path

    async def _fetch_data(self) -> list[str]:
        return [f.name for f in self.folder_path.iterdir() if f.is_file()]
