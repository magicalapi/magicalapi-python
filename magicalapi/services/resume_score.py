"""
this file stores the implementation of resume score Service.
https://magicalapi.com/services/resume-score

"""

from typing import Type
from pydantic import BaseModel
from magicalapi.types.base import ErrorResponse
from magicalapi.types.schemas import HttpResponse
from magicalapi.types.resume_score import ResumeScoreResponse
from .base import BaseService


class ResumeScore(BaseService):
    service_path = "/resume-score"

    async def get_resume_score(
        self, url: str, job_description: str
    ) -> ResumeScoreResponse | ErrorResponse:
        """this method sends request to resume score service in magicalAPI.
        https://magicalapi.com/services/resume-score

        url (``str``):
            the url of pdf resume file that you want get it's data.

        job_description (``str``):
            give some description of the job,
            your resume score will calculate based on your job description.

        """
        request_body = {
            "url": url,
            "job_description": job_description,
        }
        response = await self._send_post_request(self.service_path, data=request_body)
        return self.validate_response(
            response=response, validate_model=ResumeScoreResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: Type[BaseModel]
    ) -> ResumeScoreResponse | ErrorResponse:
        return super().validate_response(response, validate_model)
