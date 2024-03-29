"""
types schem of youtube seo service

"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

from magicalapi.types.base import BaseModelValidated, BaseResponse, OptionalModel
from magicalapi.types.resume_parser import ResumeParser


class Duration(BaseModel):
    years: int | None = None
    months: int | None = None


class YearDate(BaseModel):
    year: int | str | None = None


@dataclass
class Resume:
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


class UpdatedParser(ResumeParser):
    project_experiences: list[Resume.ProjectExperience]
    work_experiences: list[Resume.Experience]
    educations: list[Resume.Education]


class ReviewItems(BaseModelValidated, OptionalModel):
    experiences: list[str]
    skills: list[str]
    format: list[str]
    contact: list[str]
    educations: list[str]
    summary: list[str]


class ResumeReview(BaseModel):
    score: int
    good: ReviewItems
    bad: ReviewItems
    details: UpdatedParser


class ResumeReviewResponse(BaseResponse):
    data: ResumeReview
