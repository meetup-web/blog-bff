from uuid import UUID

from adaptix import Retort
from httpx import AsyncClient

from blog_bff.application.models.pagination import Pagination
from blog_bff.infrastructure.response_models import Comment, Response


class CommentLoader:
    def __init__(self, comments_api_url: str, client: AsyncClient) -> None:
        self._retort = Retort()
        self._comments_api_url = comments_api_url
        self._client = client

    async def load_comments_by_post_id(
        self, post_id: UUID, pagination: Pagination
    ) -> list[Comment]:
        response = await self._client.get(
            f"{self._comments_api_url}/comments/post/{post_id}",
            params={"limit": pagination.limit, "offset": pagination.offset},
        )

        if response.status_code != 200:
            return []

        data = self._retort.load(response.json(), Response[list[Comment]])

        return data.result if data.result else []
