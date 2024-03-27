"""
this file stores the implementation of Youtube Top Keywords Service.
https://magicalapi.com/services/youtube-keywords

"""

from typing import overload

from pydantic import BaseModel

from magicalapi.types.base import ErrorResponse
from magicalapi.types.company_data import CountriesResponse, LanguagesResponse
from magicalapi.types.schemas import HttpResponse
from magicalapi.types.youtube_top_keywords import YoutubeTopKeywordsResponse

from .base_service import BaseService


class YoutubeTopKeywordsService(BaseService):
    service_path = "youtube-keywords"

    @overload
    def validate_response(
        self,
        response: HttpResponse,
        validate_model: type[YoutubeTopKeywordsResponse],
    ) -> YoutubeTopKeywordsResponse | ErrorResponse:
        pass

    @overload
    def validate_response(
        self,
        response: HttpResponse,
        validate_model: type[CountriesResponse],
    ) -> CountriesResponse | ErrorResponse:
        pass

    @overload
    def validate_response(
        self,
        response: HttpResponse,
        validate_model: type[LanguagesResponse],
    ) -> LanguagesResponse | ErrorResponse:
        pass

    @overload
    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ) -> (
        YoutubeTopKeywordsResponse
        | LanguagesResponse
        | CountriesResponse
        | ErrorResponse
    ):
        pass

    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ) -> (
        YoutubeTopKeywordsResponse
        | LanguagesResponse
        | CountriesResponse
        | ErrorResponse
    ):
        return super().validate_response(response, validate_model)

    async def get_keywords(
        self, search_sentence: str, country: str, language: str
    ) -> YoutubeTopKeywordsResponse | ErrorResponse:
        """this method sends request to Youtube Top Keywords service in magicalAPI.
        https://magicalapi.com/services/youtube-keywords

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

        response = await self._send_post_request("/youtube-keywords", data=request_body)
        return self.validate_response(
            response=response, validate_model=YoutubeTopKeywordsResponse
        )

    async def get_countries(self) -> CountriesResponse | ErrorResponse:
        """this method retrives the supported
        countries list for Youtube Top Keywords service in magicalAPI.
        https://magicalapi.com/services/youtube-keywords

        """
        # get request
        response = await self._send_get_request(self.service_path + "/countries")
        return self.validate_response(
            response=response, validate_model=CountriesResponse
        )

    async def get_languages(self) -> LanguagesResponse | ErrorResponse:
        """this method retrives the supported
        languages list for Youtube Top Keywords service in magicalAPI.
        https://magicalapi.com/services/youtube-keywords

        """
        # get request
        response = await self._send_get_request(self.service_path + "/languages")
        return self.validate_response(
            response=response, validate_model=LanguagesResponse
        )
