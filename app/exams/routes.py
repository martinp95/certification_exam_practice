import uuid
from typing import Any, List, Dict

import jwt
from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from exams.logic import get_certification, get_questions, record_exam_attempt
from auth.security import SECRET_KEY, ALGORITHM

# Define the OAuth2 password bearer token URL for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify the JWT token and return its payload.

    Args:
        token (str): The JWT token to verify.

    Returns:
        Dict[str, Any]: The decoded token payload.

    Raises:
        HTTPException: If the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/certifications", tags=["Certifications"])
def get_certifications(token: str = Depends(oauth2_scheme)) -> Any:
    """
    Retrieve certifications after verifying the provided JWT token.

    Args:
        token (str): The JWT token provided in the request header.

    Returns:
        Any: A list or object representing the certifications.
    """
    # Validate the JWT token
    verify_token(token)
    return get_certification()


@router.get(
    "/certifications/{certification_id}/questions/{num_questions}",
    tags=["Certifications"],
)
def get_questions_for_certification(
    certification_id: uuid.UUID,
    num_questions: int,
    token: str = Depends(oauth2_scheme),
) -> Any:
    """
    Retrieve a specified number of questions for a given certification.

    Args:
        certification_id (uuid.UUID): The UUID of the certification.
        num_questions (int): The number of questions to retrieve.
        token (str): The JWT token provided in the request header.

    Returns:
        Any: A list or object containing the certification questions.
    """
    # Validate the JWT token
    verify_token(token)
    return get_questions(certification_id, num_questions)


@router.post("/attempt", tags=["Exams"])
def record_attempt(
    certification_id: uuid.UUID,
    user_id: uuid.UUID,
    answers: List[Any],
    token: str = Depends(oauth2_scheme),
) -> Any:
    """
    Record an exam attempt with the provided answers for a specific certification.

    Args:
        certification_id (uuid.UUID): The UUID of the certification.
        user_id (uuid.UUID): The UUID of the user attempting the exam.
        answers (List[Any]): The list of answers submitted by the user.
        token (str): The JWT token provided in the request header.

    Returns:
        Any: A response object indicating the result of recording the exam attempt.
    """
    # Validate the JWT token
    verify_token(token)
    return record_exam_attempt(certification_id, user_id, answers)
