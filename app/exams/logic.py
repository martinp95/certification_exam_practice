from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from database.connection import get_db
from exams.models import Certification, Question, ExamAttempt, ExamAttemptQuestion
import uuid
from datetime import datetime


def get_certification():
    db = next(get_db())
    try:
        return db.query(Certification).all()
    finally:
        db.close()


def get_questions(certification_id: uuid.UUID, number_of_questions: int):
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


def record_exam_attempt(
        certification_id: uuid.UUID, user_id: uuid.UUID, answers: list):
    db = next(get_db())
    try:
        score = 0
        for answer in answers:
            question = db.query(Question).filter(
                Question.id == answer['question_id']).first()
            if question and set(answer['user_answer']) == set(question.correct_answer):
                score += 1

        exam_attempt = ExamAttempt(
            id=uuid.uuid4(),
            user_id=user_id,
            certification_id=certification_id,
            num_questions=len(answers),
            time_limit=30,
            exam_date=datetime.now(),
            score=score
        )
        db.add(exam_attempt)
        db.commit()
        for answer in answers:
            exam_attempt_question = ExamAttemptQuestion(
                id=uuid.uuid4(),
                exam_attempt_id=exam_attempt.id,
                question_id=answer['question_id'],
                user_answer=answer['user_answer'],
                is_correct=set(answer['user_answer']) == set(
                    question.correct_answer)
            )
            db.add(exam_attempt_question)
        db.commit()
    finally:
        db.close()
