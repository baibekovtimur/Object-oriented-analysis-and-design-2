from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

from .models import User, UserPoint

T = TypeVar("T")


class Iterator(ABC, Generic[T]):
    @abstractmethod
    def has_next(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def next(self) -> T:
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError


class Aggregate(ABC, Generic[T]):
    @abstractmethod
    def create_iterator(self, reference_user_id: int, limit: int = 10) -> Iterator[T]:
        raise NotImplementedError


@dataclass(frozen=True)
class Recommendation:
    user: User
    point: UserPoint
    distance: float
    probability: float


class NearestUsersIterator(Iterator[Recommendation]):
    """Concrete iterator with explicit index control, no yield usage."""

    def __init__(self, recommendations: Sequence[Recommendation]) -> None:
        self._recommendations = list(recommendations)
        self._index = 0

    def has_next(self) -> bool:
        return self._index < len(self._recommendations)

    def next(self) -> Recommendation:
        if not self.has_next():
            raise StopIteration("No more recommendations in iterator.")

        current = self._recommendations[self._index]
        self._index += 1
        return current

    def reset(self) -> None:
        self._index = 0

    def position(self) -> int:
        return self._index

    def total(self) -> int:
        return len(self._recommendations)

    def __iter__(self) -> "NearestUsersIterator":
        return self

    def __next__(self) -> Recommendation:
        return self.next()
