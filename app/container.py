# container.py
from injectq import InjectQ

from app.source.media_file_source import MediaFileSource
from app.source.media_source import MediaSource
from config import mediaSourceSettings

container = InjectQ.get_instance()


def create_media_file_source() -> MediaFileSource:
    return MediaFileSource(folder_path=mediaSourceSettings.file)


container.bind_factory(MediaFileSource, create_media_file_source)
container.bind(MediaSource, MediaFileSource)
