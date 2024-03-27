from random import randint
from typing import Any

import pytest
from pydantic import ValidationError

from magicalapi.types.resume_parser import ResumeParserResponse


def make_dict_empty(data: dict[str, object]) -> dict[str, object]:
    # make data schema empty
    new_data = {}
    for key, value in data.items():
        if type(value) == dict:
            # handle dict
            new_data[key] = make_dict_empty(value)
        elif type(value) == list:
            # handle lists
            new_data[key] = [make_dict_empty(item) for item in value]
        else:
            # other data types going to be empty
            new_data[key] = ""

    return new_data


def test_resume_parser_validate_type(resume_data: Any):
    # test validating resume_parser response type
    response = {"data": resume_data, "usage": {"credits": randint(10, 500)}}

    assert type(ResumeParserResponse.model_validate(response)) == ResumeParserResponse


def test_resume_parser_validate_type_all_empty(resume_data: Any):
    # test validating resume_parser response type must fail
    resume_data = make_dict_empty(resume_data)

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
