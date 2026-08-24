import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class MediaSource(ABC):
    """MediaSource base class for all data sources. Services depend on this,
    never on concrete subclasses."""

    async def get_content(self) -> Any:
        """
        Public entry point — services call this as:
            data = await source.get_content()
        Error handling and cleanup are hidden here, uniform across every source type.
        """
        try:
            data = await self._fetch_data()
            return data
        except Exception:
            logger.exception("Failed to fetch data from source: %s", type(self).__name__)
            raise
        finally:
            await self._cleanup()

    @abstractmethod
    async def _fetch_data(self) -> Any:
        """Subclasses implement the actual source-specific retrieval here."""
        raise NotImplementedError

    # @abstractmethod
    async def _cleanup(self) -> None:
        """Default no-op. Override if the source holds a resource that needs releasing."""
        return None
