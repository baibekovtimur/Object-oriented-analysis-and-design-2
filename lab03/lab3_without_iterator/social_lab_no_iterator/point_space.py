from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from .models import INTEREST_CATEGORIES, User, UserPoint, UserToPointMapper


@dataclass(frozen=True)
class Recommendation:
    user: User
    point: UserPoint
    distance: float
    probability: float


class UserPointSpaceNoIterator:
    """Stores users and returns recommendation lists directly (no Iterator pattern)."""

    def __init__(self, mapper: UserToPointMapper | None = None) -> None:
        self._mapper = mapper or UserToPointMapper()
        self._users: dict[int, User] = {}
        self._points: dict[int, UserPoint] = {}

    @property
    def users(self) -> dict[int, User]:
        return dict(self._users)

    @property
    def points(self) -> dict[int, UserPoint]:
        return dict(self._points)

    def next_user_id(self) -> int:
        return max(self._users, default=0) + 1

    def add_user(self, user: User) -> None:
        if user.user_id in self._users:
            raise ValueError(f"User id {user.user_id} already exists.")

        normalized_user = self._normalize_user(user)
        self._users[normalized_user.user_id] = normalized_user

        self._points[normalized_user.user_id] = self._mapper.map_user(
            user=normalized_user,
            friend_points=self._points,
        )

    def add_users(self, users: Iterable[User]) -> None:
        for user in users:
            if user.user_id in self._users:
                raise ValueError(f"User id {user.user_id} already exists.")

            normalized_user = self._normalize_user(user)
            self._users[normalized_user.user_id] = normalized_user

        self._recalculate_points()

    def _normalize_user(self, user: User) -> User:
        if user.user_id in self._users:
            raise ValueError(f"User id {user.user_id} already exists.")

        clean_friend_ids = sorted(
            friend_id
            for friend_id in set(user.friend_ids)
            if friend_id > 0 and friend_id != user.user_id
        )
        clean_interests = {
            interest for interest in set(user.interests) if interest in INTEREST_CATEGORIES
        }

        return User(
            user_id=user.user_id,
            first_name=user.first_name.strip(),
            last_name=user.last_name.strip(),
            friend_ids=clean_friend_ids,
            interests=clean_interests,
        )

    def get_user(self, user_id: int) -> User:
        return self._users[user_id]

    def get_point(self, user_id: int) -> UserPoint:
        return self._points[user_id]

    def get_recommendations(self, reference_user_id: int, limit: int = 10) -> list[Recommendation]:
        if reference_user_id not in self._users:
            raise ValueError(f"Reference user id {reference_user_id} does not exist.")

        reference_point = self._points[reference_user_id]
        recommendations: list[Recommendation] = []

        for user_id, user in self._users.items():
            if user_id == reference_user_id:
                continue

            candidate_point = self._points[user_id]
            distance = math.dist(
                (reference_point.x, reference_point.y),
                (candidate_point.x, candidate_point.y),
            )
            probability = 1.0 / (1.0 + distance)
            recommendations.append(
                Recommendation(
                    user=user,
                    point=candidate_point,
                    distance=distance,
                    probability=probability,
                )
            )

        recommendations.sort(key=lambda item: (item.distance, item.user.user_id))
        if limit >= 0:
            return recommendations[:limit]
        return recommendations

    def _recalculate_points(self) -> None:
        baseline_points = {
            user.user_id: self._mapper.map_user(
                user=user,
                friend_points=None,
            )
            for user in self._users.values()
        }

        self._points = {
            user.user_id: self._mapper.map_user(
                user=user,
                friend_points=baseline_points,
            )
            for user in self._users.values()
        }


def create_seeded_space() -> UserPointSpaceNoIterator:
    users = [
        User(1, "Liam", "Carter", [2, 3, 5], {"sports", "technology", "gaming"}),
        User(2, "Emma", "Nelson", [1, 4], {"music", "books", "art"}),
        User(3, "Noah", "Stewart", [1, 6, 7], {"travel", "movies", "sports"}),
        User(4, "Olivia", "Collins", [2, 8], {"books", "technology", "music"}),
        User(5, "Ava", "Mitchell", [1, 9], {"gaming", "movies", "art"}),
        User(6, "Elijah", "Reed", [3, 7, 10], {"travel", "sports", "music"}),
        User(7, "Mia", "Brooks", [3, 6, 11], {"art", "books", "travel"}),
        User(8, "Lucas", "Parker", [4, 12], {"technology", "gaming", "movies"}),
        User(9, "Sophia", "Long", [5, 11], {"music", "art", "books"}),
        User(10, "James", "Morris", [6, 12], {"sports", "technology", "travel"}),
        User(11, "Charlotte", "Ward", [7, 9], {"books", "movies", "art"}),
        User(12, "Henry", "Powell", [8, 10], {"gaming", "technology", "sports"}),
    ]

    space = UserPointSpaceNoIterator()
    space.add_users(users)
    return space
