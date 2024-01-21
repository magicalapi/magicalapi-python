from pydantic import BaseModel, field_validator, validator


class Usage(BaseModel):
    credits: int


class RequestID(BaseModel):
    request_id: str


class BaseModelValidated(BaseModel):
    @field_validator("*", mode="before")
    def empty_fields_none(cls, value):
        # convert empty strings to None object
        if value == "":
            return None
        return value


class BaseResponse(BaseModelValidated):
    data: dict
    usage: Usage


class PendingResponse(BaseModel):
    data: RequestID
    usage: Usage


class ErrorResponse(BaseModel):
    usage: Usage
    message: str


class MessageResponse(BaseModel):
    message: str
