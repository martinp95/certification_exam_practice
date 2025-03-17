import uuid
from typing import Any, Dict, Optional

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from auth.models import User
from auth.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from database.connection import get_db


def register_new_user(username: str, email: str, password: str) -> Dict[str, Any]:
    """
    Register a new user.

    Creates a new user record in the database if the username or email is not already taken.
    Hashes the provided password and generates an access token upon successful registration.

    Args:
        username (str): Desired username.
        email (str): User's email address.
        password (str): User's plain text password.

    Returns:
        Dict[str, Any]: Dictionary containing a success message, user ID, and access token.

    Raises:
        HTTPException: If the username or email is already registered.
    """
    db: Session = next(get_db())
    try:
        existing_user = db.query(User).filter(
            or_(User.username == username, User.email == email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username or email already registered",
            )

        new_user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user_id": str(new_user.id),
            "token": create_access_token({"sub": new_user.username}),
        }
    finally:
        db.close()


def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate a user.

    Validates the user's credentials. Checks whether the user exists, is active,
    and that the provided password matches the stored hashed password.

    Args:
        username (str): User's username.
        password (str): User's plain text password.

    Returns:
        Dict[str, Any]: Dictionary containing a success message, user ID, and access token.

    Raises:
        HTTPException: If the user does not exist, is inactive, or password is incorrect.
    """
    db: Session = next(get_db())
    try:
        user: Optional[User] = db.query(User).filter(
            User.username == username).first()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=400, detail="User does not exist or is inactive"
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect password")

        return {
            "message": "Successfully authenticated",
            "user_id": str(user.id),
            "token": create_access_token({"sub": user.username}),
        }
    finally:
        db.close()


def deactivate_account(username: str) -> bool:
    """
    Deactivate a user account.

    Sets the user's `is_active` flag to False.

    Args:
        username (str): Username of the user to deactivate.

    Returns:
        bool: True if deactivation was successful, False otherwise.

    Raises:
        HTTPException: If the user does not exist, is inactive, or deactivation fails.
    """
    db: Session = next(get_db())
    try:
        user: Optional[User] = db.query(User).filter(
            User.username == username).first()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=400, detail="User does not exist or is inactive"
            )

        user.is_active = False
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Failed to deactivate user"
        )
    finally:
        db.close()
