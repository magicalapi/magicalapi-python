"""
types schem of youtube seo service

"""

from __future__ import annotations

from pydantic import BaseModel

from magicalapi.types.base import BaseModelValidated, BaseResponse, OptionalModel
from magicalapi.types.resume_parser import ResumeParser


class ReviewItem(BaseModelValidated):
    good: list[str] = []
    bad: list[str] = []


class ReviewItems(BaseModelValidated, OptionalModel):
    experiences: ReviewItem
    skills: ReviewItem
    format: ReviewItem
    contact: ReviewItem
    educations: ReviewItem
    summary: ReviewItem


class ResumeReview(BaseModel):
    score: int
    result: ReviewItems
    details: ResumeParser


class ResumeReviewResponse(BaseResponse):
    data: ResumeReview
