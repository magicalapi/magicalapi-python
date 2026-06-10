import json
from collections.abc import AsyncGenerator
from random import randint

import httpx
import pytest
import pytest_asyncio

from magicalapi.errors import APIServerError, APIServerTimedout
from magicalapi.services.base_service import BaseService
from magicalapi.types.base import ErrorResponse
from magicalapi.types.resume_score import ResumeScoreResponse
from magicalapi.types.schemas import HttpResponse


def _make_mock_transport(*, timeout_on_delay: bool = False) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        if timeout_on_delay and request.url.path.endswith("/delay/10"):
            raise httpx.TimeoutException("request timed out", request=request)

        if request.method == "POST":
            body = json.loads(request.content.decode()) if request.content else {}
            return httpx.Response(200, json={"json": body}, request=request)

        if request.method == "GET":
            return httpx.Response(200, json={"url": str(request.url)}, request=request)

        return httpx.Response(405, json={"message": "method not allowed"}, request=request)

    return httpx.MockTransport(handler)


@pytest_asyncio.fixture(scope="function")
async def httpxclient(request) -> AsyncGenerator[httpx.AsyncClient]:
    timeout = (
        request.param
        if hasattr(request, "param") and isinstance(request.param, int | float)
        else None
    )

    # base url is empty
    client = httpx.AsyncClient(
        headers={"content-type": "application/json"},
        timeout=timeout,
        transport=_make_mock_transport(timeout_on_delay=timeout is not None),
    )

    yield client

    await client.aclose()
    del client


@pytest.mark.asyncio
async def test_base_service_post_request(httpxclient: httpx.AsyncClient):
    base_service = BaseService(httpxclient)
    test_data = {"foo": "bar"}

    response = await base_service._send_post_request(
        path="https://example.com/post", data=test_data
    )
    # check response type
    assert isinstance(response, HttpResponse)
    # check status code
    assert response.status_code == 200
    # check data transfered
    assert json.loads(response.text)["json"] == test_data


@pytest.mark.asyncio
async def test_base_service_get_request(httpxclient: httpx.AsyncClient):
    base_service = BaseService(httpxclient)
    response = await base_service._send_get_request(path="https://example.com/get")

    # check response type
    assert isinstance(response, HttpResponse)
    # check status code
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize("httpxclient", [4.0], indirect=True)
async def test_base_service_request_timed_out(httpxclient: httpx.AsyncClient):
    base_service = BaseService(httpxclient)
    # change in fixture timeout

    # post request
    with pytest.raises(APIServerTimedout):
        await base_service._send_post_request(
            path="https://example.com/delay/10", data={}
        )
    # gee request
    with pytest.raises(APIServerTimedout):
        await base_service._send_get_request(path="https://example.com/delay/10")


def test_base_service_validating_response(httpxclient: httpx.AsyncClient):
    # test validating base service valida_response method
    base_service = BaseService(httpxclient)
    # fake response
    fake_json_response = {
        "data": {
            "score": 10,
            "summary": "some summary",
            "strengths": [{"text": "some reason", "category": "job"}],
            "improvements": [{"text": "some reason", "category": "education"}],
            "job_match": {
                "score": 10,
                "summary": "some summary",
                "pros": [{"type": "pros", "message": "some reason"}],
                "cons": [{"type": "cons", "message": "some reason"}],
                "warns": [{"type": "warn", "message": "some reason"}],
            },
            "skill_match": {
                "score": 10,
                "summary": "some summary",
                "skills": {"all_skills": ["Python"]},
                "match_result": {
                    "miss_match": ["Python"],
                    "partial_match": [],
                    "strong_match": [],
                },
            },
            "education_match": {
                "score": 10,
                "summary": "some summary",
                "pros": [{"type": "pros", "message": "some reason"}],
                "cons": [{"type": "cons", "message": "some reason"}],
                "warns": [{"type": "warn", "message": "some reason"}],
            },
            "more_information": {
                "region": "Europe",
                "overqualification_status": False,
                "qualification_reason": "some reason",
            },
            "jd_text": "some text",
        },
        "usage": {"credits": randint(1, 200)},
    }
    # test validating resume score keywords validation
    # 200 response
    fake_response = HttpResponse(text=json.dumps(fake_json_response), status_code=200)
    assert isinstance(
        base_service.validate_response(
            response=fake_response, validate_model=ResumeScoreResponse
        ),
        ResumeScoreResponse,
    )

    # 404 response
    fake_json_response = {"usage": {"credits": 0}, "message": "request not found !"}
    fake_response = HttpResponse(text=json.dumps(fake_json_response), status_code=404)
    assert isinstance(
        base_service.validate_response(
            response=fake_response, validate_model=ResumeScoreResponse
        ),
        ErrorResponse,
    )


def test_base_service_validating_response_raise_error(httpxclient: httpx.AsyncClient):
    # test validating base service valida_response method
    base_service = BaseService(httpxclient)
    # 500 response, raise error
    fake_response = HttpResponse(text="Internal Server Error!", status_code=500)
    with pytest.raises(APIServerError):
        base_service.validate_response(
            response=fake_response, validate_model=ResumeScoreResponse
        )
