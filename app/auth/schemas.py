from pydantic import BaseModel


class UserCreate(BaseModel):
    """Request model for user registration."""
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    """Request model for user login."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Response model for authentication tokens."""
    access_token: str
    token_type: str


class MessageResponse(BaseModel):
    """Generic response model for status messages."""
    message: str
