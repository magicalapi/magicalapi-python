from random import randint
from pydantic import ValidationError
import pytest

from magicalapi.types.youtube_top_keywords import (
    KeywordIdea,
    YoutubeTopKeywordsResponse,
)


@pytest.mark.dependency()
def test_youtube_top_keywords_type(dependency_keyword: KeywordIdea):
    try:
        # validating keywords
        KeywordIdea.model_validate(
            obj=dependency_keyword,
        )

    except ValidationError as exc:
        assert False, "validating youtube_top_keywords type failed : " + str(exc)


@pytest.mark.dependency(depends=["test_youtube_top_keywords_type"])
def test_youtube_top_keywords_response_type(dependency_keyword: KeywordIdea):
    try:
        response_schema = {
            "data": {"keywords": [dependency_keyword]},
            "usage": {"credits": randint(1, 200)},
        }
        YoutubeTopKeywordsResponse.model_validate(response_schema)
    except ValidationError as exc:
        assert False, "validating youtube_top_keywords response failed : " + str(exc)
