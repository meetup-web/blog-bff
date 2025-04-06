from dataclasses import dataclass
from uuid import UUID

from posts_bff.application.common.application_error import ApplicationError, ErrorType
from posts_bff.application.common.query import Query
from posts_bff.application.common.query_handler import QueryHandler
from posts_bff.application.models.post import PostReadModel
from posts_bff.application.ports.post_gateway import PostGateway


@dataclass(frozen=True)
class LoadPostById(Query[PostReadModel]):
    post_id: UUID


class LoadPostByIdHandler(QueryHandler[LoadPostById, PostReadModel]):
    def __init__(self, post_gateway: PostGateway) -> None:
        self._post_gateway = post_gateway

    async def handle(self, query: LoadPostById) -> PostReadModel:
        post = await self._post_gateway.load_post_by_id(query.post_id)

        if not post:
            raise ApplicationError(
                message="Post not found", error_type=ErrorType.NOT_FOUND
            )

        return post
