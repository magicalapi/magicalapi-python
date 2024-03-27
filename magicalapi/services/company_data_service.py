"""
this file stores the implementation of company data Service.
https://magicalapi.com/services/company-data

"""

from pydantic import BaseModel

from magicalapi.types.base import ErrorResponse
from magicalapi.types.company_data import CompanyDataResponse
from magicalapi.types.schemas import HttpResponse

from .base_service import BaseService


class CompanyDataService(BaseService):
    service_path = "company-data"

    async def get_company_data(
        self, company_name: str
    ) -> CompanyDataResponse | ErrorResponse:
        """this method sends request to company data service in magicalAPI.
        https://magicalapi.com/services/company-data

        company_name (``str``):
            the username of linkedin company that you want to get it's data.

        """
        request_body = {
            "company_name": company_name,
        }
        response = await self._send_post_request(self.service_path, data=request_body)
        return self.validate_response(
            response=response, validate_model=CompanyDataResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ) -> CompanyDataResponse | ErrorResponse:
        return super().validate_response(response, validate_model)
