"""
types schem of youtube seo service

"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

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
        standard: YoutubeAPI.Thumbnail | None = None
        maxres: YoutubeAPI.Thumbnail | None = None

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
        defaultLanguage: str | None = None
        localized: YoutubeAPI.Localized
        defaultAudioLanguage: str | None = None
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
        commentCount: int | None

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


class SeoItem(BaseModel):
    good: list[str] = []
    bad: list[str] = []


class SeoItems(BaseModel):
    title: SeoItem
    description: SeoItem
    tags: SeoItem
    video_quality: SeoItem
    comments: SeoItem


class LongVideoSeoItems(SeoItems):
    thumbnail: SeoItem


class ShortVideoSeoItems(SeoItems):
    pass


class YoutubeSeo(BaseModel):
    score: int
    result: LongVideoSeoItems | ShortVideoSeoItems
    details: YoutubeAPI.VideoDetails


class YoutubeSeoResponse(BaseResponse):
    data: YoutubeSeo
