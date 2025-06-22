"""
types schem of resume review service

"""

from __future__ import annotations

from pydantic import BaseModel

from magicalapi.types.base import BaseModelValidated, BaseResponse, OptionalModel


class ReviewCons(BaseModelValidated):
    message: str
    tips: list[str]


class ReviewItem(BaseModelValidated):
    pros: list[str]
    cons: list[ReviewCons]


class SuggestedItem(BaseModelValidated):
    content: str | None


class ReviewItems(BaseModelValidated, OptionalModel):
    experiences: ReviewItem
    skills: ReviewItem
    format: ReviewItem
    contact: ReviewItem
    educations: ReviewItem
    summary: ReviewItem


class SuggestedItems(BaseModelValidated, OptionalModel):
    experiences: SuggestedItem
    skills: SuggestedItem
    format: SuggestedItem
    contact: SuggestedItem
    educations: SuggestedItem
    summary: SuggestedItem


class ResumeReview(BaseModel):
    score: int
    result: ReviewItems
    suggested: SuggestedItems


class ResumeReviewResponse(BaseResponse):
    data: ResumeReview
