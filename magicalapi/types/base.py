from typing import Any
from pydantic import BaseModel, field_validator, validator


class Usage(BaseModel):
    credits: int = 0


class BaseModelValidated(BaseModel):
    @field_validator("*", mode="before")
    def empty_fields_none(cls, value: Any) -> None:
        # convert empty strings to None object
        if value == "":
            return None
        return value


class BaseResponse(BaseModelValidated):
    # data: dict
    usage: Usage = Usage()


class ErrorResponse(BaseResponse):
    message: str
