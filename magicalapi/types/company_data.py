from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl, field_validator
from .base import BaseResponse, BaseModelValidated


class Product(BaseModelValidated):
    name: str
    link: Optional[HttpUrl]
    type: Optional[str]


class Company(BaseModelValidated):
    """
    The main type of company data service
    """

    url: HttpUrl
    company_name: str
    crawled_at: datetime
    name: str
    tagline: Optional[str]
    cover_image_url: HttpUrl
    logo_url: Optional[HttpUrl]
    employees: str
    followers: Optional[str]
    about: str
    # FIXME features
    website: Optional[str]
    industry: Optional[str]
    size: Optional[str]
    headquarters: Optional[str]
    organizationType: Optional[str]
    foundedOn: Optional[str]
    specialties: Optional[str]
    #
    locations: List[List[str]]
    products: List[Product]

    @field_validator("crawled_at", mode="before")
    @classmethod
    def datetime_validator(cls, value: str) -> datetime:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")


class CompanyDataResponse(BaseResponse):
    data: Company


class Language(BaseModel):
    name: str
    code: str


class Country(Language):
    ...


class LanguagesResponse(BaseResponse):
    data: list[Language]


class CountriesResponse(BaseResponse):
    data: list[Country]
