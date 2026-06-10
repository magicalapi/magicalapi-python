from datetime import datetime

from pydantic import field_validator

from .base import BaseModelValidated, BaseResponse, OptionalModel


class StartEndDate(BaseModelValidated):
    # Example: "Jan 2024" or "2024-01" or "Present"
    start_date: int | str | None
    end_date: int | str | None

    # validating the dates in format %b %Y ,Example : Jan 2024
    # @field_validator("start_date", "end_date", mode="before")
    # @classmethod
    # def date_validator(cls, value: str) -> date | None:
    #     if not value:
    #         return None
    #     formats = [
    #         "%b %Y",
    #         "%Y-%m",
    #     ]
    #     while True:
    #         date_format = formats.pop(0)
    #         try:
    #             return datetime.strptime(str(value), date_format).date()
    #         except Exception as e:
    #             if not formats:
    #                 raise e
    #


class StartEndDateEducation(StartEndDate):
    pass
    # validating the dates in format %Y,Example : 2024
    # @field_validator("start_date", "end_date", mode="before")
    # @classmethod
    # def date_validator(cls, value: str) -> date | None:
    #     if not value:
    #         return None
    #     formats = [
    #         "%Y",
    #         "%b %Y",
    #         "%Y-%m",
    #     ]
    #     while True:
    #         date_format = formats.pop(0)
    #         try:
    #             return datetime.strptime(str(value), date_format).date()
    #         except Exception as e:
    #             if not formats:
    #                 raise e


class Duration(BaseModelValidated):
    years: int = 0
    months: int = 0


class StartEndDurationDate(StartEndDate):
    duration: Duration | None


class Experience(BaseModelValidated, OptionalModel):
    title: str | None
    company_name: str | None
    company_link: str | None
    image_url: str | None
    date: StartEndDurationDate | None
    location: str | None
    description: str | None


class Education(BaseModelValidated):
    university_name: str | None
    university_link: str | None
    image_url: str | None
    degree: str | None
    major: str | None
    date: StartEndDate | None


class Certification(BaseModelValidated):
    image_url: str | None
    title: str | None
    course_link: str | None
    issuer: str | None
    credential: str | None
    issued_date: str | None


class Language(BaseModelValidated):
    name: str | None
    description: str | None


class Volunteering(BaseModelValidated):
    role: str | None
    organization: str | None
    volunteering_link: str | None
    date: StartEndDurationDate | None
    cause: str | None
    description: str | None


class Publication(BaseModelValidated):
    title: str | None
    publisher: str | None
    publication_link: str | None
    publication_date: str | None
    description: str | None


class Project(BaseModelValidated):
    name: str | None
    date: StartEndDate | None
    description: str | None


class Course(BaseModelValidated):
    name: str | None
    number: str | None


class HonorAndAward(BaseModelValidated):
    title: str | None
    issuer: str | None
    issued_date: str | None
    description: str | None


class Activity(BaseModelValidated):
    title: str | None
    subtitle: str | None
    image_url: str | None
    link: str | None


class SimilarProfile(BaseModelValidated):
    url: str | None
    name: str | None
    title: str | None
    image_url: str | None


class Patent(BaseModelValidated):
    title: str | None
    patent_id: str | None
    link: str | None


class Profile(BaseModelValidated):
    """
    The main type of LinkedIn Profile Scraper service
    """

    url: str
    profile: str
    crawled_at: datetime
    name: str | None
    headline: str | None
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

    activities: list[Activity]
    similar_profiles: list[SimilarProfile]
    patents: list[Patent]

    @field_validator("crawled_at", mode="before")
    @classmethod
    def datetime_validator(cls, value: str) -> datetime:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")


class ProfileDataResponse(BaseResponse):
    data: Profile
