from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.config import databaseSettings
from app.container import container

engine = create_async_engine(databaseSettings.connection_string, echo=False)
session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Bind values directly — dict-style API
container[type(engine)] = engine


def create_session() -> AsyncSession:
    """Async factory — a new session per resolution."""
    return session_maker()


container.bind_factory(AsyncSession, create_session)
