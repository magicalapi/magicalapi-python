from random import randint
from typing import Any

import pytest
from faker import Faker
from pydantic import ValidationError

from magicalapi.types.resume_review import ResumeReviewResponse


@pytest.fixture(scope="function")
def resume_review_data(resume_data):  # type: ignore
    fake = Faker(locale="en")

    # create a sample resume review result
    resume_review = {  # type: ignore
        "score": 41,
        "result": {
            "experiences": {
                "pros": [
                    fake.text(),
                    fake.text(),
                ],
                "cons": [],
            },
            "skills": {
                "pros": [fake.text()],
                "cons": [],
            },
            "format": {
                "pros": [
                    fake.text(),
                    fake.text(),
                ],
                "cons": [],
            },
            "contact": {
                "pros": [],
                "cons": [
                    {
                        "message": fake.text(),
                        "tips": [fake.text(), fake.text()],
                    },
                ],
            },
            "educations": {
                "pros": [],
                "cons": [
                    {
                        "message": fake.text(),
                        "tips": [fake.text(), fake.text()],
                    },
                ],
            },
            "summary": {
                "pros": [],
                "cons": [
                    {
                        "message": fake.text(),
                        "tips": [fake.text(), fake.text()],
                    },
                ],
            },
        },
        "suggested": {
            "experiences": {
                "content": fake.text(),
            },
            "skills": {
                "content": fake.text(),
            },
            "format": {
                "content": fake.text(),
            },
            "contact": {
                "content": fake.text(),
            },
            "educations": {
                "content": None,
            },
            "summary": {
                "content": None,
            },
        },
    }

    yield resume_review

    del resume_review


def test_resume_review_validate_type(resume_review_data: Any):
    # test validating resume_review response type
    response = {"data": resume_review_data, "usage": {"credits": randint(10, 500)}}

    assert type(ResumeReviewResponse.model_validate(response)) == ResumeReviewResponse

    response_object = ResumeReviewResponse.model_validate(response)

    assert len(response_object.data.result.format.pros) == 2


def test_resume_review_validate_type_failing(resume_review_data: Any):
    # test validating resume_review response type must fail
    # make data schema invalid
    del resume_review_data["score"]
    resume_review_data["details"] = {}

    response = {"data": resume_review_data, "usage": {"credits": randint(10, 500)}}

    with pytest.raises(ValidationError):
        ResumeReviewResponse.model_validate(response)
