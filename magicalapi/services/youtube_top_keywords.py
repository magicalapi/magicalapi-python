from typing import Type
from pydantic import BaseModel
from magicalapi.types.base import ErrorResponse, PendingResponse
from magicalapi.types.youtube_top_keywords import YoutubeTopKeywordsResponse
from magicalapi.types.schemas import HttpResponse
from .base import BaseService


class YoutubeTopKeywords(BaseService):
    async def get_keywords(
        self, search_sentence: str, country: str, language: str, request_id: str = None
    ) -> YoutubeTopKeywordsResponse | ErrorResponse | PendingResponse:
        """this method sends request to Youtube Top Keywords service in magicalAPI.


        country (``str``):
            the country code of the country that you want to get keywords from.

        language (``str``):
            the language code of the language that you want to get keywords from.

        request_id (``str``, *optional*):
            the request_id if you have sent a request before and want to get response of it.
        """
        request_body = {
            "search_sentence": search_sentence,
            "country": country,
            "language": language,
        }
        if request_id:
            request_body["request_id"] = request_id

        response = await self._send_post_request("youtube-keywords", data=request_body)
        return self.validate_response(
            response=response, validate_model=YoutubeTopKeywordsResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: Type[BaseModel]
    ) -> YoutubeTopKeywordsResponse | ErrorResponse | PendingResponse:
        return super().validate_response(response, validate_model)
