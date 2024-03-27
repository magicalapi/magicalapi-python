"""
types schem of resume score service
https://magicalapi.com/services/resume-score
"""

from __future__ import annotations

from .base import BaseModelValidated, BaseResponse


class Captions(BaseModelValidated):
    captions: list[str]


class Titles(BaseModelValidated):
    titles: list[str]


class Hashtags(BaseModelValidated):
    hashtags: list[str]


class Keywords(BaseModelValidated):
    keywords: list[str]


class YoutubeSuggestionsResponse(BaseResponse):
    """
    the main resposne schema for resume score service
    https://magicalapi.com/services/resume-score
    """

    data: Captions | Titles | Hashtags | Keywords
