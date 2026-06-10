"""
types schema of Resume Matcher(Score) service
https://magicalapi.com/services/resume-score
"""

from __future__ import annotations

from magicalapi.types.resume_parser import ResumeParser

from .base import BaseModelValidated, BaseResponse
from typing import Literal
from pydantic import BaseModel

Category = Literal[
    "job",
    "education",
    "skills",
    "other",
]


class StrengthItem(BaseModelValidated):
    text: str | None
    category: Category


class ImprovementItem(BaseModelValidated):
    text: str | None
    category: Category


class ProsSchema(BaseModelValidated):
    type: str | None
    message: str | None


class ConsSchema(BaseModelValidated):
    type: str | None
    message: str | None


class WarnSchema(BaseModelValidated):
    type: str | None
    message: str | None


class JobMatchResponse(BaseModelValidated):
    score: int
    summary: str | None
    pros: list[ProsSchema]
    cons: list[ConsSchema]
    warns: list[WarnSchema]


class SkillGroups(BaseModelValidated):
    all_skills: list[str]


class SkillMatch(BaseModelValidated):
    miss_match: list[str]
    partial_match: list[str]
    strong_match: list[str]


class SkillMatchResponse(BaseModelValidated):
    score: int
    summary: str | None
    skills: SkillGroups
    match_result: SkillMatch


class EducationMatchResponse(BaseModelValidated):
    score: int
    summary: str | None
    pros: list[ProsSchema]
    cons: list[ConsSchema]
    warns: list[WarnSchema]


class MoreInformationResponse(BaseModelValidated):
    region: str | None
    overqualification_status: bool
    qualification_reason: str | None


class ScoreResponse(BaseModelValidated):
    score: int
    summary: str
    strengths: list[StrengthItem]
    improvements: list[ImprovementItem]
    job_match: JobMatchResponse
    skill_match: SkillMatchResponse
    education_match: EducationMatchResponse
    more_information: MoreInformationResponse
    jd_text: str | None


class ResumeScoreResponse(BaseResponse):
    """
    the main resposne schema for Resume Matcher(Score) service
    https://magicalapi.com/services/resume-score
    """

    data: ScoreResponse
