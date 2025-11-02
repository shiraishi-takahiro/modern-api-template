"""In-memory storage layer for user records."""

from __future__ import annotations

from collections.abc import Iterator, MutableMapping
from dataclasses import dataclass
from itertools import count

from .models import UserCreate, UserRead


@dataclass(frozen=True, slots=True)
class UserNotFoundError(LookupError):
    """Raised when a user record cannot be located."""

    user_id: int

    def __str__(self) -> str:
        return f"User with id {self.user_id} was not found."


class UsersRepository:
    """Simple in-memory repository for storing users."""

    def __init__(self, store: MutableMapping[int, UserRead] | None = None) -> None:
        self._store: MutableMapping[int, UserRead] = store if store is not None else {}
        self._id_counter: Iterator[int] = count(start=1)

    def add_user(self, payload: UserCreate) -> UserRead:
        """Persist a new user and return the stored record."""

        user_id: int = next(self._id_counter)
        user_record: UserRead = UserRead(id=user_id, name=payload.name, age=payload.age)
        self._store[user_id] = user_record
        return user_record

    def get_user(self, user_id: int) -> UserRead:
        """Retrieve an existing user by identifier."""

        try:
            return self._store[user_id]
        except KeyError as exc:  # noqa: PERF203 - translate exception for clarity
            raise UserNotFoundError(user_id=user_id) from exc


__all__: list[str] = ["UserNotFoundError", "UsersRepository"]
