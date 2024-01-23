from magicalapi.services.youtube_top_keywords import YoutubeTopKeywords
import httpx
from contextlib import AbstractAsyncContextManager

BASE_URL = "https://gw.magicalapi.com"


class AsyncClient(AbstractAsyncContextManager):
    """
    The MagicalAPI client module to work and connect to the api.
    """

    def __init__(self, api_key: str) -> None:
        """initializing MagicalAPI client.


        api_key(``str``):
            your Magical API account's `api_key` that you can get it from https://panel.magicalapi.com/

        """
        self._api_key = api_key
        _request_headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json",
        }
        self._httpx_client = httpx.AsyncClient(
            headers=_request_headers, base_url=BASE_URL
        )

        # create service
        self.youtube_top_keywords = YoutubeTopKeywords(httpx_client=self._httpx_client)

    @property
    def api_key(self):
        return self._api_key

    async def __aenter__(self):
        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback) -> bool | None:
        # http client
        await self._httpx_client.aclose()

    async def close(self):
        """
        close the client connection pool
        """
        # http client
        if not self._httpx_client.is_closed:
            await self._httpx_client.aclose()
