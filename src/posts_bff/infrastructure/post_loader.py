from uuid import UUID

from adaptix import Retort
from httpx import AsyncClient

from posts_bff.application.models.pagination import Pagination
from posts_bff.infrastructure.response_models import Post, Response


class PostLoader:
    def __init__(self, posts_api_url: str, client: AsyncClient) -> None:
        self._retort = Retort()
        self._posts_api_url = posts_api_url
        self._client = client

    async def load_post_by_id(self, post_id: UUID) -> Post | None:
        response = await self._client.get(f"{self._posts_api_url}/posts/post/{post_id}")

        if response.status_code != 200:
            return None

        data = self._retort.load(response.json(), Response[Post])

        return data.result if data.result else None

    async def load_posts(self, pagination: Pagination) -> list[Post]:
        response = await self._client.get(
            f"{self._posts_api_url}/posts/posts",
            params={"limit": pagination.limit, "offset": pagination.offset},
        )

        if response.status_code != 200:
            return []

        data = self._retort.load(response.json(), Response[list[Post]])

        return data.result if data.result else []
