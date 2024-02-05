from faker import Faker
import pytest
from random import randint

from magicalapi.types.youtube_suggestions import YoutubeSuggestionsResponse

Faker.seed()


@pytest.fixture(scope="function")
def captions():
    fake = Faker(locale="en")
    captions = {"captions": [fake.text() for _ in range(5)]}

    yield captions

    del captions


@pytest.fixture(scope="function")
def titles():
    fake = Faker(locale="en")
    titles = {"titles": [fake.text(max_nb_chars=80) for _ in range(5)]}

    yield titles

    del titles


@pytest.fixture(scope="function")
def hashtags():
    fake = Faker(locale="en")
    hashtags = {"hashtags": [fake.text(max_nb_chars=10) for _ in range(5)]}

    yield hashtags

    del hashtags


@pytest.fixture(scope="function")
def keywords():
    fake = Faker(locale="en")
    keywords = {"keywords": [fake.text(max_nb_chars=10) for _ in range(5)]}

    yield keywords

    del keywords


def test_youtube_suggestions_validate_type(captions, titles, hashtags, keywords):
    # test validating youtube_suggestions response type

    responses = (
        {"data": captions, "usage": {"credits": randint(10, 500)}},
        {"data": titles, "usage": {"credits": randint(10, 500)}},
        {"data": hashtags, "usage": {"credits": randint(10, 500)}},
        {"data": keywords, "usage": {"credits": randint(10, 500)}},
    )

    # check all suggestion goals
    assert all(
        [
            type(YoutubeSuggestionsResponse.model_validate(response))
            == YoutubeSuggestionsResponse
            for response in responses
        ]
    )
