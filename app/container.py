# container.py
from injectq import InjectQ
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import databaseSettings
from app.source.media_file_source import MediaFileSource
from app.source.media_source import MediaSource
from app.config import mediaSourceSettings

container = InjectQ.get_instance()

engine = create_async_engine(databaseSettings.database_url, echo=False)
session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Bind values directly — dict-style API
container[type(engine)] = engine


def create_session() -> AsyncSession:
    """Async factory — a new session per resolution."""
    return session_maker()


container.bind_factory(AsyncSession, create_session)
print("Container has  AsyncSession")
container = InjectQ.get_instance()


def create_media_file_source() -> MediaFileSource:
    return MediaFileSource(folder_path=mediaSourceSettings.file)


container.bind_factory(MediaFileSource, create_media_file_source)
container.bind(MediaSource, MediaFileSource)

print("Container has  MediaFileSource")
