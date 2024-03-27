from contextlib import AbstractAsyncContextManager

import httpx

from magicalapi.services import (
    CompanyDataService,
    ProfileDataService,
    ResumeParserService,
    ResumeScoreService,
    YoutubeSeoService,
    YoutubeSuggestionsService,
    YoutubeTopKeywordsService,
)
from magicalapi.services.resume_review_service import ResumeReviewService
from magicalapi.settings import settings
from magicalapi.utils.logger import get_logger

logger = get_logger("client")


class AsyncClient(AbstractAsyncContextManager):  # type: ignore
    """
    The MagicalAPI client module to work and connect to the api.
    """

    def __init__(self, api_key: str | None = None) -> None:
        """initializing MagicalAPI client.


        api_key(``str``):
            your Magical API account's `api_key` that you can get it from https://panel.magicalapi.com/

            if passed empty, `api_key` will read from the .env file.

        """

        # get api_key from .env or from arguments
        # prefer reading api_key from arguments
        if api_key is None:
            # load from .env
            api_key = settings.api_key

        if not isinstance(api_key, str):
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
        logger.debug("httpx client created")

        # create service
        self.youtube_top_keywords = YoutubeTopKeywordsService(
            httpx_client=self._httpx_client
        )
        self.profile_data = ProfileDataService(httpx_client=self._httpx_client)
        self.company_data = CompanyDataService(httpx_client=self._httpx_client)
        self.youtube_seo = YoutubeSeoService(httpx_client=self._httpx_client)
        self.resume_parser = ResumeParserService(httpx_client=self._httpx_client)
        self.resume_score = ResumeScoreService(httpx_client=self._httpx_client)
        self.resume_review = ResumeReviewService(httpx_client=self._httpx_client)
        self.youtube_suggestions = YoutubeSuggestionsService(
            httpx_client=self._httpx_client
        )

        logger.debug(f"async client created : {self}")

    @property
    def api_key(self):
        return self._api_key

    async def __aenter__(self):
        logger.debug("async client opened.")
        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback) -> bool | None:  # type: ignore
        await self.close()

    async def close(self):
        """
        close the client connection pool
        """
        # http client
        if not self._httpx_client.is_closed:
            await self._httpx_client.aclose()
        logger.debug("async client closed.")
