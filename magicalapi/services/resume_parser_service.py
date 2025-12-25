"""
this file stores the implementation of resume parser Service.
https://magicalapi.com/services/resume-parser

"""

from pydantic import BaseModel

from magicalapi.types.base import ErrorResponse
from magicalapi.types.resume_parser import ResumeParserResponse
from magicalapi.types.schemas import HttpResponse, WebhookCreatedResponse

from .base_service import BaseService

API_VERSION = 1


class ResumeParserService(BaseService):
    service_path = "resume-parser"

    async def get_resume_parser(
        self, url: str
    ) -> ResumeParserResponse | WebhookCreatedResponse | ErrorResponse:
        """this method sends request to resume parser service in magicalAPI.
        https://magicalapi.com/services/resume-parser

        url (``str``):
            the url of pdf resume file that you want parse it.

        Returns:
            ResumeParserResponse: When request completes successfully (no webhook).
            WebhookCreatedResponse: When using webhook_url (immediate acknowledgment).
            ErrorResponse: When an error occurs (e.g., 403 if webhook domain not whitelisted).

        """
        request_body = {
            "url": url,
        }
        request_headers = {
            "version": str(API_VERSION),
        }
        response = await self._send_post_request(
            self.service_path, data=request_body, headers=request_headers
        )
        return self.validate_response(
            response=response, validate_model=ResumeParserResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ) -> ResumeParserResponse | WebhookCreatedResponse | ErrorResponse:
        return super().validate_response(response, validate_model)
