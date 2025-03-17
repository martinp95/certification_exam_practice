import uuid
from typing import List
from sqlalchemy.sql.expression import func
from database.connection import get_db
from exams.models import Certification, QuestionType, Question, ExamAttempt, ExamAttemptQuestion


def find_all_certifications() -> List[Certification]:
    """Retrieve all certifications from the database."""
    db = next(get_db())
    try:
        return db.query(Certification).all()
    finally:
        db.close()


def create_certification(name: str, description: str, passing_score: int = 70) -> Certification:
    """Create a new certification with a specified passing score."""
    db = next(get_db())
    try:
        new_cert = Certification(
            id=uuid.uuid4(),
            name=name,
            description=description,
            passing_score=passing_score
        )
        db.add(new_cert)
        db.commit()
        db.refresh(new_cert)
        return new_cert
    finally:
        db.close()


def create_question(
    certification_id: uuid.UUID,
    question_text: str,
    question_type: str,
    answer_choices: dict,
    correct_answer: dict
) -> Question:
    """Create a new question for a given certification."""
    db = next(get_db())
    try:
        q_type = QuestionType(question_type)
        new_q = Question(
            id=uuid.uuid4(),
            certification_id=certification_id,
            question_text=question_text,
            question_type=q_type,
            answer_choices=answer_choices,
            correct_answer=correct_answer
        )
        db.add(new_q)
        db.commit()
        db.refresh(new_q)
        return new_q
    finally:
        db.close()


def get_questions(certification_id: uuid.UUID, number_of_questions: int) -> List[Question]:
    """Retrieve a random set of questions for a certification."""
    db = next(get_db())
    try:
        questions = (
            db.query(Question)
            .filter(Question.certification_id == certification_id)
            .order_by(func.random())
            .limit(number_of_questions)
            .all()
        )
        return questions
    finally:
        db.close()
