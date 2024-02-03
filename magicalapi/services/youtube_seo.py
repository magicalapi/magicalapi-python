"""
this file stores the implementation of youtube seo Service.

"""

from typing import Type
from pydantic import BaseModel
from magicalapi.types.base import ErrorResponse
from magicalapi.types.schemas import HttpResponse
from magicalapi.types.youtube_seo import YoutubeSeoResponse
from .base import BaseService


class YoutubeSeo(BaseService):
    service_path = "/youtube-seo"

    async def get_youtube_seo(self, url: str) -> YoutubeSeoResponse | ErrorResponse:
        """this method sends request to youtube seo service in magicalAPI.

        url (``str``):
            the URL of youtube video that you want to get it's seo data.

        """
        request_body = {
            "video_url": url,
        }
        response = await self._send_post_request(self.service_path, data=request_body)
        return self.validate_response(
            response=response, validate_model=YoutubeSeoResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: Type[BaseModel]
    ) -> YoutubeSeoResponse | ErrorResponse:
        return super().validate_response(response, validate_model)
