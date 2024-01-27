from datetime import date, datetime
from typing import Any, List, Optional
from pydantic import BaseModel, HttpUrl, field_validator
from .base import BaseResponse, BaseModelValidated


class StartEndDate(BaseModelValidated):
    start_date: date
    end_date: Optional[date]

    # validating the dates in format %b %Y ,Example : Jan 2024
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def date_validator(cls, value: str) -> date | None:
        if value == "":
            return None
        return datetime.strptime(value, "%b %Y").date()


class StartEndDateEducation(StartEndDate):
    # validating the dates in format %Y,Example : 2024
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def date_validator(cls, value: str) -> date | None:
        if value == "":
            return None
        return datetime.strptime(value, "%Y").date()


class Duration(BaseModel):
    years: int = 0
    months: int


class StartEndDurationDate(StartEndDate):
    duration: Optional[Duration]


class Experience(BaseModelValidated):
    image_url: Optional[HttpUrl]
    title: str
    company_name: str
    company_link: Optional[HttpUrl]
    date: Optional[StartEndDurationDate]
    location: Optional[str]
    description: Optional[str]


class Education(BaseModelValidated):
    image_url: Optional[HttpUrl]
    university_name: str
    university_link: Optional[HttpUrl]
    degree: str
    major: str
    date: Optional[StartEndDateEducation]


class Certification(BaseModelValidated):
    image_url: Optional[HttpUrl]
    title: str
    course_link: Optional[HttpUrl]
    issuer: str
    credential: Optional[str]
    issued_date: Optional[date]

    @field_validator("issued_date", mode="before")
    @classmethod
    def date_validator(cls, value: str) -> date | None:
        if value == "":
            return None
        return datetime.strptime(value, "%b %Y").date()


class Language(BaseModelValidated):
    name: str
    description: str


class Volunteering(BaseModelValidated):
    role: str
    organization: str
    volunteering_link: Optional[HttpUrl]
    date: Optional[StartEndDurationDate]
    cause: Optional[str]
    description: str


class Publication(BaseModelValidated):
    title: str
    publisher: str
    publication_link: Optional[HttpUrl]
    publication_date: str
    description: str


class Project(BaseModelValidated):
    name: str
    date: Optional[StartEndDate]
    description: str


class Course(BaseModelValidated):
    name: str
    number: Optional[str]


class HonorAndAward(BaseModelValidated):
    title: str
    issuer: str
    issued_date: Optional[date]
    description: str

    @field_validator("issued_date", mode="before")
    @classmethod
    def date_validator(cls, value: str) -> date | None:
        if value == "":
            return None
        return datetime.strptime(value, "%b %Y").date()


class Profile(BaseModelValidated):
    """
    The main type of linkedin profile data service
    """

    url: HttpUrl
    profile: str
    crawled_at: datetime
    name: str
    description: str
    location: str
    followers: str
    connections: str
    experience: List[Experience]
    education: List[Education]
    certifications: List[Certification]
    languages: List[Language]
    volunteerings: List[Volunteering]
    publications: List[Publication]
    projects: List[Project]
    courses: List[Course]
    honors_and_awards: List[HonorAndAward]

    @field_validator("crawled_at", mode="before")
    @classmethod
    def datetime_validator(cls, value: str) -> datetime:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")


class ProfileDataResponse(BaseResponse):
    data: Profile
