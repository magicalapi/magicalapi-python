from pydantic import BaseModel, validator


class Usage(BaseModel):
    credits: int


class RequestID(BaseModel):
    request_id: str


class BaseModelValidated(BaseModel):
    @validator("*", pre=True)
    @classmethod
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
    message: str
