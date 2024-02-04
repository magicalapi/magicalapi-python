"""
this file stores the implementation of profile data Service.
https://magicalapi.com/services/resume-parser

"""

from typing import Type
from pydantic import BaseModel
from magicalapi.types.base import ErrorResponse
from magicalapi.types.schemas import HttpResponse
from magicalapi.types.resume_parser import ResumeParserResponse
from .base import BaseService


class ResumeParser(BaseService):
    service_path = "/resume-parser"

    async def get_resume_parser(self, url: str) -> ResumeParserResponse | ErrorResponse:
        """this method sends request to profile data service in magicalAPI.
        https://magicalapi.com/services/resume-parser

        url (``str``):
            the username of linkedin profile that you want to get it's data.

        """
        request_body = {
            "url": url,
        }
        response = await self._send_post_request(self.service_path, data=request_body)
        return self.validate_response(
            response=response, validate_model=ResumeParserResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: Type[BaseModel]
    ) -> ResumeParserResponse | ErrorResponse:
        return super().validate_response(response, validate_model)
