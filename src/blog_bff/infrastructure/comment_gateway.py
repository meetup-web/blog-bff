from uuid import UUID

from blog_bff.application.models.author import Author
from blog_bff.application.models.comment import CommentReadModel
from blog_bff.application.models.pagination import Pagination
from blog_bff.application.ports.comments_gateway import CommentGateway
from blog_bff.infrastructure.comment_loader import CommentLoader
from blog_bff.infrastructure.profile_loader import ProfileLoader
from blog_bff.infrastructure.response_models import Comment, Profile


class HttpCommentGateway(CommentGateway):
    def __init__(
        self, comment_loader: CommentLoader, profile_loader: ProfileLoader
    ) -> None:
        self._comment_loader = comment_loader
        self._profile_loader = profile_loader

    async def load_post_comments(
        self, post_id: UUID, pagination: Pagination
    ) -> list[CommentReadModel]:
        comments = await self._comment_loader.load_comments_by_post_id(
            post_id=post_id, pagination=pagination
        )

        if not comments:
            return []

        comments_authors = await self._profile_loader.load_profiles_by_user_ids(
            user_ids=[comment.author_id for comment in comments]
        )

        if not comments_authors:
            return []

        return [
            self._load(comment=comment, author=author)
            for comment, author in zip(comments, comments_authors, strict=False)
        ]

    def _load(self, comment: Comment, author: Profile) -> CommentReadModel:
        return CommentReadModel(
            comment_id=comment.comment_id,
            post_id=comment.post_id,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            author=Author(
                profile_id=author.profile_id,
                first_name=author.fullname.first_name,
                last_name=author.fullname.last_name,
                middle_name=author.fullname.middle_name,
            ),
        )
