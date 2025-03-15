from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    """Request model for user registration."""
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    """Request model for user login."""
    username: str
    password: str
