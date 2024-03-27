from pydantic import BaseModel

from .base import Usage


class HttpResponse(BaseModel):
    text: str
    status_code: int


class RequestID(BaseModel):
    request_id: str


class PendingResponse(BaseModel):
    data: RequestID
    usage: Usage
