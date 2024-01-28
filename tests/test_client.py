import pytest
from magicalapi.client import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_client_context_manager():
    fake_api_key = str(uuid4())

    async with AsyncClient(api_key=fake_api_key) as client:
        # check httpx client is open
        assert not client._httpx_client.is_closed
        # check api_key property
        assert client.api_key == fake_api_key

    # check httpx client is closed
    assert client._httpx_client.is_closed


def test_client_empty_api_key():
    with pytest.raises(TypeError):
        AsyncClient()


def test_client_invalid_api_key_type():
    with pytest.raises(TypeError):
        AsyncClient(api_key={})


@pytest.mark.asyncio
async def test_client_close_connection_pool():
    client = AsyncClient(api_key=str(uuid4()))
    await client.close()
    assert client._httpx_client.is_closed
