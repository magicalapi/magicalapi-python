"""
types schem of resume parser service
https://magicalapi.com/services/resume-parser
"""

# from __future__ import annotations

from dataclasses import dataclass

from .base import BaseModelValidated, BaseResponse, OptionalModel


class Duration(BaseModelValidated):
    years: int | None = None
    months: int | None = None


class YearDate(BaseModelValidated):
    year: int | str | None = None


@dataclass
class Resume:
    class Basic(BaseModelValidated, OptionalModel):
        first_name: str
        last_name: str
        email: str
        phone_number: str
        location: str
        portfolio_website_url: str
        linkedin_url: str
        github_url: str
        university: str
        graduation_year: str
        majors: str

    class ProjectExperience(BaseModelValidated, OptionalModel):
        title: str | None
        description: str | None

    class Experience(BaseModelValidated, OptionalModel):
        title: str
        company: str
        location: str
        duration: Duration | None = None
        summary: str

    class Education(BaseModelValidated, OptionalModel):
        school: str
        degree: str
        field: str
        start: YearDate | None = None
        end: YearDate | None = None

    class Certification(BaseModelValidated, OptionalModel):
        title: str
        provider: str

    class Language(BaseModelValidated, OptionalModel):
        name: str

    class Skill(BaseModelValidated, OptionalModel):
        name: str


class ResumeParser(BaseModelValidated):
    basic: Resume.Basic
    summary: str | None
    project_experiences: list[Resume.ProjectExperience]
    work_experiences: list[Resume.Experience]
    educations: list[Resume.Education]
    certifications: list[Resume.Certification]
    languages: list[Resume.Language]
    skills: list[Resume.Skill]


class ResumeParserResponse(BaseResponse):
    """
    the main resposne schema for resume parser service
    https://magicalapi.com/services/resume-parser
    """

    data: ResumeParser
