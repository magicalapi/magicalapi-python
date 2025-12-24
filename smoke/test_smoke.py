"""
NOTE

this file contains some tests that call the api endpoint,
so before run this, you have to set the MAG_API_KEY in .env file,
and the more IMPORTANT thing you have to know is this process can have costs for you in panel.magicalapi.com !
because it makes real requests.

"""

import pytest
import pytest_asyncio

from magicalapi.client import AsyncClient
from magicalapi.types.base import ErrorResponse
from magicalapi.types.company_data import CompanyDataResponse
from magicalapi.types.profile_data import ProfileDataResponse
from magicalapi.types.resume_parser import ResumeParserResponse
from magicalapi.types.resume_review import ResumeReviewResponse
from magicalapi.types.resume_score import ResumeScoreResponse
from magicalapi.types.schemas import WebhookCreatedResponse


@pytest_asyncio.fixture(scope="function")
async def client():
    # create an instance of magicalAPI AsyncClient
    async with AsyncClient() as client:  # loads api_key from .env
        yield client


@pytest.mark.asyncio
async def test_profile_data(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.profile_data.get_profile_data(profile_name="amiraref")

    assert isinstance(response, ProfileDataResponse)


@pytest.mark.asyncio
async def test_company_data_with_username(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.company_data.get_company_data(company_username="google")

    assert isinstance(response, CompanyDataResponse)


@pytest.mark.asyncio
async def test_company_data_with_name_and_website(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.company_data.get_company_data(
        company_name="apple", company_website="apple.com"
    )

    assert isinstance(response, CompanyDataResponse)


@pytest.mark.asyncio
async def test_company_data_with_website(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.company_data.get_company_data(company_website="apple.com")

    assert isinstance(response, CompanyDataResponse)


@pytest.mark.asyncio
async def test_company_data_with_name(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.company_data.get_company_data(company_name="apple")

    assert isinstance(response, CompanyDataResponse)


@pytest.mark.asyncio
async def test_resume_parser(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.resume_parser.get_resume_parser(
        url="https://pub-4aa6fc29899047be8d4a342594b2c033.r2.dev/00016-poduct-manager-resume-example.pdf",
    )

    assert isinstance(response, ResumeParserResponse)


@pytest.mark.asyncio
async def test_resume_review(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.resume_review.get_resume_review(
        url="https://pub-4aa6fc29899047be8d4a342594b2c033.r2.dev/00016-poduct-manager-resume-example.pdf"
    )

    assert isinstance(response, ResumeReviewResponse)


@pytest.mark.asyncio
async def test_resume_score(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.resume_score.get_resume_score(
        url="https://pub-4aa6fc29899047be8d4a342594b2c033.r2.dev/00016-poduct-manager-resume-example.pdf",
        job_description="Sales Professional",
    )

    assert isinstance(response, ResumeScoreResponse)
