from pydantic import BaseModel

from .base import BaseResponse


class KeywordIdeaMonth(BaseModel):
    month: str
    year: int
    monthly_searches: int


class KeywordIdea(BaseModel):
    keyword: str
    search_volume: int
    competition: str
    competition_index: int
    low_top_of_page_bid_micros: int
    high_top_of_page_bid_micros: int
    average_cpc: str
    monthly_search: list[KeywordIdeaMonth]


class Keywords(BaseModel):
    keywords: list[KeywordIdea]


class YoutubeTopKeywordsResponse(BaseResponse):
    """respone model of profile data service"""

    data: Keywords
