# container.py

from injectq import InjectQ
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import databaseSettings
from app.source.file_media_adapter import FileMediaAdapter
from app.source.base_media_source import BaseMediaSource

container = InjectQ.get_instance()

engine = create_async_engine(databaseSettings.database_url, echo=False)
session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Bind values directly — dict-style API
container[type(engine)] = engine

def create_session() -> AsyncSession:
    """Async factory — a new session per resolution."""
    print("create_session")
    return session_maker()


def create_media_file_source() -> FileMediaAdapter:
    print("Creating MediaFileSource")
    return FileMediaAdapter()


session = create_session()
media_file_source = create_media_file_source()

container[type(session)] = session
print("Container has AsyncSession")
container[type(media_file_source)] = media_file_source
print("Container has  MediaFileSource")

container.bind(BaseMediaSource, FileMediaAdapter)
