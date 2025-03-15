from typing import List, Annotated
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from exams.models import ExamAttempt
from database.connection import Base


class User(Base):
    """
    User model.

    Attributes:
        id (UUID): Unique identifier for the user, generated using uuid4.
        username (str): The user's username (max 150 characters), must be unique.
        email (str): The user's email address, must be unique.
        password_hash (str): The hashed password for the user.
        is_active (bool): Flag indicating if the user is active. Defaults to True.
        exam_attempts (List[ExamAttempt]): List of exam attempts made by the user.
    """

    __tablename__ = "users"

    id: Mapped[Annotated[uuid.UUID, mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)]]
    username: Mapped[Annotated[str, mapped_column(
        String(150), nullable=False, unique=True)]]
    email: Mapped[Annotated[str, mapped_column(
        String(150), nullable=False, unique=True)]]
    password_hash: Mapped[Annotated[str,
                                    mapped_column(String, nullable=False)]]
    is_active: Mapped[Annotated[bool, mapped_column(
        Boolean, default=True, nullable=False)]]

    # Relationship: User <-> ExamAttempt
    exam_attempts: Mapped[List["ExamAttempt"]] = relationship(
        "ExamAttempt", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, email={self.email}, is_active={self.is_active})>"
