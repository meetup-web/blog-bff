from dataclasses import dataclass
from uuid import UUID

from blog_bff.application.common.query import Query
from blog_bff.application.common.query_handler import QueryHandler
from blog_bff.application.models.comment import CommentReadModel
from blog_bff.application.models.pagination import Pagination
from blog_bff.application.ports.comments_gateway import CommentGateway


@dataclass(frozen=True)
class LoadPostComments(Query[list[CommentReadModel]]):
    pagination: Pagination
    post_id: UUID


class LoadPostCommentsHandler(QueryHandler[LoadPostComments, list[CommentReadModel]]):
    def __init__(self, comment_gateway: CommentGateway) -> None:
        self._comment_gateway = comment_gateway

    async def handle(self, query: LoadPostComments) -> list[CommentReadModel]:
        comments = await self._comment_gateway.load_post_comments(
            post_id=query.post_id, pagination=query.pagination
        )

        return comments
