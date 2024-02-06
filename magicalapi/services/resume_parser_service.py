"""
this file stores the implementation of resume parser Service.
https://magicalapi.com/services/resume-parser

"""

from typing import Type
from pydantic import BaseModel
from magicalapi.types.base import ErrorResponse
from magicalapi.types.schemas import HttpResponse
from magicalapi.types.resume_parser import ResumeParserResponse
from .base_service import BaseService


class ResumeParserService(BaseService):
    service_path = "/resume-parser"

    async def get_resume_parser(self, url: str) -> ResumeParserResponse | ErrorResponse:
        """this method sends request to resume parser service in magicalAPI.
        https://magicalapi.com/services/resume-parser

        url (``str``):
            the url of pdf resume file that you want parse it.

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