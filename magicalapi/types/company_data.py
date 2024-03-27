from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator

from .base import BaseModelValidated, BaseResponse


class Product(BaseModelValidated):
    name: str
    link: HttpUrl | None
    type: str | None


class Company(BaseModelValidated):
    """
    The main type of company data service
    """

    url: HttpUrl
    company_name: str
    crawled_at: datetime
    name: str
    tagline: str | None
    cover_image_url: HttpUrl
    logo_url: HttpUrl | None
    employees: str
    followers: str | None
    #
    about: str | None
    website: str | None
    industry: str | None
    size: str | None
    headquarters: str | None
    organizationType: str | None
    foundedOn: str | None
    specialties: str | None
    #
    locations: list[list[str]]
    products: list[Product]

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
    pass


class LanguagesResponse(BaseResponse):
    data: list[Language]


class CountriesResponse(BaseResponse):
    data: list[Country]
