import json
import httpx
import logging
from pydantic import BaseModel
from typing import Type
from magicalapi.client import AsyncClient
from urllib.parse import urljoin
from magicalapi.errors import APIServerError, APIServerTimedout

from magicalapi.types.base import ErrorResponse, MessageResponse, PendingResponse

BASE_URL = "https://gw.magicalapi.com"
logging.basicConfig(level=logging.INFO)


class BaseService:
    def __init__(self, client: AsyncClient) -> None:
        self.client = client
        self._request_headers = {
            "api-key": self.client.api_key,
            "Content-Type": "application/json",
        }

    async def _send_post_request(self, path: str, body: dict) -> httpx.Response:
        """
        send a post request to the API server with the api_key and given `path` and `body`
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=urljoin(base=BASE_URL, url=path),
                    data=json.dumps(body),
                    headers=self._request_headers,
                    timeout=15,
                )
                return response
        except httpx.TimeoutException:
            raise APIServerTimedout(
                "getting response from API server Timed Out, please try again later!"
            )

    async def _send_get_request(self, path: str) -> httpx.Response:
        """
        send a get request to the API server with the api_key and given `path`
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=urljoin(base=BASE_URL, url=path), headers=self._request_headers
            )
            return response

    def validate_response(
        self, response: httpx.Response, validate_model: Type[BaseModel]
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
            _response_data = response.json()

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