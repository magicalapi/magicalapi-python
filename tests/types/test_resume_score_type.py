from random import randint
from typing import Any

import pytest
from faker import Faker
from pydantic import ValidationError

from magicalapi.types.resume_score import ResumeScoreResponse

Faker.seed()


@pytest.fixture(scope="function")
def resume_score_result():
    fake = Faker(locale="en")
    score_result = {"score": randint(0, 10), "reason": fake.text()}

    yield score_result

    del score_result


def test_resume_score_validate_type(resume_score_result: Any):
    # test validating resume_score response type

    response = {"data": resume_score_result, "usage": {"credits": randint(10, 500)}}

    assert type(ResumeScoreResponse.model_validate(response)) == ResumeScoreResponse


def test_resume_score_validate_type_failing(resume_score_result: Any):
    # test validating resume_score response type must fail
    # make data schema invalid
    del resume_score_result["score"]
    resume_score_result["reason"] = {}

    response = {"data": resume_score_result, "usage": {"credits": randint(10, 500)}}

    with pytest.raises(ValidationError):
        ResumeScoreResponse.model_validate(response)
