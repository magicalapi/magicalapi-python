"""
this file stores the implementation of youtube suggestions Service.
https://magicalapi.com/services/youtube-suggestions

"""

from typing import Literal

from pydantic import BaseModel

from magicalapi.types.base import ErrorResponse
from magicalapi.types.schemas import HttpResponse
from magicalapi.types.youtube_suggestions import YoutubeSuggestionsResponse

from .base_service import BaseService


class YoutubeSuggestionsService(BaseService):
    service_path = "youtube-suggestions"

    async def get_youtube_suggestions(
        self,
        prompt_sentence: str,
        count: int,
        suggestion_goal: Literal["caption", "title", "hashtag", "tag"],
    ) -> YoutubeSuggestionsResponse | ErrorResponse:
        """this method sends request to youtube suggestions service in magicalAPI.
        https://magicalapi.com/services/youtube-suggestions

        prompt_sentence (``str``):
            your prompt sentence to get suggestions based on it

        count (``int``)
            the number of results

        suggestion_goal (``str``):
            the goal that you want to get suggestions about it, one of `caption`, `title`, `hashtag`, `tag`

        """
        request_body = {
            "prompt_sentence": prompt_sentence,
            "count": count,
            "suggestion_goal": suggestion_goal,
        }
        response = await self._send_post_request(self.service_path, data=request_body)
        return self.validate_response(
            response=response, validate_model=YoutubeSuggestionsResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ) -> YoutubeSuggestionsResponse | ErrorResponse:
        return super().validate_response(response, validate_model)
