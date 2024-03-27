"""
types schem of resume score service
https://magicalapi.com/services/resume-score
"""

from __future__ import annotations

from .base import BaseModelValidated, BaseResponse


class ResumeScore(BaseModelValidated):
    score: int
    reason: str


class ResumeScoreResponse(BaseResponse):
    """
    the main resposne schema for resume score service
    https://magicalapi.com/services/resume-score
    """

    data: ResumeScore
