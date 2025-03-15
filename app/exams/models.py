import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Annotated, Optional

from sqlalchemy import (
    String, Integer, Boolean, ForeignKey, JSON, TIMESTAMP, Enum, Text, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from database.connection import Base


# Enum for question types
class QuestionType(PyEnum):
    MULTIPLE_CHOICE = "multiple_choice"
    SINGLE_CHOICE = "single_choice"


# Certification model
class Certification(Base):
    """Certification model."""
    __tablename__ = "certifications"

    id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]]
    name: Mapped[Annotated[str, mapped_column(
        String, unique=True, nullable=False)]]
    description: Mapped[Annotated[Optional[str],
                                  mapped_column(Text, nullable=True)]]

    # Relationship with Question
    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="certification", cascade="all, delete-orphan")


# Question model
class Question(Base):
    """Question model."""
    __tablename__ = "questions"

    id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]]
    certification_id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), ForeignKey("certifications.id"), nullable=False)]]
    question_text: Mapped[Annotated[str, mapped_column(Text, nullable=False)]]
    question_type: Mapped[Annotated[QuestionType, mapped_column(
        Enum(QuestionType, native_enum=False), nullable=False)]]
    answer_choices: Mapped[Annotated[dict,
                                     mapped_column(JSON, nullable=False)]]
    correct_answer: Mapped[Annotated[dict,
                                     mapped_column(JSON, nullable=False)]]

    # Relationship with Certification
    certification: Mapped["Certification"] = relationship(
        "Certification", back_populates="questions")


# ExamAttempt model
class ExamAttempt(Base):
    """ExamAttempt model representing an exam taken by a user."""
    __tablename__ = "exam_attempts"

    id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]]
    user_id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)]]
    certification_id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), ForeignKey("certifications.id"), nullable=False)]]
    num_questions: Mapped[Annotated[int,
                                    mapped_column(Integer, nullable=False)]]
    time_limit: Mapped[Annotated[int, mapped_column(Integer, nullable=False)]]
    exam_date: Mapped[Annotated[datetime, mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), default=datetime.utcnow)]]
    score: Mapped[Annotated[int, mapped_column(Integer, nullable=False)]]

    # Relationship with User
    user = relationship("User", back_populates="exam_attempts")
    # Relationship with Certification (if bidirectional, add back_populates="exam_attempts")
    certification: Mapped["Certification"] = relationship("Certification")
    # Relationship with ExamAttemptQuestion
    exam_attempt_questions: Mapped[List["ExamAttemptQuestion"]] = relationship(
        "ExamAttemptQuestion", back_populates="exam_attempt", cascade="all, delete-orphan"
    )


# ExamAttemptQuestion model
class ExamAttemptQuestion(Base):
    """Represents an individual question attempt within an exam attempt."""
    __tablename__ = "exam_attempt_questions"

    id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]]
    exam_attempt_id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), ForeignKey("exam_attempts.id"), nullable=False)]]
    question_id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)]]
    user_answer: Mapped[Annotated[dict, mapped_column(JSON, nullable=False)]]
    is_correct: Mapped[Annotated[bool, mapped_column(Boolean, nullable=False)]]

    # Relationship with ExamAttempt
    exam_attempt: Mapped["ExamAttempt"] = relationship(
        "ExamAttempt", back_populates="exam_attempt_questions")
    # Relationship with Question
    question: Mapped["Question"] = relationship("Question")
