from uuid import UUID

from blog_bff.application.models.author import Author
from blog_bff.application.models.pagination import Pagination
from blog_bff.application.models.post import PostReadModel
from blog_bff.application.ports.post_gateway import PostGateway
from blog_bff.infrastructure.post_loader import PostLoader
from blog_bff.infrastructure.profile_loader import ProfileLoader
from blog_bff.infrastructure.response_models import Post, Profile


class HttpPostGateway(PostGateway):
    def __init__(self, profile_loader: ProfileLoader, post_loader: PostLoader) -> None:
        self._profile_loader = profile_loader
        self._post_loader = post_loader

    async def load_user_posts(
        self, user_id: UUID, pagination: Pagination
    ) -> list[PostReadModel]:
        posts = await self._post_loader.load_user_posts(
            user_id=user_id, pagination=pagination
        )

        if not posts:
            return []

        posts_author = await self._profile_loader.load_profile_by_user_id(user_id=user_id)

        if not posts_author:
            return []

        return [self._load(profile=posts_author, post=post) for post in posts]

    async def load_posts(self, pagination: Pagination) -> list[PostReadModel]:
        posts = await self._post_loader.load_posts(pagination=pagination)

        if not posts:
            return []

        post_authors = await self._profile_loader.load_profiles_by_user_ids(
            user_ids=[post.creator_id for post in posts]
        )

        if not post_authors:
            return []

        return [
            self._load(profile=post_creator, post=post)
            for post_creator, post in zip(post_authors, posts, strict=False)
        ]

    def _load(self, profile: Profile, post: Post) -> PostReadModel:
        return PostReadModel(
            post_id=post.post_id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
            updated_at=post.updated_at,
            creator=Author(
                profile_id=profile.profile_id,
                first_name=profile.fullname.first_name,
                last_name=profile.fullname.last_name,
                middle_name=profile.fullname.middle_name,
            ),
        )
