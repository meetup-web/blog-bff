from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from blog_bff.application.models.author import Author


@dataclass(frozen=True)
class CommentReadModel:
    comment_id: UUID
    post_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
    author: Author
