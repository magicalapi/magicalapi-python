from types import NoneType
from typing import Any

from pydantic import BaseModel, field_validator


class Usage(BaseModel):
    credits: int = 0


class BaseModelValidated(BaseModel):
    @field_validator("*", mode="before")
    def empty_fields_none(cls, value: Any) -> None:
        # convert empty strings to None object
        if value == "":
            return None
        return value


class OptionalModel(BaseModel):
    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        for field in cls.model_fields.values():
            field.annotation = field.annotation | NoneType
            field.default = None

        cls.model_rebuild(force=True)


class BaseResponse(BaseModelValidated):
    # data: dict
    usage: Usage = Usage()


class ErrorResponse(BaseResponse):
    message: str
