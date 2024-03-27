"""
types schem of resume parser service
https://magicalapi.com/services/resume-parser
"""

from __future__ import annotations

from .base import BaseModelValidated, BaseResponse, OptionalModel


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

    class Experience(BaseModelValidated, OptionalModel):
        title: str
        company: str
        location: str
        duration: str
        summary: str

    class Education(BaseModelValidated, OptionalModel):
        school: str
        degree: str
        field: str
        start: str
        end: str

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
