import pytest
from magicalapi.client import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_client_context_manager():
    fake_api_key = str(uuid4())

    async with AsyncClient(api_key=fake_api_key) as client:
        # check httpx client is open
        assert not client._httpx_client.is_closed

    # check httpx client is closed
    assert client._httpx_client.is_closed
