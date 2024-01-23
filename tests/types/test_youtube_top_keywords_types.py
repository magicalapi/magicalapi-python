from random import choice, randint
import random
from pydantic import ValidationError
import pytest
from faker import Faker
from magicalapi.types.base import Usage

from magicalapi.types.youtube_top_keywords import (
    KeywordIdea,
    KeywordIdeaMonth,
    Keywords,
    YoutubeTopKeywordsResponse,
)


@pytest.fixture()
def dependency_keyword():
    # create a sample profile data dictionary
    fake = Faker(locale="en")
    MONTH_LIST = [
        "JANUARY",
        "FEBRUARY",
        "MARCH",
        "APRIL",
        "MAY",
        "JUNE",
        "JULY",
        "AUGUST",
        "SEPTEMBER",
        "OCTOBER",
        "NOVEMBER",
        "DECEMBER",
    ]
    keyword = {
        "keyword": fake.text(max_nb_chars=15),
        "search_volume": randint(1000, 1000000),
        "competition": choice(("LOW", "MEDIUM", "HIGH")),
        "competition_index": randint(0, 100),
        "low_top_of_page_bid_micros": randint(0, 10**7),
        "high_top_of_page_bid_micros": randint(0, 10**7),
        "average_cpc": f"${random.random()}",
        "monthly_search": [
            {
                "month": month,
                "year": randint(2000, 2023),
                "monthly_searches": randint(1000, 1000000),
            }
            for month in MONTH_LIST
        ],
    }

    yield keyword
    del keyword


@pytest.mark.dependency()
def test_youtube_top_keywords_type(dependency_keyword):
    try:
        # validating keywords
        KeywordIdea.model_validate(
            obj=dependency_keyword,
        )

    except ValidationError as exc:
        assert False, "validating youtube_top_keywords type failed : " + str(exc)


@pytest.mark.dependency(depends=["test_youtube_top_keywords_type"])
def test_youtube_top_keywords_response_type(dependency_keyword):
    try:
        response_schema = {
            "data": {"keywords": [dependency_keyword]},
            "usage": {"credits": randint(1, 200)},
        }
        YoutubeTopKeywordsResponse.model_validate(response_schema)
    except ValidationError as exc:
        assert False, "validating youtube_top_keywords response failed : " + str(exc)
