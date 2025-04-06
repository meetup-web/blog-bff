from uuid import UUID

from adaptix import Retort
from httpx import AsyncClient

from posts_bff.infrastructure.response_models import Profile, Response


class ProfileLoader:
    def __init__(self, profile_api_url: str, client: AsyncClient) -> None:
        self._retort = Retort()
        self._profile_api_url = profile_api_url
        self._client = client

    async def load_profile_by_user_id(self, user_id: UUID) -> Profile | None:
        response = await self._client.get(
            f"{self._profile_api_url}/profiles/profile/{user_id}"
        )

        if response.status_code != 200:
            return None

        data = self._retort.load(response.json(), Response[Profile])

        return data.result if data.result else None

    async def load_profiles_by_user_ids(self, user_ids: list[UUID]) -> list[Profile]:
        response = await self._client.get(
            f"{self._profile_api_url}/profiles/profiles/{user_ids}",
        )

        if response.status_code != 200:
            return []

        data = self._retort.load(response.json(), Response[list[Profile]])

        return data.result if data.result else []
