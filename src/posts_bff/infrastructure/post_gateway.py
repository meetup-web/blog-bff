from uuid import UUID

from posts_bff.application.models.pagination import Pagination
from posts_bff.application.models.post import PostReadModel
from posts_bff.application.models.post_creator import Creator
from posts_bff.application.ports.post_gateway import PostGateway
from posts_bff.infrastructure.post_loader import PostLoader
from posts_bff.infrastructure.profile_loader import ProfileLoader
from posts_bff.infrastructure.response_models import Post, Profile


class ApiPostGateway(PostGateway):
    def __init__(self, profile_loader: ProfileLoader, post_loader: PostLoader) -> None:
        self._profile_loader = profile_loader
        self._post_loader = post_loader

    async def load_post_by_id(self, post_id: UUID) -> PostReadModel | None:
        post = await self._post_loader.load_post_by_id(post_id=post_id)

        if not post:
            return None

        post_creator = await self._profile_loader.load_profile_by_user_id(
            user_id=post.creator_id
        )

        if not post_creator:
            return None

        return self._load(profile=post_creator, post=post)

    async def load_posts(self, pagination: Pagination) -> list[PostReadModel]:
        posts = await self._post_loader.load_posts(pagination=pagination)

        if not posts:
            return []

        post_creators = await self._profile_loader.load_profiles_by_user_ids(
            user_ids=[post.creator_id for post in posts]
        )

        if not post_creators:
            return []

        return [
            self._load(profile=post_creator, post=post)
            for post_creator, post in zip(post_creators, posts, strict=False)
        ]

    def _load(self, profile: Profile, post: Post) -> PostReadModel:
        return PostReadModel(
            post_id=post.post_id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
            creator=Creator(
                profile_id=profile.profile_id,
                first_name=profile.fullname.first_name,
                last_name=profile.fullname.last_name,
                middle_name=profile.fullname.middle_name,
            ),
        )
