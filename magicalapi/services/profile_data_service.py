"""
this file stores the implementation of profile data Service.
https://magicalapi.com/services/profile-data

"""

from pydantic import BaseModel

from magicalapi.types.base import ErrorResponse
from magicalapi.types.profile_data import ProfileDataResponse
from magicalapi.types.schemas import HttpResponse

from .base_service import BaseService

API_VERSION = 1


class ProfileDataService(BaseService):
    service_path = "profile-data"

    async def get_profile_data(
        self, profile_name: str
    ) -> ProfileDataResponse | ErrorResponse:
        """this method sends request to profile data service in magicalAPI.
        https://magicalapi.com/services/profile-data

        profile_name (``str``):
            the username of linkedin profile that you want to get it's data.

        """
        request_body = {
            "profile_name": profile_name,
        }
        request_headers = {
            "version": str(API_VERSION),
        }
        response = await self._send_post_request(
            self.service_path, data=request_body, headers=request_headers
        )
        return self.validate_response(
            response=response, validate_model=ProfileDataResponse
        )

    def validate_response(
        self, response: HttpResponse, validate_model: type[BaseModel]
    ) -> ProfileDataResponse | ErrorResponse:
        return super().validate_response(response, validate_model)  # type:ignore
