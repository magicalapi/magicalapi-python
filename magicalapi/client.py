from magicalapi.services.profile_data import ProfileData
from magicalapi.services.youtube_top_keywords import YoutubeTopKeywords
from magicalapi.settings import settings
import httpx
from contextlib import AbstractAsyncContextManager


class AsyncClient(AbstractAsyncContextManager):  # type: ignore
    """
    The MagicalAPI client module to work and connect to the api.
    """

    def __init__(self, api_key: str) -> None:
        """initializing MagicalAPI client.


        api_key(``str``):
            your Magical API account's `api_key` that you can get it from https://panel.magicalapi.com/

        """

        if type(api_key) != str:
            raise TypeError(
                f'api_key field type must be string, not a "{api_key.__class__.__name__}"'
            )

        self._api_key = api_key
        _request_headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json",
        }
        self._httpx_client = httpx.AsyncClient(
            headers=_request_headers,
            base_url=str(settings.base_url),
            timeout=settings.request_timeout,
        )

        # create service
        self.youtube_top_keywords = YoutubeTopKeywords(httpx_client=self._httpx_client)
        self.profile_data = ProfileData(httpx_client=self._httpx_client)

    @property
    def api_key(self):
        return self._api_key

    async def __aenter__(self):
        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback) -> bool | None:  # type: ignore
        # http client
        await self._httpx_client.aclose()

    async def close(self):
        """
        close the client connection pool
        """
        # http client
        if not self._httpx_client.is_closed:
            await self._httpx_client.aclose()
