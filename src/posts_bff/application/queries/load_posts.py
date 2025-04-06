from dataclasses import dataclass

from posts_bff.application.common.query import Query
from posts_bff.application.common.query_handler import QueryHandler
from posts_bff.application.models.pagination import Pagination
from posts_bff.application.models.post import PostReadModel
from posts_bff.application.ports.post_gateway import PostGateway


@dataclass(frozen=True)
class LoadPosts(Query[list[PostReadModel]]):
    pagination: Pagination


class LoadPostsHandler(QueryHandler[LoadPosts, list[PostReadModel]]):
    def __init__(self, post_gateway: PostGateway) -> None:
        self._post_gateway = post_gateway

    async def handle(self, query: LoadPosts) -> list[PostReadModel]:
        posts = await self._post_gateway.load_posts(query.pagination)
        return posts
