import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import jwt

# Load environment variables with safe defaults
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Ensure SECRET_KEY is set
if not SECRET_KEY:
    raise ValueError(
        "SECRET_KEY is not set. Please configure it as an environment variable.")

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using the bcrypt algorithm.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against its hashed version.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password for comparison.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a signed JWT access token with an expiration time.

    Args:
        data (Dict[str, Any]): Payload to include in the token (e.g., {"sub": username}).

    Returns:
        str: Encoded JWT token.

    Raises:
        ValueError: If encoding fails due to missing SECRET_KEY.
    """
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires})

    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise ValueError(f"Token generation failed: {e}")

    return encoded_jwt


# OAuth2 scheme for receiving the JWT token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Dependency to get the current authenticated user from the JWT token.

    Args:
        token (str): The JWT token passed via the Authorization header.

    Returns:
        Dict[str, Any]: A dictionary representing the authenticated user details.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    if not SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server misconfiguration: SECRET_KEY is not set."
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if not username:
            raise credentials_exception
        return {"username": username}

    except jwt.PyJWTError:
        raise credentials_exception
