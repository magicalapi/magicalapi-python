from pydantic import BaseModel


class Usage(BaseModel):
    credits: int


class RequestID(BaseModel):
    request_id: str


class BaseResponse(BaseModel):
    data: dict
    usage: Usage
    message: str


class PendingResponse(BaseResponse):
    data: RequestID
