from random import randint
from typing import Any

import pytest
from pydantic import ValidationError

from magicalapi.types.resume_review import ResumeReviewResponse


@pytest.fixture(scope="function")
def resume_review_data(resume_data):  # type: ignore
    # create a sample resume review result
    resume_review = {  # type: ignore
        "score": 41,
        "good": {
            "experiences": [
                "Job titles in the experience section are clearly defined.",
                "Company names in experiences are mentioned, adding credibility.",
                "Job durations are clearly specified, outlining stability and experience.",
            ],
            "skills": ["Skills are listed, highlighting competencies and strengths."],
            "format": [
                "Resume file size is within the required limit for easy sharing.",
                "Resume is concisely formatted to one page, focusing on relevancy.",
            ],
        },
        "bad": {
            "contact": [
                "No LinkedIn profile linked.\n<b>Tip:</b> Provide a LinkedIn URL to showcase a broader professional network and background.\n"
            ],
            "educations": [
                "Field of study missing in education.\n<b>Tip:</b> Indicate your major or field of study to outline your academic focus.\n"
            ],
            "summary": [
                "No personal summary or objective.\n<b>Tip:</b> Write a brief professional summary or objective to give an overview of your career goals and aspirations.\n"
            ],
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
