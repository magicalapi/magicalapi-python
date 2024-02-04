"""
types schem of resume parser service 
https://magicalapi.com/services/resume-parser
"""

from __future__ import annotations
from typing import Optional
from pydantic import HttpUrl
from .base import OptionalModel, BaseResponse, BaseModelValidated


class Resume:
    class Basic(BaseModelValidated, OptionalModel):
        first_name: str
        last_name: str
        email: str
        phone_number: str
        location: str
        portfolio_website_url: HttpUrl
        linkedin_url: HttpUrl
        github_url: HttpUrl
        university: str
        graduation_year: str
        majors: str

    class Experience(BaseModelValidated, OptionalModel):
        title: str
        company: str
        location: str
        duration: str
        summary: str

    class Project(BaseModelValidated, OptionalModel):
        title: str
        description: str

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
    summary: Optional[str]
    work_experiences: list[Resume.Experience]
    project_experiences: list[Resume.Project]
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
