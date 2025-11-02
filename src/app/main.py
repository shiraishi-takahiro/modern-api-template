"""FastAPI application exposing user management endpoints."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status

from .models import UserCreate, UserRead
from .storage import UserNotFoundError, UsersRepository

app: FastAPI = FastAPI(title="FastAPI Users Service", version="0.1.0")
repository: UsersRepository = UsersRepository()


@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate) -> UserRead:
    """Create a new user and return the stored record."""

    return repository.add_user(payload)


@app.get("/users/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(user_id: int) -> UserRead:
    """Fetch a user by identifier, raising 404 if not found."""

    try:
        return repository.get_user(user_id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


__all__: list[str] = ["app"]
