from pydantic import BaseModel


class HttpResponse(BaseModel):
    text: str
    status_code: int
