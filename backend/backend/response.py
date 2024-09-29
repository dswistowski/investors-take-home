import typing as t
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pagination:
    next: str | None = None
    previous: str | None = None


@dataclass(frozen=True, slots=True)
class PaginatedResponse[T]:
    data: t.Sequence[T]
    paging: Pagination
