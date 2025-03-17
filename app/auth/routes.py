from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from auth.services import register_new_user, authenticate_user, deactivate_account
from auth.schemas import UserCreate, UserLogin, TokenResponse, MessageResponse
from auth.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        201: {"description": "User registered successfully"},
        400: {"description": "Username or email already registered"},
    },
)
def register_user(user: UserCreate) -> TokenResponse:
    """
    Register a new user.

    Args:
        user (UserCreate): The user details required for registration.

    Returns:
        TokenResponse: A token response with access token and token type.
    """
    result = register_new_user(user.username, user.email, user.password)
    return TokenResponse(access_token=result["token"], token_type="bearer")


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and return JWT token",
    responses={
        200: {"description": "Authentication successful"},
        401: {"description": "Invalid username or password"},
    },
)
def login_user(user: UserLogin) -> TokenResponse:
    """
    Authenticate a user and return a JWT token.

    Args:
        user (UserLogin): The login credentials.

    Returns:
        TokenResponse: A token response with access token and token type.

    Raises:
        HTTPException: If authentication fails.
    """
    result = authenticate_user(user.username, user.password)

    if not result or "token" not in result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(access_token=result["token"], token_type="bearer")


@router.delete(
    "/deactivate",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate the current user account",
    responses={
        200: {"description": "Account deactivated successfully"},
        400: {"description": "Account deactivation failed"},
    },
)
def deactivate_user(current_user: dict = Depends(get_current_user)) -> MessageResponse:
    """
    Deactivate the account of the currently authenticated user.

    This endpoint requires a valid JWT token.

    Args:
        current_user (dict): The authenticated user's details.

    Returns:
        MessageResponse: Confirmation message.

    Raises:
        HTTPException: If deactivation fails.
    """
    success = deactivate_account(current_user["username"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account deactivation failed",
        )
    return MessageResponse(message="Account deactivated successfully")
