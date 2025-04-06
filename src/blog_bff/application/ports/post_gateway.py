from abc import ABC, abstractmethod
from uuid import UUID

from blog_bff.application.models.pagination import Pagination
from blog_bff.application.models.post import PostReadModel


class PostGateway(ABC):
    @abstractmethod
    async def load_posts(self, pagination: Pagination) -> list[PostReadModel]: ...
    @abstractmethod
    async def load_user_posts(
        self, user_id: UUID, pagination: Pagination
    ) -> list[PostReadModel]: ...
