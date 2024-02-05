"""
types schem of youtube seo service 

"""

from __future__ import annotations
from pydantic import BaseModel
from magicalapi.types.resume_parser import ResumeParser
from magicalapi.types.base import BaseModelValidated, BaseResponse, OptionalModel


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
    details: ResumeParser


class ResumeReviewResponse(BaseResponse):
    data: ResumeReview
