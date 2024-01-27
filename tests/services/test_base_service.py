import json
import httpx
import pytest
import pytest_asyncio
from magicalapi.errors import APIServerTimedout
from magicalapi.services.base import BaseService
from magicalapi.types.schemas import HttpResponse


@pytest_asyncio.fixture(scope="function")
async def httpxclient():
    # base url is empty
    client = httpx.AsyncClient(headers={"content-type": "application/json"}, timeout=5)

    yield client

    await client.aclose()
    del client


@pytest.mark.asyncio
async def test_base_service_post_request(httpxclient):
    base_service = BaseService(httpxclient)
    test_data = {"foo": "bar"}

    response = await base_service._send_post_request(
        path="https://httpbin.org/post", data=test_data
    )
    # check response type
    assert isinstance(response, HttpResponse)
    # check status code
    assert response.status_code == 200
    # check data transfered
    assert json.loads(response.text)["json"] == test_data


@pytest.mark.asyncio
async def test_base_service_get_request(httpxclient):
    base_service = BaseService(httpxclient)
    response = await base_service._send_get_request(path="https://httpbin.org/get")

    # check response type
    assert isinstance(response, HttpResponse)
    # check status code
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_base_service_request_timed_out(httpxclient):
    base_service = BaseService(httpxclient)
    # change in fixture timeout

    # post request
    with pytest.raises(APIServerTimedout):
        await base_service._send_post_request(
            path="https://httpbin.org/delay/6", data={}
        )
    # gee request
    with pytest.raises(APIServerTimedout):
        await base_service._send_get_request(path="https://httpbin.org/delay/6")
