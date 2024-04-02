from uuid import uuid4

import pytest

from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse
from magicalapi.types.youtube_seo import YoutubeSeoResponse


@pytest.mark.asyncio
async def test_video_not_found(client: AsyncClient):
    # test api returns 404 error for not found video
    response = await client.youtube_seo.get_youtube_seo(
        url=f"https://youtube.com/watch?v={uuid4()}"
    )

    assert all(
        (
            isinstance(response, ErrorResponse),
            response.status_code == 404,
        )
    )


@pytest.mark.asyncio
async def test_video_url_is_invalid(client: AsyncClient):
    # test api returns 400 error for invalid video url
    response = await client.youtube_seo.get_youtube_seo(url="https://example.com")

    assert all(
        (
            isinstance(response, ErrorResponse),
            response.status_code == 400,  # bad request
        )
    )


@pytest.mark.asyncio
async def test_video_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.youtube_seo.get_youtube_seo(
        url="https://www.youtube.com/watch?v=PZZI1QXlM80"
    )

    assert isinstance(response, YoutubeSeoResponse)
