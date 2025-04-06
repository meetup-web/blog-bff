from abc import ABC, abstractmethod
from uuid import UUID

from posts_bff.application.models.pagination import Pagination
from posts_bff.application.models.post import PostReadModel


class PostGateway(ABC):
    @abstractmethod
    async def load_posts(self, pagination: Pagination) -> list[PostReadModel]: ...
    @abstractmethod
    async def load_post_by_id(self, post_id: UUID) -> PostReadModel | None: ...
