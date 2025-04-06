from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from blog_bff.application.common.query import Query

TRes_co = TypeVar("TRes_co", covariant=True)
TQuery_contra = TypeVar("TQuery_contra", contravariant=True, bound=Query)


class QueryHandler(Generic[TQuery_contra, TRes_co], ABC):
    @abstractmethod
    async def handle(self, query: TQuery_contra) -> TRes_co: ...
