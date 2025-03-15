import uuid
from typing import Dict, Any, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from auth.models import User
from auth.security import hash_password, verify_password, create_access_token
from database.connection import get_db


def register_new_user(username: str, email: str, password: str) -> Dict[str, Any]:
    """
    Register a new user.

    This function creates a new user record in the database if the username or email is not already taken.
    It hashes the provided password and generates an access token upon successful registration.

    Args:
        username (str): The desired username.
        email (str): The user's email address.
        password (str): The user's plain text password.

    Returns:
        Dict[str, Any]: A dictionary containing a success message, the user's unique identifier, and an access token.

    Raises:
        HTTPException: If the username or email is already registered.
    """
    db: Session = next(get_db())
    try:
        # Check if the username or email is already taken
        existing_user = db.query(User).filter(
            or_(User.username == username, User.email == email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username or email already registered"
            )

        # Create a new User instance with a unique UUID and hashed password.
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
        db.close()  # Ensure the session is closed properly


def authenticate_user(username: str, password: str) -> Dict[str, Any]:
    """
    Authenticate a user.

    This function validates the user's credentials. It checks whether the user exists,
    is active, and that the provided password matches the stored hashed password.
    If authentication is successful, it returns an access token.

    Args:
        username (str): The user's username.
        password (str): The user's plain text password.

    Returns:
        Dict[str, Any]: A dictionary containing a success message, the user's unique identifier, and an access token.

    Raises:
        HTTPException: If the user does not exist, is inactive, or if the password is incorrect.
    """
    db: Session = next(get_db())
    try:
        # Retrieve the user from the database based on username.
        user: Optional[User] = db.query(User).filter(User.username == username).first()

        # Check if the user exists and is active.
        if not user or not user.is_active:
            raise HTTPException(
                status_code=400, detail="User does not exist or is inactive"
            )

        # Validate the provided password against the stored hashed password.
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect password")

        return {
            "message": "Successfully authenticated",
            "user_id": str(user.id),
            "token": create_access_token({"sub": user.username}),
        }
    finally:
        db.close()  # Close session properly


def deactivate_account(username: str) -> bool:
    """
    Deactivate a user account.

    This function deactivates a user account by setting the user's `is_active` flag to False.

    Args:
        username (str): The username of the user to deactivate.

    Returns:
        bool: True if the deactivation was successful, False otherwise.
    """
    db: Session = next(get_db())
    try:
        # Retrieve the user from the database based on username.
        user: Optional[User] = db.query(User).filter(User.username == username).first()

        # Check if the user exists and is active.
        if not user or not user.is_active:
            raise HTTPException(
                status_code=400, detail="User does not exist or is inactive"
            )

        # Deactivate the user account.
        user.is_active = False
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()  # Rollback transaction in case of failure
        raise HTTPException(
            status_code=500, detail="Failed to deactivate user"
        )
    finally:
        db.close()  # Close session properly
