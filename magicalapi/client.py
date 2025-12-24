from contextlib import AbstractAsyncContextManager

import httpx

from magicalapi.services import (
    CompanyDataService,
    ProfileDataService,
    ResumeParserService,
    ResumeScoreService,
)
from magicalapi.services.resume_review_service import ResumeReviewService
from magicalapi.settings import settings
from magicalapi.utils.logger import get_logger

logger = get_logger("client")


class AsyncClient(AbstractAsyncContextManager):  # type: ignore
    """
    The MagicalAPI client module to work and connect to the api.
    """

    def __init__(
        self, api_key: str | None = None, webhook_url: str | None = None
    ) -> None:
        """Initialize the MagicalAPI async client.

        Args:
            api_key (str | None): Your Magical API account's API key from https://panel.magicalapi.com/
                If None, will be read from .env file or MAG_API_KEY environment variable.

            webhook_url (str | None): Optional webhook URL to receive asynchronous responses.
                When provided, API responses will be sent to this URL instead of using
                the polling mechanism. If None, will be read from MAG_WEBHOOK_URL environment
                variable. The webhook listener must be implemented by the user.

                **IMPORTANT**: Your webhook domain must be registered in the whitelist via
                the MagicalAPI panel. Unregistered domains will receive a 403 error.
                See https://docs.magicalapi.com/docs/webhook for complete setup guide.

        Raises:
            TypeError: If api_key is not a string or None.
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

        # get webhook_url from settings if not provided
        if webhook_url is None:
            webhook_url = settings.webhook_url

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
        self.profile_data = ProfileDataService(
            httpx_client=self._httpx_client, webhook_url=webhook_url
        )
        self.company_data = CompanyDataService(
            httpx_client=self._httpx_client, webhook_url=webhook_url
        )
        self.resume_parser = ResumeParserService(
            httpx_client=self._httpx_client, webhook_url=webhook_url
        )
        self.resume_score = ResumeScoreService(
            httpx_client=self._httpx_client, webhook_url=webhook_url
        )
        self.resume_review = ResumeReviewService(
            httpx_client=self._httpx_client, webhook_url=webhook_url
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
