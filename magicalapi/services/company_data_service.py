"""
this file stores the implementation of company data Service.
https://magicalapi.com/services/company-data

"""

from pydantic import BaseModel

from magicalapi.types.base import ErrorResponse
from magicalapi.types.company_data import CompanyDataResponse
from magicalapi.types.schemas import HttpResponse, WebhookCreatedResponse

from .base_service import BaseService

API_VERSION = 1


class CompanyDataService(BaseService):
    service_path = "company-data"

    async def get_company_data(
        self,
        company_username: str | None = None,
        company_name: str | None = None,
        company_website: str | None = None,
    ) -> CompanyDataResponse | WebhookCreatedResponse | ErrorResponse:
        """this method sends request to company data service in magicalAPI.
        https://magicalapi.com/services/company-data

        company_name (``str``):
            the username of linkedin company that you want to get it's data.

        Returns:
            CompanyDataResponse: When request completes successfully (no webhook).
            WebhookCreatedResponse: When using webhook_url (immediate acknowledgment).
            ErrorResponse: When an error occurs (e.g., 403 if webhook domain not whitelisted).

        """
        # check which parameters passed
        if company_username is not None:
            request_body = {
                "company_username": company_username,
            }
        elif all((company_name, company_website)):
            request_body = {
                "company_website": company_website,
                "company_name": company_name,
            }
        elif company_website is not None:
            request_body = {
                "company_website": company_website,
            }
        elif company_name is not None:
            request_body = {
                "company_name": company_name,
            }
        else:
            raise ValueError(
                "one of 3 paramters company_username, company_name, company_website at least should be passed !"
            )

        request_headers = {
            "version": str(API_VERSION),
        }
        response = await self._send_post_request(
            self.service_path, data=request_body, headers=request_headers
        )
        return self.validate_response(
            response=response, validate_model=CompanyDataResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ) -> CompanyDataResponse | WebhookCreatedResponse | ErrorResponse:
        return super().validate_response(response, validate_model)
