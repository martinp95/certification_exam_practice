from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status
from uuid import UUID

from exams.logic import (
    find_all_certifications,
    create_certification as logic_create_certification,
    create_question as logic_create_question,
    get_questions as logic_get_questions,
)
from auth.security import get_current_user
from exams.schemas import (
    CertificationSchema, CertificationCreate, QuestionCreate
)

router = APIRouter(prefix="/exam", tags=["Exam Management"])


@router.get(
    "/certifications",
    response_model=List[CertificationSchema],
    response_model_exclude_none=True,
    summary="List All Certifications",
    description="Retrieve all available certifications after authentication.",
    responses={
        200: {"description": "Successful retrieval of certifications."},
        401: {"description": "Unauthorized access."}
    }
)
def get_certifications(current_user: Dict[str, Any] = Depends(get_current_user)):
    _check_user(current_user)
    certifications = find_all_certifications()
    return certifications


@router.post(
    "/certifications",
    response_model=Dict[str, str],
    response_model_exclude_none=True,
    summary="Create Certification",
    description="Create a new certification entry with a name, description, and passing score.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Certification created successfully."},
        400: {"description": "Invalid input."},
        401: {"description": "Unauthorized."}
    }
)
def create_certification(
    cert: CertificationCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    _check_user(current_user)
    new_cert = logic_create_certification(
        name=cert.name,
        description=cert.description,
        passing_score=cert.passing_score
    )
    return {"message": "Certification created", "id": str(new_cert.id)}


@router.get(
    "/questions",
    response_model_exclude_none=True,
    summary="Get Random Questions",
    description="Retrieve a random set of questions for a specified certification.",
    responses={
        200: {"description": "Questions retrieved successfully."},
        401: {"description": "Unauthorized."},
        404: {"description": "Certification not found."}
    }
)
def get_cert_questions(
    certification_id: str = Query(..., description="Certification UUID"),
    number_of_questions: int = Query(..., gt=0,
                                     description="Number of questions to retrieve"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    _check_user(current_user)
    questions = logic_get_questions(certification_id, number_of_questions)
    return questions


@router.post(
    "/questions",
    response_model=Dict[str, str],
    response_model_exclude_none=True,
    summary="Create Question",
    description="Create a new question with text, type, possible answers, and correct answer.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Question created successfully."},
        400: {"description": "Invalid input."},
        401: {"description": "Unauthorized."}
    }
)
def create_question(
    question: QuestionCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    _check_user(current_user)
    new_question = logic_create_question(
        certification_id=question.certification_id,
        question_text=question.question_text,
        question_type=question.question_type,
        answer_choices=question.answer_choices,
        correct_answer=question.correct_answer
    )
    return {"message": "Question created", "id": str(new_question.id)}


def _check_user(current_user: Dict[str, Any]):
    """
    Validate that the current user is authenticated.

    Raises:
        HTTPException: If user authentication fails.
    """
    if not current_user or "username" not in current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
