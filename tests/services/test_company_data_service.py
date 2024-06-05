from uuid import uuid4

import pytest

from magicalapi.client import AsyncClient


@pytest.mark.asyncio
async def test_get_company_data_parameters():
    # test pass invalid parameters to get_company_data function
    fake_api_key = str(uuid4())
    with pytest.raises(ValueError):
        async with AsyncClient(api_key=fake_api_key) as client:
            await client.company_data.get_company_data()

    # None parameters
    with pytest.raises(ValueError):
        async with AsyncClient(api_key=fake_api_key) as client:
            await client.company_data.get_company_data(company_username=None)
