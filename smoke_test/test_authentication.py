import pytest

from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse


@pytest.mark.asyncio
async def test_user_unauthorized(fake_client: AsyncClient):
    # test send request to server with not valid api key
    response = await fake_client.youtube_seo.get_youtube_seo(url="https://example.com/")
    assert all(
        (
            isinstance(response, ErrorResponse),
            response.usage.credits == 0,
            response.status_code == 401,
            hasattr(response, "message"),
        )
    )
