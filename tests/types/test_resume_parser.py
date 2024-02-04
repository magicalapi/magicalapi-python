import pytest
from typing import Any
from random import randint
from pydantic import ValidationError
from magicalapi.types.resume_parser import ResumeParserResponse


def test_resume_parser_validate_type(resume_data: Any):
    # test validating resume_parser response type
    response = {"data": resume_data, "usage": {"credits": randint(10, 500)}}

    assert type(ResumeParserResponse.model_validate(response)) == ResumeParserResponse


def test_resume_parser_validate_type_failing(resume_data: Any):
    # test validating resume_parser response type must fail
    # make data schema invalid
    del resume_data["summary"]
    resume_data["basic"] = {}

    response = {"data": resume_data, "usage": {"credits": randint(10, 500)}}

    with pytest.raises(ValidationError):
        ResumeParserResponse.model_validate(response)
