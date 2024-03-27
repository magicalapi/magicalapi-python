"""
this file stores the implementation of resume review Service.
https://magicalapi.com/services/resume-review

"""

from pydantic import BaseModel

from magicalapi.types.base import ErrorResponse
from magicalapi.types.resume_review import ResumeReviewResponse
from magicalapi.types.schemas import HttpResponse

from .base_service import BaseService


class ResumeReviewService(BaseService):
    service_path = "resume-review"

    async def get_resume_review(self, url: str) -> ResumeReviewResponse | ErrorResponse:
        """this method sends request to resume review service in magicalAPI.
        https://magicalapi.com/services/resume-review

        url (``str``):
            the url of pdf resume file that you want review it.

        """
        request_body = {
            "url": url,
        }
        response = await self._send_post_request(self.service_path, data=request_body)
        return self.validate_response(
            response=response, validate_model=ResumeReviewResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ) -> ResumeReviewResponse | ErrorResponse:
        return super().validate_response(response, validate_model)
