from abc import ABC, abstractmethod
from typing import TypeVar

from blog_bff.application.common.query import Query

TRes = TypeVar("TRes")


class Sender(ABC):
    @abstractmethod
    async def send(self, query: Query[TRes]) -> TRes: ...
