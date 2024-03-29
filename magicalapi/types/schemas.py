from dataclasses import dataclass

from pydantic import BaseModel

from .base import Usage


@dataclass
class HttpResponse:
    text: str
    status_code: int

    def __str__(self) -> str:
        return f'status code : {self.status_code}, resposne content : "{self.text}"'


class RequestID(BaseModel):
    request_id: str


class PendingResponse(BaseModel):
    data: RequestID
    usage: Usage
