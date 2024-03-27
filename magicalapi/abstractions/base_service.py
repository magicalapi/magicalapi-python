from abc import ABC, abstractmethod
from typing import Any

from magicalapi.types.schemas import HttpResponse


class BaseServiceAbc(ABC):
    @abstractmethod
    async def _send_post_request(self, path: str, data: dict[str, Any]) -> HttpResponse:
        pass

    @abstractmethod
    async def _send_get_request(
        self, path: str, params: dict[str, str] | None = None
    ) -> HttpResponse:
        pass
