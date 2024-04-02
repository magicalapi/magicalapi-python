import pytest

from magicalapi.client import AsyncClient
from magicalapi.types.youtube_top_keywords import YoutubeTopKeywordsResponse


@pytest.mark.asyncio
async def test_youtube_keywords_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.youtube_top_keywords.get_keywords(
        search_sentence="minecraft", language="1000", country="1"
    )

    assert isinstance(response, YoutubeTopKeywordsResponse)
