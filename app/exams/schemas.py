from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from exams.models import QuestionType


class CertificationSchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


class CertificationCreate(BaseModel):
    name: str = Field(..., example="AWS Certified Developer")
    description: Optional[str] = Field(
        None, example="Certification for AWS cloud developers")
    passing_score: int = Field(
        default=70, ge=0, le=100, description="Score required to pass", example=70)


class QuestionCreate(BaseModel):
    certification_id: UUID = Field(...,
                                   example="123e4567-e89b-12d3-a456-426614174000")
    question_text: str = Field(...,
                               example="What is the default region in AWS CLI?")
    question_type: QuestionType = Field(..., example="single_choice")
    answer_choices: Dict[str, Any] = Field(..., example={
                                           "A": "us-east-1", "B": "us-west-2"})
    correct_answer: Dict[str, Any] = Field(..., example={"A": "us-east-1"})
