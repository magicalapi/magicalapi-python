import json
import httpx
import logging
from pydantic import BaseModel
from typing import Any, Type
from contextlib import AbstractAsyncContextManager
from magicalapi.client import AsyncClient
from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.types.base import ErrorResponse, MessageResponse, PendingResponse
from magicalapi.abstractions.base_service import BaseServiceAbc
from magicalapi.types.schemas import HttpResponse

BASE_URL = "https://gw.magicalapi.com"
logging.basicConfig(level=logging.INFO)


class BaseService(BaseServiceAbc, AbstractAsyncContextManager):
    def __init__(self, client: AsyncClient) -> None:
        self.client = client
        _request_headers = {
            "api-key": self.client.api_key,
            "Content-Type": "application/json",
        }
        self._httpx_client = httpx.AsyncClient(
            headers=_request_headers, base_url=BASE_URL
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._httpx_client.aclose()

    async def _send_post_request(self, path: str, data: dict[str, Any]) -> HttpResponse:
        """
        send a post request to the API server with given `path` and `data`
        """
        try:
            httpx_response = await self._httpx_client.post(
                url=path,
                content=json.dumps(data),
                timeout=15,
            )
            return HttpResponse.model_validate(obj=httpx_response, from_attributes=True)
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

        httpx_response = await self._httpx_client.get(url=path)
        return HttpResponse.model_validate(obj=httpx_response, from_attributes=True)

    def validate_response(
        self, response: HttpResponse, validate_model: Type[BaseModel]
    ):
        """
        this method validate the response from API and returns the correct model basesd on response type.
        """
        # check response successed
        if response.status_code == 200:
            return validate_model.model_validate_json(response.text)
        # check 201 response
        if response.status_code == 201:
            return PendingResponse.model_validate_json(response.text)

        # handle user error response
        try:
            _response_data = json.loads(response.text)

            # usage field in response
            if "usage" in _response_data:
                return ErrorResponse.model_validate(_response_data)

            # only message
            return MessageResponse.model_validate(_response_data)
        except:
            # raise exception
            raise APIServerError(
                "getting response from API server got error, please try again later!"
            )
