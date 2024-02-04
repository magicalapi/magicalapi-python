"""
types schem of resume parser service 
https://magicalapi.com/services/resume-parser
"""

from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, HttpUrl
from .base import BaseModelValidated, BaseResponse


class Resume:
    class Basic(BaseModelValidated):
        first_name: str
        last_name: str
        email: str
        phone_number: str
        location: str
        portfolio_website_url: Optional[HttpUrl] = None
        linkedin_url: Optional[HttpUrl] = None
        github_url: Optional[HttpUrl] = None
        university: str
        graduation_year: str
        majors: str

    class Experience(BaseModel):
        title: str
        company: str
        location: Optional[str]
        duration: Optional[str]
        summary: Optional[str]

    class Project(BaseModel):
        title: str
        description: Optional[str]

    class Education(BaseModel):
        school: str
        degree: Optional[str]
        field: Optional[str]
        start: Optional[str]
        end: Optional[str]

    class Certification(BaseModel):
        title: str
        provider: Optional[str]

    class Language(BaseModel):
        name: str

    class Skill(BaseModel):
        name: str


class ResumeParser(BaseModel):
    basic: Resume.Basic
    summary: str
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
