import asyncio
from uuid import uuid4

import pytest
import pytest_asyncio

from magicalapi.client import AsyncClient


@pytest_asyncio.fixture()
async def fake_client():
    # create an instance of magicalAPI AsyncClient
    client = AsyncClient(api_key=str(uuid4()))

    yield client
    # close connection
    await client.close()


@pytest_asyncio.fixture(scope="function")
async def client():
    # create an instance of magicalAPI AsyncClient
    async with AsyncClient() as client:  # loads api_key from .env
        yield client
