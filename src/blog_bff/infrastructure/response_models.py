from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID


@dataclass(frozen=True)
class Response[T]:
    status: int
    result: T | None = field(default=None)


@dataclass(frozen=True)
class Post:
    post_id: UUID
    creator_id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class Fullname:
    first_name: str
    last_name: str | None = field(default=None)
    middle_name: str | None = field(default=None)


@dataclass(frozen=True)
class Profile:
    user_id: UUID
    profile_id: UUID
    fullname: Fullname
    birth_date: date | None
    created_at: datetime


@dataclass(frozen=True)
class Comment:
    comment_id: UUID
    post_id: UUID
    author_id: UUID
    content: str
    created_at: datetime
    updated_at: datetime
