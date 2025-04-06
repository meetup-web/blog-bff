from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True)
class Author:
    profile_id: UUID
    first_name: str
    last_name: str | None = field(default=None)
    middle_name: str | None = field(default=None)
