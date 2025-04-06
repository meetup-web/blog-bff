from abc import ABC, abstractmethod
from uuid import UUID

from blog_bff.application.models.comment import CommentReadModel
from blog_bff.application.models.pagination import Pagination


class CommentGateway(ABC):
    @abstractmethod
    async def load_post_comments(
        self, post_id: UUID, pagination: Pagination
    ) -> list[CommentReadModel]: ...
