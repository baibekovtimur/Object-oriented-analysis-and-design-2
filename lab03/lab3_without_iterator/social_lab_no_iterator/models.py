from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping

INTEREST_CATEGORIES = (
    "sports",
    "music",
    "movies",
    "books",
    "travel",
    "technology",
    "art",
    "gaming",
)

CATEGORY_VECTORS = {
    "sports": (8.5, 2.0),
    "music": (6.0, 7.5),
    "movies": (2.5, 8.0),
    "books": (-3.5, 7.0),
    "travel": (-8.0, 3.0),
    "technology": (-7.0, -4.0),
    "art": (-1.5, -8.5),
    "gaming": (6.5, -6.0),
}


@dataclass(frozen=True)
class User:
    user_id: int
    first_name: str
    last_name: str
    friend_ids: list[int] = field(default_factory=list)
    interests: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class UserPoint:
    x: float
    y: float
    user_id: int


class UserToPointMapper:
    """Converts users to points using friend anchor and interests offset."""

    def __init__(
        self,
        interests_weight: float = 0.08,
        friends_weight: float = 0.92,
    ) -> None:
        total = interests_weight + friends_weight
        if total <= 0:
            raise ValueError("At least one weight must be positive.")

        self.interests_weight = interests_weight / total
        self.friends_weight = friends_weight / total

    def map_user(
        self,
        user: User,
        friend_points: Mapping[int, UserPoint] | None = None,
    ) -> UserPoint:
        interests_x, interests_y = self._interests_vector(user.interests)

        friend_anchor = self._friends_anchor(user.friend_ids, friend_points)
        if friend_anchor is None:
            x, y = interests_x, interests_y
        else:
            friends_x, friends_y = friend_anchor
            if user.interests:
                x = self.friends_weight * friends_x + self.interests_weight * interests_x
                y = self.friends_weight * friends_y + self.interests_weight * interests_y
            else:
                x, y = friends_x, friends_y

        return UserPoint(x=x, y=y, user_id=user.user_id)

    def _interests_vector(self, interests: Iterable[str]) -> tuple[float, float]:
        valid_categories = [item for item in interests if item in CATEGORY_VECTORS]
        if not valid_categories:
            return 0.0, 0.0

        x_total = 0.0
        y_total = 0.0
        for category in valid_categories:
            x_part, y_part = CATEGORY_VECTORS[category]
            x_total += x_part
            y_total += y_part

        scale = 1.0 / len(valid_categories)
        return x_total * scale, y_total * scale

    def _friends_anchor(
        self,
        friend_ids: Iterable[int],
        friend_points: Mapping[int, UserPoint] | None,
    ) -> tuple[float, float] | None:
        if not friend_points:
            return None

        valid_points = [
            friend_points[friend_id]
            for friend_id in set(friend_ids)
            if friend_id in friend_points
        ]
        if not valid_points:
            return None

        x_total = 0.0
        y_total = 0.0
        for point in valid_points:
            x_total += point.x
            y_total += point.y

        scale = 1.0 / len(valid_points)
        return x_total * scale, y_total * scale
