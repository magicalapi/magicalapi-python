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
    score_result = {
        "score": randint(0, 100),
        "summary": fake.text(),
        "strengths": [
            {"text": fake.text(), "category": "job"},
            {"text": fake.text(), "category": "skills"},
        ],
        "improvements": [
            {"text": fake.text(), "category": "education"},
        ],
        "job_match": {
            "score": randint(0, 100),
            "summary": fake.text(),
            "pros": [{"type": fake.word(), "message": fake.text()}],
            "cons": [{"type": fake.word(), "message": fake.text()}],
            "warns": [{"type": fake.word(), "message": fake.text()}],
        },
        "skill_match": {
            "score": randint(0, 100),
            "summary": fake.text(),
            "skills": {"all_skills": [fake.word(), fake.word()]},
            "match_result": {
                "miss_match": [fake.word()],
                "partial_match": [fake.word()],
                "strong_match": [fake.word()],
            },
        },
        "education_match": {
            "score": randint(0, 100),
            "summary": fake.text(),
            "pros": [{"type": fake.word(), "message": fake.text()}],
            "cons": [{"type": fake.word(), "message": fake.text()}],
            "warns": [{"type": fake.word(), "message": fake.text()}],
        },
        "more_information": {
            "region": fake.word(),
            "overqualification_status": bool(randint(0, 1)),
            "qualification_reason": fake.text(),
        },
        "jd_text": fake.text(),
    }

    yield score_result

    del score_result


def test_resume_score_validate_type(resume_score_result: Any):
    # test validating resume_score response type

    response = {"data": resume_score_result, "usage": {"credits": randint(10, 500)}}

    assert type(ResumeScoreResponse.model_validate(response)) == ResumeScoreResponse
    assert len(ResumeScoreResponse.model_validate(response).data.strengths) == 2


def test_resume_score_validate_type_failing(resume_score_result: Any):
    # test validating resume_score response type must fail
    # make data schema invalid
    del resume_score_result["job_match"]["score"]
    resume_score_result["strengths"][0]["category"] = "invalid"

    response = {"data": resume_score_result, "usage": {"credits": randint(10, 500)}}

    with pytest.raises(ValidationError):
        ResumeScoreResponse.model_validate(response)
