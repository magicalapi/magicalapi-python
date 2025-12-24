"""
Unit tests for webhook_url functionality.
"""

import json
from collections.abc import AsyncGenerator

import httpx
import pytest
import pytest_asyncio

from magicalapi.client import AsyncClient
from magicalapi.services.base_service import BaseService
from magicalapi.types.schemas import HttpResponse, WebhookCreatedResponse


@pytest_asyncio.fixture(scope="function")
async def httpxclient() -> AsyncGenerator[httpx.AsyncClient]:
    """Fixture to create an httpx client for testing."""
    client = httpx.AsyncClient(
        headers={"content-type": "application/json"},
    )

    yield client

    await client.aclose()
    del client


@pytest.mark.asyncio
async def test_base_service_with_webhook_url(httpxclient: httpx.AsyncClient):
    """Test that webhook_url is properly added to request body."""
    # Set a reasonable timeout for the client
    httpxclient._timeout = httpx.Timeout(30.0)

    webhook_url = "https://example.com/webhook"
    base_service = BaseService(httpxclient, webhook_url=webhook_url)
    test_data = {"foo": "bar"}

    response = await base_service._send_post_request(
        path="https://httpbin.org/post", data=test_data
    )

    # Verify response
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    # Verify webhook_url was added to the request
    response_json = json.loads(response.text)
    assert response_json["json"]["webhook_url"] == webhook_url
    assert response_json["json"]["foo"] == "bar"


@pytest.mark.asyncio
async def test_base_service_without_webhook_url(httpxclient: httpx.AsyncClient):
    """Test that request works without webhook_url."""
    base_service = BaseService(httpxclient, webhook_url=None)
    test_data = {"foo": "bar"}

    response = await base_service._send_post_request(
        path="https://httpbin.org/post", data=test_data
    )

    # Verify response
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    # Verify webhook_url was NOT added to the request
    response_json = json.loads(response.text)
    assert "webhook_url" not in response_json["json"]
    assert response_json["json"]["foo"] == "bar"


def test_validate_webhook_created_response(httpxclient: httpx.AsyncClient):
    """Test validation of webhook created response (201 status)."""
    webhook_url = "https://example.com/webhook"
    base_service = BaseService(httpxclient, webhook_url=webhook_url)

    # Mock a 201 webhook created response
    fake_webhook_response = {
        "data": {
            "status": "created",
            "message": "Request accepted, result will be sent to webhook",
        },
        "usage": {"credits": 5},
    }

    fake_response = HttpResponse(
        text=json.dumps(fake_webhook_response), status_code=201
    )

    # Validate response
    result = base_service.validate_response(
        response=fake_response, validate_model=WebhookCreatedResponse
    )

    assert isinstance(result, WebhookCreatedResponse)
    assert result.data.status == "created"
    assert result.data.message == "Request accepted, result will be sent to webhook"
    assert result.usage.credits == 5


def test_validate_webhook_not_triggered_without_webhook_url(
    httpxclient: httpx.AsyncClient,
):
    """Test that 201 response without webhook_url raises APIServerError."""
    # No webhook_url provided
    base_service = BaseService(httpxclient, webhook_url=None)

    # Mock a 201 pending response (normal polling behavior)
    # This represents a response that would trigger retry in _send_post_request
    fake_pending_response = {
        "data": {"request_id": "req_12345"},
        "usage": {"credits": 0},
    }

    fake_response = HttpResponse(
        text=json.dumps(fake_pending_response), status_code=201
    )

    # When validate_response receives a 201 without webhook_url,
    # it should raise APIServerError since 201 is not a valid final status
    # (it's meant to be handled by retry logic in _send_post_request)
    from magicalapi.errors import APIServerError

    with pytest.raises(APIServerError):
        base_service.validate_response(
            response=fake_response, validate_model=WebhookCreatedResponse
        )


def test_client_initialization_with_webhook_url():
    """Test that AsyncClient accepts webhook_url parameter."""
    # Create client with webhook_url
    webhook_url = "https://example.com/webhook"
    client = AsyncClient(api_key="test_key", webhook_url=webhook_url)

    # Verify webhook_url is passed to services
    assert client.profile_data._webhook_url == webhook_url
    assert client.company_data._webhook_url == webhook_url
    assert client.resume_parser._webhook_url == webhook_url
    assert client.resume_score._webhook_url == webhook_url
    assert client.resume_review._webhook_url == webhook_url


def test_client_initialization_without_webhook_url():
    """Test that AsyncClient works without webhook_url."""
    client = AsyncClient(api_key="test_key")

    # Verify webhook_url defaults to None
    assert client.profile_data._webhook_url is None
    assert client.company_data._webhook_url is None
    assert client.resume_parser._webhook_url is None
    assert client.resume_score._webhook_url is None
    assert client.resume_review._webhook_url is None
