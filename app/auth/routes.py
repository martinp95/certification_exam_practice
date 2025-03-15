from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status

from auth.services import register_new_user, authenticate_user, deactivate_account
from auth.schemas import UserCreate, UserLogin
from auth.security import get_current_user

router = APIRouter()

@router.post("/register", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate) -> Dict[str, str]:
    """
    Register a new user.

    Args:
        user (UserCreate): The user details required for registration.

    Returns:
        Dict[str, str]: A dictionary with a success message and access token.
    """
    return register_new_user(user.username, user.email, user.password)


@router.post("/login", response_model=Dict[str, str])
def login_user(user: UserLogin) -> Dict[str, str]:
    """
    Authenticate a user and return a JWT token.

    Args:
        user (UserLogin): The login credentials.

    Returns:
        Dict[str, str]: A dictionary containing the access token and token type.

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

    return {"access_token": result["token"], "token_type": "bearer"}


@router.delete("/deactivate", response_model=Dict[str, str], status_code=status.HTTP_200_OK)
def deactivate_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, str]:
    """
    Deactivate the account of the currently authenticated user.

    This endpoint requires a valid JWT token.

    Args:
        current_user (Dict[str, Any]): The authenticated user's details.

    Returns:
        Dict[str, str]: A dictionary indicating the outcome of the deactivation.

    Raises:
        HTTPException: If deactivation fails.
    """
    success = deactivate_account(current_user["username"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account deactivation failed",
        )
    return {"message": "Account deactivated successfully"}
