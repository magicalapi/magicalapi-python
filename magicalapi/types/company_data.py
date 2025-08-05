from datetime import datetime
from datetime import date
from typing import TypeAlias

from pydantic import BaseModel, HttpUrl, field_validator

from .base import BaseModelValidated, BaseResponse

URL: TypeAlias = str


class Product(BaseModelValidated):
    name: str | None
    link: URL | None  # link of product in linkedin.com
    url: URL | None  # url of product
    about: str | None
    used_for: list[str]
    customers: list[URL]


class Employee(BaseModelValidated):
    title: str | None
    subtitle: str | None
    link: str | None
    image_url: URL | None


class SimilarCompany(BaseModelValidated):
    title: str | None
    subtitle: str | None
    location: str | None
    link: str | None


class Post(BaseModelValidated):
    text: str | None

    post_url: URL | None
    post_id: str | None
    time: str | None
    videos: list[str]
    images: list[str]
    likes_count: int | None
    comments_count: int | None


class Investor(BaseModelValidated):
    name: str | None
    link: str | None
    image_url: URL | None


class FundingRound(BaseModelValidated):
    date: date | None
    type: str | None
    raised_amount: str | None


class Funding(BaseModelValidated):
    last_round: FundingRound | None
    rounds_count: int | None
    investors: list[Investor]
    crunchbase_url: URL | None


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
    products: list[Product]
    locations: list[list[str]]
    #
    employees_at_linkedin: list[Employee]
    similar_companies: list[SimilarCompany]
    funding: Funding
    posts: list[Post]

    @field_validator("crawled_at", mode="before")
    @classmethod
    def datetime_validator(cls, value: str) -> datetime:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")


class CompanyDataResponse(BaseResponse):
    data: Company
