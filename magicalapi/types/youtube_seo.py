"""
types schem of youtube seo service 

"""

from __future__ import annotations
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, HttpUrl
from magicalapi.types.base import BaseResponse


class YoutubeAPI:
    # youtube api video response schema
    class PageInfo(BaseModel):
        totalResults: int
        resultsPerPage: int

    class Thumbnail(BaseModel):
        url: HttpUrl
        width: int
        height: int

    class Thumbnails(BaseModel):
        default: YoutubeAPI.Thumbnail
        medium: YoutubeAPI.Thumbnail
        high: YoutubeAPI.Thumbnail
        standard: Optional[YoutubeAPI.Thumbnail] = None
        maxres: Optional[YoutubeAPI.Thumbnail] = None

    class Localized(BaseModel):
        title: str
        description: str

    class Snippet(BaseModel):
        publishedAt: datetime
        channelId: str
        title: str
        description: str
        thumbnails: YoutubeAPI.Thumbnails
        channelTitle: str
        categoryId: str
        liveBroadcastContent: str
        defaultLanguage: Optional[str] = None
        localized: YoutubeAPI.Localized
        defaultAudioLanguage: Optional[str] = None
        tags: list[str]

    class contentDetails(BaseModel):
        duration: str
        dimension: str
        definition: Literal["hd", "sd"]
        caption: Literal["true", "false"]
        licensedContent: bool
        # TODO ensure empty always
        # contentRating:
        projection: str

    class status(BaseModel):
        uploadStatus: str
        privacyStatus: str
        license: str
        embeddable: bool
        publicStatsViewable: bool
        madeForKids: bool

    class statistics(BaseModel):
        viewCount: int
        likeCount: int
        favoriteCount: int
        commentCount: int

    class VideoItem(BaseModel):
        kind: str
        etag: str
        id: str
        snippet: YoutubeAPI.Snippet
        contentDetails: YoutubeAPI.contentDetails
        status: YoutubeAPI.status
        statistics: YoutubeAPI.statistics

    class VideoDetails(BaseModel):
        kind: str
        etag: str
        # TODO keep only the first item video
        items: list[YoutubeAPI.VideoItem]
        pageInfo: YoutubeAPI.PageInfo


class SeoItems(BaseModel):
    title: Optional[list[str]] = None
    description: Optional[list[str]] = None
    video_quality: Optional[list[str]] = None
    thumbnail: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    hashtags: Optional[list[str]] = None


class YoutubeSeo(BaseModel):
    score: int
    good: SeoItems
    bad: SeoItems
    details: YoutubeAPI.VideoDetails


class YoutubeSeoResponse(BaseResponse):
    data: YoutubeSeo
