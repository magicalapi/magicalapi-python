"""
base service implementations,
sending requests and validating the responses.

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
from magicalapi.types.schemas import HttpResponse, PendingResponse
from magicalapi.utils.logger import get_logger

logger = get_logger("base_service")


class BaseService(BaseServiceAbc):
    def __init__(self, httpx_client: httpx.AsyncClient) -> None:
        self._httpx_client = httpx_client

    async def _send_post_request(
        self, path: str, data: dict[str, Any], headers: dict[str, str] = {}
    ) -> HttpResponse:
        """
        send a post request to the API server with given `path` and `data`
        """
        try:
            logger.debug(
                f"sending POST request : {self._httpx_client.base_url.join(path)}"
            )
            httpx_response = await self._httpx_client.post(
                headers=headers,
                url=path,
                content=json.dumps(data),
            )
            logger.info(
                f"{self._httpx_client.base_url}{path} got status code {httpx_response.status_code}"
            )
            # check 201 response
            _credits = 0
            while httpx_response.status_code == 201:
                # send request with request_id
                logger.debug("hadnling response with status code 201.")
                pend_response = PendingResponse.model_validate(httpx_response.json())
                # add creadits
                _credits += pend_response.usage.credits
                data["request_id"] = pend_response.data.request_id

                logger.info(
                    f"send request again with requst_id : \"{data['request_id']}\""
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
        """
        this method validate the response from API and returns the correct model basesd on response type.
        """
        # check response successed
        logger.debug("validating response.")
        logger.debug(f"response : {response}")
        if response.status_code == 200:
            try:
                # valdiate model
                return validate_model.model_validate_json(response.text)
            except ValidationError:
                logger.exception(
                    f"parsing response JSON data for model {validate_model.__name__} failed!"
                )
                # raise exception
                raise APIServerError("parsing response JSON data failed!")

        # handle user error response
        try:
            # error response
            logger.debug("response returned an error response.")
            _response_data = json.loads(response.text)
            return ErrorResponse.model_validate(_response_data)

        except Exception:
            logger.error(f"response got an unexpected error : {response}")
            # raise exception
            raise APIServerError(
                "getting response from API server got error, please try again later!"
            )
