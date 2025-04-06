from posts_bff.application.common.query import Query
from posts_bff.application.common.query_handler import QueryHandler


class HandlersRegistry:
    def __init__(self) -> None:
        self._query_handlers: dict[type[Query], type[QueryHandler]] = {}

    def add_query_handler(
        self, query_type: type[Query], query_handler: type[QueryHandler]
    ) -> None:
        self._query_handlers[query_type] = query_handler

    def get_query_handler(self, query_type: type[Query]) -> type[QueryHandler] | None:
        return self._query_handlers.get(query_type)
