import asyncio
import json
import httpx
import logging
from pydantic import BaseModel
from typing import Any, Type
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.types.base import ErrorResponse
from magicalapi.abstractions.base_service import BaseServiceAbc
from magicalapi.types.schemas import HttpResponse, PendingResponse

logging.basicConfig(level=logging.INFO)

RETRY_201_DELAY = 2  # seconds


class BaseService(BaseServiceAbc):
    def __init__(self, httpx_client: httpx.AsyncClient) -> None:
        self._httpx_client = httpx_client

    async def _send_post_request(self, path: str, data: dict[str, Any]) -> HttpResponse:
        """
        send a post request to the API server with given `path` and `data`
        """
        try:
            httpx_response = await self._httpx_client.post(
                url=path,
                content=json.dumps(data),
            )
            # check 201 response
            _credits = 0
            while httpx_response.status_code == 201:
                # send request with request_id
                pend_response = PendingResponse.model_validate(httpx_response.json())
                _credits += pend_response.usage.credits
                data["request_id"] = pend_response.data.request_id
                httpx_response = await self._httpx_client.post(
                    url=path,
                    content=json.dumps(data),
                    timeout=15,
                )
                # send request again
                await asyncio.sleep(RETRY_201_DELAY)

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
            httpx_response = await self._httpx_client.get(url=path)
            return HttpResponse.model_validate(obj=httpx_response, from_attributes=True)
        except httpx.TimeoutException:
            raise APIServerTimedout(
                "getting response from API server Timed Out, please try again later!"
            )

    def validate_response(
        self, response: HttpResponse, validate_model: Type[BaseModel]
    ):
        """
        this method validate the response from API and returns the correct model basesd on response type.
        """
        # check response successed
        if response.status_code == 200:
            return validate_model.model_validate_json(response.text)

        # handle user error response
        try:
            # error response
            _response_data = json.loads(response.text)
            return ErrorResponse.model_validate(_response_data)

        except:
            # raise exception
            raise APIServerError(
                "getting response from API server got error, please try again later!"
            )
