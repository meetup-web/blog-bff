from dataclasses import dataclass
from uuid import UUID

from blog_bff.application.common.query import Query
from blog_bff.application.common.query_handler import QueryHandler
from blog_bff.application.models.pagination import Pagination
from blog_bff.application.models.post import PostReadModel
from blog_bff.application.ports.post_gateway import PostGateway


@dataclass(frozen=True)
class LoadUserPosts(Query[list[PostReadModel]]):
    pagination: Pagination
    user_id: UUID


class LoadUserPostsHandler(QueryHandler[LoadUserPosts, list[PostReadModel]]):
    def __init__(self, post_gateway: PostGateway) -> None:
        self._post_gateway = post_gateway

    async def handle(self, query: LoadUserPosts) -> list[PostReadModel]:
        posts = await self._post_gateway.load_user_posts(
            user_id=query.user_id, pagination=query.pagination
        )
        return posts
