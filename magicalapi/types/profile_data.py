from datetime import date, datetime

from pydantic import BaseModel, HttpUrl, field_validator

from .base import BaseModelValidated, BaseResponse, OptionalModel


class StartEndDate(BaseModelValidated):
    start_date: date | None
    end_date: date | None

    # validating the dates in format %b %Y ,Example : Jan 2024
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def date_validator(cls, value: str) -> date | None:
        if not value:
            return None
        return datetime.strptime(value, "%b %Y").date()


class StartEndDateEducation(StartEndDate):
    # validating the dates in format %Y,Example : 2024
    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def date_validator(cls, value: str) -> date | None:
        if not value:
            return None
        return datetime.strptime(value, "%Y").date()


class Duration(BaseModel):
    years: int = 0
    months: int


class StartEndDurationDate(StartEndDate):
    duration: Duration | None


class Experience(BaseModelValidated, OptionalModel):
    image_url: HttpUrl | None
    title: str | None
    company_name: str
    company_link: HttpUrl | None
    date: StartEndDurationDate | None
    location: str | None
    description: str | None


class Education(BaseModelValidated):
    image_url: HttpUrl | None
    university_name: str
    university_link: HttpUrl | None
    degree: str
    major: str
    date: StartEndDateEducation | None


class Certification(BaseModelValidated):
    image_url: HttpUrl | None
    title: str
    course_link: HttpUrl | None
    issuer: str
    credential: str | None
    issued_date: date | None

    @field_validator("issued_date", mode="before")
    @classmethod
    def date_validator(cls, value: str) -> date | None:
        if not value:
            return None
        return datetime.strptime(value, "%b %Y").date()


class Language(BaseModelValidated):
    name: str
    description: str | None


class Volunteering(BaseModelValidated):
    role: str
    organization: str | None
    volunteering_link: HttpUrl | None
    date: StartEndDurationDate | None
    cause: str | None
    description: str | None


class Publication(BaseModelValidated):
    title: str | None
    publisher: str | None
    publication_link: HttpUrl | None
    publication_date: str | None
    description: str | None


class Project(BaseModelValidated):
    name: str
    date: StartEndDate | None
    description: str | None


class Course(BaseModelValidated):
    name: str
    number: str | None


class HonorAndAward(BaseModelValidated):
    title: str
    issuer: str
    issued_date: date | None
    description: str | None

    @field_validator("issued_date", mode="before")
    @classmethod
    def date_validator(cls, value: str) -> date | None:
        if not value:
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
    description: str | None
    location: str | None
    followers: str | None
    connections: str | None
    experience: list[Experience]
    education: list[Education]
    certifications: list[Certification]
    languages: list[Language]
    volunteerings: list[Volunteering]
    publications: list[Publication]
    projects: list[Project]
    courses: list[Course]
    honors_and_awards: list[HonorAndAward]

    @field_validator("crawled_at", mode="before")
    @classmethod
    def datetime_validator(cls, value: str) -> datetime:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")


class ProfileDataResponse(BaseResponse):
    data: Profile
