from uuid import UUID

from adaptix import Retort
from httpx import AsyncClient

from blog_bff.application.models.pagination import Pagination
from blog_bff.infrastructure.response_models import Post, Response


class PostLoader:
    def __init__(self, posts_api_url: str, client: AsyncClient) -> None:
        self._retort = Retort()
        self._posts_api_url = posts_api_url
        self._client = client

    async def load_user_posts(self, user_id: UUID, pagination: Pagination) -> list[Post]:
        response = await self._client.get(
            f"{self._posts_api_url}/posts/user/{user_id}",
            params={"limit": pagination.limit, "offset": pagination.offset},
        )

        if response.status_code != 200:
            return []

        data = self._retort.load(response.json(), Response[list[Post]])

        return data.result if data.result else []

    async def load_posts(self, pagination: Pagination) -> list[Post]:
        response = await self._client.get(
            f"{self._posts_api_url}/posts/posts",
            params={"limit": pagination.limit, "offset": pagination.offset},
        )

        if response.status_code != 200:
            return []

        data = self._retort.load(response.json(), Response[list[Post]])

        return data.result if data.result else []
