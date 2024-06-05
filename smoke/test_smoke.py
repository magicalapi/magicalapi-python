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
from magicalapi.types.company_data import CompanyDataResponse
from magicalapi.types.profile_data import ProfileDataResponse
from magicalapi.types.resume_parser import ResumeParserResponse
from magicalapi.types.resume_review import ResumeReviewResponse
from magicalapi.types.resume_score import ResumeScoreResponse
from magicalapi.types.youtube_seo import YoutubeSeoResponse
from magicalapi.types.youtube_suggestions import YoutubeSuggestionsResponse
from magicalapi.types.youtube_top_keywords import YoutubeTopKeywordsResponse


@pytest_asyncio.fixture(scope="function")
async def client():
    # create an instance of magicalAPI AsyncClient
    async with AsyncClient() as client:  # loads api_key from .env
        yield client


@pytest.mark.asyncio
async def test_profile_data_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.profile_data.get_profile_data(profile_name="amiraref")

    assert isinstance(response, ProfileDataResponse)


@pytest.mark.asyncio
async def test_company_data_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.company_data.get_company_data(company_username="google")

    assert isinstance(response, CompanyDataResponse)


@pytest.mark.asyncio
async def test_resume_parser_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.resume_parser.get_resume_parser(
        url="https://resume-resource.com/wp-content/uploads/00123-sales-professional-resume.pdf"
    )

    assert isinstance(response, ResumeParserResponse)


@pytest.mark.asyncio
async def test_resume_review_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.resume_review.get_resume_review(
        url="https://resume-resource.com/wp-content/uploads/00123-sales-professional-resume.pdf"
    )

    assert isinstance(response, ResumeReviewResponse)


@pytest.mark.asyncio
async def test_resume_score_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.resume_score.get_resume_score(
        url="https://resume-resource.com/wp-content/uploads/00123-sales-professional-resume.pdf",
        job_description="Sales Professional",
    )

    assert isinstance(response, ResumeScoreResponse)


@pytest.mark.asyncio
async def test_youtube_seo_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.youtube_seo.get_youtube_seo(
        url="https://www.youtube.com/watch?v=PZZI1QXlM80"
    )

    assert isinstance(response, YoutubeSeoResponse)


@pytest.mark.asyncio
async def test_youtube_suggestions_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.youtube_suggestions.get_youtube_suggestions(
        prompt_sentence="How to create a profitable Shopify store",
        count=5,
        suggestion_goal="hashtag",
    )

    assert isinstance(response, YoutubeSuggestionsResponse)


@pytest.mark.asyncio
async def test_youtube_keywords_is_ok(client: AsyncClient):
    # test api returns 200 and correct response schema
    response = await client.youtube_top_keywords.get_keywords(
        search_sentence="movie trailers", country="1", language="1000"
    )

    assert isinstance(response, YoutubeTopKeywordsResponse)
