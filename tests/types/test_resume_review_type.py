from random import randint
from typing import Any

import pytest
from faker import Faker
from pydantic import ValidationError

from magicalapi.types.resume_review import ResumeReviewResponse


@pytest.fixture(scope="function")
def resume_review_data(resume_data):  # type: ignore
    fake = Faker(locale="en")
    # change reume_data for new version of parser data
    resume_data["project_experiences"] = [
        {"title": fake.text(), "description": fake.text()}
    ]
    for exp in resume_data["work_experiences"]:
        exp["duration"] = {
            "years": 1,
            "months": 0,
        }

    for edu in resume_data["educations"]:
        edu["start"] = {
            "year": randint(1990, 2024),
        }
        edu["end"] = {
            "year": "present",
        }
    # create a sample resume review result
    resume_review = {  # type: ignore
        "score": 41,
        "result": {
            "experiences": {
                "good": [
                    fake.text(),
                    fake.text(),
                ],
            },
            "skills": {
                "good": [fake.text()],
            },
            "format": {
                "good": [
                    fake.text(),
                    fake.text(),
                ],
            },
            "contact": {
                "bad": [fake.text()],
            },
            "educations": {
                "bad": [fake.text()],
            },
            "summary": {
                "bad": [fake.text()],
            },
        },
        "details": resume_data,
    }

    yield resume_review

    del resume_review


def test_resume_review_validate_type(resume_review_data: Any):
    # test validating resume_review response type
    response = {"data": resume_review_data, "usage": {"credits": randint(10, 500)}}

    assert type(ResumeReviewResponse.model_validate(response)) == ResumeReviewResponse


def test_resume_review_validate_type_failing(resume_review_data: Any):
    # test validating resume_review response type must fail
    # make data schema invalid
    del resume_review_data["score"]
    resume_review_data["details"] = {}

    response = {"data": resume_review_data, "usage": {"credits": randint(10, 500)}}

    with pytest.raises(ValidationError):
        ResumeReviewResponse.model_validate(response)
