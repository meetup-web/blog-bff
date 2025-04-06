from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from posts_bff.application.models.post_creator import Creator


@dataclass(frozen=True)
class PostReadModel:
    post_id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    creator: Creator
