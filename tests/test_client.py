import os
from uuid import uuid4

import pytest

import magicalapi.client
from magicalapi.client import AsyncClient
from magicalapi.settings import Settings, settings


@pytest.fixture(scope="session", autouse=True)
def api_key_env_var():
    # override environment variables
    _fake_api_key = str(uuid4())
    os.environ["MAG_API_KEY"] = _fake_api_key

    return os.environ["MAG_API_KEY"]


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
    # ensure environment variables not set
    settings.api_key = None

    with pytest.raises(TypeError):
        AsyncClient()


def test_client_load_api_key_environment_variables(api_key_env_var: str):
    # mock settings manager
    # reload settings
    magicalapi.client.settings = Settings()
    client = AsyncClient()
    assert client.api_key == api_key_env_var


def test_client_invalid_api_key_type():
    with pytest.raises(TypeError):
        AsyncClient(api_key={})


@pytest.mark.asyncio
async def test_client_close_connection_pool():
    client = AsyncClient(api_key=str(uuid4()))
    await client.close()
    assert client._httpx_client.is_closed
