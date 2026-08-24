from typing import Any

import httpx
from app.source.media_source import MediaSource

class MediaRestSource(MediaSource):
    def __init__(self, url: str) -> None:
        self.url = url
        self._client: httpx.AsyncClient | None = None

    async def _fetch_data(self) -> dict[str, Any]:
        self._client = httpx.AsyncClient()
        response = await self._client.get(self.url)
        response.raise_for_status()
        return response.json()

    async def _cleanup(self) -> None:
        if self._client is not None:
            await self._client.aclose()