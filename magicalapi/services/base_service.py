"""
Base service implementations for sending requests and validating responses.

This module provides the base service class that handles HTTP communication
with the MagicalAPI server, including webhook support and retry logic.
"""

import asyncio
import json
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

from magicalapi.abstractions.base_service import BaseServiceAbc
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.settings import settings
from magicalapi.types.base import ErrorResponse
from magicalapi.types.schemas import (
    HttpResponse,
    PendingResponse,
    WebhookCreatedResponse,
)
from magicalapi.utils.logger import get_logger

logger = get_logger("base_service")


class BaseService(BaseServiceAbc):
    def __init__(
        self, httpx_client: httpx.AsyncClient, webhook_url: str | None = None
    ) -> None:
        """Initialize the base service.

        Args:
            httpx_client (httpx.AsyncClient): The HTTP client for making requests.
            webhook_url (str | None): Optional webhook URL for asynchronous responses.
                When provided, responses will be sent to this URL instead of being
                returned synchronously via the polling mechanism.

                Note: Webhook domain must be whitelisted in MagicalAPI panel.
                See https://docs.magicalapi.com/docs/webhook
        """
        self._httpx_client = httpx_client
        self._webhook_url = webhook_url

    async def _send_post_request(
        self, path: str, data: dict[str, Any], headers: dict[str, str] = {}
    ) -> HttpResponse:
        """Send a POST request to the API server.

        Args:
            path (str): The API endpoint path.
            data (dict[str, Any]): The request payload.
            headers (dict[str, str]): Optional request headers.

        Returns:
            HttpResponse: The response from the API server.

        Raises:
            APIServerTimedout: If the request exceeds the timeout limit.

        Note:
            - If webhook_url is configured, it will be added to the request payload
              and the method returns immediately without polling for completion.
            - If webhook_url is not configured, the method will poll for completion
              using the 201 status code retry mechanism with request_id.
            - Webhook domains must be whitelisted via MagicalAPI panel to avoid 403 errors.
              See https://docs.magicalapi.com/docs/webhook for setup instructions.
        """
        try:
            logger.debug(
                f"sending POST request : {self._httpx_client.base_url.join(path)}"
            )
            # Add webhook_url to request if configured (for async webhook delivery)
            if self._webhook_url is not None:
                logger.debug(f"Adding webhook_url to request: {self._webhook_url}")
                data["webhook_url"] = self._webhook_url

            httpx_response = await self._httpx_client.post(
                headers=headers,
                url=path,
                content=json.dumps(data),
            )
            logger.info(
                f"{self._httpx_client.base_url}{path} got status code {httpx_response.status_code}"
            )

            # Skip polling retry loop when using webhook (response will be sent to webhook_url)
            if self._webhook_url is not None:
                logger.debug("Webhook mode: returning immediately without polling")
                return HttpResponse(
                    text=httpx_response.text,
                    status_code=httpx_response.status_code,
                )

            _credits = 0
            # retry to get the full response
            while httpx_response.status_code == 201:
                # send request with request_id
                logger.debug("hadnling response with status code 201.")
                pend_response = PendingResponse.model_validate(httpx_response.json())
                # add creadits
                _credits += pend_response.usage.credits
                data["request_id"] = pend_response.data.request_id

                logger.info(
                    f'send request again with requst_id : "{data["request_id"]}"'
                )
                # send request again
                httpx_response = await self._httpx_client.post(
                    url=path,
                    content=json.dumps(data),
                )
                logger.info(
                    f"{self._httpx_client.base_url}{path} got status code {httpx_response.status_code}"
                )
                # send request again
                await asyncio.sleep(settings.retry_201_delay)

            # update crdits
            _response_text = httpx_response.text
            if "usage" in _response_text:
                data = json.loads(_response_text)
                data["usage"]["credits"] += _credits
                _response_text = json.dumps(data)

            return HttpResponse(
                text=_response_text,
                status_code=httpx_response.status_code,
            )
        except httpx.TimeoutException:
            logger.warning("POST request timedout.", exc_info=True)
            raise APIServerTimedout(
                "getting response from API server Timed Out, please try again later!"
            )

    async def _send_get_request(
        self, path: str, params: dict[str, str] | None = None
    ) -> HttpResponse:
        """
        send a get request to the API server with given `path` and `params`
        """
        try:
            logger.info(
                f"sending GET request : {self._httpx_client.base_url.join(path)}"
            )
            httpx_response = await self._httpx_client.get(url=path)
            return HttpResponse(
                text=httpx_response.text, status_code=httpx_response.status_code
            )
        except httpx.TimeoutException:
            logger.warning("GET request timedout.", exc_info=True)
            raise APIServerTimedout(
                "getting response from API server Timed Out, please try again later!"
            )

    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ):
        """Validate and parse the API response.

        Args:
            response (HttpResponse): The HTTP response to validate.
            validate_model (type[BaseModel]): The Pydantic model to validate against.

        Returns:
            BaseModel | ErrorResponse | WebhookCreatedResponse: The validated response model.
            - Returns validate_model instance for successful 200 responses
            - Returns WebhookCreatedResponse for 201 responses when using webhooks
            - Returns ErrorResponse for error status codes

        Raises:
            APIServerError: If response parsing or validation fails.
        """
        logger.debug("Validating response")
        logger.debug(f"Response: {response}")

        # Validate webhook acknowledgment response (201 with webhook_url)
        if response.status_code == 201 and self._webhook_url is not None:
            logger.debug("Validating webhook created response")
            return WebhookCreatedResponse.model_validate_json(response.text)

        # Validate successful response (200)
        if response.status_code == 200:
            try:
                # Validate and parse response with the expected model
                return validate_model.model_validate_json(response.text)
            except ValidationError:
                logger.exception(
                    f"Failed to parse response JSON for model {validate_model.__name__}"
                )
                raise APIServerError("Failed to parse response JSON data")

        # Handle API error responses (4xx, 5xx)
        try:
            logger.debug("Parsing error response")
            _response_data = json.loads(response.text)
            return ErrorResponse(status_code=response.status_code, **_response_data)

        except Exception:
            logger.error(f"response got an unexpected error : {response}")
            # raise exception
            raise APIServerError(
                "getting response from API server got error, please try again later!"
            )
