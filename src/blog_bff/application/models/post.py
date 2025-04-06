from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from blog_bff.application.models.author import Author


@dataclass(frozen=True)
class PostReadModel:
    post_id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    creator: Author
