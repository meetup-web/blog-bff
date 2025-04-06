from typing import cast

from blog_bff.application.common.query import Query
from blog_bff.infrastructure.query_bus.adapters.resolver import Resolver
from blog_bff.infrastructure.query_bus.adapters.sender import Sender, TRes
from blog_bff.infrastructure.query_bus.registry import HandlersRegistry


class QuerySender(Sender):
    def __init__(self, registry: HandlersRegistry, resolver: Resolver) -> None:
        self._registry = registry
        self._resolver = resolver

    async def send(self, query: Query[TRes]) -> TRes:
        query_type = type(query)
        handler_type = self._registry.get_query_handler(query_type)

        if not handler_type:
            raise KeyError(f"Handler for query {query_type} not found")

        handler = await self._resolver.resolve(handler_type)

        return cast("TRes", await handler.handle(query))
