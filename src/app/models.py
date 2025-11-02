"""Pydantic models for user data transfer objects."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Schema for incoming user creation requests."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=120)


class UserRead(BaseModel):
    """Schema for outgoing user payloads."""

    id: int
    name: str
    age: int


__all__: list[str] = ["UserCreate", "UserRead"]
